# 🪟 Windows PostgreSQL Setup Guide

**Complete Step-by-Step Guide for Setting Up PostgreSQL on Windows**

This guide provides crystal-clear instructions for installing and configuring PostgreSQL on Windows for the Financial Automation Application.

---

## 📋 Prerequisites

- Windows 10 or Windows 11
- Administrator access on your computer
- 500 MB free disk space
- Internet connection for downloading PostgreSQL

---

## 🎯 PART 1: INSTALL POSTGRESQL

### Step 1: Download PostgreSQL

1. **Open your web browser** (Chrome, Edge, Firefox, etc.)

2. **Go to**: https://www.postgresql.org/download/windows/

3. **Click** on "Download the installer" link
   - This will take you to the EnterpriseDB website

4. **Choose version**: PostgreSQL 15.x or 16.x (latest stable version)
   - Click on **"Windows x86-64"** for 64-bit systems (most modern PCs)

5. **Download** the installer (file will be named like `postgresql-15.x-windows-x64.exe`)
   - Save it to your Downloads folder
   - File size is approximately 200-300 MB

### Step 2: Run the PostgreSQL Installer

1. **Locate the downloaded file** in your Downloads folder
   - File name: `postgresql-15.x-windows-x64.exe`

2. **Double-click** the installer file

3. **Allow changes** if Windows asks "Do you want to allow this app to make changes?"
   - Click **"Yes"**

### Step 3: Installation Wizard - Follow These Screens

#### Screen 1: Welcome
- Click **"Next"**

#### Screen 2: Installation Directory
- Default location: `C:\Program Files\PostgreSQL\15`
- **Keep the default** and click **"Next"**

#### Screen 3: Select Components
- ✅ **PostgreSQL Server** (must be checked)
- ✅ **pgAdmin 4** (must be checked - this is the management tool)
- ✅ **Stack Builder** (optional)
- ✅ **Command Line Tools** (must be checked)
- Click **"Next"**

#### Screen 4: Data Directory
- Default location: `C:\Program Files\PostgreSQL\15\data`
- **Keep the default** and click **"Next"**

#### Screen 5: Password
- **IMPORTANT**: Set a password for the PostgreSQL superuser (postgres)
- Enter a strong password (e.g., `Admin@123` or better)
- **WRITE THIS DOWN** - You'll need it later!
- Re-enter the password to confirm
- Click **"Next"**

#### Screen 6: Port Number
- Default port: **5432**
- **Keep the default** and click **"Next"**

#### Screen 7: Locale
- Default: `[Default locale]`
- **Keep the default** and click **"Next"**

#### Screen 8: Pre Installation Summary
- Review your settings
- Click **"Next"**

#### Screen 9: Ready to Install
- Click **"Next"** to begin installation
- Installation will take 2-5 minutes
- You'll see a progress bar

#### Screen 10: Completing Setup
- ✅ Installation complete!
- **Uncheck** "Launch Stack Builder at exit" (not needed right now)
- Click **"Finish"**

---

## ✅ PART 2: VERIFY POSTGRESQL INSTALLATION

### Step 1: Check if PostgreSQL is Running

1. **Press** `Windows Key + R` to open Run dialog

2. **Type**: `services.msc` and press **Enter**

3. **Look for** "postgresql-x64-15" (or your version) in the services list
   - Status should be: **Running**
   - Startup Type should be: **Automatic**

4. If not running:
   - Right-click on "postgresql-x64-15"
   - Click **"Start"**

### Step 2: Test PostgreSQL Connection

1. **Open** Windows Start Menu

2. **Search for**: "pgAdmin 4"

3. **Click** on "pgAdmin 4" to launch
   - It will open in your web browser

4. **Enter Master Password** (if prompted)
   - This is different from the postgres password
   - Set a password and remember it

5. **Expand** "Servers" in the left panel

6. **Click** on "PostgreSQL 15" (or your version)

7. **Enter the password** you set during installation
   - This is the postgres user password
   - Check "Save password" if you want

8. **Success!** If you see databases listed, PostgreSQL is working!

---

## 🗄️ PART 3: CREATE DATABASE FOR FINANCIAL AUTOMATION

### Method 1: Using pgAdmin 4 (Graphical Interface - Easier)

#### Step 1: Create Database

1. **Open pgAdmin 4** (if not already open)

2. **Connect** to PostgreSQL server (enter password if needed)

3. **Right-click** on "Databases" in the left panel

4. **Select** "Create" → "Database..."

5. **Fill in the dialog**:
   - **Database name**: `financial_automation` (exactly as written, lowercase)
   - **Owner**: Leave as "postgres"
   - **Encoding**: UTF8
   - **Template**: template0
   - **Connection limit**: -1

6. **Click** "Save"

7. ✅ Database "financial_automation" is created!

#### Step 2: Create Application User

1. **Right-click** on "Login/Group Roles" in the left panel

2. **Select** "Create" → "Login/Group Role..."

3. **Go to "General" tab**:
   - **Name**: `fin_app_user` (exactly as written)

4. **Go to "Definition" tab**:
   - **Password**: `FinApp@2025` (or choose your own - write it down!)
   - **Password expiration**: Leave blank

5. **Go to "Privileges" tab**:
   - ✅ Check **"Can login?"**
   - ✅ Check **"Create databases?"** (optional)

6. **Click** "Save"

7. ✅ User "fin_app_user" is created!

#### Step 3: Grant Permissions to User

1. **Right-click** on "financial_automation" database

2. **Select** "Properties"

3. **Go to "Security" tab**

4. **Click** the **"+"** button to add a new privilege

5. **Fill in**:
   - **Grantee**: `fin_app_user` (select from dropdown)
   - **Privileges**: Check **ALL**

6. **Click** "Save"

7. ✅ Permissions granted!

### Method 2: Using SQL Commands (Advanced)

#### Step 1: Open SQL Tool

1. **Open pgAdmin 4**

2. **Connect** to PostgreSQL server

3. **Click** on "PostgreSQL 15" server in left panel

4. **Click** "Tools" menu → "Query Tool"

#### Step 2: Run SQL Commands

**Copy and paste these commands ONE AT A TIME** into the Query Tool:

```sql
-- Create database
CREATE DATABASE financial_automation
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    TEMPLATE = template0;
```

Click **"Execute"** button (▶ icon) or press **F5**

```sql
-- Create user
CREATE USER fin_app_user WITH PASSWORD 'FinApp@2025';
```

Click **"Execute"** button

```sql
-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE financial_automation TO fin_app_user;
```

Click **"Execute"** button

```sql
-- Grant schema privileges (important!)
\c financial_automation
GRANT ALL ON SCHEMA public TO fin_app_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO fin_app_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO fin_app_user;
```

Click **"Execute"** button

✅ Database and user created successfully!

---

## 🔧 PART 4: CONFIGURE WINDOWS FIREWALL (If Using Multiple Computers)

**SKIP THIS SECTION** if you're only using PostgreSQL on the same computer as the application.

**DO THIS SECTION** if you want to access PostgreSQL from other computers on your network.

### Step 1: Open Windows Firewall

1. **Press** `Windows Key + R`

2. **Type**: `wf.msc` and press **Enter**

3. **Click** "Inbound Rules" in the left panel

### Step 2: Create Firewall Rule

1. **Click** "New Rule..." in the right panel

2. **Select** "Port" and click **"Next"**

3. **Select** "TCP"

4. **Specific local ports**: Enter `5432`

5. **Click** "Next"

6. **Select** "Allow the connection" and click **"Next"**

7. **Check all three**: Domain, Private, Public

8. **Click** "Next"

9. **Name**: `PostgreSQL`

10. **Click** "Finish"

✅ Firewall rule created!

### Step 3: Configure PostgreSQL to Accept Remote Connections

#### Edit postgresql.conf

1. **Open File Explorer**

2. **Navigate to**: `C:\Program Files\PostgreSQL\15\data`

3. **Find**: `postgresql.conf`

4. **Right-click** → "Open with" → "Notepad"

5. **Press** `Ctrl + F` to search

6. **Search for**: `listen_addresses`

7. **Find this line** (around line 59):
   ```
   #listen_addresses = 'localhost'
   ```

8. **Change it to** (remove the # and change localhost to *):
   ```
   listen_addresses = '*'
   ```

9. **Save** the file (Ctrl + S)

#### Edit pg_hba.conf

1. **In the same folder**: `C:\Program Files\PostgreSQL\15\data`

2. **Find**: `pg_hba.conf`

3. **Right-click** → "Open with" → "Notepad"

4. **Scroll to the bottom** of the file

5. **Add this line** at the end:
   ```
   host    financial_automation    fin_app_user    0.0.0.0/0    md5
   ```

6. **Save** the file (Ctrl + S)

#### Restart PostgreSQL Service

1. **Press** `Windows Key + R`

2. **Type**: `services.msc` and press **Enter**

3. **Find**: "postgresql-x64-15"

4. **Right-click** → "Restart"

5. **Wait** for service to restart (5-10 seconds)

✅ PostgreSQL now accepts remote connections!

---

## 📝 PART 5: CONFIGURE FINANCIAL AUTOMATION APPLICATION

### Step 1: Find Your Computer's IP Address (If Using Remote Database)

1. **Press** `Windows Key + R`

2. **Type**: `cmd` and press **Enter**

3. **Type**: `ipconfig` and press **Enter**

4. **Look for** "IPv4 Address" under your network adapter
   - Example: `192.168.1.100`
   - **Write this down**

### Step 2: Create .env File

1. **Open** the Financial Automation application folder
   - Example: `C:\FinancialAutomation\deployment_package_v1.0`

2. **Right-click** in the folder → "New" → "Text Document"

3. **Name it**: `.env` (yes, with the dot at the beginning)
   - Windows might warn you about changing the extension - click "Yes"

4. **Right-click** on `.env` → "Open with" → "Notepad"

5. **Copy and paste this** into the file:

**For Local PostgreSQL** (database on same computer):
```env
# Database Configuration
DB_TYPE=postgresql

# PostgreSQL Settings - Local
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=financial_automation
POSTGRES_USER=fin_app_user
POSTGRES_PASSWORD=FinApp@2025

# Connection Pool Settings
POSTGRES_MIN_CONN=2
POSTGRES_MAX_CONN=10
```

**For Remote PostgreSQL** (database on different computer):
```env
# Database Configuration
DB_TYPE=postgresql

# PostgreSQL Settings - Remote
POSTGRES_HOST=192.168.1.100
POSTGRES_PORT=5432
POSTGRES_DB=financial_automation
POSTGRES_USER=fin_app_user
POSTGRES_PASSWORD=FinApp@2025

# Connection Pool Settings
POSTGRES_MIN_CONN=2
POSTGRES_MAX_CONN=10
```

6. **IMPORTANT**: Replace values:
   - `POSTGRES_HOST`: Your database server IP (or `localhost` if same computer)
   - `POSTGRES_PASSWORD`: The password you set for fin_app_user

7. **Save** the file (Ctrl + S)

8. **Close** Notepad

---

## 🚀 PART 6: INITIALIZE DATABASE SCHEMA

Now we need to create the tables in the database.

### Step 1: Open Command Prompt

1. **Open** the Financial Automation application folder

2. **Hold Shift** and **right-click** in the folder (not on a file)

3. **Select** "Open PowerShell window here" or "Open command window here"

### Step 2: Install Python Dependencies (If Not Already Done)

```cmd
pip install -r requirements.txt
```

Press **Enter** and wait for installation (30-60 seconds)

### Step 3: Initialize Database

**Method A: Using Demo Script** (Recommended)

```cmd
python demo_db_setup_simple.py
```

Press **Enter**

You should see:
```
✅ Database initialized
✅ Admin user created
✅ 23 tables created
```

**Method B: Using Python Command** (Alternative)

```cmd
python -c "from config.database import initialize_database; initialize_database()"
```

Press **Enter**

✅ Database initialized successfully!

---

## ✅ PART 7: TEST THE CONNECTION

### Step 1: Run Application

1. **In the same Command Prompt** (or open new one in application folder)

2. **Type**:
```cmd
python main.py
```

3. **Press** Enter

4. **Application should launch!**

### Step 2: Login

1. **Default credentials**:
   - Username: `admin`
   - Password: `admin123`

2. **Click** "Login"

3. **Success!** If you see the main window, PostgreSQL is working!

### Step 3: Verify Database Connection

1. **In pgAdmin 4**, refresh the "financial_automation" database

2. **Expand** "Schemas" → "public" → "Tables"

3. **You should see 23 tables**:
   - companies
   - users
   - trial_balance
   - master_data
   - selection_sheet
   - ppe_schedule
   - ... and more

✅ Everything is working perfectly!

---

## 🎯 QUICK REFERENCE CARD

**Print this and keep it handy!**

### PostgreSQL Details
```
Server: localhost (or your IP: 192.168.1.100)
Port: 5432
Database Name: financial_automation
Username: fin_app_user
Password: [Your Password]
```

### Important File Locations
```
PostgreSQL Installation: C:\Program Files\PostgreSQL\15\
Configuration Files: C:\Program Files\PostgreSQL\15\data\
  - postgresql.conf
  - pg_hba.conf
```

### Quick Commands
```cmd
# Start PostgreSQL (if stopped)
services.msc → postgresql-x64-15 → Start

# Check if running
services.msc → postgresql-x64-15 → Status: Running

# Open pgAdmin 4
Start Menu → pgAdmin 4

# Run application
cd C:\FinancialAutomation\deployment_package_v1.0
python main.py
```

### Default Login
```
Username: admin
Password: admin123
```

---

## 🆘 TROUBLESHOOTING

### Problem: "Could not connect to server"

**Solution 1**: Check if PostgreSQL service is running
```
Windows Key + R → services.msc → postgresql-x64-15 → Start
```

**Solution 2**: Check .env file
- Make sure POSTGRES_HOST is correct (localhost or IP)
- Make sure POSTGRES_PASSWORD matches what you set
- Make sure file is named `.env` not `.env.txt`

**Solution 3**: Check firewall (if remote)
- Make sure port 5432 is allowed
- Check pg_hba.conf has the correct entry

### Problem: "Permission denied for database"

**Solution**: Grant permissions again
1. Open pgAdmin 4
2. Right-click financial_automation database
3. Properties → Security tab
4. Add fin_app_user with ALL privileges

### Problem: "Role 'fin_app_user' does not exist"

**Solution**: Create the user again
1. Open pgAdmin 4
2. Query Tool
3. Run:
```sql
CREATE USER fin_app_user WITH PASSWORD 'FinApp@2025';
GRANT ALL PRIVILEGES ON DATABASE financial_automation TO fin_app_user;
```

### Problem: "Database 'financial_automation' does not exist"

**Solution**: Create database again
1. Open pgAdmin 4
2. Right-click Databases → Create → Database
3. Name: financial_automation
4. Click Save

### Problem: "Port 5432 already in use"

**Solution**: Another service is using the port
1. Check if PostgreSQL is already running
2. Or change port in postgresql.conf and .env file

---

## 📞 NEED HELP?

### Documentation
- USER_GUIDE.md - Application usage
- QUICK_REFERENCE.md - Quick tips
- TRAINING_MATERIALS.md - Complete training

### Testing
- Run `demo_db_setup_simple.py` to test database
- Run `demo_tb_simple.py` to test full workflow

### Support
- Check documentation first
- Review troubleshooting section above
- Contact: support@yourcompany.com

---

## ✅ SETUP COMPLETE!

**Congratulations! You have successfully:**
- ✅ Installed PostgreSQL on Windows
- ✅ Created financial_automation database
- ✅ Created fin_app_user
- ✅ Configured Windows Firewall (if needed)
- ✅ Created .env configuration file
- ✅ Initialized database schema
- ✅ Tested the connection
- ✅ Ready to use the application!

**Next Steps:**
1. Read USER_GUIDE.md for application features
2. Import your Trial Balance data
3. Generate financial statements
4. Export to Excel

**Enjoy using Financial Automation Application!** 🎉

---

*Windows PostgreSQL Setup Guide*  
*Version 1.0 - Financial Automation*  
*Last Updated: October 20, 2025*
