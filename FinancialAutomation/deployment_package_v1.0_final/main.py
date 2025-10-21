"""
Financial Automation Application - Main Entry Point
Author: Auto-generated for SMBC
Date: October 15, 2025
Description: Desktop application for automated drafting of Financial Statements
             as per Schedule III and Indian Accounting Standards
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from views.login_window import LoginWindow
from config.database import initialize_database

def main():
    """Main entry point for the application"""
    
    # Initialize database
    initialize_database()
    
    # Create Qt Application
    app = QApplication(sys.argv)
    
    # Set default font to Bookman Old Style, 11pt
    font = QFont("Bookman Old Style", 11)
    app.setFont(font)
    
    # Set application metadata
    app.setApplicationName("Financial Automation")
    app.setOrganizationName("SMBC")
    app.setApplicationVersion("1.0.0")
    
    # Create and show login window
    login_window = LoginWindow()
    login_window.show()
    
    # Start event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
