"""
GUI Tests for Company Creation Workflow

This test file specifically addresses the bug you reported:
"when I click on create new company pop up box opens and when I click on ok nothing happens"

These tests will verify:
1. New Company button exists and is clickable
2. Clicking it switches to Company Info tab
3. Form is cleared for new entry
4. Saving company works correctly
"""

import pytest
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QToolBar, QAction, QPushButton


@pytest.mark.gui
class TestCompanyCreation:
    """Test suite for Company Creation workflow"""
    
    def test_new_company_button_exists(self, main_window):
        """Test that New Company button exists in toolbar"""
        # Find toolbar
        toolbar = main_window.findChild(QToolBar)
        assert toolbar is not None, "Toolbar should exist"
        
        # Find "New Company" button/action
        new_company_found = False
        for action in toolbar.actions():
            if action.text() == "New Company":
                new_company_found = True
                break
        
        # Also check for QPushButton widgets in toolbar
        if not new_company_found:
            for widget in toolbar.children():
                if isinstance(widget, QPushButton) and widget.text() == "New Company":
                    new_company_found = True
                    break
        
        assert new_company_found, "New Company button/action should exist in toolbar"
    
    def test_new_company_menu_action_exists(self, main_window):
        """Test that New Company menu action exists"""
        menubar = main_window.menuBar()
        file_menu = None
        
        # Find File menu
        for action in menubar.actions():
            if action.text() == "&File" or action.text() == "File":
                file_menu = action.menu()
                break
        
        assert file_menu is not None, "File menu should exist"
        
        # Find New Company action
        new_company_action = None
        for action in file_menu.actions():
            if "New Company" in action.text():
                new_company_action = action
                break
        
        assert new_company_action is not None, "New Company action should exist in File menu"
    
    def test_new_company_button_click_switches_tab(self, qtbot, main_window):
        """
        CRITICAL TEST: Test that clicking New Company switches to Company Info tab
        
        This is the bug you reported - let's verify it works correctly.
        """
        # Get initial tab
        initial_tab = main_window.tab_widget.currentWidget()
        
        # Find and click New Company button
        toolbar = main_window.findChild(QToolBar)
        new_company_clicked = False
        
        # Try to find as QAction
        for action in toolbar.actions():
            if action.text() == "New Company":
                action.trigger()
                new_company_clicked = True
                break
        
        # Try to find as QPushButton
        if not new_company_clicked:
            for widget in toolbar.children():
                if isinstance(widget, QPushButton) and widget.text() == "New Company":
                    qtbot.mouseClick(widget, Qt.LeftButton)
                    new_company_clicked = True
                    break
        
        assert new_company_clicked, "Should be able to click New Company button"
        
        # Wait for tab switch
        qtbot.wait(200)
        
        # Verify Company Info tab is now active
        current_tab = main_window.tab_widget.currentWidget()
        assert current_tab == main_window.company_info_tab, \
            f"Expected Company Info tab to be active, but got {current_tab}"
    
    def test_new_company_clears_form(self, qtbot, main_window):
        """Test that New Company clears the form for new entry"""
        # First, put some data in the form
        main_window.company_info_tab.entity_name_input.setText("Old Company")
        main_window.company_info_tab.cin_input.setText("L12345AB2020PLC123456")
        
        # Click New Company
        toolbar = main_window.findChild(QToolBar)
        for action in toolbar.actions():
            if action.text() == "New Company":
                action.trigger()
                break
        else:
            for widget in toolbar.children():
                if isinstance(widget, QPushButton) and widget.text() == "New Company":
                    qtbot.mouseClick(widget, Qt.LeftButton)
                    break
        
        qtbot.wait(200)
        
        # Verify form is cleared
        assert main_window.company_info_tab.entity_name_input.text() == "", \
            "Entity name should be cleared"
        assert main_window.company_info_tab.cin_input.text() == "", \
            "CIN should be cleared"
    
    def test_new_company_shows_status_message(self, qtbot, main_window):
        """Test that New Company shows guidance in status bar"""
        # Click New Company
        toolbar = main_window.findChild(QToolBar)
        for action in toolbar.actions():
            if action.text() == "New Company":
                action.trigger()
                break
        else:
            for widget in toolbar.children():
                if isinstance(widget, QPushButton) and widget.text() == "New Company":
                    qtbot.mouseClick(widget, Qt.LeftButton)
                    break
        
        qtbot.wait(200)
        
        # Check status bar message
        status_message = main_window.status_bar.currentMessage()
        assert "company information" in status_message.lower(), \
            f"Status bar should show guidance message, got: '{status_message}'"
    
    def test_company_form_has_required_fields(self, main_window):
        """Test that company form has all required input fields"""
        company_tab = main_window.company_info_tab
        
        assert hasattr(company_tab, 'entity_name_input'), "Entity name input should exist"
        assert hasattr(company_tab, 'cin_input'), "CIN input should exist"
    
    def test_save_company_button_exists(self, main_window):
        """Test that Save Company Info button exists"""
        company_tab = main_window.company_info_tab
        save_btn = company_tab.save_btn
        
        assert save_btn is not None, "Save button should exist"
        assert save_btn.isEnabled(), "Save button should be enabled"
        assert "Save" in save_btn.text(), f"Button text should contain 'Save', got '{save_btn.text()}'"
    
    def test_save_company_with_valid_data(self, qtbot, main_window, monkeypatch):
        """Test saving company with valid data"""
        company_tab = main_window.company_info_tab
        
        # Fill in required fields
        company_tab.entity_name_input.setText("Test Company Ltd")
        company_tab.cin_input.setText("L12345MH2020PLC123456")
        
        # Set financial year dates
        from PyQt5.QtCore import QDate
        company_tab.fy_start_input.setDate(QDate(2024, 4, 1))
        company_tab.fy_end_input.setDate(QDate(2025, 3, 31))
        
        # Mock QMessageBox to capture success message
        success_shown = {'value': False, 'company_name': ''}
        
        def mock_information(parent, title, message):
            success_shown['value'] = True
            if "Test Company Ltd" in message:
                success_shown['company_name'] = "Test Company Ltd"
        
        monkeypatch.setattr(QMessageBox, 'information', mock_information)
        
        # Click save button
        qtbot.mouseClick(company_tab.save_btn, Qt.LeftButton)
        qtbot.wait(500)  # Wait for save operation
        
        # Verify success message shown
        assert success_shown['value'], "Success message should be shown after save"
        assert success_shown['company_name'] == "Test Company Ltd", \
            "Success message should include company name"
    
    def test_save_company_validation_empty_name(self, qtbot, main_window, monkeypatch):
        """Test that saving with empty entity name shows validation error"""
        company_tab = main_window.company_info_tab
        
        # Clear entity name (leave it empty)
        company_tab.entity_name_input.clear()
        
        # Mock QMessageBox
        error_shown = {'value': False}
        
        def mock_warning(parent, title, message):
            error_shown['value'] = True
            assert "required" in message.lower() or "entity name" in message.lower()
        
        monkeypatch.setattr(QMessageBox, 'warning', mock_warning)
        
        # Try to save
        qtbot.mouseClick(company_tab.save_btn, Qt.LeftButton)
        qtbot.wait(200)
        
        # Verify validation error shown
        assert error_shown['value'], "Validation error should be shown for empty entity name"
    
    def test_company_selector_updates_after_save(self, qtbot, main_window, monkeypatch):
        """Test that company selector dropdown updates after saving new company"""
        # Get initial count
        initial_count = main_window.company_selector.count()
        
        # Fill and save company
        company_tab = main_window.company_info_tab
        company_tab.entity_name_input.setText("New Test Company")
        company_tab.cin_input.setText("L12345GJ2020PLC123456")
        
        from PyQt5.QtCore import QDate
        company_tab.fy_start_input.setDate(QDate(2024, 4, 1))
        company_tab.fy_end_input.setDate(QDate(2025, 3, 31))
        
        # Mock QMessageBox
        monkeypatch.setattr(QMessageBox, 'information', lambda *args: None)
        
        # Save
        qtbot.mouseClick(company_tab.save_btn, Qt.LeftButton)
        qtbot.wait(500)
        
        # Check company selector updated
        new_count = main_window.company_selector.count()
        assert new_count > initial_count, \
            f"Company selector should have more items after save (was {initial_count}, now {new_count})"
    
    @pytest.mark.slow
    def test_complete_company_creation_workflow(self, qtbot, main_window, monkeypatch):
        """
        INTEGRATION TEST: Complete end-to-end company creation workflow
        
        This tests the exact workflow you're experiencing:
        1. Click "Create New Company"
        2. Form opens and is cleared
        3. Fill in details
        4. Click Save
        5. Company appears in selector
        6. Can select and work with company
        """
        # Mock dialogs
        monkeypatch.setattr(QMessageBox, 'information', lambda *args: None)
        monkeypatch.setattr(QMessageBox, 'warning', lambda *args: None)
        
        # Step 1: Click "Create New Company"
        toolbar = main_window.findChild(QToolBar)
        for action in toolbar.actions():
            if action.text() == "New Company":
                action.trigger()
                break
        
        qtbot.wait(200)
        
        # Step 2: Verify Company Info tab opened
        assert main_window.tab_widget.currentWidget() == main_window.company_info_tab
        
        # Step 3: Verify form is empty
        assert main_window.company_info_tab.entity_name_input.text() == ""
        
        # Step 4: Fill in all required fields
        company_tab = main_window.company_info_tab
        company_tab.entity_name_input.setText("Complete Test Company")
        company_tab.cin_input.setText("L12345KA2020PLC123456")
        
        from PyQt5.QtCore import QDate
        company_tab.fy_start_input.setDate(QDate(2024, 4, 1))
        company_tab.fy_end_input.setDate(QDate(2025, 3, 31))
        
        # Step 5: Click Save
        initial_count = main_window.company_selector.count()
        qtbot.mouseClick(company_tab.save_btn, Qt.LeftButton)
        qtbot.wait(500)
        
        # Step 6: Verify company was saved
        assert main_window.company_selector.count() > initial_count
        
        # Step 7: Verify company can be selected
        # Find the new company in dropdown
        company_index = -1
        for i in range(main_window.company_selector.count()):
            if "Complete Test Company" in main_window.company_selector.itemText(i):
                company_index = i
                break
        
        assert company_index > 0, "New company should appear in selector"
        
        # Select it
        main_window.company_selector.setCurrentIndex(company_index)
        qtbot.wait(200)
        
        # Step 8: Verify company is selected
        assert main_window.current_company is not None
        assert main_window.current_company.entity_name == "Complete Test Company"
        
        print("\n✅ COMPLETE WORKFLOW TEST PASSED!")
        print("   Company creation from button click to selection works correctly.")
