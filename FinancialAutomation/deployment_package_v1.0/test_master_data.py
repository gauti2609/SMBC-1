"""Test Master Data Management functionality"""

import sys
from models.master_data import MajorHead, MinorHead, Grouping

def test_master_data():
    """Test master data CRUD operations"""
    print("Testing Master Data Management...")
    print("=" * 60)
    
    # Test Major Heads
    print("\n1. Testing Major Heads:")
    print("-" * 60)
    major_heads = MajorHead.get_all()
    print(f"   Found {len(major_heads)} major heads")
    for major in major_heads[:5]:
        print(f"   - ID: {major[0]}, Name: {major[1]}, Category: {major[2]}")
    
    # Test Minor Heads
    print("\n2. Testing Minor Heads:")
    print("-" * 60)
    if major_heads:
        first_major = major_heads[0]
        minor_heads = MinorHead.get_all(first_major[0])
        print(f"   Found {len(minor_heads)} minor heads for '{first_major[1]}'")
        for minor in minor_heads[:5]:
            print(f"   - ID: {minor[0]}, Name: {minor[2]}, Major ID: {minor[1]}")
    
    # Test Groupings
    print("\n3. Testing Groupings:")
    print("-" * 60)
    if major_heads:
        minor_heads = MinorHead.get_all(major_heads[0][0])
        if minor_heads:
            first_minor = minor_heads[0]
            groupings = Grouping.get_all(first_minor[0])
            print(f"   Found {len(groupings)} groupings for '{first_minor[2]}'")
            for grouping in groupings[:5]:
                print(f"   - ID: {grouping[0]}, Name: {grouping[2]}, Minor ID: {grouping[1]}")
    
    # Test Create, Update, Delete
    print("\n4. Testing CRUD Operations:")
    print("-" * 60)
    
    try:
        # Create test major head
        print("   Creating test major head...")
        test_id = MajorHead.create("TEST_MAJOR", "Test Category", "Test Description")
        print(f"   ✓ Created with ID: {test_id}")
        
        # Update it
        print("   Updating test major head...")
        MajorHead.update(test_id, "TEST_MAJOR_UPDATED", "Updated Category", "Updated")
        print(f"   ✓ Updated successfully")
        
        # Retrieve it
        retrieved = MajorHead.get_by_id(test_id)
        print(f"   ✓ Retrieved: {retrieved[1]}")
        
        # Delete it
        print("   Deleting test major head...")
        MajorHead.delete(test_id)
        print(f"   ✓ Deleted successfully")
        
        # Verify deletion
        deleted = MajorHead.get_by_id(test_id)
        if deleted is None:
            print(f"   ✓ Confirmed deletion (soft delete)")
        
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Master Data test completed!")
    print("\nYou can now run the main application:")
    print("   python main.py")

if __name__ == "__main__":
    test_master_data()
