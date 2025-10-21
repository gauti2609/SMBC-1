"""
Trial Balance Tab - Import and map trial balance with comparative year support
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QLabel, QFileDialog,
                             QMessageBox, QGroupBox, QFormLayout, QComboBox,
                             QProgressBar, QSpinBox, QCheckBox, QTextEdit,
                             QSplitter, QHeaderView, QAbstractItemView)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QColor
from models.trial_balance import TrialBalance
from models.company_info import CompanyInfo
from models.master_data import MajorHead, MinorHead, Grouping
import pandas as pd
import os
from datetime import datetime


class ImportWorker(QThread):
    """Worker thread for importing trial balance data"""
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str, list)
    
    def __init__(self, file_path, column_mapping, company_id, import_batch_id):
        super().__init__()
        self.file_path = file_path
        self.column_mapping = column_mapping
        self.company_id = company_id
        self.import_batch_id = import_batch_id
    
    def run(self):
        try:
            # Read file based on extension
            if self.file_path.endswith('.csv'):
                df = pd.read_csv(self.file_path)
            elif self.file_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(self.file_path)
            else:
                self.finished.emit(False, "Unsupported file format. Use CSV or Excel.", [])
                return
            
            # Validate required columns
            required = ['ledger_name']
            for req in required:
                if req not in self.column_mapping or not self.column_mapping[req]:
                    self.finished.emit(False, f"Required column '{req}' not mapped!", [])
                    return
            
            # Process entries
            entries = []
            total_rows = len(df)
            
            for index, row in df.iterrows():
                try:
                    entry = {
                        'ledger_name': str(row[self.column_mapping['ledger_name']]).strip(),
                        'opening_balance_cy': float(row[self.column_mapping.get('opening_balance_cy', 0)]) if self.column_mapping.get('opening_balance_cy') else 0,
                        'debit_cy': float(row[self.column_mapping.get('debit_cy', 0)]) if self.column_mapping.get('debit_cy') else 0,
                        'credit_cy': float(row[self.column_mapping.get('credit_cy', 0)]) if self.column_mapping.get('credit_cy') else 0,
                        'closing_balance_cy': float(row[self.column_mapping.get('closing_balance_cy', 0)]) if self.column_mapping.get('closing_balance_cy') else 0,
                        'opening_balance_py': float(row[self.column_mapping.get('opening_balance_py', 0)]) if self.column_mapping.get('opening_balance_py') else 0,
                        'debit_py': float(row[self.column_mapping.get('debit_py', 0)]) if self.column_mapping.get('debit_py') else 0,
                        'credit_py': float(row[self.column_mapping.get('credit_py', 0)]) if self.column_mapping.get('credit_py') else 0,
                        'closing_balance_py': float(row[self.column_mapping.get('closing_balance_py', 0)]) if self.column_mapping.get('closing_balance_py') else 0,
                        'type_bs_pl': 'BS',
                        'is_mapped': 0
                    }
                    
                    # Skip if ledger name is empty
                    if entry['ledger_name'] and entry['ledger_name'] != 'nan':
                        entries.append(entry)
                    
                    # Update progress
                    progress_pct = int(((index + 1) / total_rows) * 100)
                    self.progress.emit(progress_pct)
                
                except Exception as e:
                    print(f"Error processing row {index}: {str(e)}")
                    continue
            
            # Bulk import
            if entries:
                TrialBalance.bulk_import(self.company_id, entries, self.import_batch_id)
                self.finished.emit(True, f"Successfully imported {len(entries)} entries", entries)
            else:
                self.finished.emit(False, "No valid entries found in file", [])
        
        except Exception as e:
            self.finished.emit(False, f"Import failed: {str(e)}", [])


class TrialBalanceTab(QWidget):
    """Trial Balance Import and Mapping Tab with comparative year support"""
    
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.current_file_path = None
        self.column_mapping = {}
        self.import_batch_id = int(datetime.now().timestamp())
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Title
        title = QLabel("📊 Trial Balance Import with Comparative Year Data")
        title.setStyleSheet("font-size: 16pt; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)
        
        # Info section
        info_label = QLabel(
            "Import Trial Balance from Excel/CSV. Map columns for both Current Year (CY) and Previous Year (PY) "
            "to generate comparative financial statements as per Schedule III requirements."
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #7f8c8d; padding: 10px; background-color: #ecf0f1; border-radius: 5px;")
        layout.addWidget(info_label)
        
        # Splitter for two-column layout
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Import and column mapping
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)
        
        # Import section
        import_group = self.create_import_section()
        left_layout.addWidget(import_group)
        
        # Column mapping section
        mapping_group = self.create_column_mapping_section()
        left_layout.addWidget(mapping_group)
        
        left_layout.addStretch()
        
        # Right panel - Data preview and validation
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)
        
        # Statistics section
        stats_group = self.create_statistics_section()
        right_layout.addWidget(stats_group)
        
        # Data table
        table_group = self.create_data_table_section()
        right_layout.addWidget(table_group)
        
        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        layout.addWidget(splitter)
        
        # Action buttons
        action_layout = self.create_action_buttons()
        layout.addLayout(action_layout)
        
        self.setLayout(layout)
        
        # Load existing data if available
        self.refresh_data()
    
    def create_import_section(self):
        """Create file import section"""
        group = QGroupBox("📁 Import File")
        layout = QVBoxLayout()
        
        # File selection
        file_layout = QHBoxLayout()
        self.file_label = QLabel("No file selected")
        self.file_label.setStyleSheet("padding: 5px; background-color: #ffffff; border: 1px solid #bdc3c7; border-radius: 3px;")
        file_layout.addWidget(self.file_label, 1)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(browse_btn)
        
        layout.addLayout(file_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        group.setLayout(layout)
        return group
    
    def create_column_mapping_section(self):
        """Create column mapping section"""
        group = QGroupBox("🔗 Column Mapping")
        layout = QFormLayout()
        
        # Ledger Name (Required)
        self.ledger_combo = QComboBox()
        self.ledger_combo.addItem("-- Select Column --", None)
        layout.addRow("* Ledger Name:", self.ledger_combo)
        
        # Current Year columns
        cy_label = QLabel("<b>Current Year (CY):</b>")
        layout.addRow(cy_label)
        
        self.opening_cy_combo = QComboBox()
        self.opening_cy_combo.addItem("-- Select Column --", None)
        layout.addRow("  Opening Balance CY:", self.opening_cy_combo)
        
        self.debit_cy_combo = QComboBox()
        self.debit_cy_combo.addItem("-- Select Column --", None)
        layout.addRow("  Debit CY:", self.debit_cy_combo)
        
        self.credit_cy_combo = QComboBox()
        self.credit_cy_combo.addItem("-- Select Column --", None)
        layout.addRow("  Credit CY:", self.credit_cy_combo)
        
        self.closing_cy_combo = QComboBox()
        self.closing_cy_combo.addItem("-- Select Column --", None)
        layout.addRow("  Closing Balance CY:", self.closing_cy_combo)
        
        # Previous Year columns
        py_label = QLabel("<b>Previous Year (PY) - For Comparatives:</b>")
        layout.addRow(py_label)
        
        self.opening_py_combo = QComboBox()
        self.opening_py_combo.addItem("-- Select Column --", None)
        layout.addRow("  Opening Balance PY:", self.opening_py_combo)
        
        self.debit_py_combo = QComboBox()
        self.debit_py_combo.addItem("-- Select Column --", None)
        layout.addRow("  Debit PY:", self.debit_py_combo)
        
        self.credit_py_combo = QComboBox()
        self.credit_py_combo.addItem("-- Select Column --", None)
        layout.addRow("  Credit PY:", self.credit_py_combo)
        
        self.closing_py_combo = QComboBox()
        self.closing_py_combo.addItem("-- Select Column --", None)
        layout.addRow("  Closing Balance PY:", self.closing_py_combo)
        
        # Auto-map button
        auto_map_btn = QPushButton("🔍 Auto-Detect Columns")
        auto_map_btn.clicked.connect(self.auto_map_columns)
        layout.addRow(auto_map_btn)
        
        group.setLayout(layout)
        return group
    
    def create_statistics_section(self):
        """Create statistics section"""
        group = QGroupBox("📊 Trial Balance Statistics")
        layout = QVBoxLayout()
        
        self.stats_text = QTextEdit()
        self.stats_text.setReadOnly(True)
        self.stats_text.setMaximumHeight(150)
        self.stats_text.setStyleSheet("background-color: #f8f9fa; font-family: 'Courier New';")
        layout.addWidget(self.stats_text)
        
        group.setLayout(layout)
        return group
    
    def create_data_table_section(self):
        """Create data preview table"""
        group = QGroupBox("📋 Trial Balance Data Preview")
        layout = QVBoxLayout()
        
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(10)
        self.data_table.setHorizontalHeaderLabels([
            "Ledger Name", "Dr CY", "Cr CY", "Closing CY",
            "Dr PY", "Cr PY", "Closing PY", "Type", "Mapped", "Actions"
        ])
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.data_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.data_table.setAlternatingRowColors(True)
        
        layout.addWidget(self.data_table)
        
        group.setLayout(layout)
        return group
    
    def create_action_buttons(self):
        """Create action buttons"""
        layout = QHBoxLayout()
        
        # Import button
        self.import_btn = QPushButton("📥 Import Trial Balance")
        self.import_btn.setEnabled(False)
        self.import_btn.clicked.connect(self.import_data)
        self.import_btn.setStyleSheet("background-color: #3498db; color: white; padding: 10px 20px; font-weight: bold;")
        layout.addWidget(self.import_btn)
        
        # Validate button
        self.validate_btn = QPushButton("✔ Validate Balance")
        self.validate_btn.clicked.connect(self.validate_balance)
        self.validate_btn.setStyleSheet("padding: 10px 20px;")
        layout.addWidget(self.validate_btn)
        
        # Map button
        self.map_btn = QPushButton("🔗 Map to Master Data")
        self.map_btn.clicked.connect(self.open_mapping_dialog)
        self.map_btn.setStyleSheet("padding: 10px 20px;")
        layout.addWidget(self.map_btn)
        
        # Update Notes Recommendations button
        self.update_notes_btn = QPushButton("📋 Update Note Recommendations")
        self.update_notes_btn.clicked.connect(self.update_note_recommendations)
        self.update_notes_btn.setStyleSheet("background-color: #27ae60; color: white; padding: 10px 20px; font-weight: bold;")
        self.update_notes_btn.setToolTip("Analyze Trial Balance and update Selection Sheet recommendations")
        layout.addWidget(self.update_notes_btn)
        
        # Export unmapped
        self.export_unmapped_btn = QPushButton("📤 Export Unmapped Items")
        self.export_unmapped_btn.clicked.connect(self.export_unmapped)
        self.export_unmapped_btn.setStyleSheet("padding: 10px 20px;")
        layout.addWidget(self.export_unmapped_btn)
        
        # Clear button
        self.clear_btn = QPushButton("🗑 Clear All Data")
        self.clear_btn.clicked.connect(self.clear_all_data)
        self.clear_btn.setStyleSheet("padding: 10px 20px; background-color: #e74c3c; color: white;")
        layout.addWidget(self.clear_btn)
        
        layout.addStretch()
        
        return layout
    
    def browse_file(self):
        """Browse for Excel/CSV file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Trial Balance File", "",
            "Excel Files (*.xlsx *.xls);;CSV Files (*.csv);;All Files (*.*)"
        )
        
        if file_path:
            self.current_file_path = file_path
            self.file_label.setText(os.path.basename(file_path))
            self.load_file_columns()
    
    def load_file_columns(self):
        """Load columns from selected file"""
        try:
            if self.current_file_path.endswith('.csv'):
                df = pd.read_csv(self.current_file_path, nrows=1)
            else:
                df = pd.read_excel(self.current_file_path, nrows=1)
            
            columns = list(df.columns)
            
            # Populate all combo boxes
            for combo in [self.ledger_combo, self.opening_cy_combo, self.debit_cy_combo,
                         self.credit_cy_combo, self.closing_cy_combo, self.opening_py_combo,
                         self.debit_py_combo, self.credit_py_combo, self.closing_py_combo]:
                combo.clear()
                combo.addItem("-- Select Column --", None)
                for col in columns:
                    combo.addItem(col, col)
            
            self.import_btn.setEnabled(True)
            
            # Try auto-mapping
            self.auto_map_columns()
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to read file:\n{str(e)}")
    
    def auto_map_columns(self):
        """Auto-detect and map columns based on common names"""
        if not hasattr(self, 'ledger_combo'):
            return
        
        mapping_rules = {
            'ledger_name': ['ledger', 'account', 'particulars', 'name', 'ledger name', 'account name'],
            'opening_balance_cy': ['opening cy', 'opening balance cy', 'ob cy', 'opening current'],
            'debit_cy': ['debit cy', 'dr cy', 'debit current', 'dr current', 'debit'],
            'credit_cy': ['credit cy', 'cr cy', 'credit current', 'cr current', 'credit'],
            'closing_balance_cy': ['closing cy', 'closing balance cy', 'cb cy', 'closing current', 'balance'],
            'opening_balance_py': ['opening py', 'opening balance py', 'ob py', 'opening previous'],
            'debit_py': ['debit py', 'dr py', 'debit previous', 'dr previous'],
            'credit_py': ['credit py', 'cr py', 'credit previous', 'cr previous'],
            'closing_balance_py': ['closing py', 'closing balance py', 'cb py', 'closing previous']
        }
        
        combos = {
            'ledger_name': self.ledger_combo,
            'opening_balance_cy': self.opening_cy_combo,
            'debit_cy': self.debit_cy_combo,
            'credit_cy': self.credit_cy_combo,
            'closing_balance_cy': self.closing_cy_combo,
            'opening_balance_py': self.opening_py_combo,
            'debit_py': self.debit_py_combo,
            'credit_py': self.credit_py_combo,
            'closing_balance_py': self.closing_py_combo
        }
        
        for field, combo in combos.items():
            rules = mapping_rules.get(field, [])
            for i in range(combo.count()):
                col_name = combo.itemText(i).lower()
                if any(rule in col_name for rule in rules):
                    combo.setCurrentIndex(i)
                    break
    
    def import_data(self):
        """Import trial balance data"""
        if not self.current_file_path:
            QMessageBox.warning(self, "No File", "Please select a file to import")
            return
        
        # Get column mapping
        self.column_mapping = {
            'ledger_name': self.ledger_combo.currentData(),
            'opening_balance_cy': self.opening_cy_combo.currentData(),
            'debit_cy': self.debit_cy_combo.currentData(),
            'credit_cy': self.credit_cy_combo.currentData(),
            'closing_balance_cy': self.closing_cy_combo.currentData(),
            'opening_balance_py': self.opening_py_combo.currentData(),
            'debit_py': self.debit_py_combo.currentData(),
            'credit_py': self.credit_py_combo.currentData(),
            'closing_balance_py': self.closing_py_combo.currentData()
        }
        
        if not self.column_mapping['ledger_name']:
            QMessageBox.warning(self, "Mapping Required", "Please map the 'Ledger Name' column")
            return
        
        # Get company ID
        user_id = self.parent_window.user.user_id if hasattr(self.parent_window, 'user') else 1
        company = CompanyInfo.get_by_user_id(user_id)
        
        if not company:
            QMessageBox.warning(self, "Company Info Required", 
                              "Please set up Company Information first before importing Trial Balance")
            return
        
        # Confirm import
        reply = QMessageBox.question(
            self, "Confirm Import",
            f"Import Trial Balance from:\n{os.path.basename(self.current_file_path)}\n\n"
            f"This will create a new import batch. Continue?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.No:
            return
        
        # Generate new batch ID
        self.import_batch_id = int(datetime.now().timestamp())
        
        # Start import worker thread
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.import_btn.setEnabled(False)
        
        self.worker = ImportWorker(
            self.current_file_path,
            self.column_mapping,
            company.company_id,
            self.import_batch_id
        )
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.import_finished)
        self.worker.start()
    
    def update_progress(self, value):
        """Update progress bar"""
        self.progress_bar.setValue(value)
    
    def import_finished(self, success, message, entries):
        """Handle import completion"""
        self.progress_bar.setVisible(False)
        self.import_btn.setEnabled(True)
        
        if success:
            QMessageBox.information(self, "Import Complete", message)
            self.refresh_data()
        else:
            QMessageBox.critical(self, "Import Failed", message)
    
    def refresh_data(self):
        """Refresh trial balance data display"""
        user_id = self.parent_window.user.user_id if hasattr(self.parent_window, 'user') else 1
        company = CompanyInfo.get_by_user_id(user_id)
        
        if not company:
            self.update_statistics({})
            self.data_table.setRowCount(0)
            return
        
        # Get trial balance data
        tb_entries = TrialBalance.get_by_company(company.company_id)
        
        # Update statistics
        stats = TrialBalance.get_summary_stats(company.company_id)
        self.update_statistics(stats)
        
        # Update table
        self.data_table.setRowCount(len(tb_entries))
        
        for row, entry in enumerate(tb_entries):
            self.data_table.setItem(row, 0, QTableWidgetItem(entry.ledger_name))
            self.data_table.setItem(row, 1, QTableWidgetItem(f"₹{entry.debit_cy:,.2f}"))
            self.data_table.setItem(row, 2, QTableWidgetItem(f"₹{entry.credit_cy:,.2f}"))
            self.data_table.setItem(row, 3, QTableWidgetItem(f"₹{entry.closing_balance_cy:,.2f}"))
            self.data_table.setItem(row, 4, QTableWidgetItem(f"₹{entry.debit_py:,.2f}"))
            self.data_table.setItem(row, 5, QTableWidgetItem(f"₹{entry.credit_py:,.2f}"))
            self.data_table.setItem(row, 6, QTableWidgetItem(f"₹{entry.closing_balance_py:,.2f}"))
            self.data_table.setItem(row, 7, QTableWidgetItem(entry.type_bs_pl))
            
            # Mapped status
            mapped_item = QTableWidgetItem("✓ Mapped" if entry.is_mapped else "✗ Unmapped")
            if entry.is_mapped:
                mapped_item.setForeground(QColor(0, 128, 0))
            else:
                mapped_item.setForeground(QColor(255, 0, 0))
            self.data_table.setItem(row, 8, mapped_item)
    
    def update_statistics(self, stats):
        """Update statistics display"""
        if not stats:
            self.stats_text.setPlainText("No trial balance data imported yet.")
            return
        
        cy_balanced = abs(stats['total_debit_cy'] - stats['total_credit_cy']) < 1
        py_balanced = abs(stats['total_debit_py'] - stats['total_credit_py']) < 1
        
        text = f"""
╔══════════════════════════════════════════════════════════════════╗
║                    TRIAL BALANCE SUMMARY                         ║
╠══════════════════════════════════════════════════════════════════╣
║ Total Entries:      {stats['total_entries']:>6}                               ║
║ Mapped Entries:     {stats['mapped_entries']:>6} ({stats['mapped_entries']/max(stats['total_entries'],1)*100:>5.1f}%)                      ║
║ Unmapped Entries:   {stats['unmapped_entries']:>6}                               ║
╠══════════════════════════════════════════════════════════════════╣
║ CURRENT YEAR (CY)                                                ║
║ Total Debit:     ₹{stats['total_debit_cy']:>15,.2f}                          ║
║ Total Credit:    ₹{stats['total_credit_cy']:>15,.2f}                          ║
║ Difference:      ₹{stats['cy_difference']:>15,.2f}  {'✓ BALANCED' if cy_balanced else '✗ NOT BALANCED'}            ║
╠══════════════════════════════════════════════════════════════════╣
║ PREVIOUS YEAR (PY) - For Comparatives                           ║
║ Total Debit:     ₹{stats['total_debit_py']:>15,.2f}                          ║
║ Total Credit:    ₹{stats['total_credit_py']:>15,.2f}                          ║
║ Difference:      ₹{stats['py_difference']:>15,.2f}  {'✓ BALANCED' if py_balanced else '✗ NOT BALANCED'}            ║
╚══════════════════════════════════════════════════════════════════╝
"""
        self.stats_text.setPlainText(text)
    
    def validate_balance(self):
        """Validate trial balance"""
        user_id = self.parent_window.user.user_id if hasattr(self.parent_window, 'user') else 1
        company = CompanyInfo.get_by_user_id(user_id)
        
        if not company:
            QMessageBox.warning(self, "No Data", "No company information found")
            return
        
        cy_balanced, py_balanced, cy_diff, py_diff = TrialBalance.validate_balance(company.company_id)
        
        message = "TRIAL BALANCE VALIDATION RESULTS:\n\n"
        message += f"CURRENT YEAR (CY):\n"
        message += f"  Status: {'✓ BALANCED' if cy_balanced else '✗ NOT BALANCED'}\n"
        message += f"  Difference: ₹{cy_diff:,.2f}\n\n"
        message += f"PREVIOUS YEAR (PY):\n"
        message += f"  Status: {'✓ BALANCED' if py_balanced else '✗ NOT BALANCED'}\n"
        message += f"  Difference: ₹{py_diff:,.2f}\n\n"
        
        if cy_balanced and py_balanced:
            message += "Both years are balanced and ready for financial statement generation!"
            QMessageBox.information(self, "Validation Success", message)
        else:
            message += "⚠ Please verify your trial balance data before proceeding."
            QMessageBox.warning(self, "Validation Warning", message)
    
    def open_mapping_dialog(self):
        """Open mapping dialog for unmapped items"""
        # Get current company ID
        company_id = self.parent_window.current_company_id if hasattr(self.parent_window, 'current_company_id') else None
        
        if not company_id:
            QMessageBox.warning(
                self, "No Company Selected",
                "Please select a company first before mapping Trial Balance ledgers."
            )
            return
        
        # Open the mapping dialog
        from views.trial_balance_mapping_dialog import TrialBalanceMappingDialog
        dialog = TrialBalanceMappingDialog(company_id, self)
        dialog.mapping_saved.connect(self.refresh_data)
        dialog.exec_()
    
    def export_unmapped(self):
        """Export unmapped items to Excel"""
        user_id = self.parent_window.user.user_id if hasattr(self.parent_window, 'user') else 1
        company = CompanyInfo.get_by_user_id(user_id)
        
        if not company:
            QMessageBox.warning(self, "No Data", "No company information found")
            return
        
        unmapped = TrialBalance.get_unmapped(company.company_id)
        
        if not unmapped:
            QMessageBox.information(self, "All Mapped", "All entries are already mapped!")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Unmapped Items",
            f"unmapped_items_{datetime.now().strftime('%Y%m%d')}.xlsx",
            "Excel Files (*.xlsx)"
        )
        
        if file_path:
            try:
                data = []
                for entry in unmapped:
                    data.append({
                        'Ledger Name': entry.ledger_name,
                        'Debit CY': entry.debit_cy,
                        'Credit CY': entry.credit_cy,
                        'Closing CY': entry.closing_balance_cy,
                        'Debit PY': entry.debit_py,
                        'Credit PY': entry.credit_py,
                        'Closing PY': entry.closing_balance_py,
                        'Type': entry.type_bs_pl
                    })
                
                df = pd.DataFrame(data)
                df.to_excel(file_path, index=False)
                
                QMessageBox.information(self, "Success", f"Exported {len(unmapped)} unmapped items to:\n{file_path}")
            
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Export failed:\n{str(e)}")
    
    def clear_all_data(self):
        """Clear all trial balance data"""
        reply = QMessageBox.question(
            self, "Confirm Delete",
            "Are you sure you want to delete ALL trial balance data?\n\nThis action cannot be undone!",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            user_id = self.parent_window.user.user_id if hasattr(self.parent_window, 'user') else 1
            company = CompanyInfo.get_by_user_id(user_id)
            
            if company:
                TrialBalance.delete_by_company(company.company_id)
                QMessageBox.information(self, "Deleted", "All trial balance data has been deleted")
                self.refresh_data()
    
    def update_note_recommendations(self):
        """Update Selection Sheet note recommendations based on Trial Balance"""
        if not hasattr(self.parent_window, 'user'):
            QMessageBox.warning(self, "No User", "Please log in first")
            return
        
        user_id = self.parent_window.user.user_id
        company = CompanyInfo.get_by_user_id(user_id)
        
        if not company:
            QMessageBox.warning(self, "No Company", "Please create a company first")
            return
        
        company_id = company.company_id
        
        # Check if trial balance has data
        entries = TrialBalance.get_by_company(company_id)
        if not entries:
            QMessageBox.warning(
                self,
                "No Trial Balance Data",
                "Please import Trial Balance data first before updating note recommendations."
            )
            return
        
        try:
            from models.selection_sheet import SelectionSheet
            
            # Initialize notes if not already done
            SelectionSheet.initialize_default_notes(company_id)
            
            # Update system recommendations
            SelectionSheet.update_system_recommendations(company_id)
            
            # Get recommended notes count
            all_notes = SelectionSheet.get_all_for_company(company_id)
            recommended = [n for n in all_notes if n.system_recommendation == 'Yes']
            
            QMessageBox.information(
                self,
                "Note Recommendations Updated",
                f"Selection Sheet updated successfully!\n\n"
                f"System has recommended {len(recommended)} notes based on your Trial Balance.\n\n"
                f"Please go to the Selection Sheet tab to review and adjust the selections."
            )
            
            # Switch to Selection Sheet tab if available
            if hasattr(self.parent_window, 'tab_widget'):
                for i in range(self.parent_window.tab_widget.count()):
                    if 'Selection Sheet' in self.parent_window.tab_widget.tabText(i):
                        self.parent_window.tab_widget.setCurrentIndex(i)
                        break
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to update note recommendations:\n{str(e)}"
            )
