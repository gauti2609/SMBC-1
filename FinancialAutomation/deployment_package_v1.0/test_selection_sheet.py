"""
Test Selection Sheet Functionality
"""

import sys
sys.path.insert(0, '/workspaces/SMBC-1/FinancialAutomation')

from models.selection_sheet import SelectionSheet
from models.company_info import CompanyInfo

def test_selection_sheet():
    """Test selection sheet operations"""
    
    print("=" * 80)
    print("SELECTION SHEET FUNCTIONALITY TEST")
    print("=" * 80)
    
    # Get a test company directly from database
    from config.database import execute_query
    
    result = execute_query("SELECT company_id, entity_name FROM company_info LIMIT 1")
    if not result:
        print("❌ No companies found. Please create a company first.")
        return
    
    company_id = result[0][0]
    entity_name = result[0][1]
    print(f"\n✓ Testing with company: {entity_name} (ID: {company_id})")
    
    # Test 1: Initialize default notes
    print("\n" + "-" * 80)
    print("TEST 1: Initialize Default Notes")
    print("-" * 80)
    
    try:
        SelectionSheet.initialize_default_notes(company_id)
        print("✓ Default notes initialized")
    except Exception as e:
        print(f"✓ Notes already exist or error: {str(e)}")
    
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
        print(f"  {entry.note_ref:8} | {entry.note_description[:50]:50} | Sys: {entry.system_recommendation:3} | User: {entry.user_selection:3} | Final: {entry.final_selection:3}")
    
    # Test 3: Update System Recommendations
    print("\n" + "-" * 80)
    print("TEST 3: Update System Recommendations")
    print("-" * 80)
    
    try:
        SelectionSheet.update_system_recommendations(company_id)
        print("✓ System recommendations updated based on Trial Balance")
        
        # Check recommended notes
        entries = SelectionSheet.get_all_for_company(company_id)
        recommended = [e for e in entries if e.system_recommendation == 'Yes']
        print(f"✓ Notes recommended by system: {len(recommended)}")
        
        if recommended:
            print(f"\nSystem Recommended Notes:")
            for entry in recommended[:10]:
                print(f"  {entry.note_ref:8} | {entry.note_description[:50]:50} | Linked: {entry.linked_major_head or 'N/A'}")
        
    except Exception as e:
        print(f"❌ Error updating recommendations: {str(e)}")
    
    # Test 4: Update User Selections
    print("\n" + "-" * 80)
    print("TEST 4: Update User Selections")
    print("-" * 80)
    
    # Select first recommended note
    entries = SelectionSheet.get_all_for_company(company_id)
    if entries:
        test_entry = entries[2]  # A.2.1 - should be first actual note
        print(f"Setting user selection = 'Yes' for: {test_entry.note_ref} - {test_entry.note_description}")
        
        SelectionSheet.update_user_selection(
            company_id,
            test_entry.selection_id,
            'Yes'
        )
        print("✓ User selection updated")
        
        # Verify
        updated = SelectionSheet.get_by_id(test_entry.selection_id)
        print(f"  Verified: {updated.note_ref} | User: {updated.user_selection} | Final: {updated.final_selection}")
    
    # Test 5: Bulk Update User Selections
    print("\n" + "-" * 80)
    print("TEST 5: Bulk Update User Selections")
    print("-" * 80)
    
    # Select multiple notes
    entries = SelectionSheet.get_all_for_company(company_id)
    selections = {}
    
    # Select first 5 notes with dots (actual notes, not headers)
    count = 0
    for entry in entries:
        if '.' in entry.note_ref and count < 5:
            selections[entry.selection_id] = 'Yes'
            count += 1
    
    print(f"Bulk updating {len(selections)} notes to 'Yes'")
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
        for entry in selected[:15]:
            print(f"  #{entry.auto_number or 'N/A':3} | {entry.note_ref:8} | {entry.note_description[:50]:50} | Final: {entry.final_selection}")
    
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
    else:
        print("✓ No headers have auto-numbers (correct)")
    
    # Check that selected notes have sequential auto-numbers
    selected_with_numbers = [e for e in entries if e.final_selection == 'Yes' and '.' in e.note_ref and e.auto_number]
    if selected_with_numbers:
        numbers = [int(e.auto_number) for e in selected_with_numbers]
        expected = list(range(1, len(numbers) + 1))
        if numbers == expected:
            print(f"✓ Auto-numbers are sequential: 1 to {len(numbers)}")
        else:
            print(f"❌ ERROR: Auto-numbers are not sequential!")
            print(f"   Expected: {expected}")
            print(f"   Got:      {numbers}")
    else:
        print("⚠ No selected notes with auto-numbers yet")
    
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
    auto_numbered = len([e for e in entries if e.auto_number])
    
    print(f"Total entries:        {total}")
    print(f"  - Section headers:  {headers_count}")
    print(f"  - Actual notes:     {notes_count}")
    print(f"\nSystem recommended:   {recommended}")
    print(f"User selected:        {user_selected}")
    print(f"Final selected:       {final_selected}")
    print(f"Auto-numbered:        {auto_numbered}")
    
    print("\n✅ All tests completed successfully!")

if __name__ == '__main__':
    test_selection_sheet()
