"""
Test Suite for Financial Automation Application

This package contains automated tests for the PyQt5 Financial Automation application.

Test Categories:
- test_gui_*.py: GUI interaction tests using pytest-qt
- test_backend_*.py: Backend logic and database tests
- conftest.py: Shared fixtures and configuration

Requirements:
- pytest >= 8.3.0
- pytest-qt >= 4.4.0
- pytest-cov >= 5.0.0 (for coverage reports)

Run all tests:
    pytest tests/ -v

Run GUI tests only:
    pytest tests/test_gui_*.py -v

Run with coverage:
    pytest tests/ -v --cov=. --cov-report=html
"""

__version__ = "1.0.0"
