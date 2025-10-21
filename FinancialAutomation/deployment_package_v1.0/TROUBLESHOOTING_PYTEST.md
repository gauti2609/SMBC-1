# Troubleshooting pytest Installation

**Error:** `'pytest' is not recognized as an internal or external command`

---

## Solution 1: Install pytest (Most Common)

### Step 1: Open Command Prompt
```cmd
cd "C:\Financials Automation_Github\FinancialAutomation_v1.0_Complete\deployment_package_v1.0"
```

### Step 2: Run the installer
**Double-click:** `install_pytest.bat`

This will:
- ✅ Check Python installation
- ✅ Upgrade pip
- ✅ Install pytest and all dependencies
- ✅ Verify installation

---

## Solution 2: Manual Installation

If the automated installer doesn't work:

```cmd
python -m pip install pytest pytest-qt pytest-cov pytest-timeout
```

Then verify:
```cmd
python -m pytest --version
```

You should see:
```
pytest 8.3.3
```

---

## Solution 3: Python Not in PATH

If you get `'python' is not recognized`:

### Option A: Find Python Installation

1. Search for "Python" in Windows Start Menu
2. Right-click "Python 3.13" → "Open file location"
3. Note the path (e.g., `C:\Users\YourName\AppData\Local\Programs\Python\Python313\`)
4. Run with full path:

```cmd
"C:\Users\YourName\AppData\Local\Programs\Python\Python313\python.exe" -m pip install pytest pytest-qt
```

### Option B: Reinstall Python

1. Download Python 3.13 from: https://www.python.org/downloads/
2. During installation, **CHECK THE BOX**: ☑ "Add Python to PATH"
3. Complete installation
4. **Restart Command Prompt**
5. Run: `python --version` to verify

---

## Solution 4: Permission Issues

If you get "Access Denied" or "Permission Error":

### Run Command Prompt as Administrator:
1. Press Windows key
2. Type "cmd"
3. Right-click "Command Prompt"
4. Select "Run as administrator"
5. Run the install command again

---

## Solution 5: Internet/Firewall Issues

If installation hangs or fails with network errors:

### Check Internet Connection
```cmd
ping pypi.org
```

### Use Alternative pip Source
```cmd
python -m pip install --index-url https://pypi.org/simple pytest pytest-qt pytest-cov pytest-timeout
```

### Or install offline (if you have the wheel files):
```cmd
python -m pip install pytest-8.3.3-py3-none-any.whl
```

---

## Verification Commands

After installation, verify everything works:

### 1. Check Python
```cmd
python --version
```
Expected: `Python 3.13.x`

### 2. Check pip
```cmd
python -m pip --version
```
Expected: `pip 24.x.x from ...`

### 3. Check pytest
```cmd
python -m pytest --version
```
Expected: `pytest 8.3.3`

### 4. Check pytest-qt
```cmd
python -c "import pytestqt; print('pytest-qt OK')"
```
Expected: `pytest-qt OK`

### 5. Check PyQt5
```cmd
python -c "from PyQt5.QtWidgets import QApplication; print('PyQt5 OK')"
```
Expected: `PyQt5 OK`

---

## Running Tests After Installation

Once pytest is installed, use one of these methods:

### Method 1: Automated Script
```cmd
run_tests.bat
```

### Method 2: Direct Command
```cmd
python -m pytest tests/ -v --tb=short
```

### Method 3: Specific Test File
```cmd
python -m pytest tests/test_gui_company_creation.py -v
```

---

## Common Error Messages

### Error: "No module named 'PyQt5'"
**Solution:**
```cmd
python -m pip install PyQt5
```

### Error: "No module named 'pytest'"
**Solution:**
```cmd
python -m pip install pytest
```

### Error: "No module named 'pytestqt'"
**Solution:**
```cmd
python -m pip install pytest-qt
```

### Error: "Could not find a version that satisfies the requirement pytest"
**Solution:** Check Python version (must be 3.8+)
```cmd
python --version
```

### Error: "WARNING: pip is configured with locations that require TLS/SSL"
**Solution:** Update pip and setuptools:
```cmd
python -m pip install --upgrade pip setuptools
```

---

## Still Having Issues?

### Collect System Information

Run these commands and send me the output:

```cmd
echo === System Info ===
python --version
python -m pip --version
python -m pip list | findstr pytest
python -m pip list | findstr PyQt5
echo === Environment ===
echo %PATH%
```

### Create a Test Script

Create `test_install.py`:
```python
print("Testing Python installation...")

try:
    import sys
    print(f"✓ Python {sys.version}")
except:
    print("✗ Python import failed")

try:
    import pytest
    print(f"✓ pytest {pytest.__version__}")
except:
    print("✗ pytest not installed")

try:
    import pytestqt
    print(f"✓ pytest-qt installed")
except:
    print("✗ pytest-qt not installed")

try:
    from PyQt5.QtWidgets import QApplication
    print(f"✓ PyQt5 installed")
except:
    print("✗ PyQt5 not installed")

print("\nDone!")
```

Run it:
```cmd
python test_install.py
```

Send me the output and I'll help troubleshoot!

---

## Alternative: Use Python Virtual Environment

If nothing else works, create an isolated environment:

```cmd
cd "C:\Financials Automation_Github\FinancialAutomation_v1.0_Complete\deployment_package_v1.0"

REM Create virtual environment
python -m venv test_env

REM Activate it
test_env\Scripts\activate.bat

REM Install dependencies
pip install pytest pytest-qt pytest-cov PyQt5

REM Run tests
pytest tests/ -v
```

---

## Need More Help?

Send me:
1. Output of `python --version`
2. Output of `python -m pip --version`
3. Error message you're seeing
4. Operating System version

I'll provide specific instructions! 🔧
