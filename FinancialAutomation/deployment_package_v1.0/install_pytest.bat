@echo off
REM Install pytest and dependencies for Financial Automation testing

echo ================================================
echo   Installing pytest and testing dependencies
echo ================================================
echo.

REM Check Python
echo [1/3] Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please:
    echo   1. Install Python 3.13 from https://www.python.org/downloads/
    echo   2. During installation, CHECK "Add Python to PATH"
    echo   3. Restart Command Prompt
    echo   4. Run this script again
    echo.
    pause
    exit /b 1
)
echo.

REM Upgrade pip
echo [2/3] Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install test dependencies
echo [3/3] Installing test dependencies...
echo Installing: pytest pytest-qt pytest-cov pytest-timeout
python -m pip install pytest pytest-qt pytest-cov pytest-timeout
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Installation failed
    echo.
    echo Common issues:
    echo   1. No internet connection
    echo   2. Firewall blocking pip
    echo   3. Permission issues (try running as Administrator)
    echo.
    pause
    exit /b 1
)
echo.

REM Verify installation
echo ================================================
echo   Verifying installation...
echo ================================================
echo.

python -m pytest --version
if %errorlevel% neq 0 (
    echo.
    echo ERROR: pytest installation verification failed
    pause
    exit /b 1
)

echo.
echo ================================================
echo   SUCCESS! All dependencies installed
echo ================================================
echo.
echo You can now run tests using:
echo   1. Double-click run_tests.bat
echo   2. Or run: python -m pytest tests/ -v
echo.

pause
