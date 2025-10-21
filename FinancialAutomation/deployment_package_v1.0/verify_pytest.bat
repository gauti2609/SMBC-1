@echo off
REM Quick verification that pytest works with python -m

echo ================================================
echo   Pytest Installation Verification
echo ================================================
echo.

echo Testing: python -m pytest --version
python -m pytest --version

echo.
echo If you see a version number above (e.g., "pytest 8.4.2"), then pytest is installed correctly!
echo.
echo You can now run: run_tests.bat
echo.

pause
