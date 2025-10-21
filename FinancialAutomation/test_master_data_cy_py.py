"""
Test script for Master Data with CY & PY support
Tests Major Heads, Minor Heads, and Groupings with company-specific data and comparative years
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.database import initialize_database, get_connection
from models.user import User
from models.company_info import CompanyInfo
from models.master_data import MajorHead, MinorHead, Grouping

def test_master_data_cy_py():
    """Test Master Data with CY & PY support"""
    print("\n" + "="*80)
    print("TESTING MASTER DATA WITH CY & PY SUPPORT")
    print("="*80 + "\n")
    
    # Initialize database
    initialize_database()
    
    # Create test user
    print("1. Creating test user and company...")
    user_id = User.create_user(
        username="testuser_master",
        password="Test@123",
        email="testuser@master.com",
        full_name="Test User Master"
    )
    
    # Create test company
    company_id = CompanyInfo.create(
        user_id=user_id,
        entity_name='Test Manufacturing Ltd',
        address='Test Address',
        cin_no='U12345MH2020PLC123456',
        fy_start_date='2024-04-01',
        fy_end_date='2025-03-31',
        turnover=50_00_00_000,
        rounding_level='1000'
    )
    
    print(f"   ✅ Created company: Test Manufacturing Ltd (ID: {company_id})")
    
    # Test Major Heads with CY & PY
    print("\n2. Testing Major Heads with CY & PY...")
    major_heads_data = [
        {
            'name': 'Non-Current Assets',
            'category': 'Assets',
            'opening_cy': 5000000.00,
            'opening_py': 4500000.00
        },
        {
            'name': 'Current Assets',
            'category': 'Assets',
            'opening_cy': 2000000.00,
            'opening_py': 1800000.00
        },
        {
            'name': 'Equity',
            'category': 'Equity and Liabilities',
            'opening_cy': 3000000.00,
            'opening_py': 2700000.00
        }
    ]
    
    major_head_ids = []
    for data in major_heads_data:
        mh_id = MajorHead.create(
            company_id=company_id,
            major_head_name=data['name'],
            category=data['category'],
            opening_balance_cy=data['opening_cy'],
            opening_balance_py=data['opening_py']
        )
        major_head_ids.append(mh_id)
        print(f"   ✅ Created: {data['name']} (CY: ₹{data['opening_cy']:,.2f}, PY: ₹{data['opening_py']:,.2f})")
    
    # Test retrieval
    all_major_heads = MajorHead.get_all_by_company(company_id)
    if len(all_major_heads) == 3:
        print(f"   ✅ Retrieved {len(all_major_heads)} major heads")
    else:
        print(f"   ❌ Expected 3 major heads, got {len(all_major_heads)}")
        return False
    
    # Test get_by_id
    mh = MajorHead.get_by_id(major_head_ids[0])
    if mh and mh.opening_balance_cy == 5000000.00 and mh.opening_balance_py == 4500000.00:
        print(f"   ✅ get_by_id() works with CY & PY balances")
    else:
        print(f"   ❌ get_by_id() failed")
        return False
    
    # Test summary
    summary = MajorHead.get_summary_by_company(company_id)
    expected_cy = sum(d['opening_cy'] for d in major_heads_data)
    expected_py = sum(d['opening_py'] for d in major_heads_data)
    
    if (summary['total_heads'] == 3 and 
        abs(summary['total_opening_cy'] - expected_cy) < 0.01 and
        abs(summary['total_opening_py'] - expected_py) < 0.01):
        print(f"   ✅ Summary: {summary['total_heads']} heads, CY: ₹{summary['total_opening_cy']:,.2f}, PY: ₹{summary['total_opening_py']:,.2f}")
    else:
        print(f"   ❌ Summary mismatch")
        return False
    
    # Test Minor Heads with CY & PY
    print("\n3. Testing Minor Heads with CY & PY...")
    minor_heads_data = [
        {
            'major_head_idx': 0,  # Non-Current Assets
            'name': 'Property, Plant & Equipment',
            'opening_cy': 3000000.00,
            'opening_py': 2800000.00
        },
        {
            'major_head_idx': 0,  # Non-Current Assets
            'name': 'Intangible Assets',
            'opening_cy': 500000.00,
            'opening_py': 400000.00
        },
        {
            'major_head_idx': 1,  # Current Assets
            'name': 'Inventories',
            'opening_cy': 1000000.00,
            'opening_py': 900000.00
        }
    ]
    
    minor_head_ids = []
    for data in minor_heads_data:
        mh_id = MinorHead.create(
            company_id=company_id,
            major_head_id=major_head_ids[data['major_head_idx']],
            minor_head_name=data['name'],
            opening_balance_cy=data['opening_cy'],
            opening_balance_py=data['opening_py']
        )
        minor_head_ids.append(mh_id)
        print(f"   ✅ Created: {data['name']} (CY: ₹{data['opening_cy']:,.2f}, PY: ₹{data['opening_py']:,.2f})")
    
    # Test retrieval by company
    all_minor_heads = MinorHead.get_all_by_company(company_id)
    if len(all_minor_heads) == 3:
        print(f"   ✅ Retrieved {len(all_minor_heads)} minor heads")
    else:
        print(f"   ❌ Expected 3 minor heads, got {len(all_minor_heads)}")
        return False
    
    # Test retrieval by major head
    ppe_minor_heads = MinorHead.get_all_by_company(company_id, major_head_id=major_head_ids[0])
    if len(ppe_minor_heads) == 2:
        print(f"   ✅ Retrieved {len(ppe_minor_heads)} minor heads for 'Non-Current Assets'")
    else:
        print(f"   ❌ Expected 2 minor heads for major head, got {len(ppe_minor_heads)}")
        return False
    
    # Test Groupings with CY & PY
    print("\n4. Testing Groupings with CY & PY...")
    groupings_data = [
        {
            'minor_head_idx': 0,  # Property, Plant & Equipment
            'name': 'Land',
            'opening_cy': 1000000.00,
            'opening_py': 1000000.00
        },
        {
            'minor_head_idx': 0,  # Property, Plant & Equipment
            'name': 'Buildings',
            'opening_cy': 1500000.00,
            'opening_py': 1300000.00
        },
        {
            'minor_head_idx': 2,  # Inventories
            'name': 'Raw Materials',
            'opening_cy': 600000.00,
            'opening_py': 500000.00
        }
    ]
    
    grouping_ids = []
    for data in groupings_data:
        g_id = Grouping.create(
            company_id=company_id,
            minor_head_id=minor_head_ids[data['minor_head_idx']],
            grouping_name=data['name'],
            opening_balance_cy=data['opening_cy'],
            opening_balance_py=data['opening_py']
        )
        grouping_ids.append(g_id)
        print(f"   ✅ Created: {data['name']} (CY: ₹{data['opening_cy']:,.2f}, PY: ₹{data['opening_py']:,.2f})")
    
    # Test retrieval
    all_groupings = Grouping.get_all_by_company(company_id)
    if len(all_groupings) == 3:
        print(f"   ✅ Retrieved {len(all_groupings)} groupings")
    else:
        print(f"   ❌ Expected 3 groupings, got {len(all_groupings)}")
        return False
    
    # Test retrieval by minor head
    ppe_groupings = Grouping.get_all_by_company(company_id, minor_head_id=minor_head_ids[0])
    if len(ppe_groupings) == 2:
        print(f"   ✅ Retrieved {len(ppe_groupings)} groupings for 'Property, Plant & Equipment'")
    else:
        print(f"   ❌ Expected 2 groupings for minor head, got {len(ppe_groupings)}")
        return False
    
    # Test Update operations with CY & PY
    print("\n5. Testing update operations with CY & PY...")
    
    # Update major head opening balances
    MajorHead.update(
        major_head_id=major_head_ids[0],
        opening_balance_cy=5500000.00,
        opening_balance_py=4600000.00
    )
    
    updated_mh = MajorHead.get_by_id(major_head_ids[0])
    if updated_mh.opening_balance_cy == 5500000.00 and updated_mh.opening_balance_py == 4600000.00:
        print(f"   ✅ Major Head update: CY updated to ₹{updated_mh.opening_balance_cy:,.2f}, PY to ₹{updated_mh.opening_balance_py:,.2f}")
    else:
        print(f"   ❌ Major Head update failed")
        return False
    
    # Update minor head
    MinorHead.update(
        minor_head_id=minor_head_ids[0],
        opening_balance_cy=3200000.00
    )
    
    updated_minh = MinorHead.get_by_id(minor_head_ids[0])
    if updated_minh.opening_balance_cy == 3200000.00:
        print(f"   ✅ Minor Head update: CY updated to ₹{updated_minh.opening_balance_cy:,.2f}")
    else:
        print(f"   ❌ Minor Head update failed")
        return False
    
    # Test Company Isolation
    print("\n6. Testing company isolation...")
    
    # Create second company
    company_id_2 = CompanyInfo.create(
        user_id=user_id,
        entity_name='Another Company Ltd',
        address='Another Address',
        cin_no='U12345DL2021PLC654321',
        fy_start_date='2024-04-01',
        fy_end_date='2025-03-31',
        turnover=30_00_00_000,
        rounding_level='100000'
    )
    
    # Add master data to second company
    MajorHead.create(
        company_id=company_id_2,
        major_head_name='Test Major Head',
        category='Assets',
        opening_balance_cy=100000.00,
        opening_balance_py=90000.00
    )
    
    # Verify isolation
    company1_major_heads = MajorHead.get_all_by_company(company_id)
    company2_major_heads = MajorHead.get_all_by_company(company_id_2)
    
    if len(company1_major_heads) == 3 and len(company2_major_heads) == 1:
        print(f"   ✅ Company isolation verified:")
        print(f"      - Company 1: {len(company1_major_heads)} major heads")
        print(f"      - Company 2: {len(company2_major_heads)} major heads")
    else:
        print(f"   ❌ Company isolation failed")
        return False
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print("✅ User and company creation: PASS")
    print("✅ Major Heads with CY & PY: PASS")
    print("✅ Major Head summary statistics: PASS")
    print("✅ Minor Heads with CY & PY: PASS")
    print("✅ Minor Head filtering by major head: PASS")
    print("✅ Groupings with CY & PY: PASS")
    print("✅ Grouping filtering by minor head: PASS")
    print("✅ Update operations (CY & PY): PASS")
    print("✅ Company isolation: PASS")
    print("\n🎉 ALL TESTS PASSED! Master Data with CY & PY support is fully functional.\n")
    
    return True

if __name__ == '__main__':
    try:
        success = test_master_data_cy_py()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
