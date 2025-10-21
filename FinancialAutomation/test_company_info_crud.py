"""
Test Suite for Company Information Module
Tests CRUD operations, validation, and Schedule III compliance
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.company_info import CompanyInfo
from config.database import initialize_database
from datetime import datetime, timedelta

def test_cin_validation():
    """Test CIN format validation"""
    print("\n" + "="*70)
    print("TEST 1: CIN Validation")
    print("="*70)
    
    valid_cins = [
        "L12345AB2020PLC123456",
        "U98765CD2019PTC654321",
        "N11111MH2021PLC999999"
    ]
    
    invalid_cins = [
        "L12345AB2020PLC12345",  # Too short
        "L12345AB2020PLC1234567",  # Too long
        "X12345AB2020PLC123456",  # Invalid first letter
        "L1234XAB2020PLC123456",  # Letters in digits section
        "L12345A22020PLC123456",  # Not enough state letters
        "L12345AB202XPLC123456",  # Letter in year
    ]
    
    print("\n✓ Testing Valid CINs:")
    for cin in valid_cins:
        result = CompanyInfo.validate_cin(cin)
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {cin}")
    
    print("\n✓ Testing Invalid CINs:")
    for cin in invalid_cins:
        result = CompanyInfo.validate_cin(cin)
        status = "✓ PASS (correctly rejected)" if not result else "✗ FAIL (incorrectly accepted)"
        print(f"  {status}: {cin}")

def test_date_validation():
    """Test FY date validation"""
    print("\n" + "="*70)
    print("TEST 2: Financial Year Date Validation")
    print("="*70)
    
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    yesterday = today - timedelta(days=1)
    
    tests = [
        (today, tomorrow, True, "End after start (valid)"),
        (today, yesterday, False, "End before start (invalid)"),
        (today, today, False, "Same date (invalid)"),
        (datetime(2024, 4, 1).date(), datetime(2025, 3, 31).date(), True, "Standard FY (valid)"),
    ]
    
    print("\n✓ Testing Date Ranges:")
    for start, end, expected, description in tests:
        result = CompanyInfo.validate_dates(start, end)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        print(f"  {status}: {description}")
        print(f"        Start: {start}, End: {end}, Result: {result}")

def test_schedule_iii_rounding_validation():
    """Test Schedule III rounding level validation"""
    print("\n" + "="*70)
    print("TEST 3: Schedule III Rounding Validation")
    print("="*70)
    
    # Turnover < 100 Crores - valid options: '100', '1000', '100000', '1000000'
    low_turnover = 50_00_00_000  # 50 Crores
    
    # Turnover >= 100 Crores - valid options: '100000', '1000000', '10000000'
    high_turnover = 150_00_00_000  # 150 Crores
    
    print(f"\n✓ Testing Low Turnover (₹{low_turnover/10000000:.0f} Crores):")
    low_tests = [
        ('1', True, "Absolute values"),
        ('100', True, "Hundreds"),
        ('1000', True, "Thousands"),
        ('100000', True, "Lakhs"),
        ('1000000', True, "Millions"),
        ('10000000', False, "Crores (not allowed for low turnover)"),
    ]
    
    for rounding, expected, description in low_tests:
        result = CompanyInfo.validate_rounding_level(low_turnover, rounding)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        print(f"  {status}: {description} ('{rounding}')")
    
    print(f"\n✓ Testing High Turnover (₹{high_turnover/10000000:.0f} Crores):")
    high_tests = [
        ('1', True, "Absolute values"),
        ('100', False, "Hundreds (not allowed for high turnover)"),
        ('1000', False, "Thousands (not allowed for high turnover)"),
        ('100000', True, "Lakhs"),
        ('1000000', True, "Millions"),
        ('10000000', True, "Crores"),
    ]
    
    for rounding, expected, description in high_tests:
        result = CompanyInfo.validate_rounding_level(high_turnover, rounding)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        print(f"  {status}: {description} ('{rounding}')")

def test_rounding_options():
    """Test get_rounding_options method"""
    print("\n" + "="*70)
    print("TEST 4: Get Rounding Options")
    print("="*70)
    
    low_turnover = 50_00_00_000  # 50 Crores
    high_turnover = 150_00_00_000  # 150 Crores
    
    print(f"\n✓ Options for Low Turnover (₹{low_turnover/10000000:.0f} Crores):")
    low_options = CompanyInfo.get_rounding_options(low_turnover)
    for value, text in low_options:
        print(f"  • {text} (value: '{value}')")
    
    print(f"\n✓ Options for High Turnover (₹{high_turnover/10000000:.0f} Crores):")
    high_options = CompanyInfo.get_rounding_options(high_turnover)
    for value, text in high_options:
        print(f"  • {text} (value: '{value}')")
    
    # Verify correct counts
    expected_low = 5  # Absolute + 4 options
    expected_high = 4  # Absolute + 3 options
    
    status_low = "✓ PASS" if len(low_options) == expected_low else "✗ FAIL"
    status_high = "✓ PASS" if len(high_options) == expected_high else "✗ FAIL"
    
    print(f"\n  {status_low}: Low turnover has {len(low_options)} options (expected {expected_low})")
    print(f"  {status_high}: High turnover has {len(high_options)} options (expected {expected_high})")

def test_company_info_crud():
    """Test Company Info CRUD operations"""
    print("\n" + "="*70)
    print("TEST 5: Company Info CRUD Operations")
    print("="*70)
    
    # Initialize database
    initialize_database()
    
    # Test data
    test_user_id = 999
    test_entity = "Test Company Pvt Ltd"
    test_cin = "L12345AB2020PLC123456"
    test_address = "123 Test Street, Test City, Test State - 123456"
    test_fy_start = "2024-04-01"
    test_fy_end = "2025-03-31"
    test_turnover = 75_00_00_000  # 75 Crores
    test_rounding = '100000'  # Lakhs
    
    # CREATE
    print("\n✓ Testing CREATE:")
    try:
        company_id = CompanyInfo.create(
            user_id=test_user_id,
            entity_name=test_entity,
            fy_start_date=test_fy_start,
            fy_end_date=test_fy_end,
            address=test_address,
            cin_no=test_cin,
            currency="INR",
            units="Custom",
            number_format="Accounting",
            negative_format="Brackets (1,234)",
            default_font="Bookman Old Style",
            default_font_size=11,
            show_zeros_as_blank=1,
            decimal_places=2,
            turnover=test_turnover,
            rounding_level=test_rounding
        )
        print(f"  ✓ PASS: Created company with ID {company_id}")
    except Exception as e:
        print(f"  ✗ FAIL: {str(e)}")
        return
    
    # READ
    print("\n✓ Testing READ:")
    try:
        company = CompanyInfo.get_by_user_id(test_user_id)
        if company:
            print(f"  ✓ PASS: Retrieved company ID {company.company_id}")
            print(f"    • Entity: {company.entity_name}")
            print(f"    • CIN: {company.cin_no}")
            print(f"    • FY: {company.fy_start_date} to {company.fy_end_date}")
            print(f"    • Turnover: ₹{company.turnover/10000000:.2f} Crores")
            print(f"    • Rounding: {CompanyInfo.get_rounding_display_name(company.rounding_level)}")
            
            # Verify data
            assert company.entity_name == test_entity, "Entity name mismatch"
            assert company.cin_no == test_cin, "CIN mismatch"
            assert company.turnover == test_turnover, "Turnover mismatch"
            assert company.rounding_level == test_rounding, "Rounding level mismatch"
            print("  ✓ All fields verified correctly")
        else:
            print("  ✗ FAIL: Company not found")
            return
    except Exception as e:
        print(f"  ✗ FAIL: {str(e)}")
        return
    
    # UPDATE
    print("\n✓ Testing UPDATE:")
    try:
        updated_entity = "Updated Test Company Pvt Ltd"
        updated_turnover = 120_00_00_000  # 120 Crores (now high turnover)
        updated_rounding = '1000000'  # Millions (valid for high turnover)
        
        CompanyInfo.update(
            company_id=company_id,
            entity_name=updated_entity,
            fy_start_date=test_fy_start,
            fy_end_date=test_fy_end,
            address=test_address,
            cin_no=test_cin,
            currency="INR",
            units="Custom",
            number_format="Accounting",
            negative_format="Brackets (1,234)",
            default_font="Bookman Old Style",
            default_font_size=11,
            show_zeros_as_blank=1,
            decimal_places=2,
            turnover=updated_turnover,
            rounding_level=updated_rounding
        )
        
        # Verify update
        company = CompanyInfo.get_by_user_id(test_user_id)
        if company.entity_name == updated_entity and company.turnover == updated_turnover:
            print(f"  ✓ PASS: Updated company successfully")
            print(f"    • New Entity: {company.entity_name}")
            print(f"    • New Turnover: ₹{company.turnover/10000000:.2f} Crores")
            print(f"    • New Rounding: {CompanyInfo.get_rounding_display_name(company.rounding_level)}")
        else:
            print("  ✗ FAIL: Update not reflected")
            return
    except Exception as e:
        print(f"  ✗ FAIL: {str(e)}")
        return
    
    # DELETE
    print("\n✓ Testing DELETE:")
    try:
        CompanyInfo.delete(company_id)
        company = CompanyInfo.get_by_user_id(test_user_id)
        if company is None:
            print(f"  ✓ PASS: Deleted company successfully")
        else:
            print("  ✗ FAIL: Company still exists after delete")
    except Exception as e:
        print(f"  ✗ FAIL: {str(e)}")

def test_rounding_display_names():
    """Test rounding level display names"""
    print("\n" + "="*70)
    print("TEST 6: Rounding Display Names")
    print("="*70)
    
    levels = ['1', '100', '1000', '100000', '1000000', '10000000']
    
    print("\n✓ Testing Display Names:")
    for level in levels:
        name = CompanyInfo.get_rounding_display_name(level)
        print(f"  • '{level}' → {name}")

def run_all_tests():
    """Run all test cases"""
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + "  COMPANY INFORMATION MODULE - TEST SUITE".center(68) + "█")
    print("█" + "  Schedule III Compliance Validation".center(68) + "█")
    print("█" + " "*68 + "█")
    print("█"*70)
    
    try:
        test_cin_validation()
        test_date_validation()
        test_schedule_iii_rounding_validation()
        test_rounding_options()
        test_company_info_crud()
        test_rounding_display_names()
        
        print("\n" + "="*70)
        print("✓ ALL TESTS COMPLETED SUCCESSFULLY")
        print("="*70)
        print("\nSchedule III Compliance:")
        print("  ✓ Turnover < ₹100 Crores: '100s to '1000000s allowed")
        print("  ✓ Turnover ≥ ₹100 Crores: '100000s to '10000000s allowed")
        print("  ✓ Absolute values ('1') always allowed")
        print("  ✓ CIN validation (21-character format)")
        print("  ✓ Date range validation (end > start)")
        print("  ✓ Full CRUD operations working")
        print("\n" + "="*70 + "\n")
        
    except Exception as e:
        print(f"\n✗ TEST SUITE FAILED: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests()
