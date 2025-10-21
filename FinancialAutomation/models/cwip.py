"""
Capital Work in Progress (CWIP) Model - Schedule III Note 2
Tracks ongoing construction projects with CY and PY comparative data
"""
from datetime import date
from typing import List, Optional, Dict, Any
from config.database import get_connection


class CWIP:
    """Capital Work in Progress for Schedule III Note 2"""
    
    def __init__(
        self,
        cwip_id: Optional[int] = None,
        company_id: Optional[int] = None,
        project_name: str = "",
        opening_balance_cy: float = 0.0,
        additions_cy: float = 0.0,
        capitalized_cy: float = 0.0,
        closing_balance_cy: float = 0.0,
        opening_balance_py: float = 0.0,
        additions_py: float = 0.0,
        capitalized_py: float = 0.0,
        closing_balance_py: float = 0.0,
        project_start_date: Optional[date] = None,
        expected_completion_date: Optional[date] = None
    ):
        self.cwip_id = cwip_id
        self.company_id = company_id
        self.project_name = project_name
        
        # Current Year
        self.opening_balance_cy = float(opening_balance_cy or 0)
        self.additions_cy = float(additions_cy or 0)
        self.capitalized_cy = float(capitalized_cy or 0)
        self.closing_balance_cy = float(closing_balance_cy or 0)
        
        # Previous Year
        self.opening_balance_py = float(opening_balance_py or 0)
        self.additions_py = float(additions_py or 0)
        self.capitalized_py = float(capitalized_py or 0)
        self.closing_balance_py = float(closing_balance_py or 0)
        
        # Project metadata
        self.project_start_date = project_start_date
        self.expected_completion_date = expected_completion_date
    
    def calculate_closing_balance_cy(self) -> float:
        """Calculate closing balance for Current Year"""
        return self.opening_balance_cy + self.additions_cy - self.capitalized_cy
    
    def calculate_closing_balance_py(self) -> float:
        """Calculate closing balance for Previous Year"""
        return self.opening_balance_py + self.additions_py - self.capitalized_py
    
    @staticmethod
    def get_all_by_company(company_id: int) -> List['CWIP']:
        """Retrieve all CWIP projects for a company"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT cwip_id, company_id, project_name,
                   opening_balance_cy, additions_cy, capitalized_cy, closing_balance_cy,
                   opening_balance_py, additions_py, capitalized_py, closing_balance_py,
                   project_start_date, expected_completion_date
            FROM cwip_schedule
            WHERE company_id = %s
            ORDER BY project_name
        ''', (company_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        cwip_list = []
        for row in rows:
            cwip = CWIP(
                cwip_id=row[0],
                company_id=row[1],
                project_name=row[2],
                opening_balance_cy=row[3],
                additions_cy=row[4],
                capitalized_cy=row[5],
                closing_balance_cy=row[6],
                opening_balance_py=row[7],
                additions_py=row[8],
                capitalized_py=row[9],
                closing_balance_py=row[10],
                project_start_date=row[11],
                expected_completion_date=row[12]
            )
            cwip_list.append(cwip)
        
        return cwip_list
    
    @staticmethod
    def get_by_id(cwip_id: int) -> Optional['CWIP']:
        """Retrieve a specific CWIP project by ID"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT cwip_id, company_id, project_name,
                   opening_balance_cy, additions_cy, capitalized_cy, closing_balance_cy,
                   opening_balance_py, additions_py, capitalized_py, closing_balance_py,
                   project_start_date, expected_completion_date
            FROM cwip_schedule
            WHERE cwip_id = %s
        ''', (cwip_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return CWIP(
                cwip_id=row[0],
                company_id=row[1],
                project_name=row[2],
                opening_balance_cy=row[3],
                additions_cy=row[4],
                capitalized_cy=row[5],
                closing_balance_cy=row[6],
                opening_balance_py=row[7],
                additions_py=row[8],
                capitalized_py=row[9],
                closing_balance_py=row[10],
                project_start_date=row[11],
                expected_completion_date=row[12]
            )
        return None
    
    @staticmethod
    def create(
        company_id: int,
        project_name: str,
        opening_balance_cy: float = 0.0,
        additions_cy: float = 0.0,
        capitalized_cy: float = 0.0,
        opening_balance_py: float = 0.0,
        additions_py: float = 0.0,
        capitalized_py: float = 0.0,
        project_start_date: Optional[str] = None,
        expected_completion_date: Optional[str] = None
    ) -> int:
        """Create a new CWIP project with auto-calculated closing balances"""
        # Auto-calculate closing balances
        closing_balance_cy = opening_balance_cy + additions_cy - capitalized_cy
        closing_balance_py = opening_balance_py + additions_py - capitalized_py
        
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO cwip_schedule (
                company_id, project_name,
                opening_balance_cy, additions_cy, capitalized_cy, closing_balance_cy,
                opening_balance_py, additions_py, capitalized_py, closing_balance_py,
                project_start_date, expected_completion_date
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            company_id, project_name,
            opening_balance_cy, additions_cy, capitalized_cy, closing_balance_cy,
            opening_balance_py, additions_py, capitalized_py, closing_balance_py,
            project_start_date, expected_completion_date
        ))
        
        cwip_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        
        return cwip_id
    
    @staticmethod
    def update(
        cwip_id: int,
        project_name: str,
        opening_balance_cy: float,
        additions_cy: float,
        capitalized_cy: float,
        opening_balance_py: float,
        additions_py: float,
        capitalized_py: float,
        project_start_date: Optional[str] = None,
        expected_completion_date: Optional[str] = None
    ) -> bool:
        """Update a CWIP project with auto-calculated closing balances"""
        # Auto-calculate closing balances
        closing_balance_cy = opening_balance_cy + additions_cy - capitalized_cy
        closing_balance_py = opening_balance_py + additions_py - capitalized_py
        
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE cwip_schedule
            SET project_name = ?,
                opening_balance_cy = ?, additions_cy = ?, capitalized_cy = ?, closing_balance_cy = ?,
                opening_balance_py = ?, additions_py = ?, capitalized_py = ?, closing_balance_py = ?,
                project_start_date = ?, expected_completion_date = ?
            WHERE cwip_id = %s
        ''', (
            project_name,
            opening_balance_cy, additions_cy, capitalized_cy, closing_balance_cy,
            opening_balance_py, additions_py, capitalized_py, closing_balance_py,
            project_start_date, expected_completion_date,
            cwip_id
        ))
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return rows_affected > 0
    
    @staticmethod
    def delete(cwip_id: int) -> bool:
        """Delete a CWIP project"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM cwip_schedule WHERE cwip_id = %s', (cwip_id,))
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return rows_affected > 0
    
    @staticmethod
    def get_schedule_iii_format(company_id: int) -> List[Dict[str, Any]]:
        """
        Get CWIP data formatted for Schedule III Note 2
        Returns list of dicts with all required columns for financial statement
        """
        cwip_list = CWIP.get_all_by_company(company_id)
        
        schedule_data = []
        for cwip in cwip_list:
            schedule_data.append({
                'project_name': cwip.project_name,
                'opening_balance_cy': cwip.opening_balance_cy,
                'additions_cy': cwip.additions_cy,
                'capitalized_cy': cwip.capitalized_cy,
                'closing_balance_cy': cwip.calculate_closing_balance_cy(),
                'opening_balance_py': cwip.opening_balance_py,
                'additions_py': cwip.additions_py,
                'capitalized_py': cwip.capitalized_py,
                'closing_balance_py': cwip.calculate_closing_balance_py(),
                'project_start_date': cwip.project_start_date,
                'expected_completion_date': cwip.expected_completion_date
            })
        
        return schedule_data
