"""Input Forms Tab - Schedule III Data Entry"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTabWidget)
from PyQt5.QtGui import QFont
from views.ppe_input_form import PPEInputForm
from views.cwip_input_form import CWIPInputForm
from views.investments_input_form import InvestmentsInputForm

class InputFormsTab(QWidget):
    """Input Forms Tab with sub-tabs for different schedules"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("📋 Schedule III Input Forms")
        header.setFont(QFont("Bookman Old Style", 14, QFont.Bold))
        header.setStyleSheet("color: #2c3e50; padding: 10px;")
        layout.addWidget(header)
        
        # Create sub-tabs for different input forms
        self.tabs = QTabWidget()
        
        # PPE Form (Note 1)
        self.ppe_form = PPEInputForm(self.parent_window)
        self.tabs.addTab(self.ppe_form, "🏭 PPE (Note 1)")
        
        # CWIP Form (Note 2)
        self.cwip_form = CWIPInputForm(self.parent_window)
        self.tabs.addTab(self.cwip_form, "🚧 CWIP (Note 2)")
        
        # Investments Form (Notes 3, 4, 13, 14)
        self.investments_form = InvestmentsInputForm(self.parent_window)
        self.tabs.addTab(self.investments_form, "💰 Investments (Notes 3, 4, 13, 14)")
        
        layout.addWidget(self.tabs)
        self.setLayout(layout)
