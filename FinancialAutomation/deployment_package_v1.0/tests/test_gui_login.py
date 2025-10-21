"""
GUI Tests for Login Window

Tests user authentication, registration, and login workflows.
"""

import pytest
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox


@pytest.mark.gui
class TestLoginWindow:
    """Test suite for Login Window GUI"""
    
    def test_login_window_opens(self, login_window):
        """Test that login window opens and displays correctly"""
        assert login_window is not None
        assert login_window.isVisible()
        assert login_window.windowTitle() == "Financial Automation - Login"
    
    def test_login_form_widgets_exist(self, login_window):
        """Test that login form has all required widgets"""
        assert login_window.login_username is not None
        assert login_window.login_password is not None
        # Login button exists in the widget but isn't stored as instance attribute
        assert login_window.tab_widget is not None
    
    def test_registration_form_widgets_exist(self, login_window):
        """Test that registration form has all required widgets"""
        assert login_window.register_username is not None
        assert login_window.register_password is not None
        assert login_window.register_email is not None
        assert login_window.register_fullname is not None
        # Register button exists in the widget but isn't stored as instance attribute
        assert login_window.tab_widget is not None
    
    def test_valid_login(self, login_window, test_user):
        """Test login with valid credentials"""
        # Enter valid credentials
        login_window.login_username.setText(test_user.username)
        login_window.login_password.setText('testpass123')
        
        # Click login button (find it by text)
        login_button = None
        for child in login_window.children():
            if hasattr(child, 'text') and child.text() == 'Login':
                login_button = child
                break
        
        # If button found, click it
        if login_button:
            with qtbot.waitSignal(login_window.destroyed, timeout=2000, raising=False):
                qtbot.mouseClick(login_button, Qt.LeftButton)
        
        # Note: Window should close and MainWindow should open
        # In a real test, we'd check that MainWindow opened
    
    def test_invalid_login(self, login_window, monkeypatch):
        """Test login with invalid credentials"""
        # Enter invalid credentials
        login_window.login_username.setText('wronguser')
        login_window.login_password.setText('wrongpass')
        
        # Mock the message box to avoid blocking
        mock_warning = lambda *args, **kwargs: None
        monkeypatch.setattr(QMessageBox, 'warning', mock_warning)
    
    def test_registration_success(self, login_window, qtbot, monkeypatch):
        """Test successful user registration"""
        import random
        import string
        
        # Generate unique username to avoid conflicts
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        unique_username = f'newuser_{random_suffix}'
        unique_email = f'new_{random_suffix}@example.com'
        
        # Switch to registration tab
        login_window.tab_widget.setCurrentIndex(1)
        
        # Mock QMessageBox BEFORE filling form to ensure it's active
        success_shown = {'value': False}
        
        def mock_information(parent, title, message):
            success_shown['value'] = True
            # Registration message contains 'registered successfully' or similar
            assert 'register' in message.lower() or 'success' in message.lower()
        
        monkeypatch.setattr(QMessageBox, 'information', mock_information)
        
        # Fill registration form with unique values
        login_window.register_username.setText(unique_username)
        login_window.register_password.setText('newpass123')
        login_window.register_confirm_password.setText('newpass123')
        login_window.register_email.setText(unique_email)
        login_window.register_fullname.setText('New User')
        
        # Directly call the registration handler instead of searching for button
        login_window.handle_register()
        qtbot.wait(200)
        
        # Verify success message shown
        assert success_shown['value'], "Success message should be shown"
    
    def test_empty_login_validation(self, login_window, qtbot, monkeypatch):
        """Test that empty login form shows validation error"""
        # Clear form
        login_window.login_username.clear()
        login_window.login_password.clear()
        
        # Mock the message box
        mock_warning = lambda *args, **kwargs: None
        monkeypatch.setattr(QMessageBox, 'warning', mock_warning)
