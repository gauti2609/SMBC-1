# 🚀 Deployment Guide - Financial Automation Application

**Version:** 1.0.0  
**Date:** October 19, 2025  
**For:** System Administrators and DevOps Teams

---

## 📋 Table of Contents

1. [Deployment Options](#deployment-options)
2. [Single-User Deployment (SQLite)](#single-user-deployment-sqlite)
3. [Multi-User Deployment (PostgreSQL)](#multi-user-deployment-postgresql)
4. [Creating Executables](#creating-executables)
5. [Cloud Deployment](#cloud-deployment)
6. [Security Considerations](#security-considerations)
7. [Backup & Recovery](#backup--recovery)
8. [Monitoring & Maintenance](#monitoring--maintenance)

---

## 🎯 Deployment Options

### Option 1: Single-User Desktop Application (Recommended for Small Teams)

- **Database:** SQLite (embedded)
- **Deployment:** Standalone executable
- **Users:** 1-2 concurrent users
- **Setup Time:** 10 minutes
- **Infrastructure:** None required

### Option 2: Multi-User Client-Server (Recommended for Medium/Large Organizations)

- **Database:** PostgreSQL (server)
- **Deployment:** Client executables + Database server
- **Users:** 5-100+ concurrent users
- **Setup Time:** 1-2 hours
- **Infrastructure:** Database server required

### Option 3: Web-Based (Future Enhancement)

- **Technology:** Python backend + Web frontend
- **Deployment:** Cloud or on-premise server
- **Users:** Unlimited
- **Status:** Planned for v2.0

---

## 💻 Single-User Deployment (SQLite)

### Prerequisites

- Windows 10/11, macOS 10.14+, or Ubuntu 18.04+
- 4 GB RAM minimum
- 500 MB disk space

### Deployment Steps

#### Step 1: Prepare Application Files

```bash
# Clone repository
git clone <repository-url>
cd FinancialAutomation

# Install dependencies
pip install -r requirements.txt
```

#### Step 2: Create Executable (Optional)

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --name="FinancialAutomation" \
            --onefile \
            --windowed \
            --icon=resources/icons/app_icon.ico \
            --add-data="resources;resources" \
            main.py

# Output will be in dist/ folder
```

**Windows:**
```cmd
pyinstaller --name="FinancialAutomation" --onefile --windowed --icon=resources\icons\app_icon.ico main.py
```

**macOS:**
```bash
pyinstaller --name="FinancialAutomation" --onefile --windowed --icon=resources/icons/app_icon.icns main.py
```

#### Step 3: Package for Distribution

**Create Installation Package:**

1. **Create folder structure:**
```
FinancialAutomation_v1.0/
├── FinancialAutomation.exe (or binary)
├── README.txt
├── LICENSE.txt
├── USER_GUIDE.pdf
└── resources/
    ├── icons/
    ├── templates/
    └── sample_data/
```

2. **Create README.txt:**
```txt
Financial Automation Application v1.0
====================================

To Install:
1. Extract all files to a folder (e.g., C:\FinancialAutomation)
2. Run FinancialAutomation.exe
3. Create admin user on first launch
4. Refer to USER_GUIDE.pdf for usage instructions

Database:
- SQLite database will be created automatically
- Location: Same folder as executable (financial_automation.db)

Support:
- Email: support@example.com
- Documentation: See USER_GUIDE.pdf
```

3. **Create ZIP/Installer:**
   - **Windows:** Use Inno Setup or NSIS for installer
   - **macOS:** Use DMG creation tool
   - **Linux:** Create .deb or .rpm package

#### Step 4: Deploy to End Users

**Distribution Methods:**

1. **Direct Download:**
   - Upload ZIP to company server
   - Send download link to users
   - Users extract and run

2. **USB/Network Share:**
   - Copy folder to network share
   - Users run from network (or copy to local machine)

3. **Installer Package:**
   - Create Windows installer (.exe)
   - Double-click to install
   - Creates desktop shortcut

### Database Location

**Default SQLite Database Location:**
- Windows: `C:\Users\<username>\AppData\Local\FinancialAutomation\financial_automation.db`
- macOS: `~/Library/Application Support/FinancialAutomation/financial_automation.db`
- Linux: `~/.local/share/FinancialAutomation/financial_automation.db`

**Custom Location:**
Set in `.env` file:
```env
DB_TYPE=sqlite
SQLITE_DB_PATH=/path/to/custom/location/financial_automation.db
```

---

## 🌐 Multi-User Deployment (PostgreSQL)

### Prerequisites

- PostgreSQL 12+ server
- Python 3.8+ on client machines
- Network connectivity between clients and database server

### Server Setup

#### Step 1: Install PostgreSQL

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**Windows:**
1. Download PostgreSQL installer from postgresql.org
2. Run installer
3. Note the password for 'postgres' user
4. Ensure PostgreSQL service is running

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

#### Step 2: Create Database and User

```bash
# Login to PostgreSQL
sudo -u postgres psql

# Create database
CREATE DATABASE financial_automation;

# Create user
CREATE USER fin_app_user WITH PASSWORD 'SecurePassword123!';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE financial_automation TO fin_app_user;

# Exit
\q
```

#### Step 3: Configure PostgreSQL for Remote Access

**Edit `postgresql.conf`:**
```conf
# Listen on all interfaces
listen_addresses = '*'

# Connection settings
max_connections = 100
```

**Edit `pg_hba.conf`:**
```conf
# Allow connections from your network
# Format: TYPE  DATABASE        USER            ADDRESS                 METHOD
host    financial_automation    fin_app_user    192.168.1.0/24         md5
host    financial_automation    fin_app_user    0.0.0.0/0              md5  # For testing only!
```

**Restart PostgreSQL:**
```bash
sudo systemctl restart postgresql
```

#### Step 4: Initialize Database Schema

```bash
# Copy initialization script to server
cd FinancialAutomation

# Set environment variables
export DB_TYPE=postgresql
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export POSTGRES_DB=financial_automation
export POSTGRES_USER=fin_app_user
export POSTGRES_PASSWORD=SecurePassword123!

# Run initialization
python -c "from config.database import initialize_database; initialize_database()"
```

### Client Setup

#### Step 1: Create .env File

Create `.env` file on each client:

```env
# Database Configuration
DB_TYPE=postgresql

# PostgreSQL Settings
POSTGRES_HOST=192.168.1.100  # Your database server IP
POSTGRES_PORT=5432
POSTGRES_DB=financial_automation
POSTGRES_USER=fin_app_user
POSTGRES_PASSWORD=SecurePassword123!

# Connection Pool Settings
POSTGRES_MIN_CONN=2
POSTGRES_MAX_CONN=10
```

#### Step 2: Install Client Application

**Option A: Python Installation**
```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

**Option B: Executable Distribution**
```bash
# Create executable with .env bundled
pyinstaller --onefile --windowed \
            --add-data=".env;." \
            --add-data="resources;resources" \
            main.py

# Distribute to users
# Users run FinancialAutomation.exe
```

#### Step 3: Test Connection

1. Launch application on client
2. Login screen should appear
3. Create test user
4. If connection fails, check:
   - Server IP is correct
   - PostgreSQL is running
   - Firewall allows port 5432
   - .env file is in correct location

### Load Balancing (Advanced)

For high-traffic deployments:

**Option 1: PostgreSQL Read Replicas**
```env
POSTGRES_HOST_PRIMARY=192.168.1.100
POSTGRES_HOST_REPLICA1=192.168.1.101
POSTGRES_HOST_REPLICA2=192.168.1.102
```

**Option 2: PgBouncer Connection Pooling**
```bash
# Install PgBouncer
sudo apt install pgbouncer

# Configure for connection pooling
# Edit /etc/pgbouncer/pgbouncer.ini

# Point clients to PgBouncer instead of PostgreSQL
```

---

## 📦 Creating Executables

### Windows Executable (.exe)

```bash
# Install dependencies
pip install pyinstaller pillow

# Create single executable
pyinstaller --name="FinancialAutomation" \
            --onefile \
            --windowed \
            --icon=resources/icons/app_icon.ico \
            --add-data="resources;resources" \
            --add-data=".env;." \
            --hidden-import=PyQt5 \
            --hidden-import=psycopg2 \
            --hidden-import=openpyxl \
            main.py

# Output: dist/FinancialAutomation.exe
```

### macOS Application (.app)

```bash
# Create app bundle
pyinstaller --name="FinancialAutomation" \
            --onefile \
            --windowed \
            --icon=resources/icons/app_icon.icns \
            --add-data="resources:resources" \
            --add-data=".env:." \
            main.py

# Output: dist/FinancialAutomation.app

# Create DMG (optional)
hdiutil create -volname "Financial Automation" \
               -srcfolder dist/FinancialAutomation.app \
               -ov -format UDZO \
               FinancialAutomation_v1.0.dmg
```

### Linux Binary

```bash
# Create Linux executable
pyinstaller --name="FinancialAutomation" \
            --onefile \
            --windowed \
            --add-data="resources:resources" \
            --add-data=".env:." \
            main.py

# Output: dist/FinancialAutomation

# Create .deb package (optional)
# Use dpkg-deb or fpm tool
```

### Troubleshooting Executable Creation

**Issue: Missing Modules**
```bash
# Add hidden imports
--hidden-import=module_name
```

**Issue: Resource Files Not Found**
```bash
# Check add-data paths
--add-data="source_path;dest_path"  # Windows
--add-data="source_path:dest_path"  # macOS/Linux
```

**Issue: Large File Size**
```bash
# Use UPX compression
pip install pyinstaller[encryption]
pyinstaller --upx-dir=/path/to/upx ...
```

---

## ☁️ Cloud Deployment

### AWS Deployment

#### Architecture

```
[Users] → [Application Load Balancer] → [EC2 Instances]
                                              ↓
                                         [RDS PostgreSQL]
                                              ↓
                                         [S3 for Backups]
```

#### Setup Steps

**1. RDS PostgreSQL Database:**
```bash
# Create RDS instance via AWS Console or CLI
aws rds create-db-instance \
    --db-instance-identifier financial-automation-db \
    --db-instance-class db.t3.medium \
    --engine postgres \
    --master-username admin \
    --master-user-password SecurePassword123! \
    --allocated-storage 100 \
    --vpc-security-group-ids sg-xxxxx \
    --availability-zone us-east-1a
```

**2. EC2 Application Server (if web-based in future):**
```bash
# Launch EC2 instance
# Install dependencies
# Deploy application
```

**3. S3 Backup Bucket:**
```bash
# Create S3 bucket
aws s3 mb s3://financial-automation-backups

# Enable versioning
aws s3api put-bucket-versioning \
    --bucket financial-automation-backups \
    --versioning-configuration Status=Enabled
```

### Azure Deployment

```bash
# Create Azure Database for PostgreSQL
az postgres server create \
    --resource-group FinancialAutomation \
    --name financial-automation-db \
    --location eastus \
    --admin-user adminuser \
    --admin-password SecurePassword123! \
    --sku-name GP_Gen5_2

# Create Web App (if web-based)
az webapp create \
    --resource-group FinancialAutomation \
    --plan AppServicePlan \
    --name financial-automation-app \
    --runtime "PYTHON|3.9"
```

### Google Cloud Platform

```bash
# Create Cloud SQL instance
gcloud sql instances create financial-automation-db \
    --database-version=POSTGRES_13 \
    --cpu=2 \
    --memory=7680MB \
    --region=us-central1

# Create database
gcloud sql databases create financial_automation \
    --instance=financial-automation-db
```

---

## 🔒 Security Considerations

### Database Security

1. **Use Strong Passwords:**
```env
# Bad
POSTGRES_PASSWORD=admin123

# Good
POSTGRES_PASSWORD=R@nd0m!P@ssw0rd#2024$Secur3
```

2. **Encrypt Connections:**
```env
# Enable SSL/TLS
POSTGRES_SSLMODE=require
```

3. **Limit Database Access:**
```sql
-- Revoke public access
REVOKE ALL ON DATABASE financial_automation FROM PUBLIC;

-- Grant only to specific users
GRANT CONNECT ON DATABASE financial_automation TO fin_app_user;
```

4. **Use Connection Pooling:**
```env
POSTGRES_MAX_CONN=10  # Limit connections per client
```

### Application Security

1. **Password Hashing:**
```python
# Already implemented in models/user.py
# Uses bcrypt for password hashing
```

2. **Environment Variables:**
```bash
# Never commit .env file to git
echo ".env" >> .gitignore

# Use different .env for dev/prod
.env.development
.env.production
```

3. **File Permissions:**
```bash
# Restrict .env file access
chmod 600 .env

# Restrict database file (SQLite)
chmod 600 financial_automation.db
```

4. **Audit Logging:**
```python
# Add audit trail (future enhancement)
# Log all data changes with user, timestamp
```

### Network Security

1. **Firewall Rules:**
```bash
# PostgreSQL server
sudo ufw allow from 192.168.1.0/24 to any port 5432

# Block all other access
sudo ufw deny 5432
```

2. **VPN Access:**
```bash
# Require VPN for database access
# Use OpenVPN or WireGuard
```

3. **SSL Certificates:**
```bash
# Use Let's Encrypt for HTTPS (if web-based)
certbot --nginx -d financial-automation.example.com
```

---

## 💾 Backup & Recovery

### SQLite Backup

**Automated Backup Script:**
```bash
#!/bin/bash
# backup_sqlite.sh

DB_PATH="/path/to/financial_automation.db"
BACKUP_DIR="/path/to/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/financial_automation_$DATE.db"

# Create backup
cp "$DB_PATH" "$BACKUP_FILE"

# Compress
gzip "$BACKUP_FILE"

# Delete backups older than 30 days
find "$BACKUP_DIR" -name "financial_automation_*.db.gz" -mtime +30 -delete

echo "Backup completed: $BACKUP_FILE.gz"
```

**Schedule with Cron:**
```bash
# Edit crontab
crontab -e

# Daily backup at 2 AM
0 2 * * * /path/to/backup_sqlite.sh
```

### PostgreSQL Backup

**Manual Backup:**
```bash
# Full backup
pg_dump -h localhost -U fin_app_user financial_automation > backup_$(date +%Y%m%d).sql

# Compressed backup
pg_dump -h localhost -U fin_app_user financial_automation | gzip > backup_$(date +%Y%m%d).sql.gz
```

**Automated Backup Script:**
```bash
#!/bin/bash
# backup_postgres.sh

PGHOST=localhost
PGPORT=5432
PGDATABASE=financial_automation
PGUSER=fin_app_user
export PGPASSWORD=SecurePassword123!

BACKUP_DIR=/backups/postgres
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE=$BACKUP_DIR/financial_automation_$DATE.sql.gz

# Create backup
pg_dump -h $PGHOST -p $PGPORT -U $PGUSER $PGDATABASE | gzip > $BACKUP_FILE

# Upload to S3 (optional)
aws s3 cp $BACKUP_FILE s3://financial-automation-backups/

# Delete local backups older than 7 days
find $BACKUP_DIR -name "financial_automation_*.sql.gz" -mtime +7 -delete

echo "Backup completed: $BACKUP_FILE"
```

**Schedule with Cron:**
```bash
# Hourly backups
0 * * * * /path/to/backup_postgres.sh

# Or daily at 2 AM
0 2 * * * /path/to/backup_postgres.sh
```

### Restore Procedures

**SQLite Restore:**
```bash
# Stop application
# Replace database file
cp backup_20241019.db financial_automation.db
# Restart application
```

**PostgreSQL Restore:**
```bash
# Drop existing database (CAUTION!)
dropdb -h localhost -U fin_app_user financial_automation

# Recreate database
createdb -h localhost -U fin_app_user financial_automation

# Restore from backup
gunzip < backup_20241019.sql.gz | psql -h localhost -U fin_app_user financial_automation

# Or if not compressed
psql -h localhost -U fin_app_user financial_automation < backup_20241019.sql
```

---

## 📊 Monitoring & Maintenance

### Database Monitoring

**PostgreSQL Performance:**
```sql
-- Check active connections
SELECT count(*) FROM pg_stat_activity;

-- Check database size
SELECT pg_size_pretty(pg_database_size('financial_automation'));

-- Check table sizes
SELECT 
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Check slow queries
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;
```

**SQLite Monitoring:**
```bash
# Check database size
ls -lh financial_automation.db

# Check integrity
sqlite3 financial_automation.db "PRAGMA integrity_check;"

# Optimize database
sqlite3 financial_automation.db "VACUUM;"
```

### Application Logs

**Enable Logging:**
```python
# Add to main.py
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

**Monitor Logs:**
```bash
# Tail logs in real-time
tail -f app.log

# Search for errors
grep ERROR app.log

# Count errors per day
grep ERROR app.log | cut -d' ' -f1 | uniq -c
```

### Maintenance Tasks

**Daily:**
- ✅ Check application logs for errors
- ✅ Verify backups completed successfully
- ✅ Monitor database disk space

**Weekly:**
- ✅ Review user activity logs
- ✅ Test backup restoration (sample)
- ✅ Update security patches

**Monthly:**
- ✅ Database optimization (VACUUM, REINDEX)
- ✅ Review and archive old data
- ✅ Update application to latest version
- ✅ Security audit

**Quarterly:**
- ✅ Full disaster recovery test
- ✅ Performance optimization review
- ✅ User feedback and feature requests review

---

## 📝 Deployment Checklist

### Pre-Deployment

- [ ] Test application thoroughly in staging environment
- [ ] Create database backups
- [ ] Document all configuration settings
- [ ] Prepare rollback plan
- [ ] Notify users of deployment schedule
- [ ] Schedule maintenance window

### Deployment

- [ ] Deploy database changes (if any)
- [ ] Deploy application files
- [ ] Update configuration files (.env)
- [ ] Test database connectivity
- [ ] Verify all modules working
- [ ] Check logs for errors

### Post-Deployment

- [ ] Monitor application for 24 hours
- [ ] Collect user feedback
- [ ] Address any issues immediately
- [ ] Update documentation
- [ ] Mark deployment as successful

---

## 🆘 Support & Escalation

### Level 1: User Support
- User guide and FAQs
- Email support
- Basic troubleshooting

### Level 2: Technical Support
- Database issues
- Performance problems
- Bug fixes

### Level 3: Development Team
- Code changes
- New features
- Critical issues

---

## 📞 Contact Information

**Technical Support:**
- Email: support@example.com
- Phone: +91-XXXX-XXXXXX

**Emergency Escalation:**
- On-Call: +91-XXXX-XXXXXX
- Email: emergency@example.com

---

**Document Version:** 1.0  
**Last Updated:** October 19, 2025  
**Next Review:** January 19, 2026
