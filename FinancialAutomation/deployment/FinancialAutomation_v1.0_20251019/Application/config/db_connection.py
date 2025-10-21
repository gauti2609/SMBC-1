"""
Database abstraction layer supporting both SQLite and PostgreSQL
Automatically handles connection pooling, transactions, and SQL dialect differences
"""

import sqlite3
from contextlib import contextmanager
from config.settings import DB_TYPE, DB_PATH, POSTGRES_CONFIG, POOL_MIN_CONN, POOL_MAX_CONN

# Global connection pool (PostgreSQL only)
_pg_pool = None

def get_connection():
    """
    Get a database connection based on DB_TYPE configuration
    
    Returns:
        Connection object (sqlite3.Connection or psycopg2 connection)
    """
    if DB_TYPE == 'postgresql':
        import psycopg2
        from psycopg2 import pool as pg_pool
        
        global _pg_pool
        if _pg_pool is None:
            try:
                _pg_pool = pg_pool.SimpleConnectionPool(
                    minconn=POOL_MIN_CONN,
                    maxconn=POOL_MAX_CONN,
                    **POSTGRES_CONFIG
                )
                print(f"✅ PostgreSQL connection pool created ({POOL_MIN_CONN}-{POOL_MAX_CONN} connections)")
            except Exception as e:
                print(f"❌ Failed to create PostgreSQL pool: {e}")
                raise
        
        try:
            conn = _pg_pool.getconn()
            return conn
        except Exception as e:
            print(f"❌ Failed to get PostgreSQL connection: {e}")
            raise
    else:
        # SQLite
        return sqlite3.connect(DB_PATH)


def release_connection(conn):
    """
    Release connection back to pool (PostgreSQL) or close (SQLite)
    
    Args:
        conn: Connection object to release
    """
    if DB_TYPE == 'postgresql':
        global _pg_pool
        if _pg_pool:
            _pg_pool.putconn(conn)
    else:
        conn.close()


@contextmanager
def get_db_cursor(commit=False):
    """
    Context manager for database operations with automatic cleanup
    
    Args:
        commit: Auto-commit on success (default: False)
    
    Yields:
        cursor: Database cursor
    
    Example:
        with get_db_cursor(commit=True) as cursor:
            cursor.execute("INSERT INTO ...")
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        yield cursor
        if commit:
            conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        release_connection(conn)


def execute_query(query, params=None, fetch_one=False, fetch_all=False, commit=False):
    """
    Execute a SQL query with automatic connection management
    
    Args:
        query: SQL query string
        params: Query parameters (tuple or dict)
        fetch_one: Return single row (default: False)
        fetch_all: Return all rows (default: False)
        commit: Auto-commit (default: False)
    
    Returns:
        Query result based on fetch parameters, or lastrowid if INSERT
    """
    with get_db_cursor(commit=commit) as cursor:
        cursor.execute(query, params or ())
        
        if fetch_one:
            return cursor.fetchone()
        elif fetch_all:
            return cursor.fetchall()
        elif commit:
            # For INSERT, return lastrowid
            if DB_TYPE == 'postgresql':
                return cursor.fetchone()[0] if 'RETURNING' in query.upper() else None
            else:
                return cursor.lastrowid
        
        return None


def get_sql_type_mapping():
    """
    Get SQL type mappings for current database
    
    Returns:
        dict: Mapping of generic types to database-specific types
    """
    if DB_TYPE == 'postgresql':
        return {
            'AUTOINCREMENT': 'SERIAL',
            'INTEGER PRIMARY KEY AUTOINCREMENT': 'SERIAL PRIMARY KEY',
            'BOOLEAN': 'BOOLEAN',
            'TIMESTAMP': 'TIMESTAMP',
            'CURRENT_TIMESTAMP': 'NOW()',
            'REAL': 'DECIMAL(15,2)',
            'TEXT': 'VARCHAR'
        }
    else:
        return {
            'AUTOINCREMENT': 'AUTOINCREMENT',
            'INTEGER PRIMARY KEY AUTOINCREMENT': 'INTEGER PRIMARY KEY AUTOINCREMENT',
            'BOOLEAN': 'INTEGER',
            'TIMESTAMP': 'TIMESTAMP',
            'CURRENT_TIMESTAMP': 'CURRENT_TIMESTAMP',
            'REAL': 'REAL',
            'TEXT': 'TEXT'
        }


def adapt_sql(query):
    """
    Adapt SQL query to current database dialect
    
    Args:
        query: SQL query string
    
    Returns:
        str: Database-specific SQL query
    """
    if DB_TYPE == 'postgresql':
        # Replace SQLite-specific syntax with PostgreSQL
        query = query.replace('INTEGER PRIMARY KEY AUTOINCREMENT', 'SERIAL PRIMARY KEY')
        query = query.replace('AUTOINCREMENT', '')
        query = query.replace('BOOLEAN DEFAULT 1', 'BOOLEAN DEFAULT TRUE')
        query = query.replace('BOOLEAN DEFAULT 0', 'BOOLEAN DEFAULT FALSE')
        query = query.replace('CURRENT_TIMESTAMP', 'NOW()')
        
        # Add RETURNING for INSERT to get lastrowid equivalent
        if 'INSERT INTO' in query.upper() and 'RETURNING' not in query.upper():
            # Extract table name
            table_match = query.upper().find('INSERT INTO') + 12
            table_end = query.find('(', table_match)
            if table_end == -1:
                table_end = query.find(' ', table_match)
            table_name = query[table_match:table_end].strip()
            
            # Determine primary key column (assume *_id pattern)
            pk_col = f"{table_name.rstrip('s')}_id" if table_name.endswith('s') else f"{table_name}_id"
            
            # Add RETURNING clause
            query += f" RETURNING {pk_col}"
    
    return query


def close_pool():
    """Close connection pool (call on application shutdown)"""
    global _pg_pool
    if _pg_pool:
        _pg_pool.closeall()
        _pg_pool = None
        print("✅ PostgreSQL connection pool closed")
