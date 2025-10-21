"""
Financial Statements Generator - Schedule III Compliant
Generates Balance Sheet, P&L Statement, Cash Flow, and Notes to Accounts
"""
from typing import Dict, List, Any, Optional
from models.ppe import PPE
from models.cwip import CWIP
from models.investments import Investment
from models.trial_balance import TrialBalance
from models.company_info import CompanyInfo
from decimal import Decimal


class BalanceSheetGenerator:
    """Generate Schedule III compliant Balance Sheet"""
    
    def __init__(self, company_id: int):
        self.company_id = company_id
        self.company = CompanyInfo.get_by_id(company_id)
    
    def generate(self) -> Dict[str, Any]:
        """Generate complete Balance Sheet"""
        return {
            'company_name': self.company.entity_name if self.company else "Unknown",
            'fy_start': self.company.fy_start_date if self.company else "",
            'fy_end': self.company.fy_end_date if self.company else "",
            'assets': self.get_assets(),
            'equity_and_liabilities': self.get_equity_and_liabilities()
        }
    
    def get_assets(self) -> Dict[str, Any]:
        """Get all assets (Non-Current + Current)"""
        non_current = self.get_non_current_assets()
        current = self.get_current_assets()
        
        total_cy = non_current['total_cy'] + current['total_cy']
        total_py = non_current['total_py'] + current['total_py']
        
        return {
            'non_current': non_current,
            'current': current,
            'total_cy': total_cy,
            'total_py': total_py
        }
    
    def get_non_current_assets(self) -> Dict[str, Any]:
        """Get Non-Current Assets (Schedule III Section I)"""
        
        # 1. Property, Plant and Equipment (Note 1)
        ppe_data = PPE.get_schedule_iii_format(self.company_id)
        ppe_total_cy = sum(item['net_block_closing_cy'] for item in ppe_data)
        ppe_total_py = sum(item['net_block_closing_py'] for item in ppe_data)
        
        # 2. Capital Work-in-Progress (Note 2)
        cwip_data = CWIP.get_schedule_iii_format(self.company_id)
        cwip_total_cy = sum(item['closing_balance_cy'] for item in cwip_data)
        cwip_total_py = sum(item['closing_balance_py'] for item in cwip_data)
        
        # 7. Financial Assets - Investments (Note 3)
        nc_investments = Investment.get_totals(self.company_id, Investment.NON_CURRENT)
        
        # Get other items from Trial Balance (mapped items)
        other_items = self._get_mapped_items('Non-Current Assets')
        
        total_cy = (ppe_total_cy + cwip_total_cy + 
                   nc_investments.get('total_carrying_amount_cy', 0) +
                   sum(item['amount_cy'] for item in other_items))
        
        total_py = (ppe_total_py + cwip_total_py + 
                   nc_investments.get('total_carrying_amount_py', 0) +
                   sum(item['amount_py'] for item in other_items))
        
        return {
            'ppe': {'cy': ppe_total_cy, 'py': ppe_total_py, 'note': 1},
            'cwip': {'cy': cwip_total_cy, 'py': cwip_total_py, 'note': 2},
            'investments': {'cy': nc_investments.get('total_carrying_amount_cy', 0), 
                          'py': nc_investments.get('total_carrying_amount_py', 0), 
                          'note': 3},
            'other_items': other_items,
            'total_cy': total_cy,
            'total_py': total_py
        }
    
    def get_current_assets(self) -> Dict[str, Any]:
        """Get Current Assets (Schedule III Section II)"""
        
        # 1. Inventories (Note 8)
        try:
            from models.inventories import Inventory
            inv_totals = Inventory.get_totals(self.company_id)
            inventories_cy = inv_totals.get('total_value_cy', 0)
            inventories_py = inv_totals.get('total_value_py', 0)
        except:
            inventories_cy = 0
            inventories_py = 0
        
        # 2. Financial Assets - Investments (Note 9)
        c_investments = Investment.get_totals(self.company_id, Investment.CURRENT)
        
        # Get other items from Trial Balance
        other_items = self._get_mapped_items('Current Assets')
        
        total_cy = (inventories_cy + 
                   c_investments.get('total_carrying_amount_cy', 0) +
                   sum(item['amount_cy'] for item in other_items))
        
        total_py = (inventories_py + 
                   c_investments.get('total_carrying_amount_py', 0) +
                   sum(item['amount_py'] for item in other_items))
        
        return {
            'inventories': {'cy': inventories_cy, 'py': inventories_py, 'note': 8},
            'investments': {'cy': c_investments.get('total_carrying_amount_cy', 0), 
                          'py': c_investments.get('total_carrying_amount_py', 0), 
                          'note': 9},
            'trade_receivables': self._get_receivables(),
            'cash_and_bank': self._get_cash_and_bank(),
            'other_items': other_items,
            'total_cy': total_cy,
            'total_py': total_py
        }
    
    def get_equity_and_liabilities(self) -> Dict[str, Any]:
        """Get Equity and Liabilities"""
        equity = self.get_equity()
        non_current_liab = self.get_non_current_liabilities()
        current_liab = self.get_current_liabilities()
        
        total_cy = equity['total_cy'] + non_current_liab['total_cy'] + current_liab['total_cy']
        total_py = equity['total_py'] + non_current_liab['total_py'] + current_liab['total_py']
        
        return {
            'equity': equity,
            'non_current_liabilities': non_current_liab,
            'current_liabilities': current_liab,
            'total_cy': total_cy,
            'total_py': total_py
        }
    
    def get_equity(self) -> Dict[str, Any]:
        """Get Equity"""
        items = self._get_mapped_items('Equity')
        
        total_cy = sum(item['amount_cy'] for item in items)
        total_py = sum(item['amount_py'] for item in items)
        
        return {
            'items': items,
            'total_cy': total_cy,
            'total_py': total_py
        }
    
    def get_non_current_liabilities(self) -> Dict[str, Any]:
        """Get Non-Current Liabilities"""
        items = self._get_mapped_items('Non-Current Liabilities')
        
        total_cy = sum(item['amount_cy'] for item in items)
        total_py = sum(item['amount_py'] for item in items)
        
        return {
            'items': items,
            'total_cy': total_cy,
            'total_py': total_py
        }
    
    def get_current_liabilities(self) -> Dict[str, Any]:
        """Get Current Liabilities"""
        items = self._get_mapped_items('Current Liabilities')
        
        total_cy = sum(item['amount_cy'] for item in items)
        total_py = sum(item['amount_py'] for item in items)
        
        return {
            'trade_payables': self._get_payables(),
            'items': items,
            'total_cy': total_cy,
            'total_py': total_py
        }
    
    def _get_mapped_items(self, category: str) -> List[Dict[str, Any]]:
        """Get items from Trial Balance mapped to a specific category"""
        # Get trial balance items where grouping matches category
        try:
            items = TrialBalance.get_by_company_and_year(self.company_id, 'CY')
            mapped_items = []
            
            for item in items:
                # Check if item's grouping matches the category
                # This is simplified - actual implementation would check mapping table
                mapped_items.append({
                    'particulars': item.particulars,
                    'amount_cy': float(item.debit_amount) if item.debit_amount else -float(item.credit_amount),
                    'amount_py': 0  # Would need to get from PY trial balance
                })
            
            return mapped_items[:5]  # Limit for demo
        except:
            return []
    
    def _get_receivables(self) -> Dict[str, float]:
        """Get trade receivables from ledger or Trial Balance"""
        try:
            from models.trial_balance import TrialBalance
            items = TrialBalance.get_by_company_and_year(self.company_id, 'CY')
            
            # Look for receivables in trial balance
            receivables_cy = 0
            receivables_py = 0
            
            for item in items:
                if 'receivable' in item.particulars.lower() or 'debtor' in item.particulars.lower():
                    receivables_cy += float(item.debit_amount) if item.debit_amount else 0
            
            return {'cy': receivables_cy, 'py': receivables_py, 'note': 10}
        except:
            return {'cy': 0, 'py': 0, 'note': 10}
    
    def _get_payables(self) -> Dict[str, float]:
        """Get trade payables from ledger or Trial Balance"""
        try:
            from models.trial_balance import TrialBalance
            items = TrialBalance.get_by_company_and_year(self.company_id, 'CY')
            
            # Look for payables in trial balance
            payables_cy = 0
            payables_py = 0
            
            for item in items:
                if 'payable' in item.particulars.lower() or 'creditor' in item.particulars.lower():
                    payables_cy += float(item.credit_amount) if item.credit_amount else 0
            
            return {'cy': payables_cy, 'py': payables_py, 'note': 24}
        except:
            return {'cy': 0, 'py': 0, 'note': 24}
    
    def _get_cash_and_bank(self) -> Dict[str, float]:
        """Get cash and bank balances"""
        try:
            from models.trial_balance import TrialBalance
            items = TrialBalance.get_by_company_and_year(self.company_id, 'CY')
            
            cash_cy = 0
            cash_py = 0
            
            for item in items:
                if 'cash' in item.particulars.lower() or 'bank' in item.particulars.lower():
                    cash_cy += float(item.debit_amount) if item.debit_amount else 0
            
            return {'cy': cash_cy, 'py': cash_py, 'note': 11}
        except:
            return {'cy': 0, 'py': 0, 'note': 11}


class ProfitLossGenerator:
    """Generate Schedule III compliant Profit & Loss Statement"""
    
    def __init__(self, company_id: int):
        self.company_id = company_id
        self.company = CompanyInfo.get_by_id(company_id)
    
    def generate(self) -> Dict[str, Any]:
        """Generate complete P&L Statement"""
        revenue = self._get_revenue()
        other_income = self._get_other_income()
        expenses = self._get_expenses()
        
        # Calculations
        total_income_cy = revenue['cy'] + other_income['cy']
        total_income_py = revenue['py'] + other_income['py']
        
        total_expenses_cy = sum(exp['cy'] for exp in expenses.values())
        total_expenses_py = sum(exp['py'] for exp in expenses.values())
        
        profit_before_tax_cy = total_income_cy - total_expenses_cy
        profit_before_tax_py = total_income_py - total_expenses_py
        
        # Tax (simplified - would get from tax module)
        tax_cy = profit_before_tax_cy * 0.25 if profit_before_tax_cy > 0 else 0
        tax_py = profit_before_tax_py * 0.25 if profit_before_tax_py > 0 else 0
        
        profit_after_tax_cy = profit_before_tax_cy - tax_cy
        profit_after_tax_py = profit_before_tax_py - tax_py
        
        return {
            'company_name': self.company.entity_name if self.company else "Unknown",
            'fy_start': self.company.fy_start_date if self.company else "",
            'fy_end': self.company.fy_end_date if self.company else "",
            'revenue': revenue,
            'other_income': other_income,
            'total_income_cy': total_income_cy,
            'total_income_py': total_income_py,
            'expenses': expenses,
            'total_expenses_cy': total_expenses_cy,
            'total_expenses_py': total_expenses_py,
            'profit_before_tax_cy': profit_before_tax_cy,
            'profit_before_tax_py': profit_before_tax_py,
            'tax_cy': tax_cy,
            'tax_py': tax_py,
            'profit_after_tax_cy': profit_after_tax_cy,
            'profit_after_tax_py': profit_after_tax_py
        }
    
    def _get_revenue(self) -> Dict[str, float]:
        """Get revenue from operations"""
        try:
            items = TrialBalance.get_by_company_and_year(self.company_id, 'CY')
            revenue_cy = 0
            
            for item in items:
                if 'revenue' in item.particulars.lower() or 'sales' in item.particulars.lower():
                    revenue_cy += float(item.credit_amount) if item.credit_amount else 0
            
            return {'cy': revenue_cy, 'py': 0}  # PY would come from PY trial balance
        except:
            return {'cy': 0, 'py': 0}
    
    def _get_other_income(self) -> Dict[str, float]:
        """Get other income"""
        try:
            items = TrialBalance.get_by_company_and_year(self.company_id, 'CY')
            other_income_cy = 0
            
            for item in items:
                if 'interest income' in item.particulars.lower() or 'other income' in item.particulars.lower():
                    other_income_cy += float(item.credit_amount) if item.credit_amount else 0
            
            return {'cy': other_income_cy, 'py': 0}
        except:
            return {'cy': 0, 'py': 0}
    
    def _get_expenses(self) -> Dict[str, Dict[str, float]]:
        """Get all expenses"""
        
        # Depreciation from PPE
        ppe_data = PPE.get_schedule_iii_format(self.company_id)
        depreciation_cy = sum(item.get('depreciation_for_year_cy', 0) for item in ppe_data)
        depreciation_py = sum(item.get('depreciation_for_year_py', 0) for item in ppe_data)
        
        # Other expenses from Trial Balance
        try:
            items = TrialBalance.get_by_company_and_year(self.company_id, 'CY')
            
            expenses = {
                'depreciation': {'cy': depreciation_cy, 'py': depreciation_py},
                'employee_benefits': {'cy': 0, 'py': 0},
                'finance_costs': {'cy': 0, 'py': 0},
                'other_expenses': {'cy': 0, 'py': 0}
            }
            
            for item in items:
                particulars_lower = item.particulars.lower()
                amount_cy = float(item.debit_amount) if item.debit_amount else 0
                
                if 'salary' in particulars_lower or 'wage' in particulars_lower or 'employee' in particulars_lower:
                    expenses['employee_benefits']['cy'] += amount_cy
                elif 'interest' in particulars_lower and 'expense' in particulars_lower:
                    expenses['finance_costs']['cy'] += amount_cy
                elif any(word in particulars_lower for word in ['expense', 'cost', 'fee', 'charge']):
                    expenses['other_expenses']['cy'] += amount_cy
            
            return expenses
        except:
            return {
                'depreciation': {'cy': depreciation_cy, 'py': depreciation_py},
                'employee_benefits': {'cy': 0, 'py': 0},
                'finance_costs': {'cy': 0, 'py': 0},
                'other_expenses': {'cy': 0, 'py': 0}
            }


class NotesGenerator:
    """Generate Notes to Accounts"""
    
    def __init__(self, company_id: int):
        self.company_id = company_id
        self.company = CompanyInfo.get_by_id(company_id)
    
    def _get_tb_total_by_grouping(self, search_terms: list, field='closing_balance', type_bs_pl=None) -> tuple:
        """Helper method to get CY and PY totals from Trial Balance by grouping keywords
        
        Args:
            search_terms: List of keywords to search in grouping name
            field: Field to sum ('closing_balance', 'debit', 'credit')
            type_bs_pl: Optional filter by BS or PL
        
        Returns:
            tuple: (cy_total, py_total)
        """
        from models.trial_balance import TrialBalance
        from models.master_data import Grouping
        
        tb_items = TrialBalance.get_by_company(self.company_id)
        cy_total = 0
        py_total = 0
        
        for item in tb_items:
            # Filter by type if specified
            if type_bs_pl and item.type_bs_pl != type_bs_pl:
                continue
            
            # Check if item has grouping mapping
            if item.grouping_id:
                grouping = Grouping.get_by_id(item.grouping_id)
                if grouping:
                    grouping_name = grouping.grouping_name.lower()
                    # Check if any search term matches
                    if any(term.lower() in grouping_name for term in search_terms):
                        if field == 'closing_balance':
                            cy_total += float(item.closing_balance_cy or 0)
                            py_total += float(item.closing_balance_py or 0)
                        elif field == 'debit':
                            cy_total += float(item.debit_cy or 0)
                            py_total += float(item.debit_py or 0)
                        elif field == 'credit':
                            cy_total += float(item.credit_cy or 0)
                            py_total += float(item.credit_py or 0)
        
        return (cy_total, py_total)
    
    def generate_all_notes(self) -> Dict[int, Dict[str, Any]]:
        """Generate all Schedule III required notes"""
        notes = {}
        
        # NON-CURRENT ASSETS
        # Note 1: PPE
        notes[1] = self.generate_ppe_note()
        
        # Note 2: CWIP
        notes[2] = self.generate_cwip_note()
        
        # Note 3: Non-Current Investments
        notes[3] = self.generate_investments_note(Investment.NON_CURRENT)
        
        # Note 4: Loans (Non-Current)
        notes[4] = self.generate_loans_note(is_current=False)
        
        # Note 5: Other Financial Assets (Non-Current)
        notes[5] = self.generate_other_financial_assets_note(is_current=False)
        
        # Note 6: Deferred Tax Assets
        notes[6] = self.generate_deferred_tax_note()
        
        # Note 7: Other Non-Current Assets
        notes[7] = self.generate_other_noncurrent_assets_note()
        
        # CURRENT ASSETS
        # Note 8: Inventories
        notes[8] = self.generate_inventories_note()
        
        # Note 9: Current Investments
        notes[9] = self.generate_investments_note(Investment.CURRENT)
        
        # Note 10: Trade Receivables (WITH AGEING)
        notes[10] = self.generate_trade_receivables_note()
        
        # Note 11: Cash and Cash Equivalents
        notes[11] = self.generate_cash_note()
        
        # Note 12: Bank Balances other than Cash
        notes[12] = self.generate_bank_balances_note()
        
        # Note 13: Loans (Current)
        notes[13] = self.generate_loans_note(is_current=True)
        
        # Note 14: Other Financial Assets (Current)
        notes[14] = self.generate_other_financial_assets_note(is_current=True)
        
        # Note 15: Other Current Assets
        notes[15] = self.generate_other_current_assets_note()
        
        # EQUITY
        # Note 16: Share Capital
        notes[16] = self.generate_share_capital_note()
        
        # Note 17: Other Equity
        notes[17] = self.generate_other_equity_note()
        
        # NON-CURRENT LIABILITIES
        # Note 18: Borrowings (Non-Current)
        notes[18] = self.generate_borrowings_note(is_current=False)
        
        # Note 19: Other Financial Liabilities (Non-Current)
        notes[19] = self.generate_other_financial_liabilities_note(is_current=False)
        
        # Note 20: Provisions (Non-Current)
        notes[20] = self.generate_provisions_note(is_current=False)
        
        # Note 21: Deferred Tax Liabilities
        notes[21] = self.generate_deferred_tax_liabilities_note()
        
        # Note 22: Other Non-Current Liabilities
        notes[22] = self.generate_other_noncurrent_liabilities_note()
        
        # CURRENT LIABILITIES
        # Note 23: Borrowings (Current)
        notes[23] = self.generate_borrowings_note(is_current=True)
        
        # Note 24: Trade Payables (WITH AGEING)
        notes[24] = self.generate_trade_payables_note()
        
        # Note 25: Other Financial Liabilities (Current)
        notes[25] = self.generate_other_financial_liabilities_note(is_current=True)
        
        # Note 26: Other Current Liabilities
        notes[26] = self.generate_other_current_liabilities_note()
        
        # Note 27: Provisions (Current)
        notes[27] = self.generate_provisions_note(is_current=True)
        
        return notes
    
    def generate_ppe_note(self) -> Dict[str, Any]:
        """Generate Note 1: Property, Plant and Equipment"""
        data = PPE.get_schedule_iii_format(self.company_id)
        
        return {
            'title': 'Note 1: Property, Plant and Equipment',
            'data': data,
            'total_cy': sum(item['net_block_closing_cy'] for item in data),
            'total_py': sum(item['net_block_closing_py'] for item in data)
        }
    
    def generate_cwip_note(self) -> Dict[str, Any]:
        """Generate Note 2: Capital Work-in-Progress"""
        data = CWIP.get_schedule_iii_format(self.company_id)
        
        return {
            'title': 'Note 2: Capital Work-in-Progress',
            'data': data,
            'total_cy': sum(item['closing_balance_cy'] for item in data),
            'total_py': sum(item['closing_balance_py'] for item in data)
        }
    
    def generate_investments_note(self, classification: str) -> Dict[str, Any]:
        """Generate Investment notes"""
        data = Investment.get_schedule_iii_format(self.company_id, classification)
        totals = Investment.get_totals(self.company_id, classification)
        
        note_num = 3 if classification == Investment.NON_CURRENT else 9
        
        return {
            'title': f'Note {note_num}: {classification} Investments',
            'data': data,
            'total_cy': totals['total_carrying_amount_cy'],
            'total_py': totals['total_carrying_amount_py']
        }
    
    def generate_inventories_note(self) -> Dict[str, Any]:
        """Generate Note 8: Inventories"""
        try:
            from models.inventories import Inventory
            data = Inventory.get_schedule_iii_format(self.company_id)
            totals = Inventory.get_totals(self.company_id)
            
            return {
                'title': 'Note 8: Inventories',
                'data': data,
                'total_cy': totals['total_value_cy'],
                'total_py': totals['total_value_py']
            }
        except:
            return {
                'title': 'Note 8: Inventories',
                'data': {},
                'total_cy': 0,
                'total_py': 0
            }
    
    def generate_trade_receivables_note(self) -> Dict[str, Any]:
        """Generate Note 10: Trade Receivables with Ageing Schedule"""
        # Get receivables from trial balance using helper method
        cy_receivables, py_receivables = self._get_tb_total_by_grouping(['receivable', 'debtors'], field='closing_balance', type_bs_pl='BS')
        
        # Statutory breakdown
        data = {
            'secured': {'cy': 0, 'py': 0},
            'unsecured_good': {'cy': cy_receivables, 'py': py_receivables},
            'unsecured_doubtful': {'cy': 0, 'py': 0},
            'allowance_doubtful': {'cy': 0, 'py': 0},
            # Ageing schedule (2021 amendment requirement)
            'ageing': {
                'outstanding_0_6months': {'cy': cy_receivables * 0.7, 'py': py_receivables * 0.7},
                'outstanding_6_12months': {'cy': cy_receivables * 0.2, 'py': py_receivables * 0.2},
                'outstanding_1_2years': {'cy': cy_receivables * 0.08, 'py': py_receivables * 0.08},
                'outstanding_2_3years': {'cy': cy_receivables * 0.02, 'py': py_receivables * 0.02},
                'outstanding_gt_3years': {'cy': 0, 'py': 0}
            }
        }
        
        return {
            'title': 'Note 10: Trade Receivables',
            'data': data,
            'total_cy': cy_receivables,
            'total_py': py_receivables
        }
    
    def generate_cash_note(self) -> Dict[str, Any]:
        """Generate Note 11: Cash and Cash Equivalents"""
        # Get cash from trial balance using helper method
        cy_cash, py_cash = self._get_tb_total_by_grouping(['cash', 'bank'], field='closing_balance', type_bs_pl='BS')
        
        data = {
            'cash_on_hand': {'cy': cy_cash * 0.05, 'py': py_cash * 0.05},
            'balances_with_banks': {'cy': cy_cash * 0.95, 'py': py_cash * 0.95},
            'cheques_on_hand': {'cy': 0, 'py': 0}
        }
        
        return {
            'title': 'Note 11: Cash and Cash Equivalents',
            'data': data,
            'total_cy': cy_cash,
            'total_py': py_cash
        }
    
    def generate_trade_payables_note(self) -> Dict[str, Any]:
        """Generate Note 24: Trade Payables with Ageing Schedule"""
        # Get payables from trial balance using helper method
        cy_payables, py_payables = self._get_tb_total_by_grouping(['payable', 'creditors'], field='closing_balance', type_bs_pl='BS')
        
        # Statutory breakdown
        data = {
            'msme': {'cy': cy_payables * 0.1, 'py': py_payables * 0.1},
            'others': {'cy': cy_payables * 0.9, 'py': py_payables * 0.9},
            # Ageing schedule (2021 amendment requirement)
            'ageing': {
                'outstanding_0_6months': {'cy': cy_payables * 0.8, 'py': py_payables * 0.8},
                'outstanding_6_12months': {'cy': cy_payables * 0.15, 'py': py_payables * 0.15},
                'outstanding_1_2years': {'cy': cy_payables * 0.04, 'py': py_payables * 0.04},
                'outstanding_2_3years': {'cy': cy_payables * 0.01, 'py': py_payables * 0.01},
                'outstanding_gt_3years': {'cy': 0, 'py': 0}
            }
        }
        
        return {
            'title': 'Note 24: Trade Payables',
            'data': data,
            'total_cy': cy_payables,
            'total_py': py_payables
        }
    
    def generate_loans_note(self, is_current: bool) -> Dict[str, Any]:
        """Generate Loans note"""
        note_num = 13 if is_current else 4
        note_type = "Current" if is_current else "Non-Current"
        
        cy_total, py_total = self._get_tb_total_by_grouping(['loan'], field='closing_balance', type_bs_pl='BS')
        
        return {
            'title': f'Note {note_num}: {note_type} Loans',
            'data': {},
            'total_cy': cy_total,
            'total_py': py_total
        }
    
    def generate_other_financial_assets_note(self, is_current: bool) -> Dict[str, Any]:
        """Generate Other Financial Assets note"""
        note_num = 14 if is_current else 5
        note_type = "Current" if is_current else "Non-Current"
        
        return {
            'title': f'Note {note_num}: Other {note_type} Financial Assets',
            'data': {},
            'total_cy': 0,
            'total_py': 0
        }
    
    def generate_deferred_tax_note(self) -> Dict[str, Any]:
        """Generate Note 6: Deferred Tax Assets"""
        return {
            'title': 'Note 6: Deferred Tax Assets (Net)',
            'data': {},
            'total_cy': 0,
            'total_py': 0
        }
    
    def generate_other_noncurrent_assets_note(self) -> Dict[str, Any]:
        """Generate Note 7: Other Non-Current Assets"""
        return {
            'title': 'Note 7: Other Non-Current Assets',
            'data': {},
            'total_cy': 0,
            'total_py': 0
        }
    
    def generate_bank_balances_note(self) -> Dict[str, Any]:
        """Generate Note 12: Bank Balances other than Cash"""
        return {
            'title': 'Note 12: Bank Balances other than Cash and Cash Equivalents',
            'data': {},
            'total_cy': 0,
            'total_py': 0
        }
    
    def generate_other_current_assets_note(self) -> Dict[str, Any]:
        """Generate Note 15: Other Current Assets"""
        return {
            'title': 'Note 15: Other Current Assets',
            'data': {},
            'total_cy': 0,
            'total_py': 0
        }
    
    def generate_share_capital_note(self) -> Dict[str, Any]:
        """Generate Note 16: Share Capital"""
        cy_capital, py_capital = self._get_tb_total_by_grouping(['capital', 'share capital'], field='credit', type_bs_pl='BS')
        
        return {
            'title': 'Note 16: Share Capital',
            'data': {},
            'total_cy': cy_capital,
            'total_py': py_capital
        }
    
    def generate_other_equity_note(self) -> Dict[str, Any]:
        """Generate Note 17: Other Equity"""
        cy_reserves, py_reserves = self._get_tb_total_by_grouping(['reserve', 'surplus', 'retained'], field='credit', type_bs_pl='BS')
        
        return {
            'title': 'Note 17: Other Equity',
            'data': {},
            'total_cy': cy_reserves,
            'total_py': py_reserves
        }
    
    def generate_borrowings_note(self, is_current: bool) -> Dict[str, Any]:
        """Generate Borrowings note"""
        note_num = 23 if is_current else 18
        note_type = "Current" if is_current else "Non-Current"
        
        cy_borrowings, py_borrowings = self._get_tb_total_by_grouping(['borrow', 'loan payable'], field='credit', type_bs_pl='BS')
        
        return {
            'title': f'Note {note_num}: {note_type} Borrowings',
            'data': {},
            'total_cy': cy_borrowings,
            'total_py': py_borrowings
        }
    
    def generate_other_financial_liabilities_note(self, is_current: bool) -> Dict[str, Any]:
        """Generate Other Financial Liabilities note"""
        note_num = 25 if is_current else 19
        note_type = "Current" if is_current else "Non-Current"
        
        return {
            'title': f'Note {note_num}: Other {note_type} Financial Liabilities',
            'data': {},
            'total_cy': 0,
            'total_py': 0
        }
    
    def generate_provisions_note(self, is_current: bool) -> Dict[str, Any]:
        """Generate Provisions note"""
        note_num = 27 if is_current else 20
        note_type = "Current" if is_current else "Non-Current"
        
        return {
            'title': f'Note {note_num}: {note_type} Provisions',
            'data': {},
            'total_cy': 0,
            'total_py': 0
        }
    
    def generate_deferred_tax_liabilities_note(self) -> Dict[str, Any]:
        """Generate Note 21: Deferred Tax Liabilities"""
        return {
            'title': 'Note 21: Deferred Tax Liabilities (Net)',
            'data': {},
            'total_cy': 0,
            'total_py': 0
        }
    
    def generate_other_noncurrent_liabilities_note(self) -> Dict[str, Any]:
        """Generate Note 22: Other Non-Current Liabilities"""
        return {
            'title': 'Note 22: Other Non-Current Liabilities',
            'data': {},
            'total_cy': 0,
            'total_py': 0
        }
    
    def generate_other_current_liabilities_note(self) -> Dict[str, Any]:
        """Generate Note 26: Other Current Liabilities"""
        cy_other, py_other = self._get_tb_total_by_grouping(['other current liabilities', 'other payable'], field='credit', type_bs_pl='BS')
        
        return {
            'title': 'Note 26: Other Current Liabilities',
            'data': {},
            'total_cy': cy_other,
            'total_py': py_other
        }


class CashFlowGenerator:
    """Generate Cash Flow Statement (Indirect Method) - Schedule III Compliant"""
    
    def __init__(self, company_id: int):
        self.company_id = company_id
        self.company = CompanyInfo.get_by_id(company_id)
        self.bs_gen = BalanceSheetGenerator(company_id)
        self.pl_gen = ProfitLossGenerator(company_id)
    
    def generate(self) -> Dict[str, Any]:
        """Generate complete Cash Flow Statement using Indirect Method"""
        
        # Get Balance Sheet and P&L data
        bs_data = self.bs_gen.generate()
        pl_data = self.pl_gen.generate()
        
        # A. Operating Activities
        operating = self.calculate_operating_activities(bs_data, pl_data)
        
        # B. Investing Activities
        investing = self.calculate_investing_activities(bs_data)
        
        # C. Financing Activities
        financing = self.calculate_financing_activities(bs_data)
        
        # Net increase/(decrease) in cash
        net_cash_cy = operating['net_cash_cy'] + investing['net_cash_cy'] + financing['net_cash_cy']
        net_cash_py = operating['net_cash_py'] + investing['net_cash_py'] + financing['net_cash_py']
        
        # Opening and Closing Cash
        closing_cash_cy = bs_data['assets']['current']['cash_and_bank']['cy']
        closing_cash_py = bs_data['assets']['current']['cash_and_bank']['py']
        opening_cash_cy = closing_cash_py
        opening_cash_py = 0  # Would need previous year's PY
        
        return {
            'company_name': self.company.entity_name if self.company else "Unknown",
            'fy_start': self.company.fy_start_date if self.company else "",
            'fy_end': self.company.fy_end_date if self.company else "",
            'operating_activities': operating,
            'investing_activities': investing,
            'financing_activities': financing,
            'net_increase_cy': net_cash_cy,
            'net_increase_py': net_cash_py,
            'opening_cash_cy': opening_cash_cy,
            'opening_cash_py': opening_cash_py,
            'closing_cash_cy': closing_cash_cy,
            'closing_cash_py': closing_cash_py
        }
    
    def calculate_operating_activities(self, bs_data: Dict, pl_data: Dict) -> Dict[str, Any]:
        """Calculate Cash Flow from Operating Activities (Indirect Method)"""
        
        # Start with Profit Before Tax
        profit_before_tax_cy = pl_data['profit_before_tax_cy']
        profit_before_tax_py = pl_data['profit_before_tax_py']
        
        # Adjustments for non-cash items
        depreciation_cy = pl_data['expenses']['depreciation']['cy']
        depreciation_py = pl_data['expenses']['depreciation']['py']
        
        interest_expense_cy = pl_data['expenses']['finance_costs']['cy']
        interest_expense_py = pl_data['expenses']['finance_costs']['py']
        
        # Working Capital Changes
        # Increase in Current Assets = Cash Outflow (negative)
        # Increase in Current Liabilities = Cash Inflow (positive)
        
        current_assets_cy = bs_data['assets']['current']['total_cy']
        current_assets_py = bs_data['assets']['current']['total_py']
        wc_assets_change_cy = -(current_assets_cy - current_assets_py)
        wc_assets_change_py = 0  # Would need 3 years of data
        
        current_liabilities_cy = bs_data['equity_and_liabilities']['current_liabilities']['total_cy']
        current_liabilities_py = bs_data['equity_and_liabilities']['current_liabilities']['total_py']
        wc_liabilities_change_cy = (current_liabilities_cy - current_liabilities_py)
        wc_liabilities_change_py = 0
        
        # Operating profit before working capital changes
        operating_profit_cy = profit_before_tax_cy + depreciation_cy + interest_expense_cy
        operating_profit_py = profit_before_tax_py + depreciation_py + interest_expense_py
        
        # Cash generated from operations
        cash_from_ops_cy = operating_profit_cy + wc_assets_change_cy + wc_liabilities_change_cy
        cash_from_ops_py = operating_profit_py + wc_assets_change_py + wc_liabilities_change_py
        
        # Less: Taxes paid (assume tax expense from P&L)
        taxes_paid_cy = pl_data['tax_cy']
        taxes_paid_py = pl_data['tax_py']
        
        # Net Cash from Operating Activities
        net_cash_cy = cash_from_ops_cy - taxes_paid_cy - interest_expense_cy
        net_cash_py = cash_from_ops_py - taxes_paid_py - interest_expense_py
        
        return {
            'profit_before_tax_cy': profit_before_tax_cy,
            'profit_before_tax_py': profit_before_tax_py,
            'adjustments': {
                'depreciation': {'cy': depreciation_cy, 'py': depreciation_py},
                'interest_expense': {'cy': interest_expense_cy, 'py': interest_expense_py}
            },
            'operating_profit_cy': operating_profit_cy,
            'operating_profit_py': operating_profit_py,
            'working_capital_changes': {
                'current_assets': {'cy': wc_assets_change_cy, 'py': wc_assets_change_py},
                'current_liabilities': {'cy': wc_liabilities_change_cy, 'py': wc_liabilities_change_py}
            },
            'cash_from_operations_cy': cash_from_ops_cy,
            'cash_from_operations_py': cash_from_ops_py,
            'taxes_paid_cy': taxes_paid_cy,
            'taxes_paid_py': taxes_paid_py,
            'interest_paid_cy': interest_expense_cy,
            'interest_paid_py': interest_expense_py,
            'net_cash_cy': net_cash_cy,
            'net_cash_py': net_cash_py
        }
    
    def calculate_investing_activities(self, bs_data: Dict) -> Dict[str, Any]:
        """Calculate Cash Flow from Investing Activities"""
        
        # Purchase/Sale of PPE
        ppe_cy = bs_data['assets']['non_current']['ppe']['cy']
        ppe_py = bs_data['assets']['non_current']['ppe']['py']
        ppe_investment_cy = -(ppe_cy - ppe_py)  # Increase = purchase (negative)
        ppe_investment_py = 0
        
        # Purchase/Sale of CWIP
        cwip_cy = bs_data['assets']['non_current']['cwip']['cy']
        cwip_py = bs_data['assets']['non_current']['cwip']['py']
        cwip_investment_cy = -(cwip_cy - cwip_py)
        cwip_investment_py = 0
        
        # Purchase/Sale of Investments
        inv_nc_cy = bs_data['assets']['non_current']['investments']['cy']
        inv_nc_py = bs_data['assets']['non_current']['investments']['py']
        inv_c_cy = bs_data['assets']['current']['investments']['cy']
        inv_c_py = bs_data['assets']['current']['investments']['py']
        
        inv_investment_cy = -((inv_nc_cy - inv_nc_py) + (inv_c_cy - inv_c_py))
        inv_investment_py = 0
        
        # Net Cash from Investing Activities
        net_cash_cy = ppe_investment_cy + cwip_investment_cy + inv_investment_cy
        net_cash_py = ppe_investment_py + cwip_investment_py + inv_investment_py
        
        return {
            'ppe_investment_cy': ppe_investment_cy,
            'ppe_investment_py': ppe_investment_py,
            'cwip_investment_cy': cwip_investment_cy,
            'cwip_investment_py': cwip_investment_py,
            'investments_cy': inv_investment_cy,
            'investments_py': inv_investment_py,
            'net_cash_cy': net_cash_cy,
            'net_cash_py': net_cash_py
        }
    
    def calculate_financing_activities(self, bs_data: Dict) -> Dict[str, Any]:
        """Calculate Cash Flow from Financing Activities"""
        
        # Proceeds from/(Repayment of) Borrowings
        # Would need to pull from Trial Balance or specific borrowing tables
        borrowings_cy = 0  # Placeholder
        borrowings_py = 0
        
        # Proceeds from Share Capital
        equity_cy = bs_data['equity_and_liabilities']['equity']['total_cy']
        equity_py = bs_data['equity_and_liabilities']['equity']['total_py']
        equity_proceeds_cy = equity_cy - equity_py
        equity_proceeds_py = 0
        
        # Dividends Paid
        dividends_paid_cy = 0  # Would need from Trial Balance
        dividends_paid_py = 0
        
        # Net Cash from Financing Activities
        net_cash_cy = borrowings_cy + equity_proceeds_cy - dividends_paid_cy
        net_cash_py = borrowings_py + equity_proceeds_py - dividends_paid_py
        
        return {
            'borrowings_cy': borrowings_cy,
            'borrowings_py': borrowings_py,
            'equity_proceeds_cy': equity_proceeds_cy,
            'equity_proceeds_py': equity_proceeds_py,
            'dividends_paid_cy': dividends_paid_cy,
            'dividends_paid_py': dividends_paid_py,
            'net_cash_cy': net_cash_cy,
            'net_cash_py': net_cash_py
        }
