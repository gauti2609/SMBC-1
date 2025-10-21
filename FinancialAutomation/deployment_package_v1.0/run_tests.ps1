# Run Tests Script for Windows PowerShell

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Financial Automation - PyTest-Qt Test Runner" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Python
Write-Host "[1/5] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host $pythonVersion -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 2: Check pytest
Write-Host "[2/5] Checking pytest installation..." -ForegroundColor Yellow
$pytestInstalled = pip show pytest 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing test dependencies..." -ForegroundColor Yellow
    pip install -r tests\requirements_test.txt
} else {
    Write-Host "pytest is already installed" -ForegroundColor Green
}
Write-Host ""

# Step 3: Set environment
Write-Host "[3/5] Setting environment variables..." -ForegroundColor Yellow
$env:DB_TYPE = "sqlite"
$env:PYTHONPATH = $PWD.Path
Write-Host "Using SQLite for tests (fast and isolated)" -ForegroundColor Green
Write-Host ""

# Step 4: Run tests
Write-Host "[4/5] Running automated tests..." -ForegroundColor Yellow
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  TEST EXECUTION STARTED" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

pytest tests/ -v --tb=short --color=yes

# Step 5: Save results
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  TEST EXECUTION COMPLETE" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Saving test results to test_results.txt..." -ForegroundColor Yellow
pytest tests/ -v --tb=short > test_results.txt 2>&1

Write-Host ""
Write-Host "Results saved to: test_results.txt" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Review test results above" -ForegroundColor White
Write-Host "  2. If any tests FAILED, send test_results.txt to support" -ForegroundColor White
Write-Host "  3. If all tests PASSED, application is ready to deploy!" -ForegroundColor White
Write-Host ""

Read-Host "Press Enter to exit"
