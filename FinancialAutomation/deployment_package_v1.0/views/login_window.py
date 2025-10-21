"""Login window for the application"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QMessageBox, QTabWidget,
                            QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
from controllers.auth_controller import AuthController
from views.main_window import MainWindow

class LoginWindow(QWidget):
    """Login and Registration Window"""
    
    def __init__(self):
        super().__init__()
        self.main_window = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Financial Automation - Login")
        self.setGeometry(100, 100, 500, 400)
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 11pt;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
            QPushButton {
                padding: 10px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 11pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QLabel {
                font-size: 11pt;
            }
            QTabWidget::pane {
                border: 1px solid #ccc;
                background-color: white;
                border-radius: 4px;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 10px 20px;
                border: 1px solid #ccc;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid white;
            }
        """)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title_label = QLabel("Financial Automation System")
        title_font = QFont("Bookman Old Style", 16, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        main_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Schedule III & Accounting Standards Compliance")
        subtitle_font = QFont("Bookman Old Style", 10)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #7f8c8d; margin-bottom: 30px;")
        main_layout.addWidget(subtitle_label)
        
        # Tab widget for Login and Register
        self.tab_widget = QTabWidget()
        
        # Login tab
        login_tab = self.create_login_tab()
        self.tab_widget.addTab(login_tab, "Login")
        
        # Register tab
        register_tab = self.create_register_tab()
        self.tab_widget.addTab(register_tab, "Register")
        
        main_layout.addWidget(self.tab_widget)
        
        # Version info
        version_label = QLabel("Version 1.0.0")
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setStyleSheet("color: #95a5a6; font-size: 9pt; margin-top: 20px;")
        main_layout.addWidget(version_label)
        
        self.setLayout(main_layout)
    
    def create_login_tab(self):
        """Create the login tab"""
        login_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Username
        username_label = QLabel("Username:")
        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText("Enter your username")
        self.login_username.returnPressed.connect(self.handle_login)
        
        # Password
        password_label = QLabel("Password:")
        self.login_password = QLineEdit()
        self.login_password.setEchoMode(QLineEdit.Password)
        self.login_password.setPlaceholderText("Enter your password")
        self.login_password.returnPressed.connect(self.handle_login)
        
        # Login button
        login_button = QPushButton("Login")
        login_button.clicked.connect(self.handle_login)
        login_button.setCursor(Qt.PointingHandCursor)
        
        # Add widgets to layout
        layout.addWidget(username_label)
        layout.addWidget(self.login_username)
        layout.addWidget(password_label)
        layout.addWidget(self.login_password)
        layout.addSpacing(10)
        layout.addWidget(login_button)
        layout.addStretch()
        
        login_widget.setLayout(layout)
        return login_widget
    
    def create_register_tab(self):
        """Create the registration tab"""
        register_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Full Name
        fullname_label = QLabel("Full Name:")
        self.register_fullname = QLineEdit()
        self.register_fullname.setPlaceholderText("Enter your full name")
        
        # Email
        email_label = QLabel("Email:")
        self.register_email = QLineEdit()
        self.register_email.setPlaceholderText("Enter your email address")
        
        # Username
        username_label = QLabel("Username:")
        self.register_username = QLineEdit()
        self.register_username.setPlaceholderText("Choose a username (min 3 characters)")
        
        # Password
        password_label = QLabel("Password:")
        self.register_password = QLineEdit()
        self.register_password.setEchoMode(QLineEdit.Password)
        self.register_password.setPlaceholderText("Choose a password (min 6 characters)")
        
        # Confirm Password
        confirm_password_label = QLabel("Confirm Password:")
        self.register_confirm_password = QLineEdit()
        self.register_confirm_password.setEchoMode(QLineEdit.Password)
        self.register_confirm_password.setPlaceholderText("Re-enter your password")
        self.register_confirm_password.returnPressed.connect(self.handle_register)
        
        # Register button
        register_button = QPushButton("Register")
        register_button.clicked.connect(self.handle_register)
        register_button.setCursor(Qt.PointingHandCursor)
        
        # Add widgets to layout
        layout.addWidget(fullname_label)
        layout.addWidget(self.register_fullname)
        layout.addWidget(email_label)
        layout.addWidget(self.register_email)
        layout.addWidget(username_label)
        layout.addWidget(self.register_username)
        layout.addWidget(password_label)
        layout.addWidget(self.register_password)
        layout.addWidget(confirm_password_label)
        layout.addWidget(self.register_confirm_password)
        layout.addSpacing(10)
        layout.addWidget(register_button)
        layout.addStretch()
        
        register_widget.setLayout(layout)
        return register_widget
    
    def handle_login(self):
        """Handle login button click"""
        username = self.login_username.text().strip()
        password = self.login_password.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password")
            return
        
        # Authenticate user
        success, message, user = AuthController.login_user(username, password)
        
        if success:
            QMessageBox.information(self, "Login Successful", 
                                  f"Welcome {user.full_name}!\n\n{message}")
            self.open_main_window(user)
        else:
            QMessageBox.critical(self, "Login Failed", message)
    
    def handle_register(self):
        """Handle registration button click"""
        fullname = self.register_fullname.text().strip()
        email = self.register_email.text().strip()
        username = self.register_username.text().strip()
        password = self.register_password.text()
        confirm_password = self.register_confirm_password.text()
        
        # Validate inputs
        if not all([fullname, email, username, password, confirm_password]):
            QMessageBox.warning(self, "Input Error", "Please fill in all fields")
            return
        
        if password != confirm_password:
            QMessageBox.warning(self, "Password Mismatch", "Passwords do not match")
            return
        
        # Register user
        success, message, user_id = AuthController.register_user(
            username, password, email, fullname
        )
        
        if success:
            QMessageBox.information(self, "Registration Successful", 
                                  f"{message}\n\n"
                                  "You can now login with your credentials.")
            # Clear registration form
            self.register_fullname.clear()
            self.register_email.clear()
            self.register_username.clear()
            self.register_password.clear()
            self.register_confirm_password.clear()
            # Switch to login tab
            self.tab_widget.setCurrentIndex(0)
            # Set username in login form
            self.login_username.setText(username)
            self.login_password.setFocus()
        else:
            QMessageBox.critical(self, "Registration Failed", message)
    
    def open_main_window(self, user):
        """Open the main application window"""
        self.main_window = MainWindow(user)
        self.main_window.show()
        self.close()
