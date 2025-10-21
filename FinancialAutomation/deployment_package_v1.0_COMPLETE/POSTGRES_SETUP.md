# PostgreSQL Configuration for Financial Automation

## IMPORTANT: You are using PostgreSQL!

### Environment Variables Required:

Create a `.env` file in the application folder with:

```bash
DB_TYPE=postgresql
DB_HOST=your_postgres_server_ip
DB_PORT=5432
DB_NAME=financial_automation
DB_USER=your_db_username
DB_PASSWORD=your_db_password
DB_SSLMODE=prefer
```

### Example .env file:

```bash
DB_TYPE=postgresql
DB_HOST=192.168.1.100
DB_PORT=5432
DB_NAME=financial_automation
DB_USER=app_user
DB_PASSWORD=SecurePassword123
```

### Required Package:

```powershell
pip install psycopg2-binary
```

### Database Setup:

1. **Create Database** (run this on your PostgreSQL server):
```sql
CREATE DATABASE financial_automation;
CREATE USER app_user WITH PASSWORD 'SecurePassword123';
GRANT ALL PRIVILEGES ON DATABASE financial_automation TO app_user;
```

2. **Initialize Tables** (run the application once - it will create tables automatically)

### Connection Details:

- **Type:** PostgreSQL (not SQLite)
- **Location:** Your PostgreSQL server
- **Persistence:** Data stored on PostgreSQL server
- **Multi-user:** Supports multiple users simultaneously

### For .exe Deployment:

1. Copy the `.env` file to the same folder as your .exe
2. Or set environment variables system-wide
3. Ensure PostgreSQL server is accessible from all client machines
4. Each user connects to the SAME database on the server

### Network Requirements:

- PostgreSQL server must be accessible on port 5432
- Firewall must allow connections from client machines
- PostgreSQL must be configured to accept remote connections

### Troubleshooting:

**"Connection refused":**
- Check DB_HOST is correct
- Check PostgreSQL is running
- Check firewall allows port 5432

**"Authentication failed":**
- Check DB_USER and DB_PASSWORD
- Check PostgreSQL pg_hba.conf allows connections

**"Database does not exist":**
- Create the database first (see SQL above)

### Benefits of PostgreSQL:

✅ Multi-user simultaneous access
✅ Data centralized on server
✅ Better performance for large datasets
✅ ACID compliance
✅ Backup/restore capabilities
✅ Role-based access control
