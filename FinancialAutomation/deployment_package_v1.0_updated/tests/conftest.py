"""
PyTest Configuration and Shared Fixtures

This file contains pytest fixtures that are shared across all test files.
Fixtures provide pre-configured objects (database, user, windows) for testing.
"""

import pytest
import sys
import os
from pathlib import Path

# Add parent directory to path so we can import application modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from models.user import User
from models.company_info import CompanyInfo
from views.login_window import LoginWindow
from views.main_window import MainWindow
from config.database import initialize_database
from config.db_connection import get_connection, close_pool
import tempfile


@pytest.fixture(scope='session')
def qapp():
    """
    Create QApplication instance for the entire test session.
    
    This fixture is session-scoped, meaning it's created once
    and shared across all tests to improve performance.
    """
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app
    # Cleanup happens automatically


@pytest.fixture(scope='function')
def db_manager():
    """
    Create a fresh database for each test.
    
    Uses SQLite in-memory database for fast, isolated testing.
    Each test gets a clean database state.
    """
    # Use in-memory SQLite for tests (fast and isolated)
    original_db_type = os.environ.get('DB_TYPE')
    original_db_path = os.environ.get('DB_PATH')
    
    os.environ['DB_TYPE'] = 'sqlite'
    os.environ['DB_PATH'] = ':memory:'
    
    # Force reload modules to pick up test environment
    import config.settings
    import config.db_connection
    import importlib
    importlib.reload(config.settings)
    importlib.reload(config.db_connection)
    
    # Re-import after reload to get updated references
    from config.database import initialize_database as init_db
    from config.db_connection import get_connection as get_conn, close_pool as close
    
    # Initialize database tables
    init_db()
    
    # Get connection for tests to use
    conn = get_conn()
    
    yield conn
    
    # Cleanup: close connections and restore environment
    close()
    if original_db_type:
        os.environ['DB_TYPE'] = original_db_type
    else:
        os.environ.pop('DB_TYPE', None)
    if original_db_path:
        os.environ['DB_PATH'] = original_db_path
    else:
        os.environ.pop('DB_PATH', None)
    
    # Reload settings again to restore original
    importlib.reload(config.settings)
    importlib.reload(config.db_connection)


@pytest.fixture(scope='function')
def test_user(db_manager):
    """
    Create a test user for login/authentication tests.
    
    Returns:
        User object with credentials:
        - username: testuser_<random>
        - password: testpass123
        - email: test_<random>@example.com
    """
    from controllers.auth_controller import AuthController
    from models.user import User
    import random
    import string
    
    # Generate unique username to avoid conflicts
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    username = f'testuser_{random_suffix}'
    email = f'test_{random_suffix}@example.com'
    
    # Register a test user
    success, message, user_id = AuthController.register_user(
        username=username,
        password='testpass123',
        email=email,
        full_name='Test User',
        create_trial=False  # No license needed for tests
    )
    
    if not success:
        pytest.fail(f"Failed to create test user: {message}")
    
    # Return User object with user_id
    user = User(user_id=user_id, username=username, email=email, full_name='Test User')
    return user


@pytest.fixture(scope='function')
def test_company(db_manager, test_user):
    """
    Create a test company for workflow tests.
    
    Returns:
        CompanyInfo object with sample data
    """
    # Use CompanyInfo.create() static method instead of instance save()
    company_id = CompanyInfo.create(
        user_id=test_user.user_id,
        entity_name='Test Company Ltd',
        fy_start_date='2024-04-01',
        fy_end_date='2025-03-31',
        address='123 Test Street',
        cin_no='L12345MH2020PLC123456',
        currency='INR',
        units='Millions',
        rounding_level='100000',
        decimal_places=2
    )
    
    # Return CompanyInfo object
    company = CompanyInfo.get_by_id(company_id)
    return company


@pytest.fixture(scope='function')
def login_window(qtbot, qapp, db_manager):
    """
    Create LoginWindow instance for login tests.
    
    Args:
        qtbot: pytest-qt fixture for GUI interactions
        qapp: QApplication instance
        db_manager: Database manager fixture
    
    Returns:
        LoginWindow widget
    """
    window = LoginWindow()
    qtbot.addWidget(window)
    window.show()
    return window


@pytest.fixture(scope='function')
def main_window(qtbot, qapp, db_manager, test_user):
    """
    Create MainWindow instance (already logged in) for workflow tests.
    
    Args:
        qtbot: pytest-qt fixture for GUI interactions
        qapp: QApplication instance
        db_manager: Database manager fixture
        test_user: Pre-created test user
    
    Returns:
        MainWindow widget with authenticated user
    """
    window = MainWindow(test_user)
    qtbot.addWidget(window)
    window.show()
    qtbot.waitExposed(window)
    return window
    return window
    qtbot.waitForWindowShown(window)
    return window


@pytest.fixture(scope='function')
def main_window_with_company(qtbot, qapp, db_manager, test_user, test_company):
    """
    Create MainWindow with user and company pre-configured.
    
    This fixture is useful for testing workflows that require
    a company to be selected (Trial Balance, Schedules, etc.)
    
    Returns:
        MainWindow widget with company selected
    """
    window = MainWindow(test_user)
    qtbot.addWidget(window)
    
    # Set the company and trigger UI updates
    window.current_company_id = test_company.company_id
    window.current_company = test_company
    window.populate_company_selector()
    
    # Explicitly update window title to match what load_company does
    window.setWindowTitle(f"Financial Automation - {test_company.entity_name}")
    
    return window


@pytest.fixture(scope='function')
def sample_trial_balance_file():
    """
    Create a temporary Excel file with sample Trial Balance data.
    
    Returns:
        Path to temporary Excel file
    """
    from openpyxl import Workbook
    
    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.xlsx', delete=False)
    temp_file.close()
    
    # Create Excel with sample data
    wb = Workbook()
    ws = wb.active
    ws.title = "Trial Balance"
    
    # Headers
    ws.append(['Ledger Name', 'Debit', 'Credit'])
    
    # Sample data
    sample_data = [
        ['Cash in Hand', 50000, 0],
        ['Bank Balance', 100000, 0],
        ['Debtors', 75000, 0],
        ['Capital', 0, 200000],
        ['Sales', 0, 150000],
        ['Purchases', 80000, 0],
        ['Rent Expense', 20000, 0],
        ['Salary Expense', 25000, 0],
    ]
    
    for row in sample_data:
        ws.append(row)
    
    wb.save(temp_file.name)
    
    yield temp_file.name
    
    # Cleanup: delete temporary file
    try:
        os.unlink(temp_file.name)
    except:
        pass


# Custom markers for test categorization
def pytest_configure(config):
    """
    Register custom pytest markers.
    
    Markers allow categorizing tests:
    - @pytest.mark.gui: GUI interaction tests
    - @pytest.mark.backend: Backend logic tests
    - @pytest.mark.database: Database tests
    - @pytest.mark.slow: Tests that take >5 seconds
    """
    config.addinivalue_line("markers", "gui: GUI interaction tests using pytest-qt")
    config.addinivalue_line("markers", "backend: Backend logic tests (no GUI)")
    config.addinivalue_line("markers", "database: Database operation tests")
    config.addinivalue_line("markers", "slow: Tests that take more than 5 seconds")
    config.addinivalue_line("markers", "integration: End-to-end workflow tests")


# Pytest hooks for better output
def pytest_runtest_setup(item):
    """
    Hook called before each test runs.
    Print test name for better visibility.
    """
    print(f"\n▶️  Running: {item.nodeid}")


def pytest_runtest_teardown(item, nextitem):
    """
    Hook called after each test runs.
    Can be used for cleanup or logging.
    """
    pass
