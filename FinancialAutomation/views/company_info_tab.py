"""Company Information Tab - Complete form for company details and preferences"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QLineEdit, QComboBox, QMessageBox, QFormLayout,
                             QGroupBox, QCheckBox, QSpinBox, QTextEdit, QDateEdit,
                             QFileDialog, QDoubleSpinBox, QScrollArea)
from PyQt5.QtCore import Qt, QDate, pyqtSignal
from PyQt5.QtGui import QFont
from models.company_info import CompanyInfo
import json
from datetime import datetime

class CompanyInfoTab(QWidget):
    """Company Information Tab with Complete Form"""
    
    # Signal emitted when company is saved/updated (company_id, entity_name)
    company_saved = pyqtSignal(int, str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.current_company = None
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Initialize UI with form"""
        # Create scroll area for the form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        
        # Main widget inside scroll
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Header
        header = QLabel("Company Information & Preferences")
        header.setFont(QFont("Bookman Old Style", 14, QFont.Bold))
        header.setStyleSheet("color: #2c3e50; padding: 10px;")
        main_layout.addWidget(header)
        
        # Company Details Group
        details_group = self.create_company_details_group()
        main_layout.addWidget(details_group)
        
        # Financial Year Group
        fy_group = self.create_financial_year_group()
        main_layout.addWidget(fy_group)
        
        # Formatting Preferences Group
        format_group = self.create_formatting_group()
        main_layout.addWidget(format_group)
        
        # Rounding & Presentation Group (Schedule III Compliance)
        rounding_group = self.create_rounding_group()
        main_layout.addWidget(rounding_group)
        
        # Action Buttons
        button_layout = self.create_action_buttons()
        main_layout.addLayout(button_layout)
        
        # Help text
        help_text = QLabel(
            "💡 <b>Schedule III Compliance:</b><br>"
            "• Enter company turnover to see applicable rounding options<br>"
            "• Turnover < ₹100 Crores: Can use '100s to '1000000s<br>"
            "• Turnover ≥ ₹100 Crores: Can use '100000s to '10000000s<br>"
            "• Financial statements will be presented in selected rounding level"
        )
        help_text.setWordWrap(True)
        help_text.setStyleSheet("padding: 10px; background-color: #e8f5e9; border-radius: 5px;")
        main_layout.addWidget(help_text)
        
        main_layout.addStretch()
        
        main_widget.setLayout(main_layout)
        scroll.setWidget(main_widget)
        
        # Set scroll as main layout
        container_layout = QVBoxLayout()
        container_layout.addWidget(scroll)
        self.setLayout(container_layout)
    
    def create_company_details_group(self):
        """Create company details form group"""
        group = QGroupBox("Company Details")
        layout = QFormLayout()
        
        # Entity Name
        self.entity_name_input = QLineEdit()
        self.entity_name_input.setPlaceholderText("Enter company name...")
        layout.addRow("Entity Name*:", self.entity_name_input)
        
        # CIN Number
        self.cin_input = QLineEdit()
        self.cin_input.setPlaceholderText("L12345AB2020PLC123456")
        self.cin_input.setMaxLength(21)
        cin_label = QLabel("CIN Number:")
        cin_help = QLabel("<small>(21 characters, e.g., L12345AB2020PLC123456)</small>")
        cin_help.setStyleSheet("color: #666;")
        layout.addRow(cin_label, self.cin_input)
        layout.addRow("", cin_help)
        
        # Address
        self.address_input = QTextEdit()
        self.address_input.setPlaceholderText("Enter company address...")
        self.address_input.setMaximumHeight(80)
        layout.addRow("Address:", self.address_input)
        
        # Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("company@example.com")
        layout.addRow("Email:", self.email_input)
        
        # Phone
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("+91-XXX-XXXXXXX")
        layout.addRow("Phone:", self.phone_input)
        
        group.setLayout(layout)
        return group
    
    def create_financial_year_group(self):
        """Create financial year form group"""
        group = QGroupBox("Financial Year")
        layout = QFormLayout()
        
        # Current FY Start Date
        self.fy_start_input = QDateEdit()
        self.fy_start_input.setCalendarPopup(True)
        self.fy_start_input.setDisplayFormat("dd-MMM-yyyy")
        self.fy_start_input.setDate(QDate(2024, 4, 1))  # Default: Apr 1
        layout.addRow("FY Start Date*:", self.fy_start_input)
        
        # Current FY End Date
        self.fy_end_input = QDateEdit()
        self.fy_end_input.setCalendarPopup(True)
        self.fy_end_input.setDisplayFormat("dd-MMM-yyyy")
        self.fy_end_input.setDate(QDate(2025, 3, 31))  # Default: Mar 31
        layout.addRow("FY End Date*:", self.fy_end_input)
        
        # Previous FY Start Date
        self.prev_fy_start_input = QDateEdit()
        self.prev_fy_start_input.setCalendarPopup(True)
        self.prev_fy_start_input.setDisplayFormat("dd-MMM-yyyy")
        self.prev_fy_start_input.setDate(QDate(2023, 4, 1))
        layout.addRow("Prev FY Start:", self.prev_fy_start_input)
        
        # Previous FY End Date
        self.prev_fy_end_input = QDateEdit()
        self.prev_fy_end_input.setCalendarPopup(True)
        self.prev_fy_end_input.setDisplayFormat("dd-MMM-yyyy")
        self.prev_fy_end_input.setDate(QDate(2024, 3, 31))
        layout.addRow("Prev FY End:", self.prev_fy_end_input)
        
        group.setLayout(layout)
        return group
    
    def create_formatting_group(self):
        """Create formatting preferences group"""
        group = QGroupBox("Formatting Preferences")
        layout = QFormLayout()
        
        # Currency
        self.currency_combo = QComboBox()
        self.currency_combo.addItems(["INR", "USD", "EUR", "GBP", "JPY", "AUD", "CAD"])
        layout.addRow("Currency:", self.currency_combo)
        
        # Number Format
        self.number_format_combo = QComboBox()
        self.number_format_combo.addItems(["Accounting", "Financial", "Standard", "Scientific"])
        layout.addRow("Number Format:", self.number_format_combo)
        
        # Negative Format
        self.negative_format_combo = QComboBox()
        self.negative_format_combo.addItems([
            "Brackets (1,234)", 
            "Minus Sign -1,234", 
            "Red Color", 
            "Red with Brackets"
        ])
        layout.addRow("Negative Format:", self.negative_format_combo)
        
        # Default Font
        self.font_combo = QComboBox()
        self.font_combo.addItems([
            "Bookman Old Style", 
            "Arial", 
            "Times New Roman", 
            "Calibri", 
            "Verdana"
        ])
        layout.addRow("Default Font:", self.font_combo)
        
        # Font Size
        self.font_size_spinner = QSpinBox()
        self.font_size_spinner.setRange(9, 14)
        self.font_size_spinner.setValue(11)
        self.font_size_spinner.setSuffix(" pt")
        layout.addRow("Font Size:", self.font_size_spinner)
        
        # Decimal Places
        self.decimal_spinner = QSpinBox()
        self.decimal_spinner.setRange(0, 4)
        self.decimal_spinner.setValue(2)
        self.decimal_spinner.setSuffix(" digits")
        layout.addRow("Decimal Places:", self.decimal_spinner)
        
        # Show Zeros as Blank
        self.zeros_blank_check = QCheckBox("Show zeros as blank cells")
        layout.addRow("", self.zeros_blank_check)
        
        group.setLayout(layout)
        return group
    
    def create_rounding_group(self):
        """Create rounding and presentation group (Schedule III compliance)"""
        group = QGroupBox("Rounding & Presentation (Schedule III)")
        layout = QFormLayout()
        
        # Company Turnover (to determine allowed rounding levels)
        turnover_layout = QHBoxLayout()
        self.turnover_input = QDoubleSpinBox()
        self.turnover_input.setRange(0, 999999999999)  # Up to 99,999 Crores
        self.turnover_input.setValue(0)
        self.turnover_input.setPrefix("₹ ")
        self.turnover_input.setSuffix(" ")
        self.turnover_input.setGroupSeparatorShown(True)
        self.turnover_input.setDecimals(0)
        self.turnover_input.valueChanged.connect(self.on_turnover_changed)
        
        turnover_help = QLabel("<small>(Annual Revenue/Turnover)</small>")
        turnover_help.setStyleSheet("color: #666;")
        
        turnover_layout.addWidget(self.turnover_input)
        turnover_layout.addWidget(turnover_help)
        turnover_layout.addStretch()
        
        layout.addRow("Company Turnover*:", turnover_layout)
        
        # Rounding Level (dynamically populated based on turnover)
        self.rounding_combo = QComboBox()
        self.populate_rounding_options(0)  # Default for turnover = 0
        rounding_help = QLabel(
            "<small>As per Schedule III: Presentation format for financial statements</small>"
        )
        rounding_help.setStyleSheet("color: #666;")
        rounding_help.setWordWrap(True)
        layout.addRow("Rounding Level*:", self.rounding_combo)
        layout.addRow("", rounding_help)
        
        # Compliance Note
        compliance_note = QLabel(
            "<b>Schedule III Guidelines:</b><br>"
            "• Turnover < ₹100 Crores: Choose from Hundreds to Millions<br>"
            "• Turnover ≥ ₹100 Crores: Choose from Lakhs to Crores<br>"
            "• Financials will be automatically rounded to selected level"
        )
        compliance_note.setStyleSheet(
            "background-color: #fff3cd; padding: 10px; border-left: 4px solid #ffc107; border-radius: 4px;"
        )
        compliance_note.setWordWrap(True)
        layout.addRow(compliance_note)
        
        group.setLayout(layout)
        return group
    
    def create_action_buttons(self):
        """Create action buttons layout"""
        layout = QHBoxLayout()
        
        # Save Button
        self.save_btn = QPushButton("💾 Save Company Info")
        self.save_btn.clicked.connect(self.save_data)
        self.save_btn.setStyleSheet(
            "background-color: #4CAF50; color: white; padding: 10px 20px; font-weight: bold;"
        )
        layout.addWidget(self.save_btn)
        
        # Load Button
        self.load_btn = QPushButton("📂 Reload from Database")
        self.load_btn.clicked.connect(self.load_data)
        self.load_btn.setStyleSheet("padding: 10px 20px;")
        layout.addWidget(self.load_btn)
        
        # Clear Button
        self.clear_btn = QPushButton("🔄 Clear Form")
        self.clear_btn.clicked.connect(self.clear_form)
        self.clear_btn.setStyleSheet("padding: 10px 20px;")
        layout.addWidget(self.clear_btn)
        
        # Export Config
        self.export_btn = QPushButton("📤 Export Config")
        self.export_btn.clicked.connect(self.export_config)
        self.export_btn.setStyleSheet("padding: 10px 20px;")
        layout.addWidget(self.export_btn)
        
        # Import Config
        self.import_btn = QPushButton("📥 Import Config")
        self.import_btn.clicked.connect(self.import_config)
        self.import_btn.setStyleSheet("padding: 10px 20px;")
        layout.addWidget(self.import_btn)
        
        layout.addStretch()
        
        return layout
    
    def populate_rounding_options(self, turnover):
        """Populate rounding options based on turnover (Schedule III compliance)"""
        self.rounding_combo.clear()
        options = CompanyInfo.get_rounding_options(turnover)
        
        for value, text in options:
            self.rounding_combo.addItem(text, value)
        
        # Set default to Lakhs (most common)
        for i in range(self.rounding_combo.count()):
            if self.rounding_combo.itemData(i) == '100000':
                self.rounding_combo.setCurrentIndex(i)
                break
    
    def on_turnover_changed(self, value):
        """Handle turnover change - update rounding options"""
        current_rounding = self.rounding_combo.currentData()
        self.populate_rounding_options(value)
        
        # Try to restore previous selection if still valid
        for i in range(self.rounding_combo.count()):
            if self.rounding_combo.itemData(i) == current_rounding:
                self.rounding_combo.setCurrentIndex(i)
                break
    
    def validate_form(self):
        """Validate form inputs"""
        if not self.entity_name_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Entity Name is required!")
            return False
        
        # Validate CIN if provided
        cin = self.cin_input.text().strip()
        if cin and not CompanyInfo.validate_cin(cin):
            QMessageBox.warning(
                self, "Validation Error",
                "Invalid CIN format!\n\nExpected format: L12345AB2020PLC123456\n\n"
                "• First char: Letter (L/U/N)\n"
                "• Next 5: Digits\n"
                "• Next 2: State code (letters)\n"
                "• Next 4: Year (digits)\n"
                "• Next 3: Company type (letters)\n"
                "• Last 6: Sequential number (digits)"
            )
            return False
        
        # Validate date range
        fy_start = self.fy_start_input.date().toPyDate()
        fy_end = self.fy_end_input.date().toPyDate()
        
        if not CompanyInfo.validate_dates(fy_start, fy_end):
            QMessageBox.warning(
                self, "Validation Error",
                "FY End Date must be after FY Start Date!"
            )
            return False
        
        # Validate turnover and rounding level
        turnover = self.turnover_input.value()
        rounding_level = self.rounding_combo.currentData()
        
        if not CompanyInfo.validate_rounding_level(turnover, rounding_level):
            QMessageBox.warning(
                self, "Validation Error",
                "Invalid rounding level for the given turnover!\n\n"
                "As per Schedule III:\n"
                "• Turnover < ₹100 Crores: Use '100s to '1000000s\n"
                "• Turnover ≥ ₹100 Crores: Use '100000s to '10000000s"
            )
            return False
        
        return True
    
    def save_data(self):
        """Save company information"""
        if not self.validate_form():
            return
        
        try:
            # Prepare data
            entity_name = self.entity_name_input.text().strip()
            address = self.address_input.toPlainText().strip()
            cin_no = self.cin_input.text().strip() or None
            fy_start = self.fy_start_input.date().toPyDate().strftime('%Y-%m-%d')
            fy_end = self.fy_end_input.date().toPyDate().strftime('%Y-%m-%d')
            currency = self.currency_combo.currentText()
            units = "Custom"  # Using custom rounding levels
            number_format = self.number_format_combo.currentText()
            negative_format = self.negative_format_combo.currentText()
            default_font = self.font_combo.currentText()
            default_font_size = self.font_size_spinner.value()
            show_zeros_as_blank = 1 if self.zeros_blank_check.isChecked() else 0
            decimal_places = self.decimal_spinner.value()
            turnover = self.turnover_input.value()
            rounding_level = self.rounding_combo.currentData()
            
            # Get user ID from parent window
            user_id = self.parent_window.user.user_id if hasattr(self.parent_window, 'user') else 1
            
            # Check if company info exists
            existing = CompanyInfo.get_by_user_id(user_id)
            
            if existing:
                # Update existing
                CompanyInfo.update(
                    company_id=existing.company_id,
                    entity_name=entity_name,
                    fy_start_date=fy_start,
                    fy_end_date=fy_end,
                    address=address,
                    cin_no=cin_no,
                    currency=currency,
                    units=units,
                    number_format=number_format,
                    negative_format=negative_format,
                    default_font=default_font,
                    default_font_size=default_font_size,
                    show_zeros_as_blank=show_zeros_as_blank,
                    decimal_places=decimal_places,
                    turnover=turnover,
                    rounding_level=rounding_level
                )
                QMessageBox.information(
                    self, "Success",
                    f"Company information updated successfully!\n\n"
                    f"Entity: {entity_name}\n"
                    f"FY: {fy_start} to {fy_end}\n"
                    f"Rounding: {CompanyInfo.get_rounding_display_name(rounding_level)}"
                )
                # Emit signal to refresh company selector
                self.company_saved.emit(existing.company_id, entity_name)
            else:
                # Create new
                company_id = CompanyInfo.create(
                    user_id=user_id,
                    entity_name=entity_name,
                    fy_start_date=fy_start,
                    fy_end_date=fy_end,
                    address=address,
                    cin_no=cin_no,
                    currency=currency,
                    units=units,
                    number_format=number_format,
                    negative_format=negative_format,
                    default_font=default_font,
                    default_font_size=default_font_size,
                    show_zeros_as_blank=show_zeros_as_blank,
                    decimal_places=decimal_places,
                    turnover=turnover,
                    rounding_level=rounding_level
                )
                QMessageBox.information(
                    self, "Success",
                    f"Company information saved successfully!\n\n"
                    f"Company ID: {company_id}\n"
                    f"Entity: {entity_name}\n"
                    f"FY: {fy_start} to {fy_end}\n"
                    f"Rounding: {CompanyInfo.get_rounding_display_name(rounding_level)}"
                )
                # Emit signal to refresh company selector
                self.company_saved.emit(company_id, entity_name)
            
            # Store current company ID
            if hasattr(self.parent_window, 'current_company_id'):
                self.parent_window.current_company_id = existing.company_id if existing else company_id
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save company information:\n{str(e)}")
    
    def load_data(self):
        """Load company information from database"""
        try:
            # Get user ID from parent window
            user_id = self.parent_window.user.user_id if hasattr(self.parent_window, 'user') else 1
            
            company = CompanyInfo.get_by_user_id(user_id)
            
            if company:
                # Populate form
                self.entity_name_input.setText(company.entity_name)
                self.address_input.setText(company.address or "")
                self.cin_input.setText(company.cin_no or "")
                
                # Parse dates
                from datetime import datetime
                fy_start = datetime.strptime(company.fy_start_date, '%Y-%m-%d')
                fy_end = datetime.strptime(company.fy_end_date, '%Y-%m-%d')
                
                self.fy_start_input.setDate(QDate(fy_start.year, fy_start.month, fy_start.day))
                self.fy_end_input.setDate(QDate(fy_end.year, fy_end.month, fy_end.day))
                
                # Set preferences
                self.currency_combo.setCurrentText(company.currency)
                self.number_format_combo.setCurrentText(company.number_format)
                self.negative_format_combo.setCurrentText(company.negative_format)
                self.font_combo.setCurrentText(company.default_font)
                self.font_size_spinner.setValue(company.default_font_size)
                self.zeros_blank_check.setChecked(company.show_zeros_as_blank == 1)
                
                # Store current company
                self.current_company = company
                
                QMessageBox.information(
                    self, "Data Loaded",
                    f"Company information loaded successfully!\n\nEntity: {company.entity_name}"
                )
            else:
                QMessageBox.information(
                    self, "No Data",
                    "No company information found for this user.\n\nPlease fill in the form and save."
                )
        
        except Exception as e:
            QMessageBox.warning(self, "Load Error", f"Could not load data:\n{str(e)}")
    
    def clear_form(self):
        """Clear all form fields"""
        self.entity_name_input.clear()
        self.cin_input.clear()
        self.address_input.clear()
        self.email_input.clear()
        self.phone_input.clear()
        self.fy_start_input.setDate(QDate(2024, 4, 1))
        self.fy_end_input.setDate(QDate(2025, 3, 31))
        self.prev_fy_start_input.setDate(QDate(2023, 4, 1))
        self.prev_fy_end_input.setDate(QDate(2024, 3, 31))
        self.currency_combo.setCurrentIndex(0)
        self.number_format_combo.setCurrentIndex(0)
        self.negative_format_combo.setCurrentIndex(0)
        self.font_combo.setCurrentIndex(0)
        self.font_size_spinner.setValue(11)
        self.decimal_spinner.setValue(2)
        self.zeros_blank_check.setChecked(False)
        self.turnover_input.setValue(0)
        self.populate_rounding_options(0)
        self.current_company = None
    
    def export_config(self):
        """Export configuration to JSON file"""
        if not self.entity_name_input.text().strip():
            QMessageBox.warning(self, "Export Error", "Please fill in company information first!")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Configuration",
            f"company_config_{datetime.now().strftime('%Y%m%d')}.json",
            "JSON Files (*.json)"
        )
        
        if not file_path:
            return
        
        try:
            config = {
                'entity_name': self.entity_name_input.text().strip(),
                'cin_no': self.cin_input.text().strip(),
                'address': self.address_input.toPlainText().strip(),
                'email': self.email_input.text().strip(),
                'phone': self.phone_input.text().strip(),
                'fy_start_date': self.fy_start_input.date().toString("yyyy-MM-dd"),
                'fy_end_date': self.fy_end_input.date().toString("yyyy-MM-dd"),
                'currency': self.currency_combo.currentText(),
                'number_format': self.number_format_combo.currentText(),
                'negative_format': self.negative_format_combo.currentText(),
                'default_font': self.font_combo.currentText(),
                'default_font_size': self.font_size_spinner.value(),
                'decimal_places': self.decimal_spinner.value(),
                'show_zeros_as_blank': self.zeros_blank_check.isChecked(),
                'turnover': self.turnover_input.value(),
                'rounding_level': self.rounding_combo.currentData(),
                'rounding_display': self.rounding_combo.currentText()
            }
            
            with open(file_path, 'w') as f:
                json.dump(config, f, indent=4)
            
            QMessageBox.information(self, "Success", f"Configuration exported to:\n{file_path}")
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Export failed:\n{str(e)}")
    
    def import_config(self):
        """Import configuration from JSON file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Import Configuration", "",
            "JSON Files (*.json)"
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'r') as f:
                config = json.load(f)
            
            # Populate form
            self.entity_name_input.setText(config.get('entity_name', ''))
            self.cin_input.setText(config.get('cin_no', ''))
            self.address_input.setText(config.get('address', ''))
            self.email_input.setText(config.get('email', ''))
            self.phone_input.setText(config.get('phone', ''))
            
            # Dates
            from datetime import datetime
            fy_start = datetime.strptime(config.get('fy_start_date', '2024-04-01'), '%Y-%m-%d')
            fy_end = datetime.strptime(config.get('fy_end_date', '2025-03-31'), '%Y-%m-%d')
            self.fy_start_input.setDate(QDate(fy_start.year, fy_start.month, fy_start.day))
            self.fy_end_input.setDate(QDate(fy_end.year, fy_end.month, fy_end.day))
            
            # Preferences
            self.currency_combo.setCurrentText(config.get('currency', 'INR'))
            self.number_format_combo.setCurrentText(config.get('number_format', 'Accounting'))
            self.negative_format_combo.setCurrentText(config.get('negative_format', 'Brackets (1,234)'))
            self.font_combo.setCurrentText(config.get('default_font', 'Bookman Old Style'))
            self.font_size_spinner.setValue(config.get('default_font_size', 11))
            self.decimal_spinner.setValue(config.get('decimal_places', 2))
            self.zeros_blank_check.setChecked(config.get('show_zeros_as_blank', False))
            
            # Turnover and rounding
            turnover = config.get('turnover', 0)
            self.turnover_input.setValue(turnover)
            self.populate_rounding_options(turnover)
            
            rounding_level = config.get('rounding_level', '100000')
            for i in range(self.rounding_combo.count()):
                if self.rounding_combo.itemData(i) == rounding_level:
                    self.rounding_combo.setCurrentIndex(i)
                    break
            
            QMessageBox.information(
                self, "Success",
                f"Configuration imported successfully!\n\nEntity: {config.get('entity_name', 'N/A')}"
            )
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Import failed:\n{str(e)}")
