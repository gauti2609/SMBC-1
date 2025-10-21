# Network Database Architecture - Options & Recommendations

## Current State
- **Database**: SQLite (file-based, `financial_automation.db`)
- **Architecture**: Local single-user
- **License**: Local file-based

## Requirements
1. Database on server (NAS preferred: Asustor AS6704T-AB40, or Windows machine)
2. Multiple users accessing from Windows systems
3. Access from local network AND remote locations
4. Centralized license authentication on server
5. Multi-user concurrent access support

---

## ⚠️ CRITICAL: SQLite Limitations for Network Access

**SQLite is NOT recommended for network file sharing** because:
- File locking issues over SMB/NFS
- Database corruption risk with concurrent writes
- Poor performance over network
- No built-in user authentication
- No connection pooling

---

## 🎯 RECOMMENDED SOLUTION: PostgreSQL on NAS

### Architecture Overview
```
┌─────────────────────────────────────────────────────────┐
│  Asustor NAS (AS6704T-AB40)                            │
│  ┌───────────────────────────────────────────────────┐ │
│  │ PostgreSQL Server (Port 5432)                     │ │
│  │  - Database: financial_automation                 │ │
│  │  - Users: app_admin, app_user                     │ │
│  │  - SSL/TLS encryption                             │ │
│  └───────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────┐ │
│  │ License Server (Python Flask/FastAPI)             │ │
│  │  - Port 8443 (HTTPS)                              │ │
│  │  - License validation API                         │ │
│  │  - User authentication                            │ │
│  └───────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
           ↓ Network (LAN/WAN via VPN or Port Forward)
┌──────────────────────┐  ┌──────────────────────┐
│ Windows Client 1     │  │ Windows Client 2     │
│ .exe Application     │  │ .exe Application     │
│ - PyQt5 GUI          │  │ - PyQt5 GUI          │
│ - PostgreSQL Driver  │  │ - PostgreSQL Driver  │
│ - License Client     │  │ - License Client     │
└──────────────────────┘  └──────────────────────┘
```

### Why PostgreSQL?
✅ **Multi-user support**: ACID-compliant concurrent access  
✅ **Network-native**: Designed for client-server architecture  
✅ **Asustor support**: Available in App Central  
✅ **Authentication**: Built-in user/role management  
✅ **Performance**: Connection pooling, query optimization  
✅ **Reliability**: Transaction support, automatic backups  
✅ **Security**: SSL/TLS, row-level security, encryption  
✅ **Remote access**: Easy VPN or port forwarding setup  

---

## Implementation Plan

### Phase 1: Database Migration (SQLite → PostgreSQL)

#### 1.1 Install PostgreSQL on Asustor NAS
```bash
# Via Asustor App Central
1. Login to ADM (Asustor Data Master)
2. Open App Central
3. Search for "PostgreSQL"
4. Install PostgreSQL (usually version 14+)
5. Configure:
   - Port: 5432 (default)
   - Admin password: <strong password>
   - Create database: financial_automation
```

#### 1.2 Update Python Code
```python
# config/settings.py - ADD
import os

# Database configuration
DB_TYPE = os.getenv('DB_TYPE', 'sqlite')  # 'sqlite' or 'postgresql'

# SQLite (development/local)
SQLITE_DB_PATH = 'financial_automation.db'

# PostgreSQL (production/network)
POSTGRES_CONFIG = {
    'host': os.getenv('DB_HOST', '192.168.1.100'),  # NAS IP
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'financial_automation'),
    'user': os.getenv('DB_USER', 'app_user'),
    'password': os.getenv('DB_PASSWORD', ''),  # From env or encrypted file
    'sslmode': os.getenv('DB_SSLMODE', 'require')
}
```

```python
# config/database.py - MODIFY
import sqlite3
import psycopg2
from psycopg2 import pool
from config.settings import DB_TYPE, SQLITE_DB_PATH, POSTGRES_CONFIG

# Connection pool for PostgreSQL
pg_pool = None

def get_connection():
    """Get database connection based on DB_TYPE"""
    if DB_TYPE == 'postgresql':
        global pg_pool
        if pg_pool is None:
            pg_pool = psycopg2.pool.SimpleConnectionPool(
                minconn=1,
                maxconn=20,
                **POSTGRES_CONFIG
            )
        return pg_pool.getconn()
    else:
        return sqlite3.connect(SQLITE_DB_PATH)

def release_connection(conn):
    """Release connection back to pool"""
    if DB_TYPE == 'postgresql':
        pg_pool.putconn(conn)
    else:
        conn.close()
```

#### 1.3 Update requirements.txt
```txt
# Add PostgreSQL driver
psycopg2-binary>=2.9.0  # PostgreSQL adapter
python-dotenv>=1.0.0    # Environment variables
```

#### 1.4 SQL Migration Script
```python
# utils/migrate_to_postgres.py
"""
Convert SQLite schema to PostgreSQL
Run once to migrate schema and data
"""
import sqlite3
import psycopg2

# Key differences SQLite → PostgreSQL:
# - INTEGER PRIMARY KEY AUTOINCREMENT → SERIAL PRIMARY KEY
# - BOOLEAN → BOOLEAN (not INTEGER 0/1)
# - TIMESTAMP DEFAULT CURRENT_TIMESTAMP → TIMESTAMP DEFAULT NOW()
# - REAL → DECIMAL(15,2) for monetary values
```

### Phase 2: License Server Implementation

#### 2.1 Simple License Server (Flask)
```python
# license_server/app.py
"""
Lightweight license authentication server
Runs on NAS, validates user licenses
"""
from flask import Flask, request, jsonify
import psycopg2
import hashlib
import os

app = Flask(__name__)

@app.route('/api/license/validate', methods=['POST'])
def validate_license():
    """
    Validate user license
    POST body: {"username": "...", "license_key": "...", "machine_id": "..."}
    Returns: {"valid": true/false, "user_id": ..., "expires": "..."}
    """
    data = request.json
    # Check license in database
    # Validate expiry, concurrent users, machine binding
    return jsonify({"valid": True, "user_id": 1})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8443, ssl_context='adhoc')
```

#### 2.2 Client-Side License Check
```python
# models/license.py - UPDATE
import requests
import uuid
import os

LICENSE_SERVER_URL = os.getenv('LICENSE_SERVER', 'https://192.168.1.100:8443')

def get_machine_id():
    """Get unique machine ID"""
    return str(uuid.getnode())  # MAC address-based

def validate_license_remote(username, license_key):
    """Validate license with remote server"""
    try:
        response = requests.post(
            f'{LICENSE_SERVER_URL}/api/license/validate',
            json={
                'username': username,
                'license_key': license_key,
                'machine_id': get_machine_id()
            },
            verify=False,  # For self-signed cert, or use proper CA
            timeout=5
        )
        return response.json()
    except:
        # Fallback: Allow offline for X days
        return check_offline_grace_period()
```

### Phase 3: Network Configuration

#### 3.1 Local Network Access
```bash
# On Asustor NAS, configure firewall:
- Allow port 5432 (PostgreSQL) from LAN
- Allow port 8443 (License Server) from LAN

# On Windows Clients:
- Configure connection string:
  DB_HOST=192.168.1.100  # NAS IP address
  DB_PORT=5432
  DB_USER=app_user
  DB_PASSWORD=<encrypted>
```

#### 3.2 Remote Access (Outside LAN)

**Option A: VPN (RECOMMENDED)**
```
1. Setup VPN on Asustor NAS (built-in VPN Server)
2. Clients connect via VPN
3. Access NAS as if on LAN (192.168.1.100:5432)
4. Most secure, no port forwarding
```

**Option B: Port Forwarding + SSL**
```
1. Router port forward:
   External Port 55432 → NAS:5432
   External Port 58443 → NAS:8443
2. Dynamic DNS (e.g., DuckDNS, No-IP)
3. SSL certificate (Let's Encrypt)
4. Strong passwords + IP whitelisting
5. ⚠️ Less secure than VPN
```

---

## Alternative: Shared SQLite (NOT RECOMMENDED)

If you insist on SQLite:

### Setup
```
1. Place financial_automation.db on NAS shared folder
2. Mount as network drive on Windows: Z:\financial_automation.db
3. Update DB_PATH to point to Z:\
```

### Problems
❌ **Corruption risk**: 2+ users writing simultaneously  
❌ **Slow performance**: Every query over network  
❌ **File locking**: Windows SMB + SQLite = conflicts  
❌ **No authentication**: Anyone with file access can read  

### Workarounds (Still Not Ideal)
- Enable SQLite WAL mode: `PRAGMA journal_mode=WAL;`
- Use file-level locking service
- Implement application-level mutex
- **Still prone to corruption!**

---

## Migration Checklist

### Pre-Migration
- [ ] Backup current SQLite database
- [ ] Install PostgreSQL on Asustor NAS
- [ ] Test network connectivity (ping, telnet 5432)
- [ ] Create database and users
- [ ] Install psycopg2-binary on dev machine

### Migration
- [ ] Update config/settings.py with DB_TYPE toggle
- [ ] Update config/database.py with PostgreSQL pool
- [ ] Run schema migration script
- [ ] Test CRUD operations
- [ ] Migrate existing data (if any)
- [ ] Update requirements.txt
- [ ] Build .exe with PostgreSQL driver

### Post-Migration
- [ ] Test multi-user concurrent access
- [ ] Setup license server on NAS
- [ ] Configure SSL/TLS
- [ ] Setup backups (pg_dump cron job)
- [ ] Document connection parameters for users
- [ ] VPN setup for remote users

---

## Deployment Instructions for End Users

### For Local Network Users
```
1. Install FinancialAutomation.exe
2. Create config file: C:\Users\<User>\AppData\Local\FinancialAutomation\.env
3. Add:
   DB_TYPE=postgresql
   DB_HOST=192.168.1.100
   DB_PORT=5432
   DB_USER=app_user
   DB_PASSWORD=<provided>
   LICENSE_SERVER=https://192.168.1.100:8443
4. Run application
```

### For Remote Users
```
1. Install VPN client (Asustor VPN)
2. Connect to VPN
3. Follow local network instructions above
```

---

## Cost & Resources

| Component | Cost | Notes |
|-----------|------|-------|
| PostgreSQL on NAS | Free | Built-in Asustor app |
| License Server | Free | Python Flask/FastAPI |
| SSL Certificate | Free | Let's Encrypt |
| VPN | Free | Built-in Asustor VPN Server |
| psycopg2 Driver | Free | Python package |
| **Total** | **₹0** | Use existing NAS |

---

## Timeline Estimate

| Task | Time | Priority |
|------|------|----------|
| Install PostgreSQL on NAS | 1 hour | High |
| Update code for PostgreSQL | 4 hours | High |
| Schema migration | 2 hours | High |
| Testing multi-user | 2 hours | High |
| License server setup | 4 hours | Medium |
| VPN configuration | 2 hours | Medium |
| Documentation | 2 hours | Low |
| **Total** | **17 hours** | |

---

## Recommendation Summary

✅ **Use PostgreSQL on Asustor NAS**
- Proper multi-user support
- Network-native design
- ACID compliance
- Built-in security

✅ **VPN for remote access**
- Most secure
- Easy with Asustor built-in VPN

✅ **License server on NAS**
- Centralized authentication
- Works LAN + remote

❌ **Avoid shared SQLite**
- Corruption risk
- Not designed for network
- No concurrent write support

---

## Next Steps

1. **Immediate**: Modify code to support PostgreSQL (DB_TYPE toggle)
2. **This Week**: Install PostgreSQL on NAS, test connectivity
3. **Next Week**: Implement license server, VPN setup
4. **Before Deployment**: Full testing with 2-3 concurrent users

---

## Questions to Confirm

1. **Do you want to proceed with PostgreSQL migration now, or after completing more modules?**
   - Recommendation: Migrate now while codebase is smaller

2. **What is the NAS IP address and can you install PostgreSQL via App Central?**
   - I can provide step-by-step Asustor instructions

3. **How many concurrent users expected?**
   - Helps size connection pool

4. **VPN or port forwarding for remote access?**
   - Recommendation: VPN for security

Let me know your preferences and I'll implement the database abstraction layer immediately!
