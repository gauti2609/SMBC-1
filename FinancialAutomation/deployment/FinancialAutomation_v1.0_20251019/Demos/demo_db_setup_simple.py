#!/usr/bin/env python3
"""
Quick Database Setup Demo - Simplified version using direct SQL
"""

import sqlite3
from pathlib import Path
from config.settings import DB_PATH
from config.database import initialize_database
from models.user import User

def print_section(title):
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")

def main():
    print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                                                                                ║
║              FINANCIAL AUTOMATION - DATABASE SETUP DEMO                        ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")
    
    # Step 1: Initialize Database
    print_section("STEP 1: Initialize Database Schema")
    
    initialize_database()
    print(f"✅ Database initialized at: {DB_PATH}")
    
    # Show table count
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
    table_count = cursor.fetchone()[0]
    print(f"   Total tables: {table_count}")
    
    # Step 2: Create Admin User
    print_section("STEP 2: Create Admin User")
    
    cursor.execute("SELECT user_id, username, full_name FROM users WHERE username = 'admin'")
    admin = cursor.fetchone()
    
    if not admin:
        try:
            User.create_user('admin', 'admin123', 'admin@example.com', 'System Administrator')
            print("✅ Admin user created")
        except:
            print("✅ Admin user already exists")
    else:
        print("✅ Admin user already exists")
    
    print("   Username: admin")
    print("   Password: admin123")
    
    # Step 3: Show Database Statistics
    print_section("STEP 3: Database Statistics")
    
    tables = {
        'Users': 'users',
        'Companies': 'company_info',
        'Trial Balance': 'trial_balance',
        'Major Heads': 'major_heads',
        'Minor Heads': 'minor_heads',
        'Selection Sheet': 'selection_sheet',
        'PPE Schedule': 'ppe_schedule',
        'CWIP': 'cwip_schedule',
        'Investments': 'investments'
    }
    
    print("Current Database State:")
    for label, table in tables.items():
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"   {label:20s}: {count:5d} records")
    
    # Database size
    db_size = Path(DB_PATH).stat().st_size / 1024
    print(f"\n   Database Size: {db_size:.2f} KB")
    
    conn.close()
    
    # Step 4: Next Steps
    print_section("✅ DATABASE SETUP COMPLETE")
    
    print("Your database is ready!")
    print("\nNext Steps:")
    print("   1. Run: python main.py")
    print("   2. Login with: admin / admin123")
    print("   3. Run: python demo_tb_upload.py (for Trial Balance demo)")
    
    print("\n" + "="*80)
    print("  🎉 Setup Successful!")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
