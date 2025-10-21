# Troubleshooting Guide - Login/Main Window Issues

## Issue: "Login window closes immediately after login/register"

### ✅ Fixes Applied:

1. **Database initialization moved** - Now happens AFTER Qt app starts (so errors can be shown)
2. **Comprehensive error handling** - Every step wrapped in try/except with user-friendly messages
3. **Debug logging added** - Prints to console to see exactly where it fails
4. **Main window visibility** - Explicitly calls `show()`, `raise_()`, `activateWindow()`
5. **Login window kept open** - Only closes if main window opens successfully

---

## 🔍 How to Debug:

### Step 1: Run from Command Line (See Error Messages)

Instead of double-clicking the .exe, run it from command prompt:

```cmd
cd C:\Path\To\Your\Application
FinancialAutomation.exe
```

**You will see debug output like:**
```
Initializing database...
Database initialized successfully
Creating login window...
Login window shown
Creating main window for user: john
Initializing UI...
UI initialized successfully
Loading last session...
Last session loaded
MainWindow initialization complete
Main window shown and activated
Closing login window
Login window closed
```

### Step 2: Check for Error Messages

If something fails, you'll see **exactly where**:

**Example 1: Database connection error**
```
Initializing database...
❌ Failed to create PostgreSQL pool: connection refused
Database initialization error: ...
[Error dialog appears with instructions]
```

**Example 2: Main window initialization error**
```
Creating main window for user: john
Initializing UI...
Error initializing main window: relation "company_info" does not exist
[Login window stays open with error dialog]
```

---

## 🐛 Common Issues & Solutions:

### Issue 1: "Login window closes, nothing appears"

**Cause:** Main window crashes during initialization

**Debug:**
1. Run from command line (see output)
2. Look for error after "Creating main window for user: ..."
3. Check if database tables exist

**Solution:**
- If you see "relation does not exist" → Database tables not created
- If you see "connection refused" → PostgreSQL not running
- If you see "authentication failed" → Wrong credentials in .env

### Issue 2: "Database initialization error"

**Cause:** Cannot connect to database on startup

**Solutions:**
- **PostgreSQL:** Make sure it's running (`pg_ctl status`)
- **Check .env file exists** in same folder as .exe
- **Check credentials** in .env match your database
- **Create database** if it doesn't exist:
  ```sql
  CREATE DATABASE financial_automation;
  ```

### Issue 3: "Table creation order error"

**Cause:** Old version of code with table order bug

**Solution:** This is fixed in latest deployment package
- Make sure you're using `deployment_package_v1.0_COMPLETE.zip` (117KB)
- Date: October 21, 2025

---

## 📋 Checklist Before Running:

- [ ] PostgreSQL server is running
- [ ] Database `financial_automation` exists
- [ ] User `fin_app_user` has permissions
- [ ] `.env` file is in same folder as `.exe`
- [ ] `.env` has correct credentials (POSTGRES_USER, POSTGRES_PASSWORD, etc.)
- [ ] Running from command line to see errors

---

## 🔧 Test Database Connection:

Run this in command prompt to verify database works:

```cmd
psql -U fin_app_user -d financial_automation -c "SELECT version();"
```

**If this works**, your database connection is fine.

**If this fails**, fix database connection first.

---

## 📝 What the Debug Output Shows:

### Successful startup:
```
Initializing database...              ← Database connection OK
Database initialized successfully     ← Tables created/verified
Creating login window...               ← Login UI created
Login window shown                     ← You should see login window
[You login]
Creating main window for user: john   ← Starting main window
Initializing UI...                     ← Creating tabs, menus, etc.
UI initialized successfully            ← All UI components ready
Loading last session...                ← Checking for saved state
Last session loaded                    ← Session loaded (or new session)
MainWindow initialization complete     ← Main window ready
Main window shown and activated        ← You should see main window
Closing login window                   ← Login window closing
Login window closed                    ← Login window gone
```

### Failed startup (example):
```
Initializing database...
❌ Failed to create PostgreSQL pool: connection refused
Database initialization error: ...
[App exits with error dialog]
```

---

## 🚀 Quick Fix Summary:

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| App closes immediately on startup | Database connection fails | Check PostgreSQL running, .env file |
| Login window closes, nothing shows | Main window crash | Run from command line, see error |
| "relation does not exist" | Tables not created | Use latest package with table order fix |
| "authentication failed" | Wrong password in .env | Update .env with correct credentials |

---

## ✅ Expected Behavior (After Fixes):

1. **Run .exe** → Database initializes (2-3 seconds)
2. **Login window appears** → Fill in username/password
3. **Click Login** → 
   - ✅ Main window appears (with welcome screen)
   - ✅ Login window closes
   - ✅ You see: "Welcome, [Your Name]!"
4. **Create/Open Company** → All features work

---

## 📞 Still Having Issues?

If you still see the problem after these fixes:

1. **Run from command line** and copy **ALL** the output
2. **Look for the last line** before it crashes
3. **Check the .env file** - share the file (hide password)
4. **PostgreSQL logs** - check for connection attempts

Share this information for further debugging!
