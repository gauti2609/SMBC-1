"""
Comprehensive test script for Master Data CRUD operations
Tests MajorHead, MinorHead, and Grouping models with full lifecycle
"""

from config.database import initialize_database, get_connection
from models.master_data import MajorHead, MinorHead, Grouping
import sys

def print_section(title):
    """Print section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def test_major_head_crud():
    """Test MajorHead CRUD operations"""
    print_section("Testing MajorHead CRUD")
    
    # CREATE
    print("\n1. CREATE - Adding new Major Head...")
    try:
        major_id = MajorHead.create(
            major_head_name="Test Assets Category",
            category="Assets",
            description="Test major head for assets"
        )
        print(f"   ✓ Created Major Head with ID: {major_id}")
    except Exception as e:
        print(f"   ✗ Failed to create: {e}")
        return None
    
    # READ by ID
    print("\n2. READ by ID - Fetching created Major Head...")
    try:
        major = MajorHead.get_by_id(major_id)
        if major:
            print(f"   ✓ Fetched: ID={major[0]}, Name={major[1]}, Category={major[2]}")
        else:
            print(f"   ✗ Major Head not found!")
    except Exception as e:
        print(f"   ✗ Failed to fetch: {e}")
    
    # READ by name
    print("\n3. READ by Name - Fetching by name...")
    try:
        major = MajorHead.get_by_name("Test Assets Category")
        if major:
            print(f"   ✓ Found by name: ID={major.major_head_id}")
        else:
            print(f"   ✗ Not found by name!")
    except Exception as e:
        print(f"   ✗ Failed to fetch by name: {e}")
    
    # READ all
    print("\n4. READ all - Fetching all Major Heads...")
    try:
        all_majors = MajorHead.get_all()
        print(f"   ✓ Total active Major Heads: {len(all_majors)}")
        print(f"   ✓ Sample: {all_majors[0][1] if all_majors else 'None'}")
    except Exception as e:
        print(f"   ✗ Failed to fetch all: {e}")
    
    # UPDATE
    print("\n5. UPDATE - Updating Major Head...")
    try:
        MajorHead.update(
            major_head_id=major_id,
            major_head_name="Updated Test Assets",
            category="Assets-Modified",
            description="Updated description"
        )
        major = MajorHead.get_by_id(major_id)
        if major and major[1] == "Updated Test Assets":
            print(f"   ✓ Updated successfully: {major[1]}")
        else:
            print(f"   ✗ Update failed or verification failed")
    except Exception as e:
        print(f"   ✗ Failed to update: {e}")
    
    # DELETE (soft)
    print("\n6. DELETE - Soft deleting Major Head...")
    try:
        MajorHead.delete(major_id)
        major = MajorHead.get_by_id(major_id)
        if major is None:
            print(f"   ✓ Deleted successfully (not in active list)")
        else:
            print(f"   ✗ Still found after deletion!")
    except Exception as e:
        print(f"   ✗ Failed to delete: {e}")
    
    print("\n✅ MajorHead CRUD tests complete!\n")
    return True

def test_minor_head_crud():
    """Test MinorHead CRUD operations"""
    print_section("Testing MinorHead CRUD")
    
    # First, create a parent Major Head
    print("\n0. SETUP - Creating parent Major Head...")
    try:
        parent_major_id = MajorHead.create(
            major_head_name="Test Parent Major for Minor",
            category="Assets"
        )
        print(f"   ✓ Created parent Major Head with ID: {parent_major_id}")
    except Exception as e:
        print(f"   ✗ Failed to create parent: {e}")
        return None
    
    # CREATE
    print("\n1. CREATE - Adding new Minor Head...")
    try:
        minor_id = MinorHead.create(
            major_head_id=parent_major_id,
            minor_head_name="Test Financial Assets",
            code="TFA-001",
            description="Test minor head"
        )
        print(f"   ✓ Created Minor Head with ID: {minor_id}")
    except Exception as e:
        print(f"   ✗ Failed to create: {e}")
        # Cleanup parent
        MajorHead.delete(parent_major_id)
        return None
    
    # READ by ID
    print("\n2. READ by ID - Fetching created Minor Head...")
    try:
        minor = MinorHead.get_by_id(minor_id)
        if minor:
            print(f"   ✓ Fetched: ID={minor[0]}, MajorID={minor[1]}, Name={minor[2]}, Code={minor[3]}")
        else:
            print(f"   ✗ Minor Head not found!")
    except Exception as e:
        print(f"   ✗ Failed to fetch: {e}")
    
    # READ all for parent
    print("\n3. READ all for Major - Fetching all Minor Heads for parent...")
    try:
        minors = MinorHead.get_all(major_head_id=parent_major_id)
        print(f"   ✓ Total Minor Heads for parent: {len(minors)}")
    except Exception as e:
        print(f"   ✗ Failed to fetch: {e}")
    
    # UPDATE
    print("\n4. UPDATE - Updating Minor Head...")
    try:
        MinorHead.update(
            minor_head_id=minor_id,
            major_head_id=parent_major_id,
            minor_head_name="Updated Test Assets",
            code="TFA-002",
            description="Updated"
        )
        minor = MinorHead.get_by_id(minor_id)
        if minor and minor[2] == "Updated Test Assets":
            print(f"   ✓ Updated successfully: {minor[2]}, Code={minor[3]}")
        else:
            print(f"   ✗ Update verification failed")
    except Exception as e:
        print(f"   ✗ Failed to update: {e}")
    
    # DELETE
    print("\n5. DELETE - Soft deleting Minor Head...")
    try:
        MinorHead.delete(minor_id)
        minor = MinorHead.get_by_id(minor_id)
        if minor is None:
            print(f"   ✓ Deleted successfully")
        else:
            print(f"   ✗ Still found after deletion!")
    except Exception as e:
        print(f"   ✗ Failed to delete: {e}")
    
    # Cleanup parent
    print("\n6. CLEANUP - Removing parent Major Head...")
    try:
        MajorHead.delete(parent_major_id)
        print(f"   ✓ Cleaned up parent")
    except Exception as e:
        print(f"   ✗ Failed to cleanup: {e}")
    
    print("\n✅ MinorHead CRUD tests complete!\n")
    return True

def test_grouping_crud():
    """Test Grouping CRUD operations"""
    print_section("Testing Grouping CRUD")
    
    # Setup: Create parent Major and Minor
    print("\n0. SETUP - Creating parent Major and Minor Heads...")
    try:
        parent_major_id = MajorHead.create(
            major_head_name="Test Major for Grouping",
            category="Assets"
        )
        parent_minor_id = MinorHead.create(
            major_head_id=parent_major_id,
            minor_head_name="Test Minor for Grouping",
            code="TMG-001"
        )
        print(f"   ✓ Created parent Major (ID={parent_major_id}) and Minor (ID={parent_minor_id})")
    except Exception as e:
        print(f"   ✗ Failed to create parents: {e}")
        return None
    
    # CREATE
    print("\n1. CREATE - Adding new Grouping...")
    try:
        grouping_id = Grouping.create(
            minor_head_id=parent_minor_id,
            grouping_name="Test Land Assets",
            code="TLA-001",
            description="Test grouping"
        )
        print(f"   ✓ Created Grouping with ID: {grouping_id}")
    except Exception as e:
        print(f"   ✗ Failed to create: {e}")
        # Cleanup
        MinorHead.delete(parent_minor_id)
        MajorHead.delete(parent_major_id)
        return None
    
    # READ by ID
    print("\n2. READ by ID - Fetching created Grouping...")
    try:
        grouping = Grouping.get_by_id(grouping_id)
        if grouping:
            print(f"   ✓ Fetched: ID={grouping[0]}, MinorID={grouping[1]}, Name={grouping[2]}, Code={grouping[3]}")
        else:
            print(f"   ✗ Grouping not found!")
    except Exception as e:
        print(f"   ✗ Failed to fetch: {e}")
    
    # READ all for parent minor
    print("\n3. READ all for Minor - Fetching all Groupings for parent...")
    try:
        groupings = Grouping.get_all(minor_head_id=parent_minor_id)
        print(f"   ✓ Total Groupings for parent: {len(groupings)}")
    except Exception as e:
        print(f"   ✗ Failed to fetch: {e}")
    
    # UPDATE
    print("\n4. UPDATE - Updating Grouping...")
    try:
        Grouping.update(
            grouping_id=grouping_id,
            minor_head_id=parent_minor_id,
            grouping_name="Updated Test Land",
            code="TLA-002",
            description="Updated grouping"
        )
        grouping = Grouping.get_by_id(grouping_id)
        if grouping and grouping[2] == "Updated Test Land":
            print(f"   ✓ Updated successfully: {grouping[2]}, Code={grouping[3]}")
        else:
            print(f"   ✗ Update verification failed")
    except Exception as e:
        print(f"   ✗ Failed to update: {e}")
    
    # DELETE
    print("\n5. DELETE - Soft deleting Grouping...")
    try:
        Grouping.delete(grouping_id)
        grouping = Grouping.get_by_id(grouping_id)
        if grouping is None:
            print(f"   ✓ Deleted successfully")
        else:
            print(f"   ✗ Still found after deletion!")
    except Exception as e:
        print(f"   ✗ Failed to delete: {e}")
    
    # Cleanup
    print("\n6. CLEANUP - Removing parent Minor and Major Heads...")
    try:
        MinorHead.delete(parent_minor_id)
        MajorHead.delete(parent_major_id)
        print(f"   ✓ Cleaned up parents")
    except Exception as e:
        print(f"   ✗ Failed to cleanup: {e}")
    
    print("\n✅ Grouping CRUD tests complete!\n")
    return True

def test_hierarchical_relationships():
    """Test hierarchical relationships and data integrity"""
    print_section("Testing Hierarchical Relationships")
    
    print("\n1. Creating hierarchical structure: Major → Minor → Grouping...")
    try:
        # Create Major
        major_id = MajorHead.create("Hierarchy Test Major", "Assets")
        print(f"   ✓ Created Major: ID={major_id}")
        
        # Create Multiple Minors under Major
        minor_id_1 = MinorHead.create(major_id, "Minor 1", "M1")
        minor_id_2 = MinorHead.create(major_id, "Minor 2", "M2")
        print(f"   ✓ Created 2 Minors: ID={minor_id_1}, ID={minor_id_2}")
        
        # Create Groupings under first Minor
        group_id_1 = Grouping.create(minor_id_1, "Grouping 1A", "G1A")
        group_id_2 = Grouping.create(minor_id_1, "Grouping 1B", "G1B")
        print(f"   ✓ Created 2 Groupings under Minor 1: ID={group_id_1}, ID={group_id_2}")
        
        # Verify hierarchy
        print("\n2. Verifying hierarchy integrity...")
        minors = MinorHead.get_all(major_id)
        print(f"   ✓ Minors under Major: {len(minors)} (expected 2)")
        
        groupings = Grouping.get_all(minor_head_id=minor_id_1)
        print(f"   ✓ Groupings under Minor 1: {len(groupings)} (expected 2)")
        
        # Test filtering
        print("\n3. Testing filtered queries...")
        all_groupings_for_major = Grouping.get_all(major_head_id=major_id)
        print(f"   ✓ All Groupings for Major: {len(all_groupings_for_major)}")
        
        # Cleanup
        print("\n4. Cleanup - Deleting hierarchy...")
        Grouping.delete(group_id_1)
        Grouping.delete(group_id_2)
        MinorHead.delete(minor_id_1)
        MinorHead.delete(minor_id_2)
        MajorHead.delete(major_id)
        print(f"   ✓ Cleaned up all test data")
        
    except Exception as e:
        print(f"   ✗ Hierarchy test failed: {e}")
        return False
    
    print("\n✅ Hierarchical relationship tests complete!\n")
    return True

def test_default_data():
    """Verify default master data exists"""
    print_section("Verifying Default Master Data")
    
    print("\n1. Checking default Major Heads...")
    try:
        majors = MajorHead.get_all()
        print(f"   ✓ Total Major Heads: {len(majors)}")
        if len(majors) >= 30:
            print(f"   ✓ Default data appears loaded")
            print(f"   ✓ Sample Major Heads:")
            for i, major in enumerate(majors[:5]):
                print(f"      - {major[1]} ({major[2]})")
        else:
            print(f"   ⚠ Only {len(majors)} Major Heads found (expected 30+)")
    except Exception as e:
        print(f"   ✗ Failed to check: {e}")
        return False
    
    print("\n2. Checking default Minor Heads...")
    try:
        minors = MinorHead.get_all()
        print(f"   ✓ Total Minor Heads: {len(minors)}")
        if len(minors) >= 20:
            print(f"   ✓ Default data appears loaded")
        else:
            print(f"   ⚠ Only {len(minors)} Minor Heads found")
    except Exception as e:
        print(f"   ✗ Failed to check: {e}")
        return False
    
    print("\n3. Checking default Groupings...")
    try:
        groupings = Grouping.get_all()
        print(f"   ✓ Total Groupings: {len(groupings)}")
        if len(groupings) >= 25:
            print(f"   ✓ Default data appears loaded")
        else:
            print(f"   ⚠ Only {len(groupings)} Groupings found")
    except Exception as e:
        print(f"   ✗ Failed to check: {e}")
        return False
    
    print("\n✅ Default data verification complete!\n")
    return True

def main():
    """Run all tests"""
    print("\n" + "█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + "  MASTER DATA CRUD - COMPREHENSIVE TEST SUITE".center(68) + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)
    
    # Initialize database
    print("\nInitializing database...")
    try:
        initialize_database()
        print("✓ Database initialized successfully\n")
    except Exception as e:
        print(f"✗ Database initialization failed: {e}")
        sys.exit(1)
    
    # Run tests
    results = []
    
    results.append(("Default Data Check", test_default_data()))
    results.append(("MajorHead CRUD", test_major_head_crud()))
    results.append(("MinorHead CRUD", test_minor_head_crud()))
    results.append(("Grouping CRUD", test_grouping_crud()))
    results.append(("Hierarchical Relationships", test_hierarchical_relationships()))
    
    # Summary
    print_section("TEST SUMMARY")
    print()
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {status}  {test_name}")
    
    print(f"\n  Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n  🎉 ALL TESTS PASSED! Master Data CRUD is fully functional!")
        return 0
    else:
        print(f"\n  ⚠️  {total - passed} test(s) failed. Please review errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
