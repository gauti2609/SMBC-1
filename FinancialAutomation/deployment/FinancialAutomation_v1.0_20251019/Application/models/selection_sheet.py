"""
Selection Sheet Model
Manages note selection for financial statements based on Trial Balance analysis
"""

from config.database import get_connection
from typing import List, Dict, Optional, Tuple


class SelectionSheet:
    """Model for Selection Sheet entries"""
    
    def __init__(self, selection_id, company_id, note_ref, note_description,
                 linked_major_head=None, system_recommendation='No',
                 user_selection='No', final_selection='No', auto_number=None):
        self.selection_id = selection_id
        self.company_id = company_id
        self.note_ref = note_ref
        self.note_description = note_description
        self.linked_major_head = linked_major_head
        self.system_recommendation = system_recommendation
        self.user_selection = user_selection
        self.final_selection = final_selection
        self.auto_number = auto_number
    
    @staticmethod
    def initialize_default_notes(company_id: int):
        """Initialize default note structure for a company"""
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if already initialized
        cursor.execute('SELECT COUNT(*) FROM selection_sheet WHERE company_id = ?', (company_id,))
        if cursor.fetchone()[0] > 0:
            conn.close()
            return  # Already initialized
        
        # Default note structure (from VBA)
        notes_data = [
            # A. General notes and policies (mandatory)
            ('A', 'General notes and policies (mandatory)', None),
            ('A.1', 'Corporate information and basis of preparation', None),
            ('A.2', 'Significant accounting policies', None),
            ('A.2.1', 'Revenue recognition (AS 9)', 'Revenue from Operations'),
            ('A.2.2', 'Property, Plant and Equipment (PPE) and depreciation (AS 10)', 'Property, Plant and Equipment'),
            ('A.2.3', 'Intangible assets and amortization (AS 26)', 'Intangible Assets'),
            ('A.2.4', 'Impairment of assets (AS 28)', None),
            ('A.2.5', 'Inventories valuation and cost formula (AS 2)', 'Inventories'),
            ('A.2.6', 'Investments classification and valuation (AS 13)', 'Non-current Investments'),
            ('A.2.7', 'Foreign currency transactions and translation (AS 11)', None),
            ('A.2.8', 'Employee benefits (AS 15)', 'Employee Benefits Expense'),
            ('A.2.9', 'Borrowing costs and capitalization policy (AS 16)', 'Finance Costs'),
            ('A.2.10', 'Provisions, contingent liabilities, contingent assets (AS 29)', 'Long-term Provisions'),
            ('A.2.11', 'Taxes on income (current/deferred; AS 22)', 'Taxes on Income'),
            ('A.2.12', 'Government grants (AS 12)', None),
            ('A.2.13', 'Construction contracts revenue (AS 7)', None),
            ('A.2.14', 'Leases classification (AS 19)', None),
            ('A.2.15', 'Segment reporting basis (AS 17)', None),
            ('A.2.16', 'Cash and cash equivalents definition (AS 3)', 'Cash and Cash Equivalents'),
            
            # B. Equity and liabilities notes
            ('B', 'Equity and liabilities notes', None),
            ('B.1', 'Share capital', 'Equity Share Capital'),
            ('B.2', 'Reserves and surplus / other equity', 'Other Equity'),
            ('B.3', 'Long-term and short-term borrowings', 'Long-term Borrowings'),
            ('B.4', 'Trade payables', 'Trade Payables'),
            ('B.5', 'Other financial liabilities and provisions', 'Other Current Liabilities'),
            ('B.6', 'Other non-financial liabilities', 'Other Long-term Liabilities'),
            ('B.7', 'Employee benefit obligations (AS 15)', 'Long-term Provisions'),
            
            # C. Assets notes
            ('C', 'Assets notes', None),
            ('C.1', 'Property, plant and equipment (AS 10 + Schedule III)', 'Property, Plant and Equipment'),
            ('C.2', 'Capital work-in-progress (CWIP)', None),
            ('C.3', 'Intangible assets and Intangible assets under development', 'Intangible Assets'),
            ('C.4', 'Investments (AS 13)', 'Non-current Investments'),
            ('C.5', 'Inventories (AS 2)', 'Inventories'),
            ('C.6', 'Trade receivables', 'Trade Receivables'),
            ('C.7', 'Cash and cash equivalents', 'Cash and Cash Equivalents'),
            ('C.8', 'Loans, advances, and other assets', 'Long-term Loans and Advances'),
            
            # D. Profit and Loss notes
            ('D', 'Profit and Loss notes', None),
            ('D.1', 'Revenue from operations (AS 9)', 'Revenue from Operations'),
            ('D.2', 'Other income', 'Other Income'),
            ('D.3', 'Cost of materials consumed; Purchases; Changes in inventories', 'Cost of Materials Consumed'),
            ('D.4', 'Employee benefits expense (AS 15)', 'Employee Benefits Expense'),
            ('D.5', 'Finance costs (AS 16)', 'Finance Costs'),
            ('D.6', 'Depreciation and amortization expense', 'Depreciation and Amortization'),
            ('D.7', 'Other expenses (incl. CSR, Auditor Payments)', 'Other Expenses'),
            ('D.8', 'Exceptional items and extraordinary items (AS 5)', 'Exceptional Items'),
            ('D.9', 'Prior period items disclosure (AS 5)', 'Prior Period Items'),
            ('D.10', 'Earnings per share (AS 20)', None),
            ('D.11', 'Income taxes (AS 22)', 'Taxes on Income'),
            
            # E. AS-specific and cross-cutting disclosures
            ('E', 'AS-specific and cross-cutting disclosures', None),
            ('E.1', 'AS 3 Cash Flow Statement details', None),
            ('E.2', 'Events occurring after the balance sheet date', None),
            ('E.3', 'AS 18 Related party disclosures', None),
            ('E.4', 'AS 19 Leases', None),
            ('E.5', 'Contingent Liabilities and Commitments (AS 29)', None),
            
            # F. Additional Schedule III (2021) Disclosures
            ('F', 'Additional Schedule III (2021) Disclosures', None),
            ('F.1', 'Utilization of borrowed funds and share premium', None),
            ('F.2', 'Title deeds of immovable properties not in company\'s name', None),
            ('F.3', 'Proceedings for Benami property', None),
            ('F.4', 'Wilful defaulter status', None),
            ('F.5', 'Relationship with struck-off companies', None),
            ('F.6', 'Crypto/virtual currency holdings', None),
            ('F.7', 'Undisclosed income surrendered in tax assessments', None),
            ('F.8', 'Ratios with variance >25% explanations', None),
            ('F.9', 'Aging schedules: Receivables, Payables, CWIP, Intangibles under dev.', None),
            ('F.10', 'Unspent CSR amounts', None),
            
            # G. Other Statutory Disclosures
            ('G', 'Other Statutory Disclosures', None),
            ('G.1', 'Managerial remuneration (Section 197)', None),
            ('G.2', 'MSME Disclosures (Principal and Interest due)', None),
        ]
        
        # Insert all notes
        for note_ref, description, linked_major_head in notes_data:
            cursor.execute('''
                INSERT INTO selection_sheet 
                (company_id, note_ref, note_description, linked_major_head, 
                 system_recommendation, user_selection, final_selection)
                VALUES (?, ?, ?, ?, 'No', 'No', 'No')
            ''', (company_id, note_ref, description, linked_major_head))
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_all_for_company(company_id: int) -> List['SelectionSheet']:
        """Get all selection sheet entries for a company"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT selection_id, company_id, note_ref, note_description,
                   linked_major_head, system_recommendation, user_selection,
                   final_selection, auto_number
            FROM selection_sheet
            WHERE company_id = ?
            ORDER BY note_ref
        ''', (company_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [SelectionSheet(*row) for row in results]
    
    @staticmethod
    def update_system_recommendations(company_id: int):
        """Update system recommendations based on Trial Balance major heads"""
        from models.trial_balance import TrialBalance
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get all major heads from Trial Balance
        tb_entries = TrialBalance.get_by_company(company_id)
        major_heads = set()
        
        for entry in tb_entries:
            if entry.major_head_id:
                from models.master_data import MajorHead
                major_head = MajorHead.get_by_id(entry.major_head_id)
                if major_head:
                    major_heads.add(major_head.major_head_name)
        
        # Update recommendations based on linked major heads
        cursor.execute('''
            SELECT selection_id, linked_major_head
            FROM selection_sheet
            WHERE company_id = ?
        ''', (company_id,))
        
        for selection_id, linked_major_head in cursor.fetchall():
            if linked_major_head and linked_major_head in major_heads:
                recommendation = 'Yes'
            else:
                recommendation = 'No'
            
            cursor.execute('''
                UPDATE selection_sheet
                SET system_recommendation = ?
                WHERE selection_id = ?
            ''', (recommendation, selection_id))
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def update_user_selection(selection_id: int, user_selection: str):
        """Update user selection for a note"""
        conn = get_connection()
        cursor = conn.cursor()
        
        # Update user selection
        cursor.execute('''
            UPDATE selection_sheet
            SET user_selection = ?
            WHERE selection_id = ?
        ''', (user_selection, selection_id))
        
        # Update final selection logic: User overrides system
        cursor.execute('''
            UPDATE selection_sheet
            SET final_selection = CASE
                WHEN user_selection = 'Yes' THEN 'Yes'
                WHEN user_selection = 'No' THEN 'No'
                WHEN user_selection = '' AND system_recommendation = 'Yes' THEN 'Yes'
                ELSE 'No'
            END
            WHERE selection_id = ?
        ''', (selection_id,))
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def update_auto_numbering(company_id: int):
        """Update auto-numbering for selected notes"""
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get all notes with final_selection = 'Yes', ordered by note_ref
        cursor.execute('''
            SELECT selection_id, note_ref
            FROM selection_sheet
            WHERE company_id = ? AND final_selection = 'Yes'
            ORDER BY note_ref
        ''', (company_id,))
        
        results = cursor.fetchall()
        auto_number = 1
        
        for selection_id, note_ref in results:
            # Skip section headers (no dot in note_ref)
            if '.' in note_ref:
                cursor.execute('''
                    UPDATE selection_sheet
                    SET auto_number = ?
                    WHERE selection_id = ?
                ''', (str(auto_number), selection_id))
                auto_number += 1
            else:
                # Clear auto_number for section headers
                cursor.execute('''
                    UPDATE selection_sheet
                    SET auto_number = NULL
                    WHERE selection_id = ?
                ''', (selection_id,))
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_selected_notes(company_id: int) -> List[Tuple[str, str, str]]:
        """Get all selected notes with their auto-numbers"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT note_ref, note_description, auto_number
            FROM selection_sheet
            WHERE company_id = ? AND final_selection = 'Yes'
            ORDER BY note_ref
        ''', (company_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    @staticmethod
    def bulk_update_user_selections(company_id: int, selections: Dict[int, str]):
        """Bulk update user selections"""
        conn = get_connection()
        cursor = conn.cursor()
        
        for selection_id, user_selection in selections.items():
            cursor.execute('''
                UPDATE selection_sheet
                SET user_selection = ?
                WHERE selection_id = ? AND company_id = ?
            ''', (user_selection, selection_id, company_id))
        
        # Update final selections
        cursor.execute('''
            UPDATE selection_sheet
            SET final_selection = CASE
                WHEN user_selection = 'Yes' THEN 'Yes'
                WHEN user_selection = 'No' THEN 'No'
                WHEN user_selection = '' AND system_recommendation = 'Yes' THEN 'Yes'
                ELSE 'No'
            END
            WHERE company_id = ?
        ''', (company_id,))
        
        conn.commit()
        conn.close()
        
        # Update auto-numbering
        SelectionSheet.update_auto_numbering(company_id)
