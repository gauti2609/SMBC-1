"""Financials Tab - Financial Statements Display"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QTabWidget, QTextEdit, QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from models.financial_statements import (BalanceSheetGenerator, ProfitLossGenerator, 
                                        NotesGenerator, CashFlowGenerator)
import traceback


class FinancialsTab(QWidget):
    """Financials Tab - Display generated financial statements"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.company_id = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("📊 Financial Statements - Schedule III")
        header.setFont(QFont("Bookman Old Style", 14, QFont.Bold))
        header.setStyleSheet("color: #2c3e50; padding: 10px;")
        layout.addWidget(header)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.generate_btn = QPushButton("🔄 Generate/Refresh Statements")
        self.generate_btn.clicked.connect(self.generate_statements)
        self.generate_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; padding: 8px;")
        
        self.export_btn = QPushButton("📤 Export to Excel")
        self.export_btn.clicked.connect(self.export_excel)
        
        btn_layout.addWidget(self.generate_btn)
        btn_layout.addWidget(self.export_btn)
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
        
        # Tabs
        self.tabs = QTabWidget()
        
        # Balance Sheet Tab
        self.bs_widget = QTextEdit()
        self.bs_widget.setReadOnly(True)
        self.bs_widget.setFont(QFont("Courier New", 10))
        self.tabs.addTab(self.bs_widget, "📄 Balance Sheet")
        
        # P&L Tab
        self.pl_widget = QTextEdit()
        self.pl_widget.setReadOnly(True)
        self.pl_widget.setFont(QFont("Courier New", 10))
        self.tabs.addTab(self.pl_widget, "💰 Profit & Loss")
        
        # Cash Flow Tab
        self.cf_widget = QTextEdit()
        self.cf_widget.setReadOnly(True)
        self.cf_widget.setFont(QFont("Courier New", 10))
        self.tabs.addTab(self.cf_widget, "💵 Cash Flow")
        
        # Notes Tab
        self.notes_widget = QTextEdit()
        self.notes_widget.setReadOnly(True)
        self.notes_widget.setFont(QFont("Courier New", 10))
        self.tabs.addTab(self.notes_widget, "📋 Notes to Accounts")
        
        layout.addWidget(self.tabs)
        
        self.setLayout(layout)
    
    def set_company(self, company_id: int):
        """Set the company"""
        self.company_id = company_id
        # Auto-generate when company is set
        self.generate_statements()
    
    def generate_all(self):
        """Generate all financials - called from parent"""
        self.generate_statements()
    
    def generate_statements(self):
        """Generate financial statements"""
        if not self.company_id:
            QMessageBox.warning(self, "Warning", "No company selected.")
            return
        
        try:
            # Generate Balance Sheet
            bs_gen = BalanceSheetGenerator(self.company_id)
            bs_data = bs_gen.generate()
            self.display_balance_sheet(bs_data)
            
            # Generate P&L
            pl_gen = ProfitLossGenerator(self.company_id)
            pl_data = pl_gen.generate()
            self.display_profit_loss(pl_data)
            
            # Generate Cash Flow
            cf_gen = CashFlowGenerator(self.company_id)
            cf_data = cf_gen.generate()
            self.display_cash_flow(cf_data)
            
            # Generate Notes
            notes_gen = NotesGenerator(self.company_id)
            notes_data = notes_gen.generate_all_notes()
            self.display_notes(notes_data)
            
            QMessageBox.information(self, "Success", "Financial statements generated successfully!\n\nAll Schedule III notes (1-27) have been generated.")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate statements:\n{str(e)}\n{traceback.format_exc()}")
    
    def display_balance_sheet(self, data: dict):
        """Display Balance Sheet"""
        html = f"""
        <h2 style='text-align: center;'>{data['company_name']}</h2>
        <h3 style='text-align: center;'>BALANCE SHEET AS AT {data['fy_end']}</h3>
        <h4 style='text-align: center;'>As per Schedule III of Companies Act, 2013</h4>
        <p style='text-align: center;'>(Amount in ₹)</p>
        
        <table border='1' cellpadding='5' cellspacing='0' width='100%'>
        <tr style='background-color: #2196F3; color: white; font-weight: bold;'>
            <th width='10%'>Note</th>
            <th width='50%'>Particulars</th>
            <th width='20%'>Current Year</th>
            <th width='20%'>Previous Year</th>
        </tr>
        
        <tr style='background-color: #E3F2FD;'>
            <td colspan='4'><b>I. ASSETS</b></td>
        </tr>
        <tr style='background-color: #BBDEFB;'>
            <td colspan='4'><b>(1) Non-Current Assets</b></td>
        </tr>
        <tr>
            <td>1</td>
            <td>Property, Plant and Equipment</td>
            <td align='right'>{data['assets']['non_current']['ppe']['cy']:,.2f}</td>
            <td align='right'>{data['assets']['non_current']['ppe']['py']:,.2f}</td>
        </tr>
        <tr>
            <td>2</td>
            <td>Capital Work-in-Progress</td>
            <td align='right'>{data['assets']['non_current']['cwip']['cy']:,.2f}</td>
            <td align='right'>{data['assets']['non_current']['cwip']['py']:,.2f}</td>
        </tr>
        <tr>
            <td>3</td>
            <td>Financial Assets - Investments</td>
            <td align='right'>{data['assets']['non_current']['investments']['cy']:,.2f}</td>
            <td align='right'>{data['assets']['non_current']['investments']['py']:,.2f}</td>
        </tr>
        <tr style='font-weight: bold; background-color: #E8EAF6;'>
            <td></td>
            <td>Total Non-Current Assets</td>
            <td align='right'>{data['assets']['non_current']['total_cy']:,.2f}</td>
            <td align='right'>{data['assets']['non_current']['total_py']:,.2f}</td>
        </tr>
        
        <tr style='background-color: #BBDEFB;'>
            <td colspan='4'><b>(2) Current Assets</b></td>
        </tr>
        <tr>
            <td>8</td>
            <td>Inventories</td>
            <td align='right'>{data['assets']['current']['inventories']['cy']:,.2f}</td>
            <td align='right'>{data['assets']['current']['inventories']['py']:,.2f}</td>
        </tr>
        <tr>
            <td>9</td>
            <td>Financial Assets - Investments</td>
            <td align='right'>{data['assets']['current']['investments']['cy']:,.2f}</td>
            <td align='right'>{data['assets']['current']['investments']['py']:,.2f}</td>
        </tr>
        <tr>
            <td>10</td>
            <td>Trade Receivables</td>
            <td align='right'>{data['assets']['current']['trade_receivables']['cy']:,.2f}</td>
            <td align='right'>{data['assets']['current']['trade_receivables']['py']:,.2f}</td>
        </tr>
        <tr>
            <td>11</td>
            <td>Cash and Cash Equivalents</td>
            <td align='right'>{data['assets']['current']['cash_and_bank']['cy']:,.2f}</td>
            <td align='right'>{data['assets']['current']['cash_and_bank']['py']:,.2f}</td>
        </tr>
        <tr style='font-weight: bold; background-color: #E8EAF6;'>
            <td></td>
            <td>Total Current Assets</td>
            <td align='right'>{data['assets']['current']['total_cy']:,.2f}</td>
            <td align='right'>{data['assets']['current']['total_py']:,.2f}</td>
        </tr>
        
        <tr style='font-weight: bold; background-color: #4CAF50; color: white;'>
            <td></td>
            <td>TOTAL ASSETS</td>
            <td align='right'>{data['assets']['total_cy']:,.2f}</td>
            <td align='right'>{data['assets']['total_py']:,.2f}</td>
        </tr>
        
        <tr style='background-color: #E3F2FD;'>
            <td colspan='4'><b>II. EQUITY AND LIABILITIES</b></td>
        </tr>
        <tr style='background-color: #BBDEFB;'>
            <td colspan='4'><b>(1) Equity</b></td>
        </tr>
        <tr style='font-weight: bold; background-color: #E8EAF6;'>
            <td></td>
            <td>Total Equity</td>
            <td align='right'>{data['equity_and_liabilities']['equity']['total_cy']:,.2f}</td>
            <td align='right'>{data['equity_and_liabilities']['equity']['total_py']:,.2f}</td>
        </tr>
        
        <tr style='background-color: #BBDEFB;'>
            <td colspan='4'><b>(2) Non-Current Liabilities</b></td>
        </tr>
        <tr style='font-weight: bold; background-color: #E8EAF6;'>
            <td></td>
            <td>Total Non-Current Liabilities</td>
            <td align='right'>{data['equity_and_liabilities']['non_current_liabilities']['total_cy']:,.2f}</td>
            <td align='right'>{data['equity_and_liabilities']['non_current_liabilities']['total_py']:,.2f}</td>
        </tr>
        
        <tr style='background-color: #BBDEFB;'>
            <td colspan='4'><b>(3) Current Liabilities</b></td>
        </tr>
        <tr>
            <td>24</td>
            <td>Trade Payables</td>
            <td align='right'>{data['equity_and_liabilities']['current_liabilities']['trade_payables']['cy']:,.2f}</td>
            <td align='right'>{data['equity_and_liabilities']['current_liabilities']['trade_payables']['py']:,.2f}</td>
        </tr>
        <tr style='font-weight: bold; background-color: #E8EAF6;'>
            <td></td>
            <td>Total Current Liabilities</td>
            <td align='right'>{data['equity_and_liabilities']['current_liabilities']['total_cy']:,.2f}</td>
            <td align='right'>{data['equity_and_liabilities']['current_liabilities']['total_py']:,.2f}</td>
        </tr>
        
        <tr style='font-weight: bold; background-color: #4CAF50; color: white;'>
            <td></td>
            <td>TOTAL EQUITY AND LIABILITIES</td>
            <td align='right'>{data['equity_and_liabilities']['total_cy']:,.2f}</td>
            <td align='right'>{data['equity_and_liabilities']['total_py']:,.2f}</td>
        </tr>
        </table>
        """
        
        self.bs_widget.setHtml(html)
    
    def display_profit_loss(self, data: dict):
        """Display Profit & Loss Statement"""
        html = f"""
        <h2 style='text-align: center;'>{data['company_name']}</h2>
        <h3 style='text-align: center;'>STATEMENT OF PROFIT AND LOSS</h3>
        <h4 style='text-align: center;'>FOR THE YEAR ENDED {data['fy_end']}</h4>
        <h4 style='text-align: center;'>As per Schedule III of Companies Act, 2013</h4>
        <p style='text-align: center;'>(Amount in ₹)</p>
        
        <table border='1' cellpadding='5' cellspacing='0' width='100%'>
        <tr style='background-color: #2196F3; color: white; font-weight: bold;'>
            <th width='60%'>Particulars</th>
            <th width='20%'>Current Year</th>
            <th width='20%'>Previous Year</th>
        </tr>
        
        <tr>
            <td><b>I. Revenue from Operations</b></td>
            <td align='right'>{data['revenue']['cy']:,.2f}</td>
            <td align='right'>{data['revenue']['py']:,.2f}</td>
        </tr>
        <tr>
            <td><b>II. Other Income</b></td>
            <td align='right'>{data['other_income']['cy']:,.2f}</td>
            <td align='right'>{data['other_income']['py']:,.2f}</td>
        </tr>
        <tr style='font-weight: bold; background-color: #E3F2FD;'>
            <td><b>III. Total Income (I + II)</b></td>
            <td align='right'>{data['total_income_cy']:,.2f}</td>
            <td align='right'>{data['total_income_py']:,.2f}</td>
        </tr>
        
        <tr>
            <td><b>IV. Expenses:</b></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td style='padding-left: 20px;'>Employee Benefits Expense</td>
            <td align='right'>{data['expenses']['employee_benefits']['cy']:,.2f}</td>
            <td align='right'>{data['expenses']['employee_benefits']['py']:,.2f}</td>
        </tr>
        <tr>
            <td style='padding-left: 20px;'>Finance Costs</td>
            <td align='right'>{data['expenses']['finance_costs']['cy']:,.2f}</td>
            <td align='right'>{data['expenses']['finance_costs']['py']:,.2f}</td>
        </tr>
        <tr>
            <td style='padding-left: 20px;'>Depreciation and Amortisation</td>
            <td align='right'>{data['expenses']['depreciation']['cy']:,.2f}</td>
            <td align='right'>{data['expenses']['depreciation']['py']:,.2f}</td>
        </tr>
        <tr>
            <td style='padding-left: 20px;'>Other Expenses</td>
            <td align='right'>{data['expenses']['other_expenses']['cy']:,.2f}</td>
            <td align='right'>{data['expenses']['other_expenses']['py']:,.2f}</td>
        </tr>
        <tr style='font-weight: bold; background-color: #FFE0B2;'>
            <td><b>Total Expenses (IV)</b></td>
            <td align='right'>{data['total_expenses_cy']:,.2f}</td>
            <td align='right'>{data['total_expenses_py']:,.2f}</td>
        </tr>
        
        <tr style='font-weight: bold; background-color: #FFF9C4;'>
            <td><b>V. Profit/(Loss) before Tax (III - IV)</b></td>
            <td align='right'>{data['profit_before_tax_cy']:,.2f}</td>
            <td align='right'>{data['profit_before_tax_py']:,.2f}</td>
        </tr>
        
        <tr>
            <td><b>VI. Tax Expense (Estimated @ 25%)</b></td>
            <td align='right'>{data['tax_cy']:,.2f}</td>
            <td align='right'>{data['tax_py']:,.2f}</td>
        </tr>
        
        <tr style='font-weight: bold; background-color: #4CAF50; color: white; font-size: 14pt;'>
            <td><b>VII. Profit/(Loss) for the Period (V - VI)</b></td>
            <td align='right'>{data['profit_after_tax_cy']:,.2f}</td>
            <td align='right'>{data['profit_after_tax_py']:,.2f}</td>
        </tr>
        </table>
        """
        
        self.pl_widget.setHtml(html)
    
    def display_cash_flow(self, data: dict):
        """Display Cash Flow Statement"""
        # Extract nested data
        operating = data['operating_activities']
        investing = data['investing_activities']
        financing = data['financing_activities']
        
        html = f"""
        <style>
            table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #4CAF50; color: white; }}
            .section-header {{ background-color: #2196F3; color: white; font-weight: bold; }}
            .subtotal {{ background-color: #f0f0f0; font-weight: bold; }}
            .total {{ background-color: #FFD700; font-weight: bold; }}
            .right {{ text-align: right; }}
        </style>
        
        <h2 style='text-align: center;'>{data['company_name']}</h2>
        <h3 style='text-align: center;'>CASH FLOW STATEMENT FOR THE YEAR ENDED {data['fy_end']}</h3>
        <h4 style='text-align: center;'>(Indirect Method - Amount in ₹)</h4>
        
        <table>
            <tr>
                <th>Particulars</th>
                <th class='right'>Current Year</th>
                <th class='right'>Previous Year</th>
            </tr>
            
            <!-- Operating Activities -->
            <tr class='section-header'>
                <td colspan='3'>A. CASH FLOW FROM OPERATING ACTIVITIES</td>
            </tr>
            <tr>
                <td>Profit Before Tax</td>
                <td class='right'>{operating['profit_before_tax_cy']:,.2f}</td>
                <td class='right'>{operating['profit_before_tax_py']:,.2f}</td>
            </tr>
            <tr>
                <td colspan='3' style='font-weight: bold;'>Adjustments for:</td>
            </tr>
            <tr>
                <td style='padding-left: 20px;'>Depreciation and Amortization</td>
                <td class='right'>{operating['adjustments']['depreciation']['cy']:,.2f}</td>
                <td class='right'>{operating['adjustments']['depreciation']['py']:,.2f}</td>
            </tr>
            <tr>
                <td style='padding-left: 20px;'>Interest Expense</td>
                <td class='right'>{operating['adjustments']['interest_expense']['cy']:,.2f}</td>
                <td class='right'>{operating['adjustments']['interest_expense']['py']:,.2f}</td>
            </tr>
            <tr class='subtotal'>
                <td>Operating Profit Before Working Capital Changes</td>
                <td class='right'>{operating['operating_profit_cy']:,.2f}</td>
                <td class='right'>{operating['operating_profit_py']:,.2f}</td>
            </tr>
            <tr>
                <td colspan='3' style='font-weight: bold;'>Changes in Working Capital:</td>
            </tr>
            <tr>
                <td style='padding-left: 20px;'>(Increase)/Decrease in Current Assets</td>
                <td class='right'>{operating['working_capital_changes']['current_assets']['cy']:,.2f}</td>
                <td class='right'>{operating['working_capital_changes']['current_assets']['py']:,.2f}</td>
            </tr>
            <tr>
                <td style='padding-left: 20px;'>Increase/(Decrease) in Current Liabilities</td>
                <td class='right'>{operating['working_capital_changes']['current_liabilities']['cy']:,.2f}</td>
                <td class='right'>{operating['working_capital_changes']['current_liabilities']['py']:,.2f}</td>
            </tr>
            <tr class='subtotal'>
                <td>Cash Generated from Operations</td>
                <td class='right'>{operating['cash_from_operations_cy']:,.2f}</td>
                <td class='right'>{operating['cash_from_operations_py']:,.2f}</td>
            </tr>
            <tr>
                <td style='padding-left: 20px;'>Less: Direct Taxes Paid</td>
                <td class='right'>{operating['taxes_paid_cy']:,.2f}</td>
                <td class='right'>{operating['taxes_paid_py']:,.2f}</td>
            </tr>
            <tr>
                <td style='padding-left: 20px;'>Less: Interest Paid</td>
                <td class='right'>{operating['interest_paid_cy']:,.2f}</td>
                <td class='right'>{operating['interest_paid_py']:,.2f}</td>
            </tr>
            <tr class='total'>
                <td>Net Cash from Operating Activities (A)</td>
                <td class='right'>{operating['net_cash_cy']:,.2f}</td>
                <td class='right'>{operating['net_cash_py']:,.2f}</td>
            </tr>
            
            <!-- Investing Activities -->
            <tr class='section-header'>
                <td colspan='3'>B. CASH FLOW FROM INVESTING ACTIVITIES</td>
            </tr>
            <tr>
                <td>Purchase of Property, Plant and Equipment</td>
                <td class='right'>{investing['ppe_investment_cy']:,.2f}</td>
                <td class='right'>{investing['ppe_investment_py']:,.2f}</td>
            </tr>
            <tr>
                <td>Capital Work in Progress Expenditure</td>
                <td class='right'>{investing['cwip_investment_cy']:,.2f}</td>
                <td class='right'>{investing['cwip_investment_py']:,.2f}</td>
            </tr>
            <tr>
                <td>Purchase/(Sale) of Investments</td>
                <td class='right'>{investing['investments_net_cy']:,.2f}</td>
                <td class='right'>{investing['investments_net_py']:,.2f}</td>
            </tr>
            <tr class='total'>
                <td>Net Cash used in Investing Activities (B)</td>
                <td class='right'>{investing['net_cash_cy']:,.2f}</td>
                <td class='right'>{investing['net_cash_py']:,.2f}</td>
            </tr>
            
            <!-- Financing Activities -->
            <tr class='section-header'>
                <td colspan='3'>C. CASH FLOW FROM FINANCING ACTIVITIES</td>
            </tr>
            <tr>
                <td>Proceeds from Issue of Equity Shares</td>
                <td class='right'>{financing['equity_proceeds_cy']:,.2f}</td>
                <td class='right'>{financing['equity_proceeds_py']:,.2f}</td>
            </tr>
            <tr>
                <td>Proceeds from/(Repayment of) Borrowings</td>
                <td class='right'>{financing['borrowings_net_cy']:,.2f}</td>
                <td class='right'>{financing['borrowings_net_py']:,.2f}</td>
            </tr>
            <tr>
                <td>Dividends Paid</td>
                <td class='right'>{financing['dividends_paid_cy']:,.2f}</td>
                <td class='right'>{financing['dividends_paid_py']:,.2f}</td>
            </tr>
            <tr class='total'>
                <td>Net Cash from Financing Activities (C)</td>
                <td class='right'>{financing['net_cash_cy']:,.2f}</td>
                <td class='right'>{financing['net_cash_py']:,.2f}</td>
            </tr>
            
            <!-- Summary -->
            <tr style='background-color: #FF6347; color: white; font-weight: bold;'>
                <td>Net Increase/(Decrease) in Cash and Cash Equivalents (A+B+C)</td>
                <td class='right'>{data['net_increase_cy']:,.2f}</td>
                <td class='right'>{data['net_increase_py']:,.2f}</td>
            </tr>
            <tr>
                <td>Cash and Cash Equivalents at Beginning of Year</td>
                <td class='right'>{data['opening_cash_cy']:,.2f}</td>
                <td class='right'>{data['opening_cash_py']:,.2f}</td>
            </tr>
            <tr style='background-color: #32CD32; font-weight: bold;'>
                <td>Cash and Cash Equivalents at End of Year</td>
                <td class='right'>{data['closing_cash_cy']:,.2f}</td>
                <td class='right'>{data['closing_cash_py']:,.2f}</td>
            </tr>
        </table>
        """
        
        self.cf_widget.setHtml(html)
    
    def display_notes(self, notes: dict):
        """Display Notes to Accounts with detailed breakdowns"""
        html = """
        <style>
            table { border-collapse: collapse; width: 100%; margin: 10px 0; }
            th, td { border: 1px solid #ddd; padding: 6px; text-align: left; }
            th { background-color: #4CAF50; color: white; }
            .note-header { background-color: #2196F3; color: white; padding: 10px; margin-top: 15px; }
            .note-total { background-color: #FFD700; font-weight: bold; }
            .right { text-align: right; }
            .ageing-table { font-size: 0.9em; }
        </style>
        
        <h2 style='text-align: center;'>NOTES TO ACCOUNTS</h2>
        <p style='text-align: center; color: #666;'>As required under Schedule III of Companies Act, 2013</p>
        <hr>
        """
        
        for note_num, note_data in sorted(notes.items()):
            html += f"<div class='note-header'><h3 style='margin:0;'>Note {note_num}: {note_data['title']}</h3></div>"
            
            # Display data based on structure
            if 'data' in note_data and note_data['data']:
                html += "<table>"
                html += "<tr><th>Particulars</th><th class='right'>Current Year (₹)</th><th class='right'>Previous Year (₹)</th></tr>"
                
                for key, value in note_data['data'].items():
                    if isinstance(value, dict):
                        # Nested structure (e.g., ageing schedules)
                        html += f"<tr><td colspan='3' style='font-weight: bold; background-color: #f0f0f0;'>{key}</td></tr>"
                        for sub_key, sub_value in value.items():
                            if isinstance(sub_value, dict) and 'cy' in sub_value and 'py' in sub_value:
                                html += f"<tr><td style='padding-left: 20px;'>{sub_key}</td>"
                                html += f"<td class='right'>{sub_value['cy']:,.2f}</td>"
                                html += f"<td class='right'>{sub_value['py']:,.2f}</td></tr>"
                            elif isinstance(sub_value, (int, float)):
                                html += f"<tr><td style='padding-left: 20px;'>{sub_key}</td>"
                                html += f"<td class='right' colspan='2'>{sub_value:,.2f}</td></tr>"
                    elif isinstance(value, (int, float)):
                        html += f"<tr><td>{key}</td><td class='right' colspan='2'>{value:,.2f}</td></tr>"
                    else:
                        html += f"<tr><td>{key}</td><td colspan='2'>{value}</td></tr>"
                
                # Total row
                html += f"<tr class='note-total'><td>Total</td>"
                html += f"<td class='right'>{note_data['total_cy']:,.2f}</td>"
                html += f"<td class='right'>{note_data['total_py']:,.2f}</td></tr>"
                html += "</table>"
            else:
                # Simple totals only
                html += "<table>"
                html += f"<tr class='note-total'><td>Total</td>"
                html += f"<td class='right'>{note_data.get('total_cy', 0):,.2f}</td>"
                html += f"<td class='right'>{note_data.get('total_py', 0):,.2f}</td></tr>"
                html += "</table>"
            
            html += "<br>"
        
        html += f"<p style='margin-top: 30px; text-align: center; color: #666;'>"
        html += f"Total Notes Generated: {len(notes)}<br>"
        html += f"Complete Schedule III Compliance</p>"
        
        self.notes_widget.setHtml(html)
    
    def export_excel(self):
        """Export to Excel with Schedule III formatting and formula linking"""
        if not self.company_id:
            QMessageBox.warning(self, "No Company", "Please select a company first.")
            return
        
        try:
            from PyQt5.QtWidgets import QFileDialog
            from models.excel_exporter import ExcelExporter
            from models.financial_statements import BalanceSheetGenerator, ProfitLossGenerator, CashFlowGenerator, NotesGenerator
            from models.company_info import CompanyInfo
            import os
            
            # Get company info
            company = CompanyInfo.get_by_id(self.company_id)
            if not company:
                QMessageBox.warning(self, "Error", "Company not found.")
                return
            
            # Ask user for save location
            default_filename = f"{company.entity_name.replace(' ', '_')}_Financials_{company.fy_end_date}.xlsx"
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Financial Statements",
                default_filename,
                "Excel Files (*.xlsx);;All Files (*)"
            )
            
            if not file_path:
                return  # User cancelled
            
            # Generate all financial data
            QMessageBox.information(self, "Generating...", "Please wait while generating financial statements...")
            
            bs_gen = BalanceSheetGenerator(self.company_id)
            pl_gen = ProfitLossGenerator(self.company_id)
            cf_gen = CashFlowGenerator(self.company_id)
            notes_gen = NotesGenerator(self.company_id)
            
            bs_data = bs_gen.generate()
            pl_data = pl_gen.generate()
            cf_data = cf_gen.generate()
            notes = notes_gen.generate_all_notes()
            
            # Create Excel workbook
            exporter = ExcelExporter(company.entity_name, company.fy_end_date)
            exporter.create_workbook(bs_data, pl_data, cf_data, notes)
            exporter.save(file_path)
            
            QMessageBox.information(
                self,
                "Success",
                f"Financial statements exported successfully!\n\n"
                f"File: {os.path.basename(file_path)}\n"
                f"Location: {os.path.dirname(file_path)}\n\n"
                f"The Excel file includes:\n"
                f"• Balance Sheet with formula links to Notes\n"
                f"• Profit & Loss Statement\n"
                f"• Cash Flow Statement\n"
                f"• All {len(notes)} Notes to Accounts\n\n"
                f"All financial statements are formatted per Schedule III."
            )
            
        except Exception as e:
            QMessageBox.critical(self, "Export Failed", f"Failed to export to Excel:\n\n{str(e)}")
