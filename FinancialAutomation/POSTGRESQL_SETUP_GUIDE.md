# PostgreSQL Setup Guide for Asustor NAS - Step by Step

## Prerequisites
- Asustor AS6704T-AB40 NAS (or any Asustor NAS)
- Access to NAS admin panel (ADM)
- Network connectivity to NAS
- 10 minutes of time

---

## Part 1: Install PostgreSQL on Asustor NAS (5 minutes)

### Step 1: Access Asustor Data Master (ADM)
1. Open web browser
2. Navigate to: `http://[NAS-IP-ADDRESS]:8000` (e.g., `http://192.168.1.100:8000`)
3. Login with your admin credentials

### Step 2: Install PostgreSQL
1. Click **App Central** icon (looks like a shopping bag)
2. In the search box, type: **PostgreSQL**
3. Click on **PostgreSQL** in the results
4. Click **Install** button
5. Wait 2-3 minutes for installation to complete
6. Click **Open** when installation finishes

### Step 3: Configure PostgreSQL
1. PostgreSQL management interface will open
2. Note the **default admin password** (usually shown during first launch)
3. Or set a new admin password if prompted
4. Click **Apply** or **Save**

PostgreSQL is now running on your NAS! ✅

---

## Part 2: Create Database and User (3 minutes)

### Option A: Using Web Interface (Easier)

1. In ADM, go to **App Central** → **PostgreSQL** → **Open**
2. Click **pgAdmin** or **Database Manager** (if available)
3. Create database:
   - Click **Create Database**
   - Name: `financial_automation`
   - Encoding: `UTF8`
   - Click **Create**

4. Create user:
   - Go to **Users** or **Roles**
   - Click **Create User**
   - Username: `smbc_app_user`
   - Password: `[YOUR-SECURE-PASSWORD]` ← **Write this down!**
   - Privileges: Grant access to `financial_automation` database
   - Click **Create**

### Option B: Using Command Line (Advanced)

1. **SSH into NAS:**
   ```bash
   ssh admin@[NAS-IP-ADDRESS]
   ```

2. **Connect to PostgreSQL:**
   ```bash
   psql -U postgres
   ```

3. **Run these commands:**
   ```sql
   -- Create database
   CREATE DATABASE financial_automation
       WITH ENCODING='UTF8'
       LC_COLLATE='en_US.UTF-8'
       LC_CTYPE='en_US.UTF-8';
   
   -- Create user (REPLACE YourPasswordHere with your password!)
   CREATE USER smbc_app_user WITH PASSWORD 'YourPasswordHere';
   
   -- Grant privileges
   GRANT ALL PRIVILEGES ON DATABASE financial_automation TO smbc_app_user;
   
   -- Make user the owner
   ALTER DATABASE financial_automation OWNER TO smbc_app_user;
   
   -- Verify
   \l  -- List databases
   \du -- List users
   
   -- Exit
   \q
   ```

4. **Exit SSH:**
   ```bash
   exit
   ```

---

## Part 3: Configure Firewall (1 minute)

### Allow PostgreSQL Port
1. In ADM, go to **Settings** → **Firewall**
2. Add new rule:
   - **Service:** Custom
   - **Protocol:** TCP
   - **Port:** 5432
   - **Source:** LAN (192.168.1.0/24) or specific IP addresses
   - **Action:** Allow
3. Click **Apply**

---

## Part 4: Configure Application (1 minute)

### Step 1: Find Your NAS IP Address
- In ADM, go to **Settings** → **Network** → **Network Interface**
- Note the **IP Address** (e.g., `192.168.1.100`)

### Step 2: Create .env File
1. On your Windows PC, navigate to the application folder
2. Copy `.env.template` to `.env`
3. Edit `.env` file with these values:

```env
# Database Configuration
DB_TYPE=postgresql

# PostgreSQL Settings (UPDATE THESE!)
DB_HOST=192.168.1.100          ← Your NAS IP address
DB_PORT=5432
DB_NAME=financial_automation
DB_USER=smbc_app_user
DB_PASSWORD=YourPasswordHere   ← Password you set in Part 2

# Connection Pool
POOL_MIN_CONN=1
POOL_MAX_CONN=20

# SSL (for local network, prefer or disable)
DB_SSLMODE=prefer
```

4. Save the file

---

## Part 5: Test Connection

### From Development PC:
```bash
cd /path/to/FinancialAutomation
python test_postgres_connection.py
```

**Expected output:**
```
================================================================================
POSTGRESQL CONNECTION TEST
================================================================================

1. Configuration loaded:
   DB_TYPE: postgresql

2. PostgreSQL Configuration:
   Host: 192.168.1.100
   Port: 5432
   Database: financial_automation
   User: smbc_app_user
   Password: **********
   SSL Mode: prefer

3. Checking psycopg2 driver...
   ✅ psycopg2 version: 2.9.x

4. Testing network connectivity to 192.168.1.100:5432...
   ✅ Port 5432 is reachable

5. Testing PostgreSQL connection...
   ✅ Connected successfully!
   PostgreSQL version: PostgreSQL 14.x

   No tables yet (database is empty)
   Run initialize_database() to create schema

6. Testing connection pool...
   Pool settings: 1 min, 20 max connections
   ✅ Connection pool working correctly

================================================================================
CONNECTION TEST SUMMARY
================================================================================
✅ Configuration: OK
✅ psycopg2 driver: OK
✅ Network connectivity: OK
✅ PostgreSQL connection: OK
✅ Connection pool: OK

🎉 PostgreSQL is ready for use!
```

---

## Part 6: Initialize Database Schema

```bash
python -c "from config.database import initialize_database; initialize_database(); print('✅ Database initialized!')"
```

---

## Part 7: Verify Everything Works

Run the test suite:
```bash
python test_company_selection.py
```

Should output:
```
🎉 ALL TESTS PASSED! Company selection feature is fully functional.
```

---

## Troubleshooting

### Cannot reach NAS on port 5432
**Problem:** Network test fails  
**Solutions:**
1. Check NAS IP: `ping [NAS-IP]`
2. Verify PostgreSQL is running: In ADM → **App Central** → **PostgreSQL** → Status should be "Running"
3. Check firewall: Ensure port 5432 is allowed
4. Try from same computer as NAS initially

### Connection refused
**Problem:** PostgreSQL not accepting connections  
**Solutions:**
1. In NAS, check PostgreSQL settings
2. Ensure "Allow remote connections" is enabled
3. Check `pg_hba.conf` allows connections from your IP
4. Restart PostgreSQL service

### Authentication failed
**Problem:** Wrong password  
**Solutions:**
1. Verify password in `.env` matches what you set
2. Try resetting user password:
   ```sql
   ALTER USER smbc_app_user WITH PASSWORD 'NewPassword';
   ```
3. Update `.env` with new password

### Database does not exist
**Problem:** Database not created  
**Solutions:**
1. Verify database exists: `psql -U postgres -l`
2. Create it manually (see Part 2)

---

## Quick Reference

### Important Information to Note:

| Item | Value | Notes |
|------|-------|-------|
| NAS IP Address | ________________ | Check in ADM Network settings |
| PostgreSQL Port | 5432 | Default, usually don't change |
| Database Name | `financial_automation` | Fixed in application |
| Username | `smbc_app_user` | Fixed in application |
| Password | ________________ | **Write this down securely!** |

### Useful Commands:

```bash
# Test connection manually
psql -h [NAS-IP] -U smbc_app_user -d financial_automation

# Check PostgreSQL status (on NAS via SSH)
systemctl status postgresql

# View PostgreSQL logs (on NAS via SSH)
tail -f /var/log/postgresql/postgresql-*.log

# Backup database (run periodically)
pg_dump -h [NAS-IP] -U smbc_app_user financial_automation > backup_$(date +%Y%m%d).sql

# Restore database
psql -h [NAS-IP] -U smbc_app_user financial_automation < backup_20251016.sql
```

---

## Security Best Practices

### 1. Strong Password
- Use at least 16 characters
- Mix uppercase, lowercase, numbers, symbols
- Don't use dictionary words
- Example: `Fn#2k$M9pQ7@vL3x`

### 2. Limit Network Access
- Only allow connections from specific IP addresses in firewall
- Don't expose PostgreSQL to internet unless using VPN

### 3. Regular Backups
- Schedule weekly backups using cron on NAS
- Store backups on separate device/cloud

### 4. SSL Certificate (Optional, for remote access)
- Use Let's Encrypt or self-signed certificate
- Set `DB_SSLMODE=require` in `.env`

---

## Remote Access Setup (Optional)

### Option 1: VPN (Recommended)
1. In ADM, go to **Services** → **VPN Server**
2. Enable **OpenVPN** or **L2TP/IPSec**
3. Download VPN configuration
4. Install VPN client on remote computer
5. Connect to VPN, then use NAS IP as if local

### Option 2: Port Forwarding (Less Secure)
1. In router, forward external port 55432 to NAS:5432
2. Get dynamic DNS (DuckDNS, No-IP)
3. Update `.env`:
   ```env
   DB_HOST=your-dynamic-dns.duckdns.org
   DB_PORT=55432
   DB_SSLMODE=require
   ```
4. **Enable SSL certificate!**

---

## Done! 🎉

You now have:
- ✅ PostgreSQL running on NAS
- ✅ Database created
- ✅ User configured
- ✅ Application connected
- ✅ Multi-user support enabled

The application can now be used by multiple users simultaneously over the network!

---

## Next Steps

1. **Deploy to other PCs:**
   - Copy `.exe` and `.env` to each user's computer
   - Ensure all PCs can reach NAS IP
   - Each user gets their own username/password in PostgreSQL

2. **Setup backups:**
   - Create cron job for daily backups
   - Test restore procedure

3. **Monitor performance:**
   - Check connection pool usage
   - Adjust `POOL_MAX_CONN` if needed

4. **Train users:**
   - Show company selection dropdown
   - Demonstrate multi-user workflow
   - Explain session persistence
