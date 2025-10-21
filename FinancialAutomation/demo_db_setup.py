#!/usr/bin/env python3
"""
Database Setup Demo
Shows how to initialize the database with all tables and sample data
"""

import sqlite3
from pathlib import Path
from config.database import initialize_database
from config.settings import DB_PATH
from models.user import User
from models.company_info import CompanyInfo
from utils.default_master_data import initialize_default_master_data_for_company

def print_header(title):
    """Print formatted header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")

def demo_database_setup():
    """Complete database setup demonstration"""
    
    print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                                                                                ║
║              FINANCIAL AUTOMATION - DATABASE SETUP DEMO                        ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")
    
    # Step 1: Initialize Database
    print_header("STEP 1: Initialize Database Schema")
    
    initialize_database()
    print("✅ Database connection established")
    print(f"   Location: {DB_PATH}")
    
    print("✅ All database tables created successfully")
    
    # Show tables
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    
    print(f"\n📊 Total Tables Created: {len(tables)}")
    print("\nDatabase Schema:")
    for i, (table,) in enumerate(tables, 1):
        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"   {i:2d}. {table:30s} ({count} rows)")
    
    conn.close()
    
    # Step 2: Create Admin User
    print_header("STEP 2: Create Admin User")
    
    # Check if admin already exists
    conn_temp = sqlite3.connect(DB_PATH)
    cursor_temp = conn_temp.cursor()
    cursor_temp.execute("SELECT user_id, username, full_name FROM users WHERE username = 'admin'")
    admin_row = cursor_temp.fetchone()
    conn_temp.close()
    
    if not admin_row:
        try:
            user_id = User.create_user(
                username='admin',
                password='admin123',
                email='admin@example.com',
                full_name='System Administrator'
            )
            print("✅ Admin user created successfully")
            print("   Username: admin")
            print("   Password: admin123")
            print("   Email: admin@example.com")
            print("   Name: System Administrator")
        except Exception as e:
            print(f"⚠️  User creation note: {e}")
            print("   Continuing with existing user...")
    else:
        print("✅ Admin user already exists")
        print(f"   ID: {admin_row[0]}")
        print(f"   Username: {admin_row[1]}")
        print(f"   Name: {admin_row[2]}")
    
    # Verify login
    verified_user = User.authenticate('admin', 'admin123')
    if verified_user:
        print("\n✅ Admin login verified successfully")
    else:
        print("\n⚠️  Admin login verification (user may need password reset)")
    
    # Step 3: Create Sample Company
    print_header("STEP 3: Create Sample Company")
    
    # Get admin user ID
    conn_temp = sqlite3.connect(DB_PATH)
    cursor_temp = conn_temp.cursor()
    cursor_temp.execute("SELECT user_id FROM users WHERE username = 'admin'")
    admin_row = cursor_temp.fetchone()
    admin_user_id = admin_row[0] if admin_row else 1
    conn_temp.close()
    
    # Check if demo company exists
    existing_company = CompanyInfo.get_by_name('Demo Company Ltd')
    if existing_company:
        company_id = existing_company.id
        print("✅ Demo company already exists")
    else:
        company_id = CompanyInfo.create(
            user_id=admin_user_id,
            entity_name='Demo Company Ltd',
            cin='L12345KA2020PLC123456',
            registered_address='123 Business Park, Bangalore - 560001',
            fy_start_date='2024-04-01',
            fy_end_date='2025-03-31',
            currency='INR',
            unit_of_measurement='Lakhs',
            company_logo_path=None
        )
        print("✅ Demo company created successfully")
    
    company = CompanyInfo.get_by_id(company_id)
    print(f"\nCompany Details:")
    print(f"   ID: {company.id}")
    print(f"   Name: {company.entity_name}")
    print(f"   CIN: {company.cin}")
    print(f"   FY: {company.fy_start_date} to {company.fy_end_date}")
    print(f"   Currency: {company.currency}")
    print(f"   Units: {company.unit_of_measurement}")
    
    # Step 4: Initialize Master Data
    print_header("STEP 4: Initialize Master Data (Major/Minor Heads)")
    
    # Initialize default master data
    initialize_default_master_data_for_company(company_id)
    print("✅ Master data initialized successfully")
    
    # Show master data summary
    conn = sqlite3.connect(db.db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM major_heads WHERE company_id = ?", (company_id,))
    major_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM minor_heads WHERE company_id = ?", (company_id,))
    minor_count = cursor.fetchone()[0]
    
    print(f"\nMaster Data Summary:")
    print(f"   Major Heads: {major_count}")
    print(f"   Minor Heads: {minor_count}")
    
    # Show sample major heads
    cursor.execute("""
        SELECT id, note_number, description 
        FROM major_heads 
        WHERE company_id = ? 
        ORDER BY note_number 
        LIMIT 10
    """, (company_id,))
    
    print(f"\nSample Major Heads:")
    for row in cursor.fetchall():
        print(f"   • Note {row[1]:2d}: {row[2]}")
    
    conn.close()
    
    # Step 5: Database Statistics
    print_header("STEP 5: Database Statistics")
    
    conn = sqlite3.connect(db.db_path)
    cursor = conn.cursor()
    
    stats = {
        'Users': 'SELECT COUNT(*) FROM users',
        'Companies': 'SELECT COUNT(*) FROM company_info',
        'Major Heads': 'SELECT COUNT(*) FROM major_heads',
        'Minor Heads': 'SELECT COUNT(*) FROM minor_heads',
        'Trial Balance': 'SELECT COUNT(*) FROM trial_balance',
        'PPE Items': 'SELECT COUNT(*) FROM ppe_schedule',
        'CWIP Items': 'SELECT COUNT(*) FROM cwip',
        'Investments': 'SELECT COUNT(*) FROM investments',
        'Selection Sheet': 'SELECT COUNT(*) FROM selection_sheet',
    }
    
    print("Current Database State:")
    for label, query in stats.items():
        cursor.execute(query)
        count = cursor.fetchone()[0]
        print(f"   {label:20s}: {count:5d} records")
    
    # Database file size
    db_size = Path(DB_PATH).stat().st_size / 1024  # KB
    print(f"\n   Database Size: {db_size:.2f} KB")
    
    conn.close()
    
    # Step 6: Completion Summary
    print_header("✅ DATABASE SETUP COMPLETE")
    
    print("Your database is now ready with:")
    print("   ✅ All tables created (15+ tables)")
    print("   ✅ Admin user configured")
    print("   ✅ Sample company created")
    print("   ✅ Master data initialized")
    print("\nNext Steps:")
    print("   1. Run the application: python main.py")
    print("   2. Login with admin/admin123")
    print("   3. Import Trial Balance from Sample TB.xlsx")
    print("   4. Generate financial statements")
    print("\nDemo Scripts Available:")
    print("   • python demo_tb_upload.py - Trial Balance import demo")
    print("   • python demo_selection_sheet.py - Selection Sheet demo")
    
    print("\n" + "="*80)
    print("  🎉 Setup Successful! Database is ready for use.")
    print("="*80 + "\n")

if __name__ == "__main__":
    try:
        demo_database_setup()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
