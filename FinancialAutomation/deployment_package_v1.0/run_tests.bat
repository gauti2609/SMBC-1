@echo off
REM Quick Start Script for PyTest-Qt Testing
REM This script sets up environment and runs all tests

echo ================================================
echo   Financial Automation - PyTest-Qt Test Runner
echo ================================================
echo.

REM Step 1: Check Python installation
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.13 first
    pause
    exit /b 1
)
python --version
echo.

REM Step 2: Check if pytest is installed
echo [2/5] Checking pytest installation...
python -m pip show pytest >nul 2>&1
if %errorlevel% neq 0 (
    echo pytest not found. Installing test dependencies...
    echo Installing: pytest pytest-qt pytest-cov pytest-timeout
    python -m pip install pytest pytest-qt pytest-cov pytest-timeout
    if %errorlevel% neq 0 (
        echo.
        echo ERROR: Failed to install pytest
        echo Please check your internet connection and Python installation
        pause
        exit /b 1
    )
    echo Installation complete!
    echo.
) else (
    echo pytest is already installed
    echo.
)

REM Step 3: Set environment variables
echo [3/5] Setting environment variables...
set DB_TYPE=sqlite
set PYTHONPATH=%CD%
echo Using SQLite for tests (fast and isolated)
echo.

REM Step 4: Run tests
echo [4/5] Running automated tests...
echo.
echo ================================================
echo   TEST EXECUTION STARTED
echo ================================================
echo.
echo Command: python -m pytest tests/ -v --tb=short --color=yes
echo.

python -m pytest tests/ -v --tb=short --color=yes

REM Step 5: Show summary
echo.
echo ================================================
echo   TEST EXECUTION COMPLETE
echo ================================================
echo.

REM Save results to file
echo Saving test results to test_results.txt...
echo Command: python -m pytest tests/ -v --tb=short
python -m pytest tests/ -v --tb=short > test_results.txt 2>&1

echo.
echo Results saved to: test_results.txt
echo.
echo Next steps:
echo   1. Review test results above
echo   2. If any tests FAILED, send test_results.txt to support
echo   3. If all tests PASSED, application is ready to deploy!
echo.

pause
