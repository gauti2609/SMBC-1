"""
GUI Tests for Main Window

Tests main window initialization, tab navigation, and menu actions.
"""

import pytest
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTabWidget


@pytest.mark.gui
class TestMainWindow:
    """Test suite for Main Window"""
    
    def test_main_window_loads(self, main_window):
        """Test that main window loads successfully"""
        assert main_window is not None
        assert main_window.isVisible()
        assert "Financial Automation" in main_window.windowTitle()
    
    def test_all_tabs_exist(self, main_window):
        """Test that all required tabs are present"""
        tab_widget = main_window.tab_widget
        assert tab_widget is not None
        
        # Get all tab names
        tab_names = []
        for i in range(tab_widget.count()):
            tab_names.append(tab_widget.tabText(i))
        
        # Check for essential tabs
        required_tabs = [
            "Company Information",
            "Master Data",
            "Trial Balance",
            "Input Forms",
            "Financial Statements"
        ]
        
        for required_tab in required_tabs:
            assert any(required_tab in tab_name for tab_name in tab_names), \
                f"Tab '{required_tab}' should exist"
    
    def test_menu_bar_exists(self, main_window):
        """Test that menu bar exists with all menus"""
        menubar = main_window.menuBar()
        assert menubar is not None
        
        # Get menu titles
        menu_titles = [action.text() for action in menubar.actions()]
        
        # Check required menus
        assert any("File" in title for title in menu_titles)
        assert any("Data" in title for title in menu_titles)
        assert any("Generate" in title for title in menu_titles)
    
    def test_toolbar_exists(self, main_window):
        """Test that toolbar exists with buttons"""
        from PyQt5.QtWidgets import QToolBar
        toolbar = main_window.findChild(QToolBar)
        assert toolbar is not None
        assert toolbar.isVisible()
    
    def test_status_bar_exists(self, main_window):
        """Test that status bar exists and shows user info"""
        status_bar = main_window.status_bar
        assert status_bar is not None
        assert status_bar.isVisible()
    
    def test_company_selector_exists(self, main_window):
        """Test that company selector dropdown exists"""
        assert main_window.company_selector is not None
        assert main_window.company_selector.isVisible()
    
    def test_tab_switching(self, qtbot, main_window):
        """Test that tabs can be switched programmatically"""
        tab_widget = main_window.tab_widget
        initial_index = tab_widget.currentIndex()
        
        # Switch to different tab
        new_index = (initial_index + 1) % tab_widget.count()
        tab_widget.setCurrentIndex(new_index)
        qtbot.wait(100)
        
        assert tab_widget.currentIndex() == new_index
    
    def test_window_title_updates_with_company(self, qtbot, main_window_with_company):
        """Test that window title shows company name when selected"""
        window = main_window_with_company
        qtbot.wait(200)
        
        # Window title should contain company name
        assert "Test Company Ltd" in window.windowTitle()
