# .exe Error Analysis and Troubleshooting

## Error Information

**Error Message (Partial):**
```
Traceback (most recent call last):
  File "main.py", line 13, in
```

**Note:** The full traceback was not provided, but based on line 13 of main.py, the error occurs at the import statement.

## Analysis of main.py Line 13

Looking at the main.py file:

```python
9. import sys
10. import os
11. from PyQt5.QtWidgets import QApplication
12. from PyQt5.QtGui import QFont
13. from views.login_window import LoginWindow  # <-- LINE 13
14. from config.database import initialize_database
```

## Possible Causes

### 1. Missing PyQt5 Dependencies in .exe Build

**Most Likely Cause:** The .exe file was built without including PyQt5 and its dependencies.

**Symptoms:**
- Import error on line 13 (PyQt5 imports)
- Works in development but fails as .exe

**Solution:**
```python
# In build_executable.py or .spec file, ensure PyQt5 is included:

hiddenimports = [
    'PyQt5.QtCore',
    'PyQt5.QtGui',
    'PyQt5.QtWidgets',
    'PyQt5.sip',
]
```

### 2. Missing Database Configuration

**Cause:** The .env file or database configuration is not bundled with the .exe

**Symptoms:**
- Database initialization error
- Missing environment variables

**Solution:**
- Ensure .env file is in the same directory as the .exe
- Or include database configuration in the executable

### 3. Incorrect Module Paths in .exe

**Cause:** PyInstaller may not resolve relative imports correctly

**Symptoms:**
- ImportError for local modules (views, config, models)

**Solution:**
```python
# Add to build_executable.py:
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = collect_submodules('views') + \
                collect_submodules('models') + \
                collect_submodules('config') + \
                collect_submodules('controllers')
```

### 4. Missing psycopg2 Dependencies

**Cause:** psycopg2 (PostgreSQL driver) not included or incompatible binary

**Symptoms:**
- Import error when loading database module

**Solution:**
```bash
# Use psycopg2-binary for .exe builds
pip install psycopg2-binary

# In .spec file:
hiddenimports.append('psycopg2')
```

## Recommended Fix Steps

### Step 1: Check the Full Error Message

Run the .exe from command line to see the complete error:

```bash
# Windows
cd path\to\exe
FinancialAutomation.exe

# This will show the full traceback
```

### Step 2: Update build_executable.py

Ensure the build script includes all dependencies:

```python
# build_executable.py
import PyInstaller.__main__
import os

PyInstaller.__main__.run([
    'main.py',
    '--name=FinancialAutomation',
    '--onefile',
    '--windowed',  # Remove this for debugging to see console output
    '--icon=icon.ico',  # if you have an icon
    '--add-data=.env.example:.',
    '--hidden-import=PyQt5',
    '--hidden-import=PyQt5.QtCore',
    '--hidden-import=PyQt5.QtGui',
    '--hidden-import=PyQt5.QtWidgets',
    '--hidden-import=psycopg2',
    '--hidden-import=views.login_window',
    '--hidden-import=views.main_window',
    '--hidden-import=config.database',
    '--hidden-import=models.trial_balance',
    '--collect-submodules=views',
    '--collect-submodules=models',
    '--collect-submodules=config',
    '--collect-submodules=controllers',
])
```

### Step 3: Use .spec File for Better Control

Create FinancialAutomation.spec:

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('.env.example', '.')],
    hiddenimports=[
        'PyQt5.QtCore',
        'PyQt5.QtGui', 
        'PyQt5.QtWidgets',
        'PyQt5.sip',
        'psycopg2',
        'views.login_window',
        'views.main_window',
        'views.company_info_tab',
        'views.trial_balance_tab',
        'views.master_data_tab',
        'config.database',
        'config.db_connection',
        'config.settings',
        'models.trial_balance',
        'models.company_info',
        'models.master_data',
        'models.user',
        'controllers.auth_controller',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='FinancialAutomation',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Set to True for debugging, False for release
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```

Then build with:
```bash
pyinstaller FinancialAutomation.spec
```

### Step 4: Test in Console Mode First

Change `console=True` in the .spec file to see error messages, then change back to `console=False` for production.

## Common Error Messages and Solutions

| Error Message | Cause | Solution |
|---------------|-------|----------|
| `ModuleNotFoundError: No module named 'PyQt5'` | PyQt5 not bundled | Add PyQt5 to hiddenimports |
| `ModuleNotFoundError: No module named 'psycopg2'` | Database driver missing | Add psycopg2 to hiddenimports |
| `FileNotFoundError: [Errno 2] No such file or directory: '.env'` | Config file missing | Include .env or use defaults |
| `ImportError: DLL load failed` | Missing DLL dependencies | Use `--collect-all PyQt5` flag |

## Additional Debugging Steps

1. **Enable Console Output:**
   ```python
   # Change in .spec file:
   console=True  # Shows errors in console window
   ```

2. **Check Dependencies:**
   ```bash
   # List all imports in the exe
   pyi-archive_viewer FinancialAutomation.exe
   ```

3. **Test Import Chain:**
   ```python
   # Create test_imports.py
   try:
       from PyQt5.QtWidgets import QApplication
       print("✓ PyQt5 imported")
   except Exception as e:
       print(f"✗ PyQt5 failed: {e}")
   
   try:
       from views.login_window import LoginWindow
       print("✓ views.login_window imported")
   except Exception as e:
       print(f"✗ views.login_window failed: {e}")
   ```

## Quick Fix Checklist

- [ ] Run .exe from command line to get full error message
- [ ] Verify PyQt5 is installed: `pip list | grep PyQt5`
- [ ] Verify psycopg2 is installed: `pip list | grep psycopg2`
- [ ] Create/update .spec file with all hidden imports
- [ ] Build with `console=True` for debugging
- [ ] Include .env file in same directory as .exe
- [ ] Test on clean system without Python installed

## Contact for Further Help

If the error persists after these steps:
1. Share the **complete error traceback** (run .exe from command line)
2. Share the build command or .spec file being used
3. Confirm Python version and PyQt5 version
4. Confirm whether issue occurs in development or only in .exe

---

**Last Updated:** October 22, 2025
