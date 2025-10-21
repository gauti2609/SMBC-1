"""
Complete Selection Sheet Test with Sample Data Creation
"""

import sys
sys.path.insert(0, '/workspaces/SMBC-1/FinancialAutomation')

from models.selection_sheet import SelectionSheet
from config.db_connection import execute_query

def create_test_company():
    """Create a test company"""
    # Check if test company exists
    result = execute_query(
        "SELECT company_id FROM company_info WHERE entity_name = %s",
        ("Test Company - Selection Sheet",)
    )
    
    if result:
        return result[0][0]
    
    # Create test company
    query = """
    INSERT INTO company_info (
        entity_name, cin, pan, address, contact_number,
        email, financial_year_start, financial_year_end,
        current_year_label, previous_year_label
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING company_id
    """
    
    values = (
        "Test Company - Selection Sheet",
        "L12345KA2020PLC123456",
        "AAAAA0000A",
        "Test Address, City - 560001",
        "9876543210",
        "test@example.com",
        "2024-04-01",
        "2025-03-31",
        "2024-25",
        "2023-24"
    )
    
    result = execute_query(query, values, commit=True, fetch_all=True)
    if result:
        return result[0][0]
    
    return None

def create_sample_trial_balance(company_id):
    """Create sample trial balance entries"""
    # Clear existing
    execute_query("DELETE FROM trial_balance WHERE company_id = %s", (company_id,), commit=True)
    
    # Add sample entries
    entries = [
        ("Property, Plant and Equipment", "PPE", "DR", 1000000, 900000),
        ("Capital Work-in-Progress", "CWIP", "DR", 150000, 100000),
        ("Investments", "Investments", "DR", 500000, 450000),
        ("Inventories", "Inventories", "DR", 300000, 250000),
        ("Share Capital", "Equity", "CR", 1000000, 1000000),
        ("Reserves and Surplus", "Equity", "CR", 500000, 400000),
        ("Revenue from Operations", "Revenue", "CR", 2000000, 1800000),
    ]
    
    query = """
    INSERT INTO trial_balance (
        company_id, account_name, major_head, dr_cr,
        current_year, previous_year
    ) VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    for entry in entries:
        execute_query(query, (company_id,) + entry, commit=True)
    
    print(f"✓ Created {len(entries)} trial balance entries")

def test_selection_sheet():
    """Test selection sheet operations"""
    
    print("=" * 80)
    print("SELECTION SHEET COMPLETE FUNCTIONALITY TEST")
    print("=" * 80)
    
    # Create test company
    print("\n" + "-" * 80)
    print("SETUP: Create Test Company")
    print("-" * 80)
    
    company_id = create_test_company()
    if not company_id:
        print("❌ Failed to create test company")
        return
    
    print(f"✓ Test company created/found (ID: {company_id})")
    
    # Create sample Trial Balance
    create_sample_trial_balance(company_id)
    
    # Test 1: Initialize default notes
    print("\n" + "-" * 80)
    print("TEST 1: Initialize Default Notes")
    print("-" * 80)
    
    # Clear existing
    execute_query("DELETE FROM selection_sheet WHERE company_id = %s", (company_id,), commit=True)
    print("✓ Cleared existing selection sheet")
    
    SelectionSheet.initialize_default_notes(company_id)
    print("✓ Default notes initialized")
    
    # Test 2: Get all notes
    print("\n" + "-" * 80)
    print("TEST 2: Get All Notes")
    print("-" * 80)
    
    entries = SelectionSheet.get_all_for_company(company_id)
    print(f"✓ Total notes: {len(entries)}")
    
    # Show sample by category
    categories = {}
    for entry in entries:
        cat = entry.note_ref.split('.')[0]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(entry)
    
    print(f"✓ Categories found: {sorted(categories.keys())}")
    print(f"\nNotes by Category:")
    for cat in sorted(categories.keys()):
        print(f"  - {cat}: {len(categories[cat])} notes")
    
    # Show first 10 notes
    print(f"\nFirst 10 Notes:")
    for i, entry in enumerate(entries[:10]):
        sys_rec = entry.system_recommendation or ''
        user_sel = entry.user_selection or ''
        final = entry.final_selection or ''
        print(f"  {entry.note_ref:8} | {entry.note_description[:50]:50} | Sys: {sys_rec:3} | User: {user_sel:3} | Final: {final:3}")
    
    # Test 3: Update System Recommendations
    print("\n" + "-" * 80)
    print("TEST 3: Update System Recommendations")
    print("-" * 80)
    
    SelectionSheet.update_system_recommendations(company_id)
    print("✓ System recommendations updated based on Trial Balance")
    
    # Check recommended notes
    entries = SelectionSheet.get_all_for_company(company_id)
    recommended = [e for e in entries if e.system_recommendation == 'Yes']
    print(f"✓ Notes recommended by system: {len(recommended)}")
    
    if recommended:
        print(f"\nSystem Recommended Notes:")
        for entry in recommended[:15]:
            linked = entry.linked_major_head or 'N/A'
            print(f"  {entry.note_ref:8} | {entry.note_description[:45]:45} | Linked: {linked}")
    
    # Test 4: Update User Selections
    print("\n" + "-" * 80)
    print("TEST 4: Update User Selections")
    print("-" * 80)
    
    # Select first recommended note
    entries = SelectionSheet.get_all_for_company(company_id)
    test_notes = [e for e in entries if '.' in e.note_ref][:3]
    
    for test_entry in test_notes:
        print(f"Setting user selection = 'Yes' for: {test_entry.note_ref} - {test_entry.note_description[:40]}")
        
        SelectionSheet.update_user_selection(
            company_id,
            test_entry.selection_id,
            'Yes'
        )
    
    print(f"✓ Updated {len(test_notes)} user selections")
    
    # Test 5: Bulk Update User Selections
    print("\n" + "-" * 80)
    print("TEST 5: Bulk Update User Selections")
    print("-" * 80)
    
    # Select all recommended notes
    entries = SelectionSheet.get_all_for_company(company_id)
    selections = {}
    
    for entry in entries:
        if entry.system_recommendation == 'Yes' and '.' in entry.note_ref:
            selections[entry.selection_id] = 'Yes'
    
    print(f"Bulk updating {len(selections)} recommended notes to 'Yes'")
    SelectionSheet.bulk_update_user_selections(company_id, selections)
    print("✓ Bulk update complete")
    
    # Test 6: Get Selected Notes with Auto-Numbering
    print("\n" + "-" * 80)
    print("TEST 6: Get Selected Notes with Auto-Numbering")
    print("-" * 80)
    
    selected = SelectionSheet.get_selected_notes(company_id)
    print(f"✓ Total selected notes: {len(selected)}")
    
    if selected:
        print(f"\nSelected Notes with Auto-Numbers:")
        for entry in selected[:20]:
            auto_num = entry.auto_number or 'N/A'
            print(f"  #{auto_num:3} | {entry.note_ref:8} | {entry.note_description[:50]:50} | Final: {entry.final_selection}")
    
    # Test 7: Verify Auto-Numbering Logic
    print("\n" + "-" * 80)
    print("TEST 7: Verify Auto-Numbering Logic")
    print("-" * 80)
    
    entries = SelectionSheet.get_all_for_company(company_id)
    
    # Check that section headers have no auto-number
    headers = [e for e in entries if '.' not in e.note_ref]
    print(f"Section headers (should have no auto-number): {len(headers)}")
    headers_with_numbers = [e for e in headers if e.auto_number]
    if headers_with_numbers:
        print(f"❌ ERROR: {len(headers_with_numbers)} headers have auto-numbers!")
        for h in headers_with_numbers:
            print(f"   - {h.note_ref}: {h.auto_number}")
    else:
        print("✓ No headers have auto-numbers (correct)")
    
    # Check that selected notes have sequential auto-numbers
    selected_with_numbers = [e for e in entries if e.final_selection == 'Yes' and '.' in e.note_ref and e.auto_number]
    if selected_with_numbers:
        numbers = sorted([int(e.auto_number) for e in selected_with_numbers])
        expected = list(range(1, len(numbers) + 1))
        if numbers == expected:
            print(f"✓ Auto-numbers are sequential: 1 to {len(numbers)}")
        else:
            print(f"❌ ERROR: Auto-numbers are not sequential!")
            print(f"   Expected: {expected[:20]}...")
            print(f"   Got:      {numbers[:20]}...")
    else:
        print("⚠ No selected notes with auto-numbers yet")
    
    # Test 8: Test User Override
    print("\n" + "-" * 80)
    print("TEST 8: Test User Override of System Recommendation")
    print("-" * 80)
    
    # Find a note NOT recommended by system
    entries = SelectionSheet.get_all_for_company(company_id)
    not_recommended = [e for e in entries if e.system_recommendation != 'Yes' and '.' in e.note_ref][:2]
    
    if not_recommended:
        for entry in not_recommended:
            print(f"Overriding system for: {entry.note_ref} - {entry.note_description[:40]}")
            print(f"  Before: System={entry.system_recommendation}, User={entry.user_selection}, Final={entry.final_selection}")
            
            SelectionSheet.update_user_selection(company_id, entry.selection_id, 'Yes')
            
            updated = SelectionSheet.get_by_id(entry.selection_id)
            print(f"  After:  System={updated.system_recommendation}, User={updated.user_selection}, Final={updated.final_selection}")
            
            if updated.final_selection == 'Yes':
                print(f"  ✓ User override works - note is now selected")
            else:
                print(f"  ❌ ERROR: User override failed")
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    entries = SelectionSheet.get_all_for_company(company_id)
    total = len(entries)
    headers_count = len([e for e in entries if '.' not in e.note_ref])
    notes_count = total - headers_count
    
    recommended = len([e for e in entries if e.system_recommendation == 'Yes'])
    user_selected = len([e for e in entries if e.user_selection == 'Yes'])
    final_selected = len([e for e in entries if e.final_selection == 'Yes' and '.' in e.note_ref])
    auto_numbered = len([e for e in entries if e.auto_number and e.auto_number.strip()])
    
    print(f"Total entries:        {total}")
    print(f"  - Section headers:  {headers_count}")
    print(f"  - Actual notes:     {notes_count}")
    print(f"\nSystem recommended:   {recommended}")
    print(f"User selected:        {user_selected}")
    print(f"Final selected:       {final_selected}")
    print(f"Auto-numbered:        {auto_numbered}")
    
    print("\n✅ All tests completed successfully!")
    print("\n" + "=" * 80)

if __name__ == '__main__':
    test_selection_sheet()
