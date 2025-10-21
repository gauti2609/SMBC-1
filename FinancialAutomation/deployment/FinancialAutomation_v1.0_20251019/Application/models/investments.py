"""
Investments Model - Schedule III Notes 3, 4, 13, 14
Tracks investments in subsidiaries, associates, equity, debt instruments
Classification: Non-Current (Notes 3, 4) and Current (Notes 13, 14)
"""
from typing import List, Optional, Dict, Any
from config.database import get_connection


class Investment:
    """Investment model for Schedule III compliance"""
    
    # Investment classifications
    NON_CURRENT = "Non-Current"
    CURRENT = "Current"
    
    # Investment types
    TYPE_SUBSIDIARY = "Subsidiaries"
    TYPE_ASSOCIATE = "Associates"
    TYPE_JOINT_VENTURE = "Joint Ventures"
    TYPE_EQUITY = "Equity Instruments"
    TYPE_PREFERENCE = "Preference Shares"
    TYPE_DEBT = "Debt Instruments"
    TYPE_MUTUAL_FUND = "Mutual Funds"
    TYPE_GOVERNMENT_SECURITIES = "Government Securities"
    TYPE_OTHERS = "Others"
    
    def __init__(
        self,
        investment_id: Optional[int] = None,
        company_id: Optional[int] = None,
        investment_particulars: str = "",
        classification: str = NON_CURRENT,
        investment_type: str = TYPE_EQUITY,
        is_quoted: bool = False,
        quantity_cy: int = 0,
        quantity_py: int = 0,
        cost_cy: float = 0.0,
        cost_py: float = 0.0,
        fair_value_cy: float = 0.0,
        fair_value_py: float = 0.0,
        carrying_amount_cy: float = 0.0,
        carrying_amount_py: float = 0.0,
        market_value_cy: float = 0.0,
        market_value_py: float = 0.0
    ):
        self.investment_id = investment_id
        self.company_id = company_id
        self.investment_particulars = investment_particulars
        self.classification = classification
        self.investment_type = investment_type
        self.is_quoted = is_quoted
        
        # Quantities
        self.quantity_cy = int(quantity_cy or 0)
        self.quantity_py = int(quantity_py or 0)
        
        # Current Year
        self.cost_cy = float(cost_cy or 0)
        self.fair_value_cy = float(fair_value_cy or 0)
        self.carrying_amount_cy = float(carrying_amount_cy or 0)
        self.market_value_cy = float(market_value_cy or 0)
        
        # Previous Year
        self.cost_py = float(cost_py or 0)
        self.fair_value_py = float(fair_value_py or 0)
        self.carrying_amount_py = float(carrying_amount_py or 0)
        self.market_value_py = float(market_value_py or 0)
    
    @staticmethod
    def get_all_by_company(company_id: int, classification: Optional[str] = None) -> List['Investment']:
        """Retrieve all investments for a company, optionally filtered by classification"""
        conn = get_connection()
        cursor = conn.cursor()
        
        if classification:
            cursor.execute('''
                SELECT investment_id, company_id, investment_particulars, classification, investment_type,
                       is_quoted, quantity_cy, quantity_py,
                       cost_cy, cost_py, fair_value_cy, fair_value_py,
                       carrying_amount_cy, carrying_amount_py,
                       market_value_cy, market_value_py
                FROM investments
                WHERE company_id = ? AND classification = ?
                ORDER BY investment_type, investment_particulars
            ''', (company_id, classification))
        else:
            cursor.execute('''
                SELECT investment_id, company_id, investment_particulars, classification, investment_type,
                       is_quoted, quantity_cy, quantity_py,
                       cost_cy, cost_py, fair_value_cy, fair_value_py,
                       carrying_amount_cy, carrying_amount_py,
                       market_value_cy, market_value_py
                FROM investments
                WHERE company_id = ?
                ORDER BY classification, investment_type, investment_particulars
            ''', (company_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        investments = []
        for row in rows:
            inv = Investment(
                investment_id=row[0],
                company_id=row[1],
                investment_particulars=row[2],
                classification=row[3],
                investment_type=row[4],
                is_quoted=bool(row[5]),
                quantity_cy=row[6],
                quantity_py=row[7],
                cost_cy=row[8],
                cost_py=row[9],
                fair_value_cy=row[10],
                fair_value_py=row[11],
                carrying_amount_cy=row[12],
                carrying_amount_py=row[13],
                market_value_cy=row[14],
                market_value_py=row[15]
            )
            investments.append(inv)
        
        return investments
    
    @staticmethod
    def get_by_id(investment_id: int) -> Optional['Investment']:
        """Retrieve a specific investment by ID"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT investment_id, company_id, investment_particulars, classification, investment_type,
                   is_quoted, quantity_cy, quantity_py,
                   cost_cy, cost_py, fair_value_cy, fair_value_py,
                   carrying_amount_cy, carrying_amount_py,
                   market_value_cy, market_value_py
            FROM investments
            WHERE investment_id = ?
        ''', (investment_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Investment(
                investment_id=row[0],
                company_id=row[1],
                investment_particulars=row[2],
                classification=row[3],
                investment_type=row[4],
                is_quoted=bool(row[5]),
                quantity_cy=row[6],
                quantity_py=row[7],
                cost_cy=row[8],
                cost_py=row[9],
                fair_value_cy=row[10],
                fair_value_py=row[11],
                carrying_amount_cy=row[12],
                carrying_amount_py=row[13],
                market_value_cy=row[14],
                market_value_py=row[15]
            )
        return None
    
    @staticmethod
    def create(
        company_id: int,
        investment_particulars: str,
        classification: str,
        investment_type: str,
        is_quoted: bool = False,
        quantity_cy: int = 0,
        quantity_py: int = 0,
        cost_cy: float = 0.0,
        cost_py: float = 0.0,
        fair_value_cy: float = 0.0,
        fair_value_py: float = 0.0,
        carrying_amount_cy: float = 0.0,
        carrying_amount_py: float = 0.0,
        market_value_cy: float = 0.0,
        market_value_py: float = 0.0
    ) -> int:
        """Create a new investment"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO investments (
                company_id, investment_particulars, classification, investment_type,
                is_quoted, quantity_cy, quantity_py,
                cost_cy, cost_py, fair_value_cy, fair_value_py,
                carrying_amount_cy, carrying_amount_py,
                market_value_cy, market_value_py
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            company_id, investment_particulars, classification, investment_type,
            is_quoted, quantity_cy, quantity_py,
            cost_cy, cost_py, fair_value_cy, fair_value_py,
            carrying_amount_cy, carrying_amount_py,
            market_value_cy, market_value_py
        ))
        
        investment_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return investment_id
    
    @staticmethod
    def update(
        investment_id: int,
        investment_particulars: str,
        classification: str,
        investment_type: str,
        is_quoted: bool,
        quantity_cy: int,
        quantity_py: int,
        cost_cy: float,
        cost_py: float,
        fair_value_cy: float,
        fair_value_py: float,
        carrying_amount_cy: float,
        carrying_amount_py: float,
        market_value_cy: float,
        market_value_py: float
    ) -> bool:
        """Update an investment"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE investments
            SET investment_particulars = ?, classification = ?, investment_type = ?,
                is_quoted = ?, quantity_cy = ?, quantity_py = ?,
                cost_cy = ?, cost_py = ?, fair_value_cy = ?, fair_value_py = ?,
                carrying_amount_cy = ?, carrying_amount_py = ?,
                market_value_cy = ?, market_value_py = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE investment_id = ?
        ''', (
            investment_particulars, classification, investment_type,
            is_quoted, quantity_cy, quantity_py,
            cost_cy, cost_py, fair_value_cy, fair_value_py,
            carrying_amount_cy, carrying_amount_py,
            market_value_cy, market_value_py,
            investment_id
        ))
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return rows_affected > 0
    
    @staticmethod
    def delete(investment_id: int) -> bool:
        """Delete an investment"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM investments WHERE investment_id = ?', (investment_id,))
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return rows_affected > 0
    
    @staticmethod
    def get_schedule_iii_format(company_id: int, classification: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get investments formatted for Schedule III
        Returns dict grouped by investment type
        """
        investments = Investment.get_all_by_company(company_id, classification)
        
        # Group by investment type
        grouped_data = {}
        for inv in investments:
            if inv.investment_type not in grouped_data:
                grouped_data[inv.investment_type] = []
            
            grouped_data[inv.investment_type].append({
                'particulars': inv.investment_particulars,
                'quoted': inv.is_quoted,
                'quantity_cy': inv.quantity_cy,
                'quantity_py': inv.quantity_py,
                'cost_cy': inv.cost_cy,
                'cost_py': inv.cost_py,
                'fair_value_cy': inv.fair_value_cy,
                'fair_value_py': inv.fair_value_py,
                'carrying_amount_cy': inv.carrying_amount_cy,
                'carrying_amount_py': inv.carrying_amount_py,
                'market_value_cy': inv.market_value_cy,
                'market_value_py': inv.market_value_py
            })
        
        return grouped_data
    
    @staticmethod
    def get_totals(company_id: int, classification: str) -> Dict[str, float]:
        """Get total carrying amounts for a classification"""
        investments = Investment.get_all_by_company(company_id, classification)
        
        total_cy = sum(inv.carrying_amount_cy for inv in investments)
        total_py = sum(inv.carrying_amount_py for inv in investments)
        
        return {
            'total_carrying_amount_cy': total_cy,
            'total_carrying_amount_py': total_py
        }
