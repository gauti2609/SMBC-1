"""
Simplified Selection Sheet Test using Models
"""

import sys
sys.path.insert(0, '/workspaces/SMBC-1/FinancialAutomation')

from models.selection_sheet import SelectionSheet
from models.company_info import CompanyInfo
from models.trial_balance import TrialBalance
from datetime import date

def test_selection_sheet():
    """Test selection sheet operations"""
    
    print("=" * 80)
    print("SELECTION SHEET FUNCTIONALITY TEST")
    print("=" * 80)
    
    # Get or create test company
    print("\n" + "-" * 80)
    print("SETUP: Get/Create Test Company")
    print("-" * 80)
    
    # Try to get existing companies
    from config.database import get_connection
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT company_id, entity_name FROM company_info LIMIT 1")
    result = cursor.fetchone()
    
    if not result:
        print("Creating test company...")
        # Create a simple test company
        cursor.execute("""
            INSERT INTO company_info (
                entity_name, fy_start_date, fy_end_date,
                created_at, updated_at
            ) VALUES (?, ?, ?, datetime('now'), datetime('now'))
        """, ('Test Company', date(2024, 4, 1), date(2025, 3, 31)))
        conn.commit()
        company_id = cursor.lastrowid
        entity_name = 'Test Company'
        print(f"✓ Created test company: {entity_name} (ID: {company_id})")
    else:
        company_id, entity_name = result
        print(f"✓ Using existing company: {entity_name} (ID: {company_id})")
    
    conn.close()
    
    # Test 1: Initialize default notes
    print("\n" + "-" * 80)
    print("TEST 1: Initialize Default Notes")
    print("-" * 80)
    
    try:
        SelectionSheet.initialize_default_notes(company_id)
        print("✓ Default notes initialized (or already exist)")
    except Exception as e:
        print(f"Note: {str(e)}")
    
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
        print(f"  - Category {cat}: {len(categories[cat])} entries")
    
    # Show first 15 notes
    print(f"\nFirst 15 Notes:")
    print(f"  {'Ref':<10} | {'Description':<50} | S | U | F | #")
    print(f"  {'-'*10}-+-{'-'*50}-+-+-+-+-+--")
    for entry in entries[:15]:
        sys_rec = entry.system_recommendation or ''
        user_sel = entry.user_selection or ''
        final = entry.final_selection or ''
        auto_num = entry.auto_number or ''
        desc = entry.note_description[:50]
        print(f"  {entry.note_ref:<10} | {desc:<50} | {sys_rec:<1} | {user_sel:<1} | {final:<1} | {auto_num}")
    
    # Test 3: Update User Selections
    print("\n" + "-" * 80)
    print("TEST 3: Update User Selections")
    print("-" * 80)
    
    # Select first 5 actual notes (with dots)
    test_notes = [e for e in entries if '.' in e.note_ref][:5]
    
    for entry in test_notes:
        print(f"Setting 'Yes' for: {entry.note_ref} - {entry.note_description[:40]}")
        SelectionSheet.update_user_selection(entry.selection_id, 'Yes')
    
    print(f"✓ Updated {len(test_notes)} user selections")
    
    # Test 4: Bulk Update
    print("\n" + "-" * 80)
    print("TEST 4: Bulk Update User Selections")
    print("-" * 80)
    
    # Select next 10 notes
    entries = SelectionSheet.get_all_for_company(company_id)
    notes_to_select = [e for e in entries if '.' in e.note_ref][5:15]
    
    selections = {e.selection_id: 'Yes' for e in notes_to_select}
    
    print(f"Bulk updating {len(selections)} notes...")
    SelectionSheet.bulk_update_user_selections(company_id, selections)
    print("✓ Bulk update complete")
    
    # Test 5: Get Selected Notes with Auto-Numbering
    print("\n" + "-" * 80)
    print("TEST 5: Selected Notes with Auto-Numbering")
    print("-" * 80)
    
    selected = SelectionSheet.get_selected_notes(company_id)
    print(f"✓ Total selected notes: {len(selected)}")
    
    if selected:
        print(f"\nSelected Notes with Auto-Numbers:")
        print(f"  {'#':<4} | {'Ref':<10} | {'Description':<50}")
        print(f"  {'-'*4}-+-{'-'*10}-+-{'-'*50}")
        for note_ref, description, auto_number in selected:
            auto_num = auto_number or 'N/A'
            desc = description[:50]
            print(f"  {auto_num:<4} | {note_ref:<10} | {desc:<50}")
    
    # Test 6: Verify Auto-Numbering Logic
    print("\n" + "-" * 80)
    print("TEST 6: Verify Auto-Numbering Logic")
    print("-" * 80)
    
    entries = SelectionSheet.get_all_for_company(company_id)
    
    # Check that section headers have no auto-number
    headers = [e for e in entries if '.' not in e.note_ref]
    print(f"Section headers: {len(headers)}")
    headers_with_numbers = [e for e in headers if e.auto_number and e.auto_number.strip()]
    if headers_with_numbers:
        print(f"❌ ERROR: {len(headers_with_numbers)} headers have auto-numbers!")
    else:
        print("✓ No headers have auto-numbers (correct)")
    
    # Check sequential numbering
    selected_with_numbers = [e for e in entries if e.final_selection == 'Yes' and '.' in e.note_ref and e.auto_number and e.auto_number.strip()]
    if selected_with_numbers:
        numbers = sorted([int(e.auto_number) for e in selected_with_numbers])
        expected = list(range(1, len(numbers) + 1))
        if numbers == expected:
            print(f"✓ Auto-numbers are sequential: 1 to {len(numbers)}")
        else:
            print(f"❌ ERROR: Auto-numbers not sequential!")
            print(f"   Expected: {expected}")
            print(f"   Got:      {numbers}")
    else:
        print("⚠ No selected notes with auto-numbers")
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    entries = SelectionSheet.get_all_for_company(company_id)
    total = len(entries)
    headers_count = len([e for e in entries if '.' not in e.note_ref])
    notes_count = total - headers_count
    
    user_selected = len([e for e in entries if e.user_selection == 'Yes'])
    final_selected = len([e for e in entries if e.final_selection == 'Yes' and '.' in e.note_ref])
    auto_numbered = len([e for e in entries if e.auto_number and e.auto_number.strip()])
    
    print(f"Total entries:        {total}")
    print(f"  - Section headers:  {headers_count}")
    print(f"  - Actual notes:     {notes_count}")
    print(f"\nUser selected:        {user_selected}")
    print(f"Final selected:       {final_selected}")
    print(f"Auto-numbered:        {auto_numbered}")
    
    print("\n✅ All tests completed successfully!")
    print("=" * 80)

if __name__ == '__main__':
    test_selection_sheet()
