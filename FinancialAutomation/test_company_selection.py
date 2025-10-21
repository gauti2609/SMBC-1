"""
Test script for Company Selection and Session Management
Tests multi-company workflow, dropdown population, and session persistence
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.database import initialize_database, get_connection
from models.user import User
from models.company_info import CompanyInfo
import json

def test_company_selection():
    """Test company selection and session management"""
    print("\n" + "="*80)
    print("TESTING COMPANY SELECTION & SESSION MANAGEMENT")
    print("="*80 + "\n")
    
    # Initialize database
    initialize_database()
    
    # Create test user
    print("1. Creating test user...")
    user_id = User.create_user(
        username="testuser_company",
        password="Test@123",
        email="testuser@company.com",
        full_name="Test User Company"
    )
    
    if not user_id:
        print("❌ Failed to create test user")
        return False
    
    # Fetch the user object
    test_user = User.authenticate("testuser_company", "Test@123")
    if not test_user:
        print("❌ Failed to authenticate test user")
        return False
    
    print(f"✅ Created user: {test_user.username} (ID: {user_id})")
    
    # Create test companies
    print("\n2. Creating test companies...")
    companies = []
    company_data = [
        {
            'entity_name': 'ABC Manufacturing Ltd',
            'cin_no': 'U12345MH2020PLC123456',
            'address': '123 Industrial Area, Mumbai - 400001',
            'fy_start_date': '2024-04-01',
            'fy_end_date': '2025-03-31',
            'turnover': 5_00_00_000,  # 5 Crores = 50000000
            'rounding_level': '1000'  # Thousands
        },
        {
            'entity_name': 'XYZ Retail Pvt Ltd',
            'cin_no': 'U51909DL2019PTC987654',
            'address': '456 Commercial Complex, New Delhi - 110001',
            'fy_start_date': '2024-04-01',
            'fy_end_date': '2025-03-31',
            'turnover': 7_50_00_000,  # 7.5 Crores = 75000000
            'rounding_level': '100000'  # Lakhs
        },
        {
            'entity_name': 'Global Tech Solutions Ltd',
            'cin_no': 'U72900KA2021PLC654321',
            'address': '789 Tech Park, Bangalore - 560001',
            'fy_start_date': '2024-04-01',
            'fy_end_date': '2025-03-31',
            'turnover': 120_00_00_000,  # 120 Crores = 1200000000
            'rounding_level': '10000000'  # Crores (mandatory for >= 100 Cr)
        }
    ]
    
    for data in company_data:
        company_id = CompanyInfo.create(
            user_id=user_id,
            entity_name=data['entity_name'],
            address=data['address'],
            cin_no=data['cin_no'],
            fy_start_date=data['fy_start_date'],
            fy_end_date=data['fy_end_date'],
            currency='INR',
            units='Lakhs',
            number_format='Indian',
            negative_format='Red with -',
            default_font='Arial',
            default_font_size=10,
            show_zeros_as_blank=True,
            decimal_places=2,
            turnover=data['turnover'],
            rounding_level=data['rounding_level']
        )
        
        if company_id:
            # Retrieve the created company
            company = CompanyInfo.get_by_id(company_id)
            if company:
                companies.append(company)
                print(f"   ✅ Created: {company.entity_name} (ID: {company.company_id})")
            else:
                print(f"   ❌ Failed to retrieve company ID: {company_id}")
                return False
        else:
            print(f"   ❌ Failed to create: {data['entity_name']}")
            return False
    
    # Test get_all_by_user
    print("\n3. Testing get_all_by_user()...")
    all_companies = CompanyInfo.get_all_by_user(user_id)
    print(f"   Retrieved {len(all_companies)} companies:")
    
    for company in all_companies:
        print(f"   - {company.entity_name} (ID: {company.company_id})")
    
    if len(all_companies) != 3:
        print(f"   ❌ Expected 3 companies, got {len(all_companies)}")
        return False
    
    print("   ✅ All companies retrieved successfully")
    
    # Verify alphabetical ordering
    expected_order = ['ABC Manufacturing Ltd', 'Global Tech Solutions Ltd', 'XYZ Retail Pvt Ltd']
    actual_order = [c.entity_name for c in all_companies]
    
    if actual_order == expected_order:
        print("   ✅ Companies ordered alphabetically by entity_name")
    else:
        print(f"   ❌ Ordering incorrect. Expected: {expected_order}, Got: {actual_order}")
        return False
    
    # Test get_by_id
    print("\n4. Testing get_by_id()...")
    for company in companies:
        retrieved = CompanyInfo.get_by_id(company.company_id)
        
        if not retrieved:
            print(f"   ❌ Failed to retrieve company ID: {company.company_id}")
            return False
        
        if retrieved.entity_name != company.entity_name:
            print(f"   ❌ Name mismatch. Expected: {company.entity_name}, Got: {retrieved.entity_name}")
            return False
        
        if retrieved.turnover != company.turnover:
            print(f"   ❌ Turnover mismatch for {company.entity_name}")
            return False
        
        if retrieved.rounding_level != company.rounding_level:
            print(f"   ❌ Rounding level mismatch for {company.entity_name}")
            return False
        
        print(f"   ✅ Retrieved: {retrieved.entity_name} (Turnover: ₹{retrieved.turnover:,.2f}, Rounding: {retrieved.rounding_level})")
    
    # Test session management
    print("\n5. Testing session management...")
    session_file = f'.session_{user_id}.json'
    
    # Simulate saving session
    session_data = {
        'user_id': user_id,
        'last_company_id': companies[1].company_id,  # XYZ Retail
        'timestamp': '2025-10-16T10:30:00'
    }
    
    with open(session_file, 'w') as f:
        json.dump(session_data, f, indent=2)
    
    print(f"   ✅ Session saved: {session_file}")
    
    # Simulate loading session
    if os.path.exists(session_file):
        with open(session_file, 'r') as f:
            loaded_session = json.load(f)
        
        last_company_id = loaded_session.get('last_company_id')
        last_company = CompanyInfo.get_by_id(last_company_id)
        
        if last_company and last_company.entity_name == 'XYZ Retail Pvt Ltd':
            print(f"   ✅ Session loaded successfully. Last company: {last_company.entity_name}")
        else:
            print(f"   ❌ Session load failed or wrong company")
            return False
        
        # Clean up session file
        os.remove(session_file)
        print(f"   ✅ Session file cleaned up")
    else:
        print(f"   ❌ Session file not found")
        return False
    
    # Test company data isolation
    print("\n6. Testing company data isolation...")
    from models.trial_balance import TrialBalance
    
    # Add TB entries for first company
    tb1 = TrialBalance.create(
        company_id=companies[0].company_id,
        ledger_name='Cash on Hand',
        opening_balance_cy=100000,
        debit_cy=50000,
        credit_cy=30000,
        closing_balance_cy=120000,
        opening_balance_py=80000,
        debit_py=40000,
        credit_py=20000,
        closing_balance_py=100000
    )
    
    # Add TB entries for second company
    tb2 = TrialBalance.create(
        company_id=companies[1].company_id,
        ledger_name='Bank Account',
        opening_balance_cy=500000,
        debit_cy=200000,
        credit_cy=150000,
        closing_balance_cy=550000,
        opening_balance_py=400000,
        debit_py=150000,
        credit_py=50000,
        closing_balance_py=500000
    )
    
    if not tb1 or not tb2:
        print("   ❌ Failed to create TB entries")
        return False
    
    # Verify isolation
    company1_tb = TrialBalance.get_by_company(companies[0].company_id)
    company2_tb = TrialBalance.get_by_company(companies[1].company_id)
    company3_tb = TrialBalance.get_by_company(companies[2].company_id)
    
    if len(company1_tb) == 1 and len(company2_tb) == 1 and len(company3_tb) == 0:
        print(f"   ✅ Data isolation verified:")
        print(f"      - {companies[0].entity_name}: {len(company1_tb)} TB entry")
        print(f"      - {companies[1].entity_name}: {len(company2_tb)} TB entry")
        print(f"      - {companies[2].entity_name}: {len(company3_tb)} TB entries")
    else:
        print(f"   ❌ Data isolation failed")
        return False
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print("✅ User creation: PASS")
    print("✅ Company creation (3 companies): PASS")
    print("✅ get_all_by_user() retrieval: PASS")
    print("✅ Alphabetical ordering: PASS")
    print("✅ get_by_id() retrieval: PASS")
    print("✅ Session save/load: PASS")
    print("✅ Company data isolation: PASS")
    print("\n🎉 ALL TESTS PASSED! Company selection feature is fully functional.\n")
    
    return True

if __name__ == '__main__':
    try:
        success = test_company_selection()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
