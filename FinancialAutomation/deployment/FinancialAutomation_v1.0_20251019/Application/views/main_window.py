"""Main application window"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QTabWidget, QMenuBar, QMenu, QAction, QStatusBar,
                            QLabel, QMessageBox, QToolBar, QPushButton, QFileDialog,
                            QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from controllers.auth_controller import AuthController
from models.license import License
from models.company_info import CompanyInfo
import json
import os

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.current_company_id = None
        self.current_company = None
        self.session_file = os.path.join(os.path.dirname(__file__), '..', f'.session_{user.user_id}.json')
        self.init_ui()
        self.check_license_status()
        self.load_last_session()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Financial Automation - Main Application")
        self.setGeometry(50, 50, 1400, 900)
        
        # Set default font
        font = QFont("Bookman Old Style", 11)
        self.setFont(font)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create toolbar
        self.create_toolbar()
        
        # Create central widget with tab system
        self.create_central_widget()
        
        # Create status bar
        self.create_status_bar()
        
        # Apply stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QTabWidget::pane {
                border: 1px solid #ccc;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 10px 20px;
                border: 1px solid #ccc;
                border-bottom: none;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid white;
            }
            QTabBar::tab:hover {
                background-color: #d0d0d0;
            }
            QPushButton {
                padding: 8px 16px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QToolBar {
                background-color: #34495e;
                border: none;
                padding: 5px;
            }
            QToolButton {
                color: white;
                background-color: transparent;
                border: none;
                padding: 8px;
            }
            QToolButton:hover {
                background-color: #415f7d;
            }
        """)
    
    def create_menu_bar(self):
        """Create the menu bar"""
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #2c3e50;
                color: white;
                padding: 5px;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 8px 12px;
            }
            QMenuBar::item:selected {
                background-color: #34495e;
            }
            QMenu {
                background-color: white;
                color: black;
            }
            QMenu::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        new_company_action = QAction("New Company", self)
        new_company_action.setShortcut("Ctrl+N")
        new_company_action.triggered.connect(self.new_company)
        file_menu.addAction(new_company_action)
        
        open_company_action = QAction("Open Company", self)
        open_company_action.setShortcut("Ctrl+O")
        open_company_action.triggered.connect(self.open_company)
        file_menu.addAction(open_company_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Data menu
        data_menu = menubar.addMenu("&Data")
        
        master_data_action = QAction("Master Data Management", self)
        master_data_action.triggered.connect(self.open_master_data)
        data_menu.addAction(master_data_action)
        
        import_tb_action = QAction("Import Trial Balance", self)
        import_tb_action.setShortcut("Ctrl+I")
        import_tb_action.triggered.connect(self.import_trial_balance)
        data_menu.addAction(import_tb_action)
        
        data_menu.addSeparator()
        
        company_info_action = QAction("Company Information", self)
        company_info_action.triggered.connect(self.edit_company_info)
        data_menu.addAction(company_info_action)
        
        # Generate menu
        generate_menu = menubar.addMenu("&Generate")
        
        generate_all_action = QAction("Generate All Statements", self)
        generate_all_action.setShortcut("F5")
        generate_all_action.triggered.connect(self.generate_all_statements)
        generate_menu.addAction(generate_all_action)
        
        generate_menu.addSeparator()
        
        generate_bs_action = QAction("Balance Sheet", self)
        generate_bs_action.triggered.connect(self.generate_balance_sheet)
        generate_menu.addAction(generate_bs_action)
        
        generate_pl_action = QAction("Profit & Loss", self)
        generate_pl_action.triggered.connect(self.generate_profit_loss)
        generate_menu.addAction(generate_pl_action)
        
        generate_cf_action = QAction("Cash Flow", self)
        generate_cf_action.triggered.connect(self.generate_cash_flow)
        generate_menu.addAction(generate_cf_action)
        
        generate_notes_action = QAction("Notes to Accounts", self)
        generate_notes_action.triggered.connect(self.generate_notes)
        generate_menu.addAction(generate_notes_action)
        
        # Export menu
        export_menu = menubar.addMenu("&Export")
        
        export_excel_action = QAction("Export to Excel", self)
        export_excel_action.setShortcut("Ctrl+E")
        export_excel_action.triggered.connect(self.export_to_excel)
        export_menu.addAction(export_excel_action)
        
        export_pdf_action = QAction("Export to PDF", self)
        export_pdf_action.triggered.connect(self.export_to_pdf)
        export_menu.addAction(export_pdf_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("&Tools")
        
        validate_action = QAction("Validate Data", self)
        validate_action.triggered.connect(self.validate_data)
        tools_menu.addAction(validate_action)
        
        ratios_action = QAction("Ratio Analysis", self)
        ratios_action.triggered.connect(self.show_ratio_analysis)
        tools_menu.addAction(ratios_action)
        
        aging_action = QAction("Aging Schedules", self)
        aging_action.triggered.connect(self.show_aging_schedules)
        tools_menu.addAction(aging_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        user_manual_action = QAction("User Manual", self)
        user_manual_action.setShortcut("F1")
        user_manual_action.triggered.connect(self.show_user_manual)
        help_menu.addAction(user_manual_action)
        
        license_info_action = QAction("License Information", self)
        license_info_action.triggered.connect(self.show_license_info)
        help_menu.addAction(license_info_action)
        
        help_menu.addSeparator()
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_toolbar(self):
        """Create the toolbar"""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        # Company Selector
        company_label = QLabel("  Company: ")
        company_label.setStyleSheet("color: white; font-weight: bold; padding: 5px;")
        toolbar.addWidget(company_label)
        
        self.company_selector = QComboBox()
        self.company_selector.setMinimumWidth(300)
        self.company_selector.setStyleSheet("""
            QComboBox {
                background-color: white;
                color: #2c3e50;
                border: 2px solid #3498db;
                border-radius: 4px;
                padding: 5px 10px;
                font-weight: bold;
            }
            QComboBox:hover {
                border: 2px solid #2980b9;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
        """)
        self.company_selector.currentIndexChanged.connect(self.on_company_changed)
        toolbar.addWidget(self.company_selector)
        
        toolbar.addSeparator()
        
        # New Company
        new_company_btn = QAction("➕ New Company", self)
        new_company_btn.triggered.connect(self.new_company)
        toolbar.addAction(new_company_btn)
        
        toolbar.addSeparator()
        
        # Import Trial Balance
        import_tb_btn = QAction("📥 Import TB", self)
        import_tb_btn.triggered.connect(self.import_trial_balance)
        toolbar.addAction(import_tb_btn)
        
        toolbar.addSeparator()
        
        # Generate Statements
        generate_btn = QAction("Generate All", self)
        generate_btn.triggered.connect(self.generate_all_statements)
        toolbar.addAction(generate_btn)
        
        toolbar.addSeparator()
        
        # Export
        export_btn = QAction("Export Excel", self)
        export_btn.triggered.connect(self.export_to_excel)
        toolbar.addAction(export_btn)
        
        toolbar.addSeparator()
        
        # Validate
        validate_btn = QAction("Validate", self)
        validate_btn.triggered.connect(self.validate_data)
        toolbar.addAction(validate_btn)
    
    def create_central_widget(self):
        """Create the central widget with tabs"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Welcome panel (shown when no company is selected)
        self.welcome_widget = self.create_welcome_widget()
        
        # Tab widget (shown when company is selected)
        self.tab_widget = QTabWidget()
        self.tab_widget.setVisible(False)
        
        # Create tabs (will be populated when company is loaded)
        self.create_tabs()
        
        layout.addWidget(self.welcome_widget)
        layout.addWidget(self.tab_widget)
        
        central_widget.setLayout(layout)
    
    def create_welcome_widget(self):
        """Create welcome widget"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        # Welcome message
        welcome_label = QLabel(f"Welcome, {self.user.full_name}!")
        welcome_label.setFont(QFont("Bookman Old Style", 18, QFont.Bold))
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("color: #2c3e50; margin: 20px;")
        
        # Instructions
        instruction_label = QLabel("Get started by creating a new company or opening an existing one")
        instruction_label.setFont(QFont("Bookman Old Style", 12))
        instruction_label.setAlignment(Qt.AlignCenter)
        instruction_label.setStyleSheet("color: #7f8c8d; margin: 10px;")
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.setSpacing(20)
        
        new_company_btn = QPushButton("Create New Company")
        new_company_btn.setMinimumSize(200, 50)
        new_company_btn.setFont(QFont("Bookman Old Style", 12, QFont.Bold))
        new_company_btn.clicked.connect(self.new_company)
        new_company_btn.setCursor(Qt.PointingHandCursor)
        
        open_company_btn = QPushButton("Open Existing Company")
        open_company_btn.setMinimumSize(200, 50)
        open_company_btn.setFont(QFont("Bookman Old Style", 12, QFont.Bold))
        open_company_btn.clicked.connect(self.open_company)
        open_company_btn.setCursor(Qt.PointingHandCursor)
        
        button_layout.addWidget(new_company_btn)
        button_layout.addWidget(open_company_btn)
        
        layout.addWidget(welcome_label)
        layout.addWidget(instruction_label)
        layout.addSpacing(30)
        layout.addLayout(button_layout)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def create_tabs(self):
        """Create application tabs"""
        # Company Info tab
        from views.company_info_tab import CompanyInfoTab
        self.company_info_tab = CompanyInfoTab(self)
        self.company_info_tab.company_saved.connect(self.on_company_saved)
        self.tab_widget.addTab(self.company_info_tab, "Company Information")
        
        # Master Data tab
        from views.master_data_tab import MasterDataTab
        self.master_data_tab = MasterDataTab(self)
        self.tab_widget.addTab(self.master_data_tab, "Master Data")
        
        # Trial Balance tab
        from views.trial_balance_tab import TrialBalanceTab
        self.trial_balance_tab = TrialBalanceTab(self)
        self.tab_widget.addTab(self.trial_balance_tab, "Trial Balance")
        
        # Input Forms tab
        from views.input_forms_tab import InputFormsTab
        self.input_forms_tab = InputFormsTab(self)
        self.tab_widget.addTab(self.input_forms_tab, "Input Forms")
        
        # Selection Sheet tab
        from views.selection_sheet_tab import SelectionSheetTab
        self.selection_sheet_tab = SelectionSheetTab(self)
        self.tab_widget.addTab(self.selection_sheet_tab, "Selection Sheet")
        
        # Financials tab
        from views.financials_tab import FinancialsTab
        self.financials_tab = FinancialsTab(self)
        self.tab_widget.addTab(self.financials_tab, "Financial Statements")
    
    def create_status_bar(self):
        """Create status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #ecf0f1;
                color: #2c3e50;
                border-top: 1px solid #bdc3c7;
            }
        """)
        self.update_status_bar("Ready")
    
    def update_status_bar(self, message):
        """Update status bar message"""
        self.status_bar.showMessage(message)
    
    def check_license_status(self):
        """Check and display license status"""
        is_valid, message = License.validate_license(self.user.user_id)
        license = AuthController.get_license_info(self.user.user_id)
        
        if license:
            # Add license info to status bar
            license_label = QLabel(f"  License: {license.license_type} - {message}")
            license_label.setStyleSheet("color: #27ae60; font-weight: bold;")
            self.status_bar.addPermanentWidget(license_label)
        
        # Add company status indicator
        self.company_status_label = QLabel("  No company selected")
        self.company_status_label.setStyleSheet("color: #e74c3c; font-weight: bold; padding: 0 10px;")
        self.status_bar.addPermanentWidget(self.company_status_label)
    
    # Company Management Methods
    def populate_company_selector(self):
        """Populate company selector with available companies"""
        self.company_selector.blockSignals(True)  # Prevent triggering change event
        self.company_selector.clear()
        self.company_selector.addItem("-- Select Company --", None)
        
        # Get all companies for this user
        companies = CompanyInfo.get_all_by_user(self.user.user_id)
        
        for company in companies:
            display_text = f"{company.entity_name}"
            if company.cin_no:
                display_text += f" (CIN: {company.cin_no[:10]}...)"
            self.company_selector.addItem(display_text, company.company_id)
        
        self.company_selector.blockSignals(False)
    
    def on_company_changed(self, index):
        """Handle company selection change"""
        company_id = self.company_selector.currentData()
        
        if company_id:
            self.load_company(company_id)
        else:
            self.clear_company()
    
    def on_company_saved(self, company_id, entity_name):
        """Handle company saved signal - refresh selector and set as current"""
        # Refresh the company selector dropdown
        self.populate_company_selector()
        
        # Find and select the saved company in the dropdown
        for i in range(self.company_selector.count()):
            if self.company_selector.itemData(i) == company_id:
                self.company_selector.blockSignals(True)
                self.company_selector.setCurrentIndex(i)
                self.company_selector.blockSignals(False)
                break
        
        # Update current company
        self.current_company_id = company_id
        company = CompanyInfo.get_by_id(company_id)
        if company:
            self.current_company = company
            self.company_status_label.setText(f"  Active: {entity_name}")
            self.company_status_label.setStyleSheet("color: #27ae60; font-weight: bold; padding: 0 10px;")
            self.update_status_bar(f"Company saved: {entity_name}")
            self.save_session(company_id)
    
    def load_company(self, company_id):
        """Load selected company data"""
        try:
            company = CompanyInfo.get_by_id(company_id)
            
            if company:
                self.current_company_id = company_id
                self.current_company = company
                
                # Update UI
                self.company_status_label.setText(f"  Active: {company.entity_name}")
                self.company_status_label.setStyleSheet("color: #27ae60; font-weight: bold; padding: 0 10px;")
                self.update_status_bar(f"Loaded company: {company.entity_name}")
                
                # Refresh all tabs with company data
                self.refresh_all_tabs()
                
                # Save session
                self.save_session(company_id)
                
                QMessageBox.information(
                    self, "Company Loaded",
                    f"Successfully loaded:\n\n"
                    f"Entity: {company.entity_name}\n"
                    f"FY: {company.fy_start_date} to {company.fy_end_date}"
                )
            else:
                QMessageBox.warning(self, "Error", "Company not found")
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load company:\n{str(e)}")
    
    def clear_company(self):
        """Clear current company selection"""
        self.current_company_id = None
        self.current_company = None
        self.company_status_label.setText("  No company selected")
        self.company_status_label.setStyleSheet("color: #e74c3c; font-weight: bold; padding: 0 10px;")
        self.update_status_bar("No company selected")
    
    def refresh_all_tabs(self):
        """Refresh all tabs with current company data"""
        if hasattr(self, 'company_info_tab'):
            self.company_info_tab.load_data()
        
        if hasattr(self, 'trial_balance_tab'):
            self.trial_balance_tab.refresh_data()
        
        if hasattr(self, 'master_data_tab'):
            # Refresh master data with new company
            self.master_data_tab.load_data()
        
        if hasattr(self, 'selection_sheet_tab'):
            # Load selection sheet for new company
            self.selection_sheet_tab.set_company(self.current_company_id)
    
    def save_session(self, company_id):
        """Save current session state"""
        try:
            session_data = {
                'user_id': self.user.user_id,
                'last_company_id': company_id,
                'timestamp': str(Qt.QDateTime.currentDateTime().toString())
            }
            
            with open(self.session_file, 'w') as f:
                json.dump(session_data, f)
        
        except Exception as e:
            print(f"Failed to save session: {str(e)}")
    
    def load_last_session(self):
        """Load last session state"""
        try:
            # Populate company selector first
            self.populate_company_selector()
            
            if os.path.exists(self.session_file):
                with open(self.session_file, 'r') as f:
                    session_data = json.load(f)
                
                last_company_id = session_data.get('last_company_id')
                
                if last_company_id:
                    # Find and select the company in dropdown
                    for i in range(self.company_selector.count()):
                        if self.company_selector.itemData(i) == last_company_id:
                            self.company_selector.setCurrentIndex(i)
                            break
        
        except Exception as e:
            print(f"Failed to load last session: {str(e)}")
            # Just populate with available companies
            self.populate_company_selector()
    
    # Menu action handlers
    def new_company(self):
        """Create new company - switch to Company Info tab"""
        if hasattr(self, 'company_info_tab'):
            self.tab_widget.setCurrentWidget(self.company_info_tab)
            self.company_info_tab.clear_form()
            QMessageBox.information(
                self, "New Company",
                "Please fill in the Company Information form and click 'Save Company Info'.\n\n"
                "After saving, the company will appear in the Company selector."
            )
        else:
            QMessageBox.warning(self, "Error", "Company Info tab not initialized")
    
    def open_company(self):
        """Open existing company - show company selector"""
        self.populate_company_selector()
        
        if self.company_selector.count() > 1:  # More than just "-- Select Company --"
            QMessageBox.information(
                self, "Open Company",
                "Please select a company from the dropdown in the toolbar to continue working."
            )
        else:
            reply = QMessageBox.question(
                self, "No Companies Found",
                "No companies found for your account.\n\nWould you like to create a new company?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.new_company()
    
    def open_master_data(self):
        """Open master data management"""
        if self.current_company_id:
            self.tab_widget.setCurrentWidget(self.master_data_tab)
        else:
            QMessageBox.warning(self, "No Company", "Please create or open a company first")
    
    def import_trial_balance(self):
        """Import trial balance"""
        if self.current_company_id:
            self.tab_widget.setCurrentWidget(self.trial_balance_tab)
            self.trial_balance_tab.import_trial_balance()
        else:
            QMessageBox.warning(self, "No Company", "Please create or open a company first")
    
    def edit_company_info(self):
        """Edit company information"""
        if self.current_company_id:
            self.tab_widget.setCurrentWidget(self.company_info_tab)
        else:
            QMessageBox.warning(self, "No Company", "Please create or open a company first")
    
    def generate_all_statements(self):
        """Generate all financial statements"""
        if self.current_company_id:
            self.tab_widget.setCurrentWidget(self.financials_tab)
            self.financials_tab.generate_all()
        else:
            QMessageBox.warning(self, "No Company", "Please create or open a company first")
    
    def generate_balance_sheet(self):
        """Generate balance sheet"""
        QMessageBox.information(self, "Generate", "Balance Sheet generation coming soon!")
    
    def generate_profit_loss(self):
        """Generate profit & loss"""
        QMessageBox.information(self, "Generate", "P&L generation coming soon!")
    
    def generate_cash_flow(self):
        """Generate cash flow"""
        QMessageBox.information(self, "Generate", "Cash Flow generation coming soon!")
    
    def generate_notes(self):
        """Generate notes to accounts"""
        QMessageBox.information(self, "Generate", "Notes generation coming soon!")
    
    def export_to_excel(self):
        """Export to Excel"""
        if self.current_company_id:
            QMessageBox.information(self, "Export", "Excel export coming soon!")
        else:
            QMessageBox.warning(self, "No Company", "Please create or open a company first")
    
    def export_to_pdf(self):
        """Export to PDF"""
        QMessageBox.information(self, "Export", "PDF export coming soon!")
    
    def validate_data(self):
        """Validate data"""
        if self.current_company_id:
            QMessageBox.information(self, "Validate", "Data validation coming soon!")
        else:
            QMessageBox.warning(self, "No Company", "Please create or open a company first")
    
    def show_ratio_analysis(self):
        """Show ratio analysis"""
        QMessageBox.information(self, "Ratios", "Ratio analysis coming soon!")
    
    def show_aging_schedules(self):
        """Show aging schedules"""
        QMessageBox.information(self, "Aging", "Aging schedules coming soon!")
    
    def show_user_manual(self):
        """Show user manual"""
        QMessageBox.information(self, "Help", "User manual coming soon!")
    
    def show_license_info(self):
        """Show license information"""
        license = AuthController.get_license_info(self.user.user_id)
        if license:
            info = f"""
            <b>License Information</b><br><br>
            <b>Type:</b> {license.license_type}<br>
            <b>License Key:</b> {license.license_key}<br>
            <b>Issue Date:</b> {license.issue_date}<br>
            <b>Expiry Date:</b> {license.expiry_date if license.expiry_date else 'Never'}<br>
            <b>Status:</b> {'Active' if license.is_active else 'Inactive'}
            """
            QMessageBox.information(self, "License Information", info)
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
        <h2>Financial Automation System</h2>
        <p><b>Version:</b> 1.0.0</p>
        <p><b>Description:</b> Automated drafting of Financial Statements as per 
        Schedule III of the Companies Act and Indian Accounting Standards</p>
        <p><b>Division:</b> AS Division I (Not Ind AS)</p>
        <br>
        <p>© 2025 SMBC. All rights reserved.</p>
        """
        QMessageBox.about(self, "About Financial Automation", about_text)
