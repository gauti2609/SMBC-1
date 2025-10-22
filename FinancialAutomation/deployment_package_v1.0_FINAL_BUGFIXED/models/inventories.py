"""
Inventories Model - Schedule III Note 8
Raw Materials, Work-in-Progress, Finished Goods, Stock-in-Trade
"""
from typing import List, Optional, Dict, Any
from config.database import get_connection


class Inventory:
    """Inventory model for Schedule III Note 8"""
    
    # Inventory categories
    CAT_RAW_MATERIALS = "Raw Materials"
    CAT_WIP = "Work-in-Progress"
    CAT_FINISHED_GOODS = "Finished Goods"
    CAT_STOCK_IN_TRADE = "Stock-in-Trade"
    CAT_STORES_SPARES = "Stores and Spares"
    CAT_LOOSE_TOOLS = "Loose Tools"
    
    def __init__(
        self,
        inventory_id: Optional[int] = None,
        company_id: Optional[int] = None,
        category: str = "",
        particulars: str = "",
        quantity_cy: float = 0.0,
        quantity_py: float = 0.0,
        unit: str = "",
        value_cy: float = 0.0,
        value_py: float = 0.0
    ):
        self.inventory_id = inventory_id
        self.company_id = company_id
        self.category = category
        self.particulars = particulars
        self.quantity_cy = float(quantity_cy or 0)
        self.quantity_py = float(quantity_py or 0)
        self.unit = unit
        self.value_cy = float(value_cy or 0)
        self.value_py = float(value_py or 0)
    
    @staticmethod
    def get_all_by_company(company_id: int) -> List['Inventory']:
        """Retrieve all inventory items for a company"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT inventory_id, company_id, category, particulars,
                   quantity_cy, quantity_py, unit, value_cy, value_py
            FROM inventories
            WHERE company_id = %s
            ORDER BY category, particulars
        ''', (company_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        items = []
        for row in rows:
            items.append(Inventory(
                inventory_id=row[0],
                company_id=row[1],
                category=row[2],
                particulars=row[3],
                quantity_cy=row[4],
                quantity_py=row[5],
                unit=row[6],
                value_cy=row[7],
                value_py=row[8]
            ))
        
        return items
    
    @staticmethod
    def create(
        company_id: int,
        category: str,
        particulars: str,
        quantity_cy: float = 0.0,
        quantity_py: float = 0.0,
        unit: str = "",
        value_cy: float = 0.0,
        value_py: float = 0.0
    ) -> int:
        """Create a new inventory item"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO inventories (
                company_id, category, particulars,
                quantity_cy, quantity_py, unit, value_cy, value_py
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (company_id, category, particulars, quantity_cy, quantity_py, unit, value_cy, value_py))
        
        inventory_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        
        return inventory_id
    
    @staticmethod
    def update(
        inventory_id: int,
        category: str,
        particulars: str,
        quantity_cy: float,
        quantity_py: float,
        unit: str,
        value_cy: float,
        value_py: float
    ) -> bool:
        """Update an inventory item"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE inventories
            SET category = %s, particulars = %s,
                quantity_cy = %s, quantity_py = %s, unit = %s,
                value_cy = %s, value_py = %s
            WHERE inventory_id = %s
        ''', (category, particulars, quantity_cy, quantity_py, unit, value_cy, value_py, inventory_id))
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return rows_affected > 0
    
    @staticmethod
    def delete(inventory_id: int) -> bool:
        """Delete an inventory item"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM inventories WHERE inventory_id = %s', (inventory_id,))
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return rows_affected > 0
    
    @staticmethod
    def get_schedule_iii_format(company_id: int) -> Dict[str, List[Dict[str, Any]]]:
        """Get inventories formatted for Schedule III Note 8 grouped by category"""
        items = Inventory.get_all_by_company(company_id)
        
        grouped = {}
        for item in items:
            if item.category not in grouped:
                grouped[item.category] = []
            
            grouped[item.category].append({
                'particulars': item.particulars,
                'quantity_cy': item.quantity_cy,
                'quantity_py': item.quantity_py,
                'unit': item.unit,
                'value_cy': item.value_cy,
                'value_py': item.value_py
            })
        
        return grouped
    
    @staticmethod
    def get_totals(company_id: int) -> Dict[str, float]:
        """Get total inventory values"""
        items = Inventory.get_all_by_company(company_id)
        
        total_cy = sum(item.value_cy for item in items)
        total_py = sum(item.value_py for item in items)
        
        return {
            'total_value_cy': total_cy,
            'total_value_py': total_py
        }
