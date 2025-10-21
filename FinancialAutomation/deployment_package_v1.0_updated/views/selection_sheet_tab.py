"""
Selection Sheet Tab - Note Selection and Auto-Numbering
Allows users to select which notes should be included in financial statements
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QTableWidget, QTableWidgetItem, QHeaderView, QLabel,
                            QMessageBox, QComboBox, QAbstractItemView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont


class SelectionSheetTab(QWidget):
    """Selection Sheet Tab for note selection"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.company_id = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        
        # Title
        title_label = QLabel("📋 Selection Sheet - Notes to Accounts")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # Instructions
        instructions = QLabel(
            "Select which notes should be included in your financial statements.\n"
            "• System Recommendation: Based on Trial Balance data analysis\n"
            "• User Selection: Override system recommendation (Yes/No/Blank for auto)\n"
            "• Final Selection: Actual notes that will be generated\n"
            "• Auto-Number: Sequential numbering for selected notes"
        )
        instructions.setStyleSheet("color: #666; padding: 10px; background-color: #f0f0f0; border-radius: 5px;")
        layout.addWidget(instructions)
        
        # Buttons row
        button_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton("🔄 Update Recommendations")
        self.refresh_btn.clicked.connect(self.update_recommendations)
        self.refresh_btn.setToolTip("Analyze Trial Balance and update system recommendations")
        button_layout.addWidget(self.refresh_btn)
        
        self.select_all_btn = QPushButton("✓ Select All Recommended")
        self.select_all_btn.clicked.connect(self.select_all_recommended)
        self.select_all_btn.setToolTip("Set User Selection = Yes for all system recommendations")
        button_layout.addWidget(self.select_all_btn)
        
        self.clear_all_btn = QPushButton("✗ Clear All Selections")
        self.clear_all_btn.clicked.connect(self.clear_all_selections)
        self.clear_all_btn.setToolTip("Clear all user selections")
        button_layout.addWidget(self.clear_all_btn)
        
        self.save_btn = QPushButton("💾 Save Selections")
        self.save_btn.clicked.connect(self.save_selections)
        self.save_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        button_layout.addWidget(self.save_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            'Note Ref', 'Note Description', 'Linked Major Head',
            'System Rec.', 'User Selection', 'Final', 'Auto-Number'
        ])
        
        # Table properties
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(2, 200)
        self.table.setColumnWidth(3, 100)
        self.table.setColumnWidth(4, 120)
        self.table.setColumnWidth(5, 80)
        self.table.setColumnWidth(6, 100)
        
        layout.addWidget(self.table)
        
        # Status bar
        self.status_label = QLabel("Ready. Select a company to load selection sheet.")
        self.status_label.setStyleSheet("color: #666; font-style: italic;")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
    
    def set_company(self, company_id: int):
        """Set the active company"""
        self.company_id = company_id
        self.load_selection_sheet()
    
    def load_selection_sheet(self):
        """Load selection sheet data"""
        if not self.company_id:
            self.status_label.setText("No company selected.")
            return
        
        try:
            from models.selection_sheet import SelectionSheet
            
            # Initialize if needed
            SelectionSheet.initialize_default_notes(self.company_id)
            
            # Load all entries
            entries = SelectionSheet.get_all_for_company(self.company_id)
            
            # Populate table
            self.table.setRowCount(len(entries))
            self.table.setUpdatesEnabled(False)
            
            for row, entry in enumerate(entries):
                # Note Ref
                ref_item = QTableWidgetItem(entry.note_ref)
                ref_item.setData(Qt.UserRole, entry.selection_id)  # Store ID
                if '.' not in entry.note_ref:  # Section header
                    font = ref_item.font()
                    font.setBold(True)
                    ref_item.setFont(font)
                    ref_item.setBackground(QColor("#E7E6E6"))
                ref_item.setFlags(ref_item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row, 0, ref_item)
                
                # Description
                desc_item = QTableWidgetItem(entry.note_description)
                if '.' not in entry.note_ref:
                    font = desc_item.font()
                    font.setBold(True)
                    desc_item.setFont(font)
                    desc_item.setBackground(QColor("#E7E6E6"))
                desc_item.setFlags(desc_item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row, 1, desc_item)
                
                # Linked Major Head
                major_head_item = QTableWidgetItem(entry.linked_major_head or '')
                major_head_item.setFlags(major_head_item.flags() & ~Qt.ItemIsEditable)
                major_head_item.setForeground(QColor("#666"))
                self.table.setItem(row, 2, major_head_item)
                
                # System Recommendation
                sys_rec_item = QTableWidgetItem(entry.system_recommendation)
                sys_rec_item.setFlags(sys_rec_item.flags() & ~Qt.ItemIsEditable)
                sys_rec_item.setTextAlignment(Qt.AlignCenter)
                if entry.system_recommendation == 'Yes':
                    sys_rec_item.setBackground(QColor("#D4EDDA"))
                    sys_rec_item.setForeground(QColor("#155724"))
                self.table.setItem(row, 3, sys_rec_item)
                
                # User Selection - Dropdown
                user_sel_combo = QComboBox()
                user_sel_combo.addItems(['', 'Yes', 'No'])
                user_sel_combo.setCurrentText(entry.user_selection)
                user_sel_combo.currentTextChanged.connect(
                    lambda text, r=row: self.on_user_selection_changed(r, text)
                )
                if '.' not in entry.note_ref:  # Disable for section headers
                    user_sel_combo.setEnabled(False)
                self.table.setCellWidget(row, 4, user_sel_combo)
                
                # Final Selection
                final_item = QTableWidgetItem(entry.final_selection)
                final_item.setFlags(final_item.flags() & ~Qt.ItemIsEditable)
                final_item.setTextAlignment(Qt.AlignCenter)
                if entry.final_selection == 'Yes':
                    final_item.setBackground(QColor("#FFD966"))
                    final_item.setForeground(QColor("#000"))
                    font = final_item.font()
                    font.setBold(True)
                    final_item.setFont(font)
                self.table.setItem(row, 5, final_item)
                
                # Auto-Number
                auto_num_item = QTableWidgetItem(entry.auto_number or '')
                auto_num_item.setFlags(auto_num_item.flags() & ~Qt.ItemIsEditable)
                auto_num_item.setTextAlignment(Qt.AlignCenter)
                if entry.auto_number:
                    font = auto_num_item.font()
                    font.setBold(True)
                    auto_num_item.setFont(font)
                    auto_num_item.setBackground(QColor("#4CAF50"))
                    auto_num_item.setForeground(QColor("white"))
                self.table.setItem(row, 6, auto_num_item)
            
            self.table.setUpdatesEnabled(True)
            
            # Update status
            selected_count = sum(1 for e in entries if e.final_selection == 'Yes' and '.' in e.note_ref)
            self.status_label.setText(
                f"Loaded {len(entries)} notes. {selected_count} notes selected for generation."
            )
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load selection sheet:\n{str(e)}")
    
    def on_user_selection_changed(self, row: int, text: str):
        """Handle user selection change"""
        # Update the visual feedback immediately
        selection_id = self.table.item(row, 0).data(Qt.UserRole)
        
        # Update final selection logic
        sys_rec = self.table.item(row, 3).text()
        if text == 'Yes':
            final = 'Yes'
        elif text == 'No':
            final = 'No'
        elif text == '' and sys_rec == 'Yes':
            final = 'Yes'
        else:
            final = 'No'
        
        # Update Final column
        final_item = self.table.item(row, 5)
        final_item.setText(final)
        if final == 'Yes':
            final_item.setBackground(QColor("#FFD966"))
            final_item.setForeground(QColor("#000"))
            font = final_item.font()
            font.setBold(True)
            final_item.setFont(font)
        else:
            final_item.setBackground(QColor("white"))
            final_item.setForeground(QColor("#000"))
            font = final_item.font()
            font.setBold(False)
            final_item.setFont(font)
    
    def update_recommendations(self):
        """Update system recommendations based on Trial Balance"""
        if not self.company_id:
            QMessageBox.warning(self, "No Company", "Please select a company first.")
            return
        
        try:
            from models.selection_sheet import SelectionSheet
            
            QMessageBox.information(
                self,
                "Updating...",
                "Analyzing Trial Balance to update recommendations..."
            )
            
            SelectionSheet.update_system_recommendations(self.company_id)
            
            # Reload table
            self.load_selection_sheet()
            
            QMessageBox.information(
                self,
                "Success",
                "System recommendations updated based on Trial Balance data."
            )
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update recommendations:\n{str(e)}")
    
    def select_all_recommended(self):
        """Select all system recommended notes"""
        if not self.company_id:
            QMessageBox.warning(self, "No Company", "Please select a company first.")
            return
        
        count = 0
        for row in range(self.table.rowCount()):
            sys_rec = self.table.item(row, 3).text()
            if sys_rec == 'Yes':
                combo = self.table.cellWidget(row, 4)
                if combo and combo.isEnabled():
                    combo.setCurrentText('Yes')
                    count += 1
        
        self.status_label.setText(f"Selected {count} recommended notes.")
    
    def clear_all_selections(self):
        """Clear all user selections"""
        if not self.company_id:
            QMessageBox.warning(self, "No Company", "Please select a company first.")
            return
        
        reply = QMessageBox.question(
            self,
            "Confirm Clear",
            "Are you sure you want to clear all user selections?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            for row in range(self.table.rowCount()):
                combo = self.table.cellWidget(row, 4)
                if combo and combo.isEnabled():
                    combo.setCurrentText('')
            
            self.status_label.setText("All user selections cleared.")
    
    def save_selections(self):
        """Save all selections to database"""
        if not self.company_id:
            QMessageBox.warning(self, "No Company", "Please select a company first.")
            return
        
        try:
            from models.selection_sheet import SelectionSheet
            
            # Collect all user selections
            selections = {}
            for row in range(self.table.rowCount()):
                selection_id = self.table.item(row, 0).data(Qt.UserRole)
                combo = self.table.cellWidget(row, 4)
                if combo:
                    user_selection = combo.currentText()
                    selections[selection_id] = user_selection
            
            # Bulk update
            SelectionSheet.bulk_update_user_selections(self.company_id, selections)
            
            # Reload to show updated auto-numbers
            self.load_selection_sheet()
            
            QMessageBox.information(
                self,
                "Success",
                "Selections saved successfully!\n\n"
                "Auto-numbering has been updated for selected notes."
            )
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save selections:\n{str(e)}")

