# 🔧 PostgreSQL Connection Troubleshooting

## ❌ Error: "no password supplied"

This error means the application cannot find your `.env` configuration file or the password is not being read correctly.

---

## 🎯 SOLUTION - Step by Step

### **STEP 1: Check if .env file exists**

1. **Open** your application folder:
   ```
   C:\Financials Automation_Github\FinancialAutomation_v1.0_Complete\deployment_package_v1.0
   ```

2. **Look for** a file named `.env` (starts with a dot)
   - In Windows Explorer, you might not see it by default
   - Click on "View" tab → Check "File name extensions" and "Hidden items"

3. **If you DON'T see .env file** → Go to STEP 2
4. **If you DO see .env file** → Go to STEP 3

---

### **STEP 2: Create .env File** (If it doesn't exist)

#### Method A: Using PowerShell (Recommended)

1. **Open PowerShell** in your application folder
   - Hold Shift + Right-click in folder
   - Select "Open PowerShell window here"

2. **Run this command**:
   ```powershell
   @"
# Database Configuration
DB_TYPE=postgresql

# PostgreSQL Settings
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=financial_automation
POSTGRES_USER=fin_app_user
POSTGRES_PASSWORD=FinApp@2025

# Connection Pool Settings
POSTGRES_MIN_CONN=2
POSTGRES_MAX_CONN=10
"@ | Out-File -FilePath .env -Encoding UTF8
   ```

3. **Verify** the file was created:
   ```powershell
   Get-Content .env
   ```

4. **Done!** Now go to STEP 4

#### Method B: Using Notepad (Alternative)

1. **Open Notepad**

2. **Copy and paste** this EXACTLY:
   ```
   # Database Configuration
   DB_TYPE=postgresql

   # PostgreSQL Settings
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   POSTGRES_DB=financial_automation
   POSTGRES_USER=fin_app_user
   POSTGRES_PASSWORD=FinApp@2025

   # Connection Pool Settings
   POSTGRES_MIN_CONN=2
   POSTGRES_MAX_CONN=10
   ```

3. **Replace** `FinApp@2025` with YOUR password (the one you set for fin_app_user)

4. **Click** File → Save As

5. **Important**: In the Save dialog:
   - File name: `.env` (with the dot, including quotes: `".env"`)
   - Save as type: **All Files (*.*)**
   - Encoding: **UTF-8**
   - Location: Your application folder

6. **Click** Save

7. **Verify**: You should now see `.env` file in your folder

8. **Done!** Now go to STEP 4

---

### **STEP 3: Verify .env File Contents** (If file exists)

1. **Right-click** on `.env` file

2. **Select** "Open with" → "Notepad"

3. **Check** that it contains:
   ```
   DB_TYPE=postgresql
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   POSTGRES_DB=financial_automation
   POSTGRES_USER=fin_app_user
   POSTGRES_PASSWORD=YOUR_PASSWORD_HERE
   ```

4. **Verify**:
   - ✅ No extra spaces before or after `=`
   - ✅ Password matches what you set in PostgreSQL
   - ✅ No quotes around values (unless your password contains special characters)
   - ✅ File is saved as `.env` not `.env.txt`

5. **If anything is wrong** → Fix it and save

---

### **STEP 4: Run Diagnostic Script**

1. **Open PowerShell** in your application folder

2. **Run diagnostic**:
   ```powershell
   python check_env.py
   ```

3. **Review the output**:
   - It will show if `.env` file exists
   - It will show the contents (password hidden)
   - It will show if settings are loaded correctly

4. **If it shows "❌ .env file NOT FOUND"** → Go back to STEP 2

5. **If it shows all settings correctly** → Continue to STEP 5

---

### **STEP 5: Initialize Database Again**

Now that `.env` file is correct, try initializing again:

#### Option A: Using Demo Script (Easier)
```powershell
python demo_db_setup_simple.py
```

#### Option B: Using Python Command
```powershell
python -c "from config.database import initialize_database; initialize_database()"
```

**Expected output**:
```
✅ Database initialized
✅ Admin user created
✅ 23 tables created
```

---

## 🔍 COMMON ISSUES & FIXES

### Issue 1: File is named `.env.txt` instead of `.env`

**How to check**:
```powershell
Get-ChildItem -Force | Where-Object { $_.Name -like "*.env*" }
```

**Fix**:
```powershell
Rename-Item .env.txt .env
```

### Issue 2: Wrong password in .env file

**Symptoms**: 
- Error: "password authentication failed for user"
- Error: "no password supplied"

**Fix**:
1. Open pgAdmin 4
2. Right-click on "fin_app_user" → Properties
3. Go to Definition tab
4. Set new password: `FinApp@2025` (or note your password)
5. Update `.env` file with the same password

### Issue 3: User doesn't exist

**Error**: "role 'fin_app_user' does not exist"

**Fix** - Run in pgAdmin Query Tool:
```sql
-- Create user
CREATE USER fin_app_user WITH PASSWORD 'FinApp@2025';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE financial_automation TO fin_app_user;
GRANT ALL ON SCHEMA public TO fin_app_user;
```

### Issue 4: Database doesn't exist

**Error**: "database 'financial_automation' does not exist"

**Fix** - Run in pgAdmin Query Tool:
```sql
CREATE DATABASE financial_automation
    ENCODING = 'UTF8'
    TEMPLATE = template0;
```

### Issue 5: PostgreSQL not running

**Error**: "could not connect to server"

**Fix**:
1. Press `Windows Key + R`
2. Type: `services.msc`
3. Find: `postgresql-x64-15`
4. Right-click → Start

### Issue 6: Wrong host or port

**Symptoms**: "Connection refused" or "could not connect"

**Fix** - Verify in .env:
```
POSTGRES_HOST=localhost    # Use localhost if same computer
POSTGRES_PORT=5432         # Default PostgreSQL port
```

---

## 🧪 QUICK TEST COMMANDS

### Test 1: Check if .env file exists
```powershell
Test-Path .env
```
**Expected**: `True`

### Test 2: Show .env contents (safe)
```powershell
Get-Content .env | ForEach-Object { 
    if ($_ -match 'PASSWORD') { 
        ($_ -split '=')[0] + '=***HIDDEN***' 
    } else { 
        $_ 
    }
}
```

### Test 3: Check PostgreSQL connection
```powershell
python -c "import psycopg2; conn = psycopg2.connect(host='localhost', port=5432, dbname='financial_automation', user='fin_app_user', password='FinApp@2025'); print('✅ Connection successful!'); conn.close()"
```
**Note**: Replace `FinApp@2025` with your actual password

### Test 4: List PostgreSQL databases
```powershell
python -c "import psycopg2; conn = psycopg2.connect(host='localhost', port=5432, dbname='postgres', user='postgres', password='YOUR_POSTGRES_PASSWORD'); cur = conn.cursor(); cur.execute('SELECT datname FROM pg_database'); print('\n'.join([row[0] for row in cur.fetchall()])); conn.close()"
```
**Note**: Replace `YOUR_POSTGRES_PASSWORD` with postgres user password

---

## 📋 COMPLETE .env FILE TEMPLATE

**Copy this EXACTLY** (update password):

```env
# Database Configuration
DB_TYPE=postgresql

# PostgreSQL Settings - Local Installation
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=financial_automation
POSTGRES_USER=fin_app_user
POSTGRES_PASSWORD=FinApp@2025

# Connection Pool Settings
POSTGRES_MIN_CONN=2
POSTGRES_MAX_CONN=10

# Optional: SSL Mode (uncomment if needed)
# POSTGRES_SSLMODE=prefer
```

---

## 🎯 COMPLETE WORKFLOW TO FIX

**Follow these steps in order**:

```powershell
# Step 1: Go to application folder
cd "C:\Financials Automation_Github\FinancialAutomation_v1.0_Complete\deployment_package_v1.0"

# Step 2: Create .env file (copy from template above)
notepad .env

# Step 3: Run diagnostic
python check_env.py

# Step 4: Initialize database
python demo_db_setup_simple.py

# Step 5: Run application
python main.py
```

---

## 🆘 STILL NOT WORKING?

### Checklist:
- [ ] `.env` file exists in the same folder as `main.py`
- [ ] `.env` file has correct password
- [ ] PostgreSQL service is running (check services.msc)
- [ ] Database `financial_automation` exists (check in pgAdmin)
- [ ] User `fin_app_user` exists (check in pgAdmin)
- [ ] User has permissions on database (check in pgAdmin)
- [ ] No firewall blocking port 5432
- [ ] Python can import psycopg2 (`pip install psycopg2`)

### Get More Help:
1. Run diagnostic script: `python check_env.py`
2. Check the output carefully
3. Follow the specific fix for your issue above
4. If still stuck, provide the output of the diagnostic script

---

## ✅ SUCCESS INDICATORS

**You know it's working when**:
1. `python check_env.py` shows all settings correctly
2. `python demo_db_setup_simple.py` completes without errors
3. You see "✅ Database initialized" message
4. Application launches and you can login

---

*PostgreSQL Troubleshooting Guide*  
*Financial Automation v1.0*  
*Last Updated: October 20, 2025*
