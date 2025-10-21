"""
Database connection layer - PostgreSQL only
"""

import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
from config.settings import POSTGRES_CONFIG, POOL_MIN_CONN, POOL_MAX_CONN

# Global connection pool
_pg_pool = None


def get_connection():
    """
    Get a PostgreSQL database connection from the pool
    
    Returns:
        psycopg2 connection object
    """
    global _pg_pool
    
    if _pg_pool is None:
        try:
            _pg_pool = pool.SimpleConnectionPool(
                POOL_MIN_CONN,
                POOL_MAX_CONN,
                host=POSTGRES_CONFIG['host'],
                port=POSTGRES_CONFIG['port'],
                database=POSTGRES_CONFIG['database'],
                user=POSTGRES_CONFIG['user'],
                password=POSTGRES_CONFIG['password']
            )
            print(f"✓ PostgreSQL connection pool created successfully")
            print(f"  Host: {POSTGRES_CONFIG['host']}")
            print(f"  Database: {POSTGRES_CONFIG['database']}")
            print(f"  User: {POSTGRES_CONFIG['user']}")
        except Exception as e:
            print(f"❌ Failed to create PostgreSQL pool: {e}")
            raise
    
    try:
        conn = _pg_pool.getconn()
        return conn
    except Exception as e:
        print(f"❌ Failed to get connection from pool: {e}")
        raise


def release_connection(conn):
    """
    Release connection back to pool
    
    Args:
        conn: Connection to release
    """
    if _pg_pool and conn:
        _pg_pool.putconn(conn)


@contextmanager
def get_db_cursor(commit=False):
    """
    Context manager for database operations
    
    Args:
        commit: Whether to auto-commit
    
    Yields:
        Database cursor
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
        query: SQL query string (use %s for parameters)
        params: Query parameters (tuple or dict)
        fetch_one: Return single row (default: False)
        fetch_all: Return all rows (default: False)
        commit: Auto-commit (default: False)
    
    Returns:
        Query result based on fetch parameters, or lastrowid if INSERT with RETURNING
    """
    with get_db_cursor(commit=commit) as cursor:
        cursor.execute(query, params or ())
        
        if fetch_one:
            return cursor.fetchone()
        elif fetch_all:
            return cursor.fetchall()
        elif commit:
            # For INSERT with RETURNING, fetch the returned ID
            if 'RETURNING' in query.upper():
                return cursor.fetchone()[0]
            return None
        
        return None


def close_pool():
    """Close connection pool (call on application shutdown)"""
    global _pg_pool
    if _pg_pool:
        _pg_pool.closeall()
        _pg_pool = None
        print("✓ PostgreSQL connection pool closed")
