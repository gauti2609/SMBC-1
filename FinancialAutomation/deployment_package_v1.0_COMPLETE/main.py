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
    
    # Create Qt Application first (so error dialogs can be shown)
    app = QApplication(sys.argv)
    
    # Set default font to Bookman Old Style, 11pt
    font = QFont("Bookman Old Style", 11)
    app.setFont(font)
    
    # Set application metadata
    app.setApplicationName("Financial Automation")
    app.setOrganizationName("SMBC")
    app.setApplicationVersion("1.0.0")
    
    try:
        # Initialize database
        print("Initializing database...")
        initialize_database()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Database initialization error: {e}")
        import traceback
        traceback.print_exc()
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.critical(
            None,
            "Database Error",
            f"Failed to initialize database:\\n\\n{str(e)}\\n\\n" +
            "Please check:\\n" +
            "1. Database server is running\\n" +
            "2. Database credentials in .env file are correct\\n" +
            "3. Database 'financial_automation' exists"
        )
        sys.exit(1)
    
    # Create and show login window
    print("Creating login window...")
    login_window = LoginWindow()
    login_window.show()
    print("Login window shown")
    
    # Start event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
