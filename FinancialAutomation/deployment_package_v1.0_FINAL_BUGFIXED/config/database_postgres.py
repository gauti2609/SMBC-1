"""PostgreSQL-compatible database initialization"""

from .db_connection import get_connection, release_connection
from config.settings import DB_TYPE

def get_create_table_sql(table_name):
    """Get PostgreSQL or SQLite compatible CREATE TABLE SQL"""
    
    if DB_TYPE == 'postgresql':
        # PostgreSQL uses SERIAL, VARCHAR, BOOLEAN TRUE/FALSE
        id_col = 'SERIAL PRIMARY KEY'
        text_type = 'VARCHAR(255)'
        long_text = 'TEXT'
        bool_true = 'BOOLEAN DEFAULT TRUE'
        bool_false = 'BOOLEAN DEFAULT FALSE'
        timestamp_default = 'TIMESTAMP DEFAULT NOW()'
        real_type = 'DECIMAL(15,2)'
    else:
        # SQLite uses AUTOINCREMENT, TEXT, INTEGER for boolean
        id_col = 'INTEGER PRIMARY KEY AUTOINCREMENT'
        text_type = 'TEXT'
        long_text = 'TEXT'
        bool_true = 'INTEGER DEFAULT 1'
        bool_false = 'INTEGER DEFAULT 0'
        timestamp_default = 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
        real_type = 'REAL'
    
    tables = {
        'users': f'''
            CREATE TABLE IF NOT EXISTS users (
                user_id {id_col},
                username {text_type} UNIQUE NOT NULL,
                password_hash {text_type} NOT NULL,
                email {text_type} UNIQUE NOT NULL,
                full_name {text_type},
                created_at {timestamp_default},
                last_login TIMESTAMP,
                is_active {bool_true}
            )
        ''',
        # Add other tables here...
    }
    
    return tables.get(table_name, '')

