"""Master data models for Major Heads, Minor Heads, and Groupings with CY & PY support"""

from config.database import get_connection

class MajorHead:
    """
    Major Head model with company-specific data and comparative year support
    """
    
    def __init__(self, major_head_id=None, company_id=None, major_head_name=None, 
                 category=None, opening_balance_cy=0.0, opening_balance_py=0.0, 
                 display_order=None):
        self.major_head_id = major_head_id
        self.company_id = company_id
        self.major_head_name = major_head_name
        self.category = category
        self.opening_balance_cy = opening_balance_cy or 0.0
        self.opening_balance_py = opening_balance_py or 0.0
        self.display_order = display_order
    
    @staticmethod
    def get_all_by_company(company_id):
        """Get all active major heads for a company"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT major_head_id, company_id, major_head_name, category,
                   opening_balance_cy, opening_balance_py, display_order
            FROM major_heads
            WHERE company_id = %s AND is_active = 1
            ORDER BY display_order, major_head_name
        ''', (company_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        major_heads = []
        for row in results:
            major_heads.append(MajorHead(
                major_head_id=row[0],
                company_id=row[1],
                major_head_name=row[2],
                category=row[3],
                opening_balance_cy=row[4] or 0.0,
                opening_balance_py=row[5] or 0.0,
                display_order=row[6]
            ))
        
        return major_heads
    
    @staticmethod
    def get_all():
        """DEPRECATED: Use get_all_by_company() instead. Kept for backward compatibility."""
        import warnings
        warnings.warn(
            "MajorHead.get_all() is deprecated. Use get_all_by_company(company_id) instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return []
    
    @staticmethod
    def get_by_id(major_head_id):
        """Get major head by ID - returns tuple"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT major_head_id, major_head_name, category, 
                   COALESCE(category, '') as description
            FROM major_heads
            WHERE major_head_id = %s AND is_active = 1
        ''', (major_head_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result
    
    @staticmethod
    def get_by_name(name):
        """Get major head by name"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT major_head_id, major_head_name, category, display_order
            FROM major_heads
            WHERE major_head_name = %s AND is_active = 1
        ''', (name,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            # Query returns: major_head_id, major_head_name, category, display_order
            # Constructor needs: major_head_id, company_id, major_head_name, category, ...
            return MajorHead(
                major_head_id=result[0],
                company_id=None,  # Not available from this query - will be set by caller if needed
                major_head_name=result[1],
                category=result[2],
                opening_balance_cy=0.0,
                opening_balance_py=0.0,
                display_order=result[3]
            )
        return None
    
    @staticmethod
    def create(company_id, major_head_name, category, opening_balance_cy=0.0, 
               opening_balance_py=0.0, description=None):
        """Create a new major head for a company"""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            # Get max display_order for this company
            cursor.execute(
                'SELECT MAX(display_order) FROM major_heads WHERE company_id = %s',
                (company_id,)
            )
            max_order = cursor.fetchone()[0]
            display_order = (max_order or 0) + 1
            
            cursor.execute('''
                INSERT INTO major_heads (company_id, major_head_name, category, 
                                        opening_balance_cy, opening_balance_py, display_order)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (company_id, major_head_name, category or description or '', 
                  opening_balance_cy or 0.0, opening_balance_py or 0.0, display_order))
            
            major_head_id = cursor.fetchone()[0]
            conn.commit()
            conn.close()
            return major_head_id
        except Exception as e:
            conn.close()
            raise e
    
    @staticmethod
    def update(major_head_id, major_head_name, category, opening_balance_cy=None, 
               opening_balance_py=None, description=None):
        """Update a major head"""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            if opening_balance_cy is not None and opening_balance_py is not None:
                cursor.execute('''
                    UPDATE major_heads
                    SET major_head_name = ?, category = ?, 
                        opening_balance_cy = ?, opening_balance_py = ?
                    WHERE major_head_id = %s
                ''', (major_head_name, category or description or '', 
                      opening_balance_cy, opening_balance_py, major_head_id))
            else:
                cursor.execute('''
                    UPDATE major_heads
                    SET major_head_name = ?, category = ?
                    WHERE major_head_id = %s
                ''', (major_head_name, category or description or '', major_head_id))
            
            conn.commit()
            conn.close()
        except Exception as e:
            conn.close()
            raise e
    
    @staticmethod
    def delete(major_head_id):
        """Soft delete a major head"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE major_heads
            SET is_active = 0
            WHERE major_head_id = %s
        ''', (major_head_id,))
        
        conn.commit()
        conn.close()


class MinorHead:
    """Minor Head model with company-specific data and comparative year support"""
    
    def __init__(self, minor_head_id=None, company_id=None, minor_head_name=None, 
                 major_head_id=None, opening_balance_cy=0.0, opening_balance_py=0.0, 
                 display_order=None):
        self.minor_head_id = minor_head_id
        self.company_id = company_id
        self.minor_head_name = minor_head_name
        self.major_head_id = major_head_id
        self.opening_balance_cy = opening_balance_cy or 0.0
        self.opening_balance_py = opening_balance_py or 0.0
        self.display_order = display_order
    
    @staticmethod
    def get_all(company_id=None, major_head_id=None):
        """Get all active minor heads, optionally filtered by company and major head - returns tuples"""
        conn = get_connection()
        cursor = conn.cursor()
        
        if company_id and major_head_id:
            cursor.execute('''
                SELECT minor_head_id, company_id, major_head_id, minor_head_name,
                       opening_balance_cy, opening_balance_py,
                       CAST(minor_head_id AS TEXT) as code, '' as description
                FROM minor_heads
                WHERE company_id = %s AND major_head_id = %s AND is_active = 1
                ORDER BY display_order, minor_head_name
            ''', (company_id, major_head_id))
        elif company_id:
            cursor.execute('''
                SELECT minor_head_id, company_id, major_head_id, minor_head_name,
                       opening_balance_cy, opening_balance_py,
                       CAST(minor_head_id AS TEXT) as code, '' as description
                FROM minor_heads
                WHERE company_id = %s AND is_active = 1
                ORDER BY major_head_id, display_order, minor_head_name
            ''', (company_id,))
        elif major_head_id:
            cursor.execute('''
                SELECT minor_head_id, company_id, major_head_id, minor_head_name,
                       opening_balance_cy, opening_balance_py,
                       CAST(minor_head_id AS TEXT) as code, '' as description
                FROM minor_heads
                WHERE major_head_id = %s AND is_active = 1
                ORDER BY display_order, minor_head_name
            ''', (major_head_id,))
        else:
            cursor.execute('''
                SELECT minor_head_id, company_id, major_head_id, minor_head_name,
                       opening_balance_cy, opening_balance_py,
                       CAST(minor_head_id AS TEXT) as code, '' as description
                FROM minor_heads
                WHERE is_active = 1
                ORDER BY company_id, major_head_id, display_order, minor_head_name
            ''')
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    @staticmethod
    def get_by_id(minor_head_id):
        """Get minor head by ID - returns tuple"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT minor_head_id, major_head_id, minor_head_name, 
                   CAST(minor_head_id AS TEXT) as code, '' as description
            FROM minor_heads
            WHERE minor_head_id = %s AND is_active = 1
        ''', (minor_head_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result
    
    @staticmethod
    def get_by_name_and_major(name, major_head_id):
        """Get minor head by name and major head"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT minor_head_id, minor_head_name, major_head_id, display_order
            FROM minor_heads
            WHERE minor_head_name = %s AND major_head_id = %s AND is_active = 1
        ''', (name, major_head_id))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return MinorHead(result[0], result[1], result[2], result[3])
        return None
    
    @staticmethod
    def create(company_id, major_head_id, minor_head_name, opening_balance_cy=0.0,
               opening_balance_py=0.0, code=None, description=None):
        """Create a new minor head for a company"""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            # Get max display_order for this major head and company
            cursor.execute(
                'SELECT MAX(display_order) FROM minor_heads WHERE company_id = %s AND major_head_id = %s',
                (company_id, major_head_id)
            )
            max_order = cursor.fetchone()[0]
            display_order = (max_order or 0) + 1
            
            cursor.execute('''
                INSERT INTO minor_heads (company_id, minor_head_name, major_head_id, 
                                        opening_balance_cy, opening_balance_py, display_order)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (company_id, minor_head_name, major_head_id, 
                  opening_balance_cy or 0.0, opening_balance_py or 0.0, display_order))
            
            minor_head_id = cursor.fetchone()[0]
            conn.commit()
            conn.close()
            return minor_head_id
        except Exception as e:
            conn.close()
            raise e
    
    @staticmethod
    def update(minor_head_id, major_head_id, minor_head_name, opening_balance_cy=None,
               opening_balance_py=None, code=None, description=None):
        """Update a minor head"""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            if opening_balance_cy is not None and opening_balance_py is not None:
                cursor.execute('''
                    UPDATE minor_heads
                    SET minor_head_name = %s, major_head_id = %s,
                        opening_balance_cy = %s, opening_balance_py = %s
                    WHERE minor_head_id = %s
                ''', (minor_head_name, major_head_id, opening_balance_cy, opening_balance_py, minor_head_id))
            else:
                cursor.execute('''
                    UPDATE minor_heads
                    SET minor_head_name = %s, major_head_id = %s
                    WHERE minor_head_id = %s
                ''', (minor_head_name, major_head_id, minor_head_id))
            
            conn.commit()
            conn.close()
        except Exception as e:
            conn.close()
            raise e
    
    @staticmethod
    def delete(minor_head_id):
        """Soft delete a minor head"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE minor_heads
            SET is_active = 0
            WHERE minor_head_id = %s
        ''', (minor_head_id,))
        
        conn.commit()
        conn.close()


class Grouping:
    """Grouping model with company-specific data and comparative year support"""
    
    def __init__(self, grouping_id=None, company_id=None, grouping_name=None, 
                 minor_head_id=None, major_head_id=None, opening_balance_cy=0.0,
                 opening_balance_py=0.0, display_order=None):
        self.grouping_id = grouping_id
        self.company_id = company_id
        self.grouping_name = grouping_name
        self.minor_head_id = minor_head_id
        self.major_head_id = major_head_id
        self.opening_balance_cy = opening_balance_cy or 0.0
        self.opening_balance_py = opening_balance_py or 0.0
        self.display_order = display_order
    
    @staticmethod
    def get_all(company_id=None, minor_head_id=None, major_head_id=None):
        """Get all active groupings, optionally filtered - returns tuples"""
        conn = get_connection()
        cursor = conn.cursor()
        
        if company_id and minor_head_id:
            cursor.execute('''
                SELECT grouping_id, company_id, minor_head_id, grouping_name,
                       opening_balance_cy, opening_balance_py,
                       CAST(grouping_id AS TEXT) as code, '' as description
                FROM groupings
                WHERE company_id = %s AND minor_head_id = %s AND is_active = 1
                ORDER BY display_order, grouping_name
            ''', (company_id, minor_head_id))
        elif company_id and major_head_id:
            cursor.execute('''
                SELECT grouping_id, company_id, minor_head_id, grouping_name,
                       opening_balance_cy, opening_balance_py,
                       CAST(grouping_id AS TEXT) as code, '' as description
                FROM groupings
                WHERE company_id = %s AND major_head_id = %s AND is_active = 1
                ORDER BY minor_head_id, display_order, grouping_name
            ''', (company_id, major_head_id))
        elif company_id:
            cursor.execute('''
                SELECT grouping_id, company_id, minor_head_id, grouping_name,
                       opening_balance_cy, opening_balance_py,
                       CAST(grouping_id AS TEXT) as code, '' as description
                FROM groupings
                WHERE company_id = %s AND is_active = 1
                ORDER BY major_head_id, minor_head_id, display_order, grouping_name
            ''', (company_id,))
        elif minor_head_id:
            cursor.execute('''
                SELECT grouping_id, company_id, minor_head_id, grouping_name,
                       opening_balance_cy, opening_balance_py,
                       CAST(grouping_id AS TEXT) as code, '' as description
                FROM groupings
                WHERE minor_head_id = %s AND is_active = 1
                ORDER BY display_order, grouping_name
            ''', (minor_head_id,))
        elif major_head_id:
            cursor.execute('''
                SELECT grouping_id, company_id, minor_head_id, grouping_name,
                       opening_balance_cy, opening_balance_py,
                       CAST(grouping_id AS TEXT) as code, '' as description
                FROM groupings
                WHERE major_head_id = %s AND is_active = 1
                ORDER BY minor_head_id, display_order, grouping_name
            ''', (major_head_id,))
        else:
            cursor.execute('''
                SELECT grouping_id, company_id, minor_head_id, grouping_name,
                       opening_balance_cy, opening_balance_py,
                       CAST(grouping_id AS TEXT) as code, '' as description
                FROM groupings
                WHERE is_active = 1
                ORDER BY company_id, major_head_id, minor_head_id, display_order, grouping_name
            ''')
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    @staticmethod
    def get_by_id(grouping_id):
        """Get grouping by ID - returns tuple"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT grouping_id, minor_head_id, grouping_name, 
                   CAST(grouping_id AS TEXT) as code, '' as description
            FROM groupings
            WHERE grouping_id = %s AND is_active = 1
        ''', (grouping_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result
    
    @staticmethod
    def get_by_name(name, minor_head_id=None, major_head_id=None):
        """Get grouping by name"""
        conn = get_connection()
        cursor = conn.cursor()
        
        if minor_head_id:
            cursor.execute('''
                SELECT grouping_id, grouping_name, minor_head_id, major_head_id, display_order
                FROM groupings
                WHERE grouping_name = %s AND minor_head_id = %s AND is_active = 1
            ''', (name, minor_head_id))
        elif major_head_id:
            cursor.execute('''
                SELECT grouping_id, grouping_name, minor_head_id, major_head_id, display_order
                FROM groupings
                WHERE grouping_name = %s AND major_head_id = %s AND is_active = 1
            ''', (name, major_head_id))
        else:
            cursor.execute('''
                SELECT grouping_id, grouping_name, minor_head_id, major_head_id, display_order
                FROM groupings
                WHERE grouping_name = %s AND is_active = 1
            ''', (name,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return Grouping(result[0], result[1], result[2], result[3], result[4])
        return None
    
    @staticmethod
    def create(company_id, minor_head_id, grouping_name, opening_balance_cy=0.0,
               opening_balance_py=0.0, code=None, description=None):
        """Create a new grouping for a company"""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            # Get major_head_id from minor_head
            cursor.execute(
                'SELECT major_head_id FROM minor_heads WHERE minor_head_id = %s',
                (minor_head_id,)
            )
            result = cursor.fetchone()
            if not result:
                raise ValueError(f"Minor head {minor_head_id} not found")
            major_head_id = result[0]
            
            # Get max display_order for this minor head and company
            cursor.execute(
                'SELECT MAX(display_order) FROM groupings WHERE company_id = %s AND minor_head_id = %s',
                (company_id, minor_head_id)
            )
            max_order = cursor.fetchone()[0]
            display_order = (max_order or 0) + 1
            
            cursor.execute('''
                INSERT INTO groupings (company_id, grouping_name, minor_head_id, major_head_id,
                                      opening_balance_cy, opening_balance_py, display_order)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (company_id, grouping_name, minor_head_id, major_head_id,
                  opening_balance_cy or 0.0, opening_balance_py or 0.0, display_order))
            
            grouping_id = cursor.fetchone()[0]
            conn.commit()
            conn.close()
            return grouping_id
        except Exception as e:
            conn.close()
            raise e
    
    @staticmethod
    def update(grouping_id, minor_head_id, grouping_name, opening_balance_cy=None,
               opening_balance_py=None, code=None, description=None):
        """Update a grouping"""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            # Get major_head_id from minor_head
            cursor.execute(
                'SELECT major_head_id FROM minor_heads WHERE minor_head_id = %s',
                (minor_head_id,)
            )
            result = cursor.fetchone()
            if not result:
                raise ValueError(f"Minor head {minor_head_id} not found")
            major_head_id = result[0]
            
            if opening_balance_cy is not None and opening_balance_py is not None:
                cursor.execute('''
                    UPDATE groupings
                    SET grouping_name = ?, minor_head_id = ?, major_head_id = ?,
                        opening_balance_cy = ?, opening_balance_py = ?
                    WHERE grouping_id = %s
                ''', (grouping_name, minor_head_id, major_head_id, 
                      opening_balance_cy, opening_balance_py, grouping_id))
            else:
                cursor.execute('''
                    UPDATE groupings
                    SET grouping_name = ?, minor_head_id = ?, major_head_id = ?
                    WHERE grouping_id = %s
                ''', (grouping_name, minor_head_id, major_head_id, grouping_id))
            
            conn.commit()
            conn.close()
        except Exception as e:
            conn.close()
            raise e
    
    @staticmethod
    def delete(grouping_id):
        """Soft delete a grouping"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE groupings
            SET is_active = 0
            WHERE grouping_id = %s
        ''', (grouping_id,))
        
        conn.commit()
        conn.close()
