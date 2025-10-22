"""
Trial Balance Model
Handles Trial Balance import, storage, and mapping with comparative year support
"""

from config.database import get_connection
from datetime import datetime


class TrialBalance:
    """Model for Trial Balance entries with current and previous year data"""
    
    def __init__(self, tb_id, company_id, ledger_name, 
                 opening_balance_cy=0, debit_cy=0, credit_cy=0, closing_balance_cy=0,
                 opening_balance_py=0, debit_py=0, credit_py=0, closing_balance_py=0,
                 type_bs_pl='BS', major_head_id=None, minor_head_id=None, 
                 grouping_id=None, is_mapped=0, import_batch_id=None):
        self.tb_id = tb_id
        self.company_id = company_id
        self.ledger_name = ledger_name
        
        # Current Year (CY) data
        self.opening_balance_cy = opening_balance_cy
        self.debit_cy = debit_cy
        self.credit_cy = credit_cy
        self.closing_balance_cy = closing_balance_cy
        
        # Previous Year (PY) data for comparatives
        self.opening_balance_py = opening_balance_py
        self.debit_py = debit_py
        self.credit_py = credit_py
        self.closing_balance_py = closing_balance_py
        
        # Classification and mapping
        self.type_bs_pl = type_bs_pl
        self.major_head_id = major_head_id
        self.minor_head_id = minor_head_id
        self.grouping_id = grouping_id
        self.is_mapped = is_mapped
        self.import_batch_id = import_batch_id
    
    @staticmethod
    def create(company_id, ledger_name, 
               opening_balance_cy=0, debit_cy=0, credit_cy=0, closing_balance_cy=0,
               opening_balance_py=0, debit_py=0, credit_py=0, closing_balance_py=0,
               type_bs_pl='BS', major_head_id=None, minor_head_id=None,
               grouping_id=None, is_mapped=0, import_batch_id=None):
        """Create new trial balance entry"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO trial_balance (
                    company_id, ledger_name,
                    opening_balance_cy, debit_cy, credit_cy, closing_balance_cy,
                    opening_balance_py, debit_py, credit_py, closing_balance_py,
                    type_bs_pl, major_head_id, minor_head_id, grouping_id,
                    is_mapped, import_batch_id, created_at, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING tb_id
            ''', (company_id, ledger_name,
                  opening_balance_cy, debit_cy, credit_cy, closing_balance_cy,
                  opening_balance_py, debit_py, credit_py, closing_balance_py,
                  type_bs_pl, major_head_id, minor_head_id, grouping_id,
                  is_mapped, import_batch_id,
                  datetime.now(), datetime.now()))
            
            tb_id = cursor.fetchone()[0]
            conn.commit()
            return tb_id
        
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def get_by_company(company_id, import_batch_id=None):
        """Get all trial balance entries for a company"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            if import_batch_id:
                cursor.execute('''
                    SELECT tb_id, company_id, ledger_name,
                           opening_balance_cy, debit_cy, credit_cy, closing_balance_cy,
                           opening_balance_py, debit_py, credit_py, closing_balance_py,
                           type_bs_pl, major_head_id, minor_head_id, grouping_id,
                           is_mapped, import_batch_id
                    FROM trial_balance
                    WHERE company_id = %s AND import_batch_id = %s
                    ORDER BY ledger_name
                ''', (company_id, import_batch_id))
            else:
                cursor.execute('''
                    SELECT tb_id, company_id, ledger_name,
                           opening_balance_cy, debit_cy, credit_cy, closing_balance_cy,
                           opening_balance_py, debit_py, credit_py, closing_balance_py,
                           type_bs_pl, major_head_id, minor_head_id, grouping_id,
                           is_mapped, import_batch_id
                    FROM trial_balance
                    WHERE company_id = %s
                    ORDER BY ledger_name
                ''', (company_id,))
            
            results = cursor.fetchall()
            return [TrialBalance(*row) for row in results]
        
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def get_unmapped(company_id, import_batch_id=None):
        """Get unmapped trial balance entries"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            if import_batch_id:
                cursor.execute('''
                    SELECT tb_id, company_id, ledger_name,
                           opening_balance_cy, debit_cy, credit_cy, closing_balance_cy,
                           opening_balance_py, debit_py, credit_py, closing_balance_py,
                           type_bs_pl, major_head_id, minor_head_id, grouping_id,
                           is_mapped, import_batch_id
                    FROM trial_balance
                    WHERE company_id = %s AND is_mapped = 0 AND import_batch_id = %s
                    ORDER BY ledger_name
                ''', (company_id, import_batch_id))
            else:
                cursor.execute('''
                    SELECT tb_id, company_id, ledger_name,
                           opening_balance_cy, debit_cy, credit_cy, closing_balance_cy,
                           opening_balance_py, debit_py, credit_py, closing_balance_py,
                           type_bs_pl, major_head_id, minor_head_id, grouping_id,
                           is_mapped, import_batch_id
                    FROM trial_balance
                    WHERE company_id = %s AND is_mapped = 0
                    ORDER BY ledger_name
                ''', (company_id,))
            
            results = cursor.fetchall()
            return [TrialBalance(*row) for row in results]
        
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def update_mapping(tb_id, major_head_id, minor_head_id, grouping_id, type_bs_pl='BS'):
        """Update trial balance mapping"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE trial_balance
                SET major_head_id = %s, minor_head_id = %s, grouping_id = %s,
                    type_bs_pl = %s, is_mapped = 1, updated_at = %s
                WHERE tb_id = %s
            ''', (major_head_id, minor_head_id, grouping_id, type_bs_pl,
                  datetime.now(), tb_id))
            
            conn.commit()
        
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def update_values(tb_id, opening_balance_cy=None, debit_cy=None, credit_cy=None, 
                     closing_balance_cy=None, opening_balance_py=None, debit_py=None,
                     credit_py=None, closing_balance_py=None):
        """Update trial balance values"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Build dynamic update query
            updates = []
            params = []
            
            if opening_balance_cy is not None:
                updates.append("opening_balance_cy = %s")
                params.append(opening_balance_cy)
            if debit_cy is not None:
                updates.append("debit_cy = %s")
                params.append(debit_cy)
            if credit_cy is not None:
                updates.append("credit_cy = %s")
                params.append(credit_cy)
            if closing_balance_cy is not None:
                updates.append("closing_balance_cy = %s")
                params.append(closing_balance_cy)
            
            if opening_balance_py is not None:
                updates.append("opening_balance_py = %s")
                params.append(opening_balance_py)
            if debit_py is not None:
                updates.append("debit_py = %s")
                params.append(debit_py)
            if credit_py is not None:
                updates.append("credit_py = %s")
                params.append(credit_py)
            if closing_balance_py is not None:
                updates.append("closing_balance_py = %s")
                params.append(closing_balance_py)
            
            if updates:
                updates.append("updated_at = %s")
                params.append(datetime.now())
                params.append(tb_id)
                
                query = f"UPDATE trial_balance SET {', '.join(updates)} WHERE tb_id = %s"
                cursor.execute(query, params)
                
                conn.commit()
        
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def delete(tb_id):
        """Delete trial balance entry"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM trial_balance WHERE tb_id = %s', (tb_id,))
            
            conn.commit()
        
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def delete_by_company(company_id, import_batch_id=None):
        """Delete all trial balance entries for a company"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            if import_batch_id:
                cursor.execute('DELETE FROM trial_balance WHERE company_id = %s AND import_batch_id = %s',
                              (company_id, import_batch_id))
            else:
                cursor.execute('DELETE FROM trial_balance WHERE company_id = %s', (company_id,))
            
            conn.commit()
        
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def validate_balance(company_id, import_batch_id=None):
        """
        Validate that trial balance is balanced for both current and previous year
        Returns tuple: (cy_balanced, py_balanced, cy_diff, py_diff)
        """
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            if import_batch_id:
                cursor.execute('''
                    SELECT 
                        SUM(debit_cy) as total_debit_cy,
                        SUM(credit_cy) as total_credit_cy,
                        SUM(debit_py) as total_debit_py,
                        SUM(credit_py) as total_credit_py
                    FROM trial_balance
                    WHERE company_id = %s AND import_batch_id = %s
                ''', (company_id, import_batch_id))
            else:
                cursor.execute('''
                    SELECT 
                        SUM(debit_cy) as total_debit_cy,
                        SUM(credit_cy) as total_credit_cy,
                        SUM(debit_py) as total_debit_py,
                        SUM(credit_py) as total_credit_py
                    FROM trial_balance
                    WHERE company_id = %s
                ''', (company_id,))
            
            result = cursor.fetchone()
            
            if result:
                total_debit_cy = result[0] or 0
                total_credit_cy = result[1] or 0
                total_debit_py = result[2] or 0
                total_credit_py = result[3] or 0
                
                cy_diff = abs(total_debit_cy - total_credit_cy)
                py_diff = abs(total_debit_py - total_credit_py)
                
                # Consider balanced if difference is less than 1 rupee (rounding tolerance)
                cy_balanced = cy_diff < 1
                py_balanced = py_diff < 1
                
                return (cy_balanced, py_balanced, cy_diff, py_diff)
            
            return (False, False, 0, 0)
        
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def get_summary_stats(company_id, import_batch_id=None):
        """Get summary statistics for trial balance"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            if import_batch_id:
                cursor.execute('''
                    SELECT 
                        COUNT(*) as total_entries,
                        SUM(CASE WHEN is_mapped = 1 THEN 1 ELSE 0 END) as mapped_entries,
                        SUM(debit_cy) as total_debit_cy,
                        SUM(credit_cy) as total_credit_cy,
                        SUM(debit_py) as total_debit_py,
                        SUM(credit_py) as total_credit_py
                    FROM trial_balance
                    WHERE company_id = %s AND import_batch_id = %s
                ''', (company_id, import_batch_id))
            else:
                cursor.execute('''
                    SELECT 
                        COUNT(*) as total_entries,
                        SUM(CASE WHEN is_mapped = 1 THEN 1 ELSE 0 END) as mapped_entries,
                        SUM(debit_cy) as total_debit_cy,
                        SUM(credit_cy) as total_credit_cy,
                        SUM(debit_py) as total_debit_py,
                        SUM(credit_py) as total_credit_py
                    FROM trial_balance
                    WHERE company_id = %s
                ''', (company_id,))
            
            result = cursor.fetchone()
            
            if result:
                return {
                    'total_entries': result[0] or 0,
                    'mapped_entries': result[1] or 0,
                    'unmapped_entries': (result[0] or 0) - (result[1] or 0),
                    'total_debit_cy': result[2] or 0,
                    'total_credit_cy': result[3] or 0,
                    'total_debit_py': result[4] or 0,
                    'total_credit_py': result[5] or 0,
                    'cy_difference': abs((result[2] or 0) - (result[3] or 0)),
                    'py_difference': abs((result[4] or 0) - (result[5] or 0))
                }
            
            return {
                'total_entries': 0,
                'mapped_entries': 0,
                'unmapped_entries': 0,
                'total_debit_cy': 0,
                'total_credit_cy': 0,
                'total_debit_py': 0,
                'total_credit_py': 0,
                'cy_difference': 0,
                'py_difference': 0
            }
        
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def bulk_import(company_id, entries, import_batch_id):
        """
        Bulk import trial balance entries
        entries: list of dicts with keys matching column names
        """
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            for entry in entries:
                cursor.execute('''
                    INSERT INTO trial_balance (
                        company_id, ledger_name,
                        opening_balance_cy, debit_cy, credit_cy, closing_balance_cy,
                        opening_balance_py, debit_py, credit_py, closing_balance_py,
                        type_bs_pl, major_head_id, minor_head_id, grouping_id,
                        is_mapped, import_batch_id, created_at, updated_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (
                    company_id,
                    entry.get('ledger_name', ''),
                    entry.get('opening_balance_cy', 0),
                    entry.get('debit_cy', 0),
                    entry.get('credit_cy', 0),
                    entry.get('closing_balance_cy', 0),
                    entry.get('opening_balance_py', 0),
                    entry.get('debit_py', 0),
                    entry.get('credit_py', 0),
                    entry.get('closing_balance_py', 0),
                    entry.get('type_bs_pl', 'BS'),
                    entry.get('major_head_id'),
                    entry.get('minor_head_id'),
                    entry.get('grouping_id'),
                    entry.get('is_mapped', 0),
                    import_batch_id,
                    datetime.now(),
                    datetime.now()
                ))
            
            conn.commit()
            return len(entries)
        
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        
        finally:
            if conn:
                conn.close()
