"""Property, Plant & Equipment (PPE) Model - Schedule III Note 1"""

from config.database import get_connection
from datetime import datetime

class PPE:
    """
    Property, Plant & Equipment model with CY & PY support
    Represents Schedule III Note 1 - Property, Plant and Equipment
    """
    
    def __init__(self, ppe_id=None, company_id=None, asset_class=None,
                 opening_gross_block_cy=0.0, additions_cy=0.0, disposals_gross_cy=0.0, closing_gross_block_cy=0.0,
                 opening_acc_depreciation_cy=0.0, depreciation_for_year_cy=0.0, 
                 acc_depr_on_disposals_cy=0.0, closing_acc_depreciation_cy=0.0,
                 opening_gross_block_py=0.0, additions_py=0.0, disposals_gross_py=0.0, closing_gross_block_py=0.0,
                 opening_acc_depreciation_py=0.0, depreciation_for_year_py=0.0,
                 acc_depr_on_disposals_py=0.0, closing_acc_depreciation_py=0.0,
                 depreciation_rate=0.0, useful_life_years=0):
        self.ppe_id = ppe_id
        self.company_id = company_id
        self.asset_class = asset_class
        
        # Current Year
        self.opening_gross_block_cy = opening_gross_block_cy or 0.0
        self.additions_cy = additions_cy or 0.0
        self.disposals_gross_cy = disposals_gross_cy or 0.0
        self.closing_gross_block_cy = closing_gross_block_cy or 0.0
        
        self.opening_acc_depreciation_cy = opening_acc_depreciation_cy or 0.0
        self.depreciation_for_year_cy = depreciation_for_year_cy or 0.0
        self.acc_depr_on_disposals_cy = acc_depr_on_disposals_cy or 0.0
        self.closing_acc_depreciation_cy = closing_acc_depreciation_cy or 0.0
        
        # Previous Year
        self.opening_gross_block_py = opening_gross_block_py or 0.0
        self.additions_py = additions_py or 0.0
        self.disposals_gross_py = disposals_gross_py or 0.0
        self.closing_gross_block_py = closing_gross_block_py or 0.0
        
        self.opening_acc_depreciation_py = opening_acc_depreciation_py or 0.0
        self.depreciation_for_year_py = depreciation_for_year_py or 0.0
        self.acc_depr_on_disposals_py = acc_depr_on_disposals_py or 0.0
        self.closing_acc_depreciation_py = closing_acc_depreciation_py or 0.0
        
        self.depreciation_rate = depreciation_rate or 0.0
        self.useful_life_years = useful_life_years or 0
    
    def calculate_closing_gross_block_cy(self):
        """Calculate closing gross block for CY"""
        return self.opening_gross_block_cy + self.additions_cy - self.disposals_gross_cy
    
    def calculate_closing_acc_depreciation_cy(self):
        """Calculate closing accumulated depreciation for CY"""
        return (self.opening_acc_depreciation_cy + self.depreciation_for_year_cy - 
                self.acc_depr_on_disposals_cy)
    
    def calculate_net_block_cy(self):
        """Calculate net block (WDV) for CY"""
        return self.closing_gross_block_cy - self.closing_acc_depreciation_cy
    
    def calculate_closing_gross_block_py(self):
        """Calculate closing gross block for PY"""
        return self.opening_gross_block_py + self.additions_py - self.disposals_gross_py
    
    def calculate_closing_acc_depreciation_py(self):
        """Calculate closing accumulated depreciation for PY"""
        return (self.opening_acc_depreciation_py + self.depreciation_for_year_py - 
                self.acc_depr_on_disposals_py)
    
    def calculate_net_block_py(self):
        """Calculate net block (WDV) for PY"""
        return self.closing_gross_block_py - self.closing_acc_depreciation_py
    
    @staticmethod
    def get_all_by_company(company_id):
        """Get all PPE entries for a company"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT ppe_id, company_id, asset_class,
                   opening_gross_block_cy, additions_cy, disposals_gross_cy, closing_gross_block_cy,
                   opening_acc_depreciation_cy, depreciation_for_year_cy, 
                   acc_depr_on_disposals_cy, closing_acc_depreciation_cy,
                   opening_gross_block_py, additions_py, disposals_gross_py, closing_gross_block_py,
                   opening_acc_depreciation_py, depreciation_for_year_py,
                   acc_depr_on_disposals_py, closing_acc_depreciation_py,
                   depreciation_rate, useful_life_years
            FROM ppe_schedule
            WHERE company_id = ?
            ORDER BY asset_class
        ''', (company_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        ppe_list = []
        for row in results:
            ppe_list.append(PPE(*row))
        
        return ppe_list
    
    @staticmethod
    def get_by_id(ppe_id):
        """Get PPE entry by ID"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT ppe_id, company_id, asset_class,
                   opening_gross_block_cy, additions_cy, disposals_gross_cy, closing_gross_block_cy,
                   opening_acc_depreciation_cy, depreciation_for_year_cy,
                   acc_depr_on_disposals_cy, closing_acc_depreciation_cy,
                   opening_gross_block_py, additions_py, disposals_gross_py, closing_gross_block_py,
                   opening_acc_depreciation_py, depreciation_for_year_py,
                   acc_depr_on_disposals_py, closing_acc_depreciation_py,
                   depreciation_rate, useful_life_years
            FROM ppe_schedule
            WHERE ppe_id = ?
        ''', (ppe_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return PPE(*row)
        return None
    
    @staticmethod
    def create(company_id, asset_class, 
               opening_gross_block_cy=0.0, additions_cy=0.0, disposals_gross_cy=0.0,
               opening_acc_depreciation_cy=0.0, depreciation_for_year_cy=0.0, acc_depr_on_disposals_cy=0.0,
               opening_gross_block_py=0.0, additions_py=0.0, disposals_gross_py=0.0,
               opening_acc_depreciation_py=0.0, depreciation_for_year_py=0.0, acc_depr_on_disposals_py=0.0,
               depreciation_rate=0.0, useful_life_years=0):
        """Create a new PPE entry"""
        conn = get_connection()
        cursor = conn.cursor()
        
        # Calculate closing values
        closing_gross_block_cy = opening_gross_block_cy + additions_cy - disposals_gross_cy
        closing_acc_depreciation_cy = (opening_acc_depreciation_cy + depreciation_for_year_cy - 
                                       acc_depr_on_disposals_cy)
        
        closing_gross_block_py = opening_gross_block_py + additions_py - disposals_gross_py
        closing_acc_depreciation_py = (opening_acc_depreciation_py + depreciation_for_year_py - 
                                       acc_depr_on_disposals_py)
        
        try:
            cursor.execute('''
                INSERT INTO ppe_schedule (
                    company_id, asset_class,
                    opening_gross_block_cy, additions_cy, disposals_gross_cy, closing_gross_block_cy,
                    opening_acc_depreciation_cy, depreciation_for_year_cy,
                    acc_depr_on_disposals_cy, closing_acc_depreciation_cy,
                    opening_gross_block_py, additions_py, disposals_gross_py, closing_gross_block_py,
                    opening_acc_depreciation_py, depreciation_for_year_py,
                    acc_depr_on_disposals_py, closing_acc_depreciation_py,
                    depreciation_rate, useful_life_years
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (company_id, asset_class,
                  opening_gross_block_cy, additions_cy, disposals_gross_cy, closing_gross_block_cy,
                  opening_acc_depreciation_cy, depreciation_for_year_cy,
                  acc_depr_on_disposals_cy, closing_acc_depreciation_cy,
                  opening_gross_block_py, additions_py, disposals_gross_py, closing_gross_block_py,
                  opening_acc_depreciation_py, depreciation_for_year_py,
                  acc_depr_on_disposals_py, closing_acc_depreciation_py,
                  depreciation_rate, useful_life_years))
            
            ppe_id = cursor.lastrowid
            conn.commit()
            return ppe_id
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    @staticmethod
    def update(ppe_id, asset_class,
               opening_gross_block_cy=0.0, additions_cy=0.0, disposals_gross_cy=0.0,
               opening_acc_depreciation_cy=0.0, depreciation_for_year_cy=0.0, acc_depr_on_disposals_cy=0.0,
               opening_gross_block_py=0.0, additions_py=0.0, disposals_gross_py=0.0,
               opening_acc_depreciation_py=0.0, depreciation_for_year_py=0.0, acc_depr_on_disposals_py=0.0,
               depreciation_rate=0.0, useful_life_years=0):
        """Update an existing PPE entry"""
        conn = get_connection()
        cursor = conn.cursor()
        
        # Calculate closing values
        closing_gross_block_cy = opening_gross_block_cy + additions_cy - disposals_gross_cy
        closing_acc_depreciation_cy = (opening_acc_depreciation_cy + depreciation_for_year_cy - 
                                       acc_depr_on_disposals_cy)
        
        closing_gross_block_py = opening_gross_block_py + additions_py - disposals_gross_py
        closing_acc_depreciation_py = (opening_acc_depreciation_py + depreciation_for_year_py - 
                                       acc_depr_on_disposals_py)
        
        try:
            cursor.execute('''
                UPDATE ppe_schedule SET
                    asset_class = ?,
                    opening_gross_block_cy = ?, additions_cy = ?, disposals_gross_cy = ?,
                    closing_gross_block_cy = ?,
                    opening_acc_depreciation_cy = ?, depreciation_for_year_cy = ?,
                    acc_depr_on_disposals_cy = ?, closing_acc_depreciation_cy = ?,
                    opening_gross_block_py = ?, additions_py = ?, disposals_gross_py = ?,
                    closing_gross_block_py = ?,
                    opening_acc_depreciation_py = ?, depreciation_for_year_py = ?,
                    acc_depr_on_disposals_py = ?, closing_acc_depreciation_py = ?,
                    depreciation_rate = ?, useful_life_years = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE ppe_id = ?
            ''', (asset_class,
                  opening_gross_block_cy, additions_cy, disposals_gross_cy, closing_gross_block_cy,
                  opening_acc_depreciation_cy, depreciation_for_year_cy,
                  acc_depr_on_disposals_cy, closing_acc_depreciation_cy,
                  opening_gross_block_py, additions_py, disposals_gross_py, closing_gross_block_py,
                  opening_acc_depreciation_py, depreciation_for_year_py,
                  acc_depr_on_disposals_py, closing_acc_depreciation_py,
                  depreciation_rate, useful_life_years, ppe_id))
            
            conn.commit()
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    @staticmethod
    def delete(ppe_id):
        """Delete a PPE entry"""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM ppe_schedule WHERE ppe_id = ?', (ppe_id,))
            conn.commit()
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    @staticmethod
    def get_schedule_iii_format(company_id):
        """
        Get PPE data in Schedule III format with calculations
        Returns list of dicts with all required columns
        """
        ppe_list = PPE.get_all_by_company(company_id)
        
        schedule_data = []
        for ppe in ppe_list:
            schedule_data.append({
                'asset_class': ppe.asset_class,
                # Current Year - Gross Block
                'gross_block_opening_cy': ppe.opening_gross_block_cy,
                'gross_block_additions_cy': ppe.additions_cy,
                'gross_block_disposals_cy': ppe.disposals_gross_cy,
                'gross_block_closing_cy': ppe.calculate_closing_gross_block_cy(),
                # Current Year - Depreciation
                'depreciation_opening_cy': ppe.opening_acc_depreciation_cy,
                'depreciation_for_year_cy': ppe.depreciation_for_year_cy,
                'depreciation_on_disposals_cy': ppe.acc_depr_on_disposals_cy,
                'depreciation_closing_cy': ppe.calculate_closing_acc_depreciation_cy(),
                # Current Year - Net Block
                'net_block_opening_cy': ppe.opening_gross_block_cy - ppe.opening_acc_depreciation_cy,
                'net_block_closing_cy': ppe.calculate_net_block_cy(),
                # Previous Year - Gross Block
                'gross_block_opening_py': ppe.opening_gross_block_py,
                'gross_block_additions_py': ppe.additions_py,
                'gross_block_disposals_py': ppe.disposals_gross_py,
                'gross_block_closing_py': ppe.calculate_closing_gross_block_py(),
                # Previous Year - Depreciation
                'depreciation_opening_py': ppe.opening_acc_depreciation_py,
                'depreciation_for_year_py': ppe.depreciation_for_year_py,
                'depreciation_on_disposals_py': ppe.acc_depr_on_disposals_py,
                'depreciation_closing_py': ppe.calculate_closing_acc_depreciation_py(),
                # Previous Year - Net Block
                'net_block_opening_py': ppe.opening_gross_block_py - ppe.opening_acc_depreciation_py,
                'net_block_closing_py': ppe.calculate_net_block_py(),
                # Metadata
                'depreciation_rate': ppe.depreciation_rate,
                'useful_life': ppe.useful_life_years
            })
        
        return schedule_data
