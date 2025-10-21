"""
Test PostgreSQL connection using settings from .env file
Run this after configuring PostgreSQL on NAS to verify connectivity
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_postgres_connection():
    """Test PostgreSQL connection and display configuration"""
    
    print("\n" + "="*80)
    print("POSTGRESQL CONNECTION TEST")
    print("="*80 + "\n")
    
    # Load configuration
    try:
        from config.settings import DB_TYPE, POSTGRES_CONFIG
        print(f"1. Configuration loaded:")
        print(f"   DB_TYPE: {DB_TYPE}")
        
        if DB_TYPE != 'postgresql':
            print(f"\n⚠️  DB_TYPE is set to '{DB_TYPE}', not 'postgresql'")
            print(f"   Update .env file and set DB_TYPE=postgresql")
            return False
        
        print(f"\n2. PostgreSQL Configuration:")
        print(f"   Host: {POSTGRES_CONFIG['host']}")
        print(f"   Port: {POSTGRES_CONFIG['port']}")
        print(f"   Database: {POSTGRES_CONFIG['database']}")
        print(f"   User: {POSTGRES_CONFIG['user']}")
        print(f"   Password: {'*' * len(POSTGRES_CONFIG['password']) if POSTGRES_CONFIG['password'] else '(not set)'}")
        print(f"   SSL Mode: {POSTGRES_CONFIG['sslmode']}")
        
    except Exception as e:
        print(f"❌ Failed to load configuration: {e}")
        return False
    
    # Test psycopg2 installation
    print(f"\n3. Checking psycopg2 driver...")
    try:
        import psycopg2
        print(f"   ✅ psycopg2 version: {psycopg2.__version__}")
    except ImportError:
        print(f"   ❌ psycopg2 not installed!")
        print(f"   Install with: pip install psycopg2-binary")
        return False
    
    # Test network connectivity
    print(f"\n4. Testing network connectivity to {POSTGRES_CONFIG['host']}:{POSTGRES_CONFIG['port']}...")
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((POSTGRES_CONFIG['host'], int(POSTGRES_CONFIG['port'])))
        sock.close()
        
        if result == 0:
            print(f"   ✅ Port {POSTGRES_CONFIG['port']} is reachable")
        else:
            print(f"   ❌ Cannot reach {POSTGRES_CONFIG['host']}:{POSTGRES_CONFIG['port']}")
            print(f"   Check:")
            print(f"   - Is PostgreSQL running on NAS?")
            print(f"   - Is the IP address correct?")
            print(f"   - Is port {POSTGRES_CONFIG['port']} open in firewall?")
            return False
    except Exception as e:
        print(f"   ❌ Network test failed: {e}")
        return False
    
    # Test PostgreSQL connection
    print(f"\n5. Testing PostgreSQL connection...")
    try:
        import psycopg2
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        cursor = conn.cursor()
        
        # Test query
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"   ✅ Connected successfully!")
        print(f"   PostgreSQL version: {version.split(',')[0]}")
        
        # Test database access
        cursor.execute("SELECT current_database(), current_user;")
        db, user = cursor.fetchone()
        print(f"   Current database: {db}")
        print(f"   Current user: {user}")
        
        # List existing tables
        cursor.execute("""
            SELECT tablename FROM pg_catalog.pg_tables 
            WHERE schemaname = 'public'
            ORDER BY tablename;
        """)
        tables = cursor.fetchall()
        
        if tables:
            print(f"\n   Existing tables ({len(tables)}):")
            for table in tables:
                print(f"   - {table[0]}")
        else:
            print(f"\n   No tables yet (database is empty)")
            print(f"   Run initialize_database() to create schema")
        
        cursor.close()
        conn.close()
        
    except psycopg2.OperationalError as e:
        print(f"   ❌ Connection failed: {e}")
        print(f"\n   Troubleshooting:")
        print(f"   1. Verify PostgreSQL is running: systemctl status postgresql")
        print(f"   2. Check database exists: psql -U postgres -l")
        print(f"   3. Verify user exists: psql -U postgres -c \"\\du\"")
        print(f"   4. Test manual connection: psql -h {POSTGRES_CONFIG['host']} -U {POSTGRES_CONFIG['user']} -d {POSTGRES_CONFIG['database']}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False
    
    # Test connection pool
    print(f"\n6. Testing connection pool...")
    try:
        from config.db_connection import get_connection, release_connection, close_pool
        from config.settings import POOL_MIN_CONN, POOL_MAX_CONN
        
        print(f"   Pool settings: {POOL_MIN_CONN} min, {POOL_MAX_CONN} max connections")
        
        # Get a connection
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()
        cursor.close()
        release_connection(conn)
        
        if result[0] == 1:
            print(f"   ✅ Connection pool working correctly")
        
        # Clean up
        close_pool()
        
    except Exception as e:
        print(f"   ❌ Connection pool test failed: {e}")
        return False
    
    # Success summary
    print(f"\n" + "="*80)
    print(f"CONNECTION TEST SUMMARY")
    print(f"="*80)
    print(f"✅ Configuration: OK")
    print(f"✅ psycopg2 driver: OK")
    print(f"✅ Network connectivity: OK")
    print(f"✅ PostgreSQL connection: OK")
    print(f"✅ Connection pool: OK")
    print(f"\n🎉 PostgreSQL is ready for use!")
    print(f"\nNext steps:")
    print(f"1. Run initialize_database() to create schema")
    print(f"2. Test with: python test_company_selection.py")
    print(f"3. Start using the application\n")
    
    return True

if __name__ == '__main__':
    try:
        success = test_postgres_connection()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
