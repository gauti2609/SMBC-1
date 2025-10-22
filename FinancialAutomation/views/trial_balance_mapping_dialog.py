"""Trial Balance Mapping Dialog - Map TB ledgers to Master Data hierarchy"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QTreeWidget, QTreeWidgetItem, QSplitter,
                             QMessageBox, QComboBox, QLineEdit, QGroupBox,
                             QCheckBox, QProgressDialog, QTableWidget,
                             QTableWidgetItem, QHeaderView, QAbstractItemView)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor
from models.master_data import MajorHead, MinorHead, Grouping
from config.database import get_connection

class TrialBalanceMappingDialog(QDialog):
    """Dialog for mapping Trial Balance ledgers to Master Data hierarchy"""
    
    # Signal emitted when mapping is saved
    mapping_saved = pyqtSignal()
    
    def __init__(self, company_id, parent=None):
        super().__init__(parent)
        self.company_id = company_id
        self.unmapped_ledgers = []
        self.master_data_tree = {}  # Cache for master data hierarchy
        self.selected_ledger_ids = []
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("Trial Balance Mapping - Map Ledgers to Master Data")
        self.setGeometry(100, 100, 1400, 800)
        
        main_layout = QVBoxLayout()
        
        # Header
        header = QLabel("Map Trial Balance Ledgers to Chart of Accounts")
        header.setFont(QFont("Bookman Old Style", 14, QFont.Bold))
        header.setStyleSheet("color: #2c3e50; padding: 10px;")
        main_layout.addWidget(header)
        
        # Create splitter for side-by-side layout
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Unmapped TB Ledgers
        left_panel = self.create_ledgers_panel()
        splitter.addWidget(left_panel)
        
        # Right panel - Master Data Hierarchy
        right_panel = self.create_master_data_panel()
        splitter.addWidget(right_panel)
        
        # Set initial sizes (50-50 split)
        splitter.setSizes([700, 700])
        
        main_layout.addWidget(splitter)
        
        # Mapping controls
        mapping_controls = self.create_mapping_controls()
        main_layout.addLayout(mapping_controls)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("💾 Save Mappings")
        save_btn.clicked.connect(self.save_mappings)
        save_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-weight: bold;")
        button_layout.addWidget(save_btn)
        
        clear_all_btn = QPushButton("🗑️ Clear All Mappings")
        clear_all_btn.clicked.connect(self.clear_all_mappings)
        clear_all_btn.setStyleSheet("background-color: #f44336; color: white; padding: 10px;")
        button_layout.addWidget(clear_all_btn)
        
        close_btn = QPushButton("✖ Close")
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        
        main_layout.addLayout(button_layout)
        
        # Status bar
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("padding: 5px; background-color: #f0f0f0;")
        main_layout.addWidget(self.status_label)
        
        self.setLayout(main_layout)
    
    def create_ledgers_panel(self):
        """Create panel showing unmapped TB ledgers"""
        panel = QGroupBox("Trial Balance Ledgers (Unmapped)")
        layout = QVBoxLayout()
        
        # Filter controls
        filter_layout = QHBoxLayout()
        
        filter_label = QLabel("Filter:")
        filter_layout.addWidget(filter_label)
        
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Search ledger names...")
        self.filter_input.textChanged.connect(self.filter_ledgers)
        filter_layout.addWidget(self.filter_input)
        
        self.show_all_check = QCheckBox("Show All (including mapped)")
        self.show_all_check.stateChanged.connect(self.load_ledgers)
        filter_layout.addWidget(self.show_all_check)
        
        layout.addLayout(filter_layout)
        
        # Ledgers table
        self.ledgers_table = QTableWidget()
        self.ledgers_table.setColumnCount(6)
        self.ledgers_table.setHorizontalHeaderLabels([
            "Select", "Ledger Name", "BS/PL", "Closing Bal (CY)", "Current Mapping", "TB ID"
        ])
        self.ledgers_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ledgers_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ledgers_table.verticalHeader().setVisible(False)
        self.ledgers_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.ledgers_table.setColumnWidth(0, 60)
        self.ledgers_table.setColumnWidth(2, 60)
        self.ledgers_table.setColumnWidth(3, 120)
        self.ledgers_table.setColumnWidth(4, 200)
        self.ledgers_table.setColumnHidden(5, True)  # Hide TB ID column
        self.ledgers_table.itemSelectionChanged.connect(self.on_ledger_selection_changed)
        layout.addWidget(self.ledgers_table)
        
        # Quick select buttons
        select_layout = QHBoxLayout()
        select_all_btn = QPushButton("Select All")
        select_all_btn.clicked.connect(self.select_all_ledgers)
        select_layout.addWidget(select_all_btn)
        
        select_none_btn = QPushButton("Select None")
        select_none_btn.clicked.connect(self.select_none_ledgers)
        select_layout.addWidget(select_none_btn)
        
        select_unmapped_btn = QPushButton("Select Unmapped")
        select_unmapped_btn.clicked.connect(self.select_unmapped_ledgers)
        select_layout.addWidget(select_unmapped_btn)
        
        layout.addLayout(select_layout)
        
        panel.setLayout(layout)
        return panel
    
    def create_master_data_panel(self):
        """Create panel showing Master Data hierarchy"""
        panel = QGroupBox("Chart of Accounts - Select Mapping Target")
        layout = QVBoxLayout()
        
        # Search box
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        search_layout.addWidget(search_label)
        
        self.master_search_input = QLineEdit()
        self.master_search_input.setPlaceholderText("Search major/minor/grouping...")
        self.master_search_input.textChanged.connect(self.filter_master_data)
        search_layout.addWidget(self.master_search_input)
        
        layout.addLayout(search_layout)
        
        # Master data tree
        self.master_tree = QTreeWidget()
        self.master_tree.setHeaderLabels(["Name", "Type", "ID"])
        self.master_tree.setColumnWidth(0, 400)
        self.master_tree.setColumnWidth(1, 100)
        self.master_tree.setColumnHidden(2, True)  # Hide ID column
        self.master_tree.itemClicked.connect(self.on_master_item_clicked)
        layout.addWidget(self.master_tree)
        
        # Selected mapping display
        self.selected_mapping_label = QLabel("Selected: None")
        self.selected_mapping_label.setStyleSheet(
            "padding: 10px; background-color: #e3f2fd; "
            "border: 2px solid #2196F3; border-radius: 5px; font-weight: bold;"
        )
        layout.addWidget(self.selected_mapping_label)
        
        panel.setLayout(layout)
        return panel
    
    def create_mapping_controls(self):
        """Create mapping action controls"""
        layout = QHBoxLayout()
        
        map_btn = QPushButton("➡️ Map Selected Ledgers to Highlighted Item")
        map_btn.setMinimumHeight(40)
        map_btn.clicked.connect(self.map_selected_ledgers)
        map_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")
        layout.addWidget(map_btn)
        
        clear_selected_btn = QPushButton("✖ Clear Selected Mappings")
        clear_selected_btn.setMinimumHeight(40)
        clear_selected_btn.clicked.connect(self.clear_selected_mappings)
        layout.addWidget(clear_selected_btn)
        
        return layout
    
    def load_data(self):
        """Load trial balance ledgers and master data"""
        self.load_ledgers()
        self.load_master_data()
    
    def load_ledgers(self):
        """Load trial balance ledgers"""
        self.ledgers_table.setRowCount(0)
        
        if not self.company_id:
            self.update_status("⚠️ No company selected", error=True)
            return
        
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            # Load ledgers (unmapped or all based on checkbox)
            if self.show_all_check.isChecked():
                cursor.execute('''
                    SELECT tb_id, ledger_name, type_bs_pl, closing_balance_cy,
                           major_head_id, minor_head_id, grouping_id, is_mapped
                    FROM trial_balance
                    WHERE company_id = %s
                    ORDER BY ledger_name
                ''', (self.company_id,))
            else:
                cursor.execute('''
                    SELECT tb_id, ledger_name, type_bs_pl, closing_balance_cy,
                           major_head_id, minor_head_id, grouping_id, is_mapped
                    FROM trial_balance
                    WHERE company_id = %s AND is_mapped = 0
                    ORDER BY ledger_name
                ''', (self.company_id,))
            
            ledgers = cursor.fetchall()
            
            for ledger in ledgers:
                tb_id, name, type_bs_pl, closing_cy, major_id, minor_id, grouping_id, is_mapped = ledger
                
                row = self.ledgers_table.rowCount()
                self.ledgers_table.insertRow(row)
                
                # Checkbox
                check_item = QTableWidgetItem()
                check_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                check_item.setCheckState(Qt.Unchecked)
                self.ledgers_table.setItem(row, 0, check_item)
                
                # Ledger name
                name_item = QTableWidgetItem(name)
                if is_mapped:
                    name_item.setBackground(QColor("#c8e6c9"))  # Light green for mapped
                self.ledgers_table.setItem(row, 1, name_item)
                
                # BS/PL
                type_item = QTableWidgetItem(type_bs_pl)
                self.ledgers_table.setItem(row, 2, type_item)
                
                # Closing balance
                balance_item = QTableWidgetItem(f"₹ {closing_cy:,.2f}")
                balance_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.ledgers_table.setItem(row, 3, balance_item)
                
                # Current mapping
                mapping_text = self.get_mapping_text(major_id, minor_id, grouping_id)
                mapping_item = QTableWidgetItem(mapping_text)
                if is_mapped:
                    mapping_item.setForeground(QColor("#2e7d32"))  # Dark green
                else:
                    mapping_item.setForeground(QColor("#d32f2f"))  # Red
                self.ledgers_table.setItem(row, 4, mapping_item)
                
                # TB ID (hidden)
                id_item = QTableWidgetItem(str(tb_id))
                self.ledgers_table.setItem(row, 5, id_item)
            
            total = len(ledgers)
            mapped_count = sum(1 for l in ledgers if l[7] == 1)
            unmapped_count = total - mapped_count
            
            self.update_status(
                f"📊 Loaded {total} ledgers | "
                f"✅ {mapped_count} mapped | "
                f"⚠️ {unmapped_count} unmapped"
            )
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load ledgers:\n{str(e)}")
        finally:
            conn.close()
    
    def get_mapping_text(self, major_id, minor_id, grouping_id):
        """Get readable mapping text"""
        if not major_id:
            return "❌ Not mapped"
        
        parts = []
        
        if major_id:
            major = MajorHead.get_by_id(major_id)
            if major:
                parts.append(major[1])  # major_head_name
        
        if minor_id:
            minor = MinorHead.get_by_id(minor_id)
            if minor:
                parts.append(minor[2])  # minor_head_name
        
        if grouping_id:
            grouping = Grouping.get_by_id(grouping_id)
            if grouping:
                parts.append(grouping[2])  # grouping_name
        
        return " → ".join(parts) if parts else "❌ Not mapped"
    
    def load_master_data(self):
        """Load master data hierarchy into tree"""
        self.master_tree.clear()
        
        if not self.company_id:
            return
        
        try:
            # Load major heads
            majors = MajorHead.get_all_by_company(self.company_id)
            
            for major in majors:
                major_item = QTreeWidgetItem(self.master_tree)
                major_item.setText(0, major.major_head_name)
                major_item.setText(1, "Major")
                major_item.setText(2, f"major_{major.major_head_id}")
                major_item.setForeground(0, QColor("#1976d2"))
                major_item.setFont(0, QFont("Bookman Old Style", 10, QFont.Bold))
                major_item.setData(0, Qt.UserRole, {
                    "type": "major",
                    "major_id": major.major_head_id,
                    "minor_id": None,
                    "grouping_id": None
                })
                
                # Load minor heads
                minors = MinorHead.get_all(company_id=self.company_id, major_head_id=major.major_head_id)
                for minor in minors:
                    minor_id, _, _, minor_name = minor[0], minor[1], minor[2], minor[3]
                    
                    minor_item = QTreeWidgetItem(major_item)
                    minor_item.setText(0, minor_name)
                    minor_item.setText(1, "Minor")
                    minor_item.setText(2, f"minor_{minor_id}")
                    minor_item.setForeground(0, QColor("#388e3c"))
                    minor_item.setFont(0, QFont("Bookman Old Style", 9))
                    minor_item.setData(0, Qt.UserRole, {
                        "type": "minor",
                        "major_id": major.major_head_id,
                        "minor_id": minor_id,
                        "grouping_id": None
                    })
                    
                    # Load groupings
                    groupings = Grouping.get_all(company_id=self.company_id, minor_head_id=minor_id)
                    for grouping in groupings:
                        grouping_id, _, _, grouping_name = grouping[0], grouping[1], grouping[2], grouping[3]
                        
                        grouping_item = QTreeWidgetItem(minor_item)
                        grouping_item.setText(0, grouping_name)
                        grouping_item.setText(1, "Grouping")
                        grouping_item.setText(2, f"grouping_{grouping_id}")
                        grouping_item.setForeground(0, QColor("#7b1fa2"))
                        grouping_item.setData(0, Qt.UserRole, {
                            "type": "grouping",
                            "major_id": major.major_head_id,
                            "minor_id": minor_id,
                            "grouping_id": grouping_id
                        })
            
            self.master_tree.expandAll()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load master data:\n{str(e)}")
    
    def on_master_item_clicked(self, item, column):
        """Handle master data item click"""
        data = item.data(0, Qt.UserRole)
        if not data:
            return
        
        # Build display text
        parts = []
        if data["major_id"]:
            major = MajorHead.get_by_id(data["major_id"])
            if major:
                parts.append(f"Major: {major[1]}")
        
        if data["minor_id"]:
            minor = MinorHead.get_by_id(data["minor_id"])
            if minor:
                parts.append(f"Minor: {minor[2]}")
        
        if data["grouping_id"]:
            grouping = Grouping.get_by_id(data["grouping_id"])
            if grouping:
                parts.append(f"Grouping: {grouping[2]}")
        
        self.selected_mapping_label.setText(f"Selected: {' → '.join(parts)}")
    
    def map_selected_ledgers(self):
        """Map selected ledgers to highlighted master data item"""
        # Get selected master data item
        selected_master = self.master_tree.currentItem()
        if not selected_master:
            QMessageBox.warning(self, "Warning", "Please select a mapping target from Master Data tree!")
            return
        
        mapping_data = selected_master.data(0, Qt.UserRole)
        if not mapping_data:
            return
        
        # Get checked ledgers
        checked_tb_ids = []
        for row in range(self.ledgers_table.rowCount()):
            check_item = self.ledgers_table.item(row, 0)
            if check_item and check_item.checkState() == Qt.Checked:
                tb_id = int(self.ledgers_table.item(row, 5).text())
                checked_tb_ids.append(tb_id)
        
        if not checked_tb_ids:
            QMessageBox.warning(self, "Warning", "Please select at least one ledger to map!")
            return
        
        # Confirm mapping
        reply = QMessageBox.question(
            self, "Confirm Mapping",
            f"Map {len(checked_tb_ids)} ledger(s) to:\n\n{self.selected_mapping_label.text()}\n\nContinue?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.No:
            return
        
        # Perform mapping
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            for tb_id in checked_tb_ids:
                cursor.execute('''
                    UPDATE trial_balance
                    SET major_head_id = %s,
                        minor_head_id = %s,
                        grouping_id = %s,
                        is_mapped = 1,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE tb_id = %s
                ''', (mapping_data["major_id"], mapping_data["minor_id"], 
                      mapping_data["grouping_id"], tb_id))
            
            conn.commit()
            QMessageBox.information(
                self, "Success",
                f"✅ Successfully mapped {len(checked_tb_ids)} ledger(s)!"
            )
            
            # Reload ledgers
            self.load_ledgers()
            
        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Error", f"Failed to map ledgers:\n{str(e)}")
        finally:
            conn.close()
    
    def clear_selected_mappings(self):
        """Clear mappings for selected ledgers"""
        # Get checked ledgers
        checked_tb_ids = []
        for row in range(self.ledgers_table.rowCount()):
            check_item = self.ledgers_table.item(row, 0)
            if check_item and check_item.checkState() == Qt.Checked:
                tb_id = int(self.ledgers_table.item(row, 5).text())
                checked_tb_ids.append(tb_id)
        
        if not checked_tb_ids:
            QMessageBox.warning(self, "Warning", "Please select at least one ledger!")
            return
        
        reply = QMessageBox.question(
            self, "Confirm Clear",
            f"Clear mappings for {len(checked_tb_ids)} ledger(s)?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.No:
            return
        
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            for tb_id in checked_tb_ids:
                cursor.execute('''
                    UPDATE trial_balance
                    SET major_head_id = NULL,
                        minor_head_id = NULL,
                        grouping_id = NULL,
                        is_mapped = 0,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE tb_id = %s
                ''', (tb_id,))
            
            conn.commit()
            QMessageBox.information(self, "Success", f"Cleared {len(checked_tb_ids)} mapping(s)!")
            self.load_ledgers()
            
        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Error", f"Failed to clear mappings:\n{str(e)}")
        finally:
            conn.close()
    
    def clear_all_mappings(self):
        """Clear all mappings for this company"""
        reply = QMessageBox.question(
            self, "Confirm Clear All",
            "Clear ALL mappings for this company?\n\nThis cannot be undone!",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.No:
            return
        
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE trial_balance
                SET major_head_id = NULL,
                    minor_head_id = NULL,
                    grouping_id = NULL,
                    is_mapped = 0,
                    updated_at = CURRENT_TIMESTAMP
                WHERE company_id = %s
            ''', (self.company_id,))
            
            conn.commit()
            QMessageBox.information(self, "Success", "All mappings cleared!")
            self.load_ledgers()
            
        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Error", f"Failed to clear mappings:\n{str(e)}")
        finally:
            conn.close()
    
    def save_mappings(self):
        """Save and close dialog"""
        self.mapping_saved.emit()
        QMessageBox.information(self, "Success", "Mappings saved successfully!")
        self.accept()
    
    def filter_ledgers(self, text):
        """Filter ledgers table by search text"""
        for row in range(self.ledgers_table.rowCount()):
            name_item = self.ledgers_table.item(row, 1)
            if name_item:
                should_show = text.lower() in name_item.text().lower()
                self.ledgers_table.setRowHidden(row, not should_show)
    
    def filter_master_data(self, text):
        """Filter master data tree by search text"""
        def filter_item(item, text):
            item_text = item.text(0).lower()
            matches = text.lower() in item_text
            
            # Check children
            has_matching_child = False
            for i in range(item.childCount()):
                child_matches = filter_item(item.child(i), text)
                has_matching_child = has_matching_child or child_matches
            
            # Show item if it matches or has matching children
            should_show = matches or has_matching_child or not text
            item.setHidden(not should_show)
            
            return should_show
        
        # Filter all top-level items
        for i in range(self.master_tree.topLevelItemCount()):
            filter_item(self.master_tree.topLevelItem(i), text)
    
    def select_all_ledgers(self):
        """Select all visible ledgers"""
        for row in range(self.ledgers_table.rowCount()):
            if not self.ledgers_table.isRowHidden(row):
                check_item = self.ledgers_table.item(row, 0)
                if check_item:
                    check_item.setCheckState(Qt.Checked)
    
    def select_none_ledgers(self):
        """Deselect all ledgers"""
        for row in range(self.ledgers_table.rowCount()):
            check_item = self.ledgers_table.item(row, 0)
            if check_item:
                check_item.setCheckState(Qt.Unchecked)
    
    def select_unmapped_ledgers(self):
        """Select only unmapped ledgers"""
        for row in range(self.ledgers_table.rowCount()):
            mapping_item = self.ledgers_table.item(row, 4)
            check_item = self.ledgers_table.item(row, 0)
            if check_item and mapping_item:
                is_unmapped = "Not mapped" in mapping_item.text()
                check_item.setCheckState(Qt.Checked if is_unmapped else Qt.Unchecked)
    
    def on_ledger_selection_changed(self):
        """Handle ledger selection change"""
        selected_count = sum(
            1 for row in range(self.ledgers_table.rowCount())
            if self.ledgers_table.item(row, 0) and 
            self.ledgers_table.item(row, 0).checkState() == Qt.Checked
        )
        if selected_count > 0:
            self.update_status(f"📌 {selected_count} ledger(s) selected for mapping")
    
    def update_status(self, message, error=False):
        """Update status label"""
        self.status_label.setText(message)
        if error:
            self.status_label.setStyleSheet("padding: 5px; background-color: #ffcdd2; color: #c62828;")
        else:
            self.status_label.setStyleSheet("padding: 5px; background-color: #c8e6c9; color: #2e7d32;")
