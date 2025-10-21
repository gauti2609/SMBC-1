@echo off
REM Simplified test runner - just runs pytest directly
echo Running tests with: python -m pytest tests/ -v --tb=short
echo.
python -m pytest tests/ -v --tb=short
echo.
echo Tests complete! Press any key to exit.
pause
