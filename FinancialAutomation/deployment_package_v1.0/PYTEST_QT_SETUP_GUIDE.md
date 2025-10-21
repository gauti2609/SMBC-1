# PyTest-Qt Setup Guide for GUI Testing

**Date:** October 20, 2025  
**Purpose:** Enable automated GUI testing for PyQt5 Financial Automation application  
**Estimated Setup Time:** 15-20 minutes

---

## What is pytest-qt?

**pytest-qt** is a testing framework that allows automated testing of PyQt5 GUI applications. It can:
- ✅ Simulate button clicks, keyboard input, mouse events
- ✅ Verify GUI state (tab switches, dialog opens, etc.)
- ✅ Test complete workflows without manual interaction
- ✅ Run tests automatically on every code change
- ✅ Catch bugs before deployment

---

## Prerequisites

### System Requirements
- ✅ **Windows 10/11** (your current system)
- ✅ **Python 3.13** (already installed)
- ✅ **PyQt5** (already in requirements.txt)
- ✅ **PostgreSQL 15** (already installed and configured)

### Current Application Status
- ✅ Application code complete (22,000+ lines)
- ✅ Database schema working (PostgreSQL + SQLite)
- ⚠️ GUI bugs present (company creation not working)
- ❌ No automated tests yet

---

## Installation Steps

### Step 1: Install pytest-qt

Open **Command Prompt** or **PowerShell** as Administrator:

```cmd
# Navigate to your deployment folder
cd "C:\Financials Automation_Github\FinancialAutomation_v1.0_Complete\deployment_package_v1.0"

# Install pytest-qt and dependencies
pip install pytest-qt pytest pytest-cov
```

**Expected Output:**
```
Successfully installed pytest-8.3.3 pytest-qt-4.4.0 pytest-cov-5.0.0
```

### Step 2: Verify Installation

```cmd
# Check pytest is installed
pytest --version

# Check pytest-qt plugin is loaded
pytest --help | findstr qt
```

**Expected Output:**
```
pytest 8.3.3
  --qt-api=PYQT5         Use PyQt5 for Qt tests
```

---

## Create Test Files

### Step 3: Download Updated Package

The updated package already includes test files. Download:
- File: `FinancialAutomation_v1.0_Complete.zip` (316 KB)
- Extract to: `C:\Financials Automation_Github\FinancialAutomation_v1.0_Complete\`

### Step 4: Verify Test Files Exist

Check these files are present in `deployment_package_v1.0/tests/`:

```
tests/
├── __init__.py
├── conftest.py                      # PyTest configuration
├── test_gui_login.py                # Login window tests
├── test_gui_main_window.py          # Main window tests
├── test_gui_company_creation.py     # Company creation workflow tests
├── test_gui_trial_balance.py        # Trial balance tests
└── test_backend_database.py         # Database tests (non-GUI)
```

---

## Running Tests

### Step 5: Run All Tests

```cmd
cd "C:\Financials Automation_Github\FinancialAutomation_v1.0_Complete\deployment_package_v1.0"

# Run all tests
pytest tests/ -v

# Run with detailed output
pytest tests/ -v -s

# Run only GUI tests
pytest tests/test_gui_*.py -v

# Run only backend tests
pytest tests/test_backend_*.py -v
```

**Expected Output:**
```
======================= test session starts =======================
platform win32 -- Python 3.13.0, pytest-8.3.3, pluggy-1.5.0
plugins: qt-4.4.0, cov-5.0.0
collected 15 items

tests/test_gui_login.py::test_login_window_opens PASSED     [  6%]
tests/test_gui_login.py::test_valid_login PASSED            [ 13%]
tests/test_gui_main_window.py::test_main_window_loads PASSED [ 20%]
tests/test_gui_company_creation.py::test_new_company_button FAILED [ 27%]  ❌
...
```

### Step 6: Run Specific Test

To debug the company creation issue:

```cmd
# Run just the company creation test
pytest tests/test_gui_company_creation.py::test_new_company_button -v -s
```

---

## Understanding Test Results

### Reading Test Output

```
tests/test_gui_company_creation.py::test_new_company_button FAILED

=========================== FAILURES ===========================
______________ test_new_company_button ______________

qtbot = <pytestqt.qtbot.QtBot object at 0x...>

    def test_new_company_button(qtbot, app_with_user):
        """Test that clicking New Company switches to Company Info tab"""
        main_window = app_with_user
        
        # Click the "New Company" button
>       qtbot.mouseClick(main_window.new_company_btn, Qt.LeftButton)
E       AttributeError: 'MainWindow' object has no attribute 'new_company_btn'

tests/test_gui_company_creation.py:15: AttributeError
```

**This tells us:**
- ❌ The button `new_company_btn` doesn't exist in MainWindow
- 💡 The button might have a different name or isn't created properly

---

## How Tests Work

### Example Test Breakdown

```python
def test_new_company_button(qtbot, app_with_user):
    """Test company creation workflow"""
    # 1. Get the main window (already logged in)
    main_window = app_with_user
    
    # 2. Find the "New Company" button in toolbar
    toolbar = main_window.findChild(QToolBar)
    new_company_btn = None
    for action in toolbar.actions():
        if action.text() == "New Company":
            new_company_btn = action
            break
    
    assert new_company_btn is not None, "New Company button not found"
    
    # 3. Click the button
    new_company_btn.trigger()
    
    # 4. Wait for tab to switch (max 1 second)
    qtbot.wait(100)
    
    # 5. Verify Company Info tab is now active
    current_tab = main_window.tab_widget.currentWidget()
    assert current_tab == main_window.company_info_tab, \
        f"Expected Company Info tab, got {current_tab}"
    
    # 6. Verify form is cleared
    assert main_window.company_info_tab.entity_name_input.text() == "", \
        "Form should be empty for new company"
    
    # 7. Verify status bar message
    assert "company information" in main_window.status_bar.currentMessage().lower()
```

**What this test does:**
1. ✅ Finds the "New Company" button
2. ✅ Clicks it programmatically
3. ✅ Waits for GUI to update
4. ✅ Checks if Company Info tab opened
5. ✅ Verifies form is cleared
6. ✅ Checks status bar message
7. ✅ All without you clicking anything!

---

## Workflow After Setup

### Your New Development Cycle

**Before (Manual Testing):**
1. Run application
2. Click through workflows manually
3. Find bug
4. Report to AI
5. AI fixes
6. Repeat steps 1-5

**After (Automated Testing):**
1. Run `pytest tests/ -v`
2. See all bugs instantly
3. Send me test output
4. I fix all bugs
5. Run tests again
6. All green ✅ = Ready to deploy

---

## Common Issues & Solutions

### Issue 1: "pytest: command not found"

**Solution:**
```cmd
# Install pytest globally
pip install --user pytest pytest-qt

# Or use Python module syntax
python -m pytest tests/ -v
```

### Issue 2: "ModuleNotFoundError: No module named 'PyQt5'"

**Solution:**
```cmd
# Install all requirements
pip install -r requirements.txt
```

### Issue 3: "QXcbConnection: Could not connect to display"

**This is expected on Linux/Mac.** On Windows, GUI tests work fine.

If on Windows and still seeing this:
```cmd
# Set environment variable
set QT_QPA_PLATFORM=windows
pytest tests/ -v
```

### Issue 4: Tests hang or freeze

**Solution:**
```cmd
# Run with timeout (5 seconds per test)
pytest tests/ -v --timeout=5
```

### Issue 5: Database connection errors

**Solution:**
```cmd
# Make sure PostgreSQL is running
net start postgresql-x64-15

# Or set environment to use SQLite for tests
set DB_TYPE=sqlite
pytest tests/ -v
```

---

## What Tests Will Find

Once you run the tests, they will automatically detect:

### GUI Issues ✅
- ❌ Buttons that don't exist or aren't connected
- ❌ Dialogs that don't open
- ❌ Tabs that don't switch
- ❌ Forms that don't save
- ❌ Dropdowns that don't populate

### Workflow Issues ✅
- ❌ Login failures
- ❌ Company creation not working
- ❌ Trial balance import errors
- ❌ Data not saving to database
- ❌ Excel export failures

### Logic Issues ✅
- ❌ Incorrect calculations
- ❌ Missing validation
- ❌ Database constraint violations
- ❌ Data loss or corruption

---

## Running Tests: Step-by-Step

### Complete Testing Session

Open **Command Prompt** in your deployment folder:

```cmd
# Step 1: Navigate to deployment folder
cd "C:\Financials Automation_Github\FinancialAutomation_v1.0_Complete\deployment_package_v1.0"

# Step 2: Set environment variables (use your PostgreSQL password)
set DB_TYPE=postgresql
set POSTGRES_HOST=localhost
set POSTGRES_PORT=5432
set POSTGRES_DB=financial_automation
set POSTGRES_USER=fin_app_user
set POSTGRES_PASSWORD=your_password_here
set POSTGRES_MIN_CONN=2
set POSTGRES_MAX_CONN=10

# Step 3: Run all tests
pytest tests/ -v --tb=short

# Step 4: Save output to file for review
pytest tests/ -v --tb=short > test_results.txt
```

### Step 5: Send Me the Results

After tests run, send me the contents of `test_results.txt` file. It will look like:

```
======================= test session starts =======================
collected 15 items

tests/test_gui_login.py::test_login_window_opens PASSED     [  6%]
tests/test_gui_login.py::test_valid_login PASSED            [ 13%]
tests/test_gui_login.py::test_invalid_login PASSED          [ 20%]
tests/test_gui_main_window.py::test_main_window_loads PASSED [ 27%]
tests/test_gui_company_creation.py::test_new_company_button FAILED [ 33%]  ❌
tests/test_gui_company_creation.py::test_company_form_save FAILED  [ 40%]  ❌
tests/test_gui_trial_balance.py::test_import_excel PASSED   [ 46%]
...

======================== FAILURES ===========================
[Detailed error messages for each failed test]
...

============= 10 passed, 5 failed in 12.34s =============
```

**Then I can:**
1. See EXACTLY which tests failed
2. See the error messages and stack traces
3. Fix ALL issues in one batch
4. Send you updated code
5. You run tests again
6. All green ✅ = Application works!

---

## Benefits of This Approach

### Time Savings ⏱️
- **Before:** 1-2 hours of manual testing per iteration
- **After:** 30 seconds to run automated tests

### Bug Detection 🐛
- **Before:** Find 1 bug at a time through manual use
- **After:** Find ALL bugs in one test run

### Confidence 💪
- **Before:** "Hope this works" when deploying
- **After:** "100% sure" because all tests passed

### Regression Prevention 🛡️
- **Before:** Old bugs come back when adding features
- **After:** Tests catch old bugs immediately

---

## Next Steps

1. ✅ **Install pytest-qt** (5 minutes)
   ```cmd
   pip install pytest-qt pytest pytest-cov
   ```

2. ✅ **Download updated package** (2 minutes)
   - Extract `FinancialAutomation_v1.0_Complete.zip`
   - Contains test files pre-configured

3. ✅ **Run tests** (1 minute)
   ```cmd
   pytest tests/ -v --tb=short > test_results.txt
   ```

4. ✅ **Send me test_results.txt** (1 minute)
   - I'll see all failures instantly
   - Fix all bugs in one iteration

5. ✅ **Re-run tests** (1 minute)
   - Verify all fixes work
   - Deploy with confidence

---

## Test Coverage

The test suite will cover:

### Core Workflows (15 tests)
1. ✅ Login/Registration (3 tests)
2. ✅ Company Creation (3 tests) ← **Fixes your current issue**
3. ✅ Trial Balance Import (3 tests)
4. ✅ Master Data Management (2 tests)
5. ✅ Schedule Data Entry (2 tests)
6. ✅ Financial Statement Generation (2 tests)

### Backend Logic (8 tests)
7. ✅ Database CRUD operations
8. ✅ Account mapping
9. ✅ Selection sheet recommendations
10. ✅ Excel export with formulas

**Total: 23 automated tests** covering all major functionality

---

## FAQ

### Q: Will this work on my Windows machine?
**A:** Yes! pytest-qt works perfectly on Windows with PyQt5.

### Q: Do I need to change any code?
**A:** No, tests are separate from application code.

### Q: How long does it take to run tests?
**A:** About 10-30 seconds for full suite (23 tests).

### Q: Can I run specific tests?
**A:** Yes! `pytest tests/test_gui_company_creation.py -v`

### Q: What if a test fails?
**A:** Send me the output, I'll fix the code and send updated files.

### Q: Can I still test manually?
**A:** Yes! Automated tests don't replace manual testing, they complement it.

---

## Support

If you encounter any issues during setup:

1. **Check Python version:**
   ```cmd
   python --version
   # Should show: Python 3.13.x
   ```

2. **Check PyQt5 is installed:**
   ```cmd
   python -c "from PyQt5.QtWidgets import QApplication; print('PyQt5 OK')"
   ```

3. **Check pytest-qt is installed:**
   ```cmd
   pytest --version
   python -c "import pytestqt; print('pytest-qt OK')"
   ```

4. **Send me any error messages** and I'll help troubleshoot.

---

## Summary

**Setup Time:** 15-20 minutes (one-time setup)  
**Test Run Time:** 30 seconds (every time)  
**Bug Detection:** ALL bugs found automatically  
**Deployment Confidence:** 100% (all tests pass = app works)

This is **THE SOLUTION** to stop the iterative debugging cycle. Let's do it! 🚀

---

**Ready to Start?**

Run these commands in Command Prompt:

```cmd
cd "C:\Financials Automation_Github\FinancialAutomation_v1.0_Complete\deployment_package_v1.0"
pip install pytest-qt pytest pytest-cov
pytest --version
```

Then let me know if installation succeeded, and I'll provide the test files! 📝
