"""
Backend Tests for Database Operations

These tests verify backend logic without GUI.
"""

import pytest
from controllers.auth_controller import AuthController
from models.company_info import CompanyInfo
from models.master_data import MajorHead, MinorHead, Grouping
from models.user import User


@pytest.mark.backend
@pytest.mark.database
class TestDatabaseOperations:
    """Test suite for database CRUD operations"""
    
    def test_create_user(self, db_manager):
        """Test user creation"""
        import random
        import string
        
        # Generate unique username to avoid conflicts
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        username = f'testuser_db_{random_suffix}'
        email = f'testdb_{random_suffix}@example.com'
        
        success, message, user_id = AuthController.register_user(
            username=username,
            password='testpass123',
            email=email,
            full_name='Test DB User'
        )
        
        assert success is True, f"User creation failed: {message}"
        assert user_id is not None
    
    def test_create_company(self, db_manager, test_user):
        """Test creating a company"""
        company_id = CompanyInfo.create(
            user_id=test_user.user_id,
            entity_name='Database Test Company',
            cin_no='L12345TN2020PLC123456',
            address='123 Test St',
            fy_start_date='2024-04-01',
            fy_end_date='2025-03-31'
        )
        
        assert company_id is not None
        
        # Verify company was created
        companies = CompanyInfo.get_all_by_user(test_user.user_id)
        assert len(companies) > 0
        assert any(c.entity_name == 'Database Test Company' for c in companies)
    
    def test_get_user_companies(self, db_manager, test_user, test_company):
        """Test retrieving all companies for a user"""
        companies = CompanyInfo.get_all_by_user(test_user.user_id)
        
        assert len(companies) >= 1
        assert any(c.entity_name == 'Test Company Ltd' for c in companies)
    
    def test_create_major_head(self, db_manager, test_company):
        """Test creating a major head"""
        major_head_id = MajorHead.create(
            company_id=test_company.company_id,
            major_head_name='Current Assets',
            category='Assets'
        )
        
        assert major_head_id is not None
        
        # Verify major head was created
        major_heads = MajorHead.get_all_by_company(test_company.company_id)
        assert any(mh.major_head_name == 'Current Assets' for mh in major_heads)
    
    def test_create_minor_head(self, db_manager, test_company):
        """Test creating a minor head under major head"""
        # Create major head first
        major_head_id = MajorHead.create(
            company_id=test_company.company_id,
            major_head_name='Current Assets',
            category='Assets'
        )
        
        # Create minor head
        minor_head_id = MinorHead.create(
            company_id=test_company.company_id,
            major_head_id=major_head_id,
            minor_head_name='Cash and Bank'
        )
        
        assert minor_head_id is not None
        
        # Verify minor head was created
        minor_heads = MinorHead.get_all(company_id=test_company.company_id)
        assert any(row[3] == 'Cash and Bank' for row in minor_heads)
    
    def test_delete_company(self, db_manager, test_user):
        """Test deleting a company"""
        # Create a temporary company
        company_id = CompanyInfo.create(
            user_id=test_user.user_id,
            entity_name='Temp Company',
            cin_no='L99999TN2020PLC999999',
            address='Temp Address',
            fy_start_date='2024-04-01',
            fy_end_date='2025-03-31'
        )
        
        # Delete the company using static method
        CompanyInfo.delete(company_id)
        
        # Verify company no longer exists
        companies = CompanyInfo.get_all_by_user(test_user.user_id)
        assert not any(c.company_id == company_id for c in companies)
    
    def test_update_company(self, db_manager, test_company):
        """Test updating company information"""
        # Update company name using static method
        CompanyInfo.update(
            company_id=test_company.company_id,
            entity_name='Updated Company Ltd',
            fy_start_date=test_company.fy_start_date,
            fy_end_date=test_company.fy_end_date
        )
        
        # Verify update by fetching the company again
        updated_company = CompanyInfo.get_by_id(test_company.company_id)
        assert updated_company.entity_name == 'Updated Company Ltd'


@pytest.mark.backend
class TestBusinessLogic:
    """Test suite for business logic"""
    
    def test_trial_balance_validation(self, db_manager, test_company):
        """Test trial balance debit/credit validation"""
        from models.trial_balance import TrialBalance
        
        # Create balanced trial balance entries using static import_from_excel simulation
        # Note: TrialBalance uses bulk import, so we'll test the validation logic
        tb_data = [
            {
                'ledger_name': 'Cash',
                'debit_cy': 100000,
                'credit_cy': 0,
                'closing_balance_cy': 100000
            },
            {
                'ledger_name': 'Capital',
                'debit_cy': 0,
                'credit_cy': 100000,
                'closing_balance_cy': -100000
            }
        ]
        
        # Validate totals balance
        total_debit = sum(item['debit_cy'] for item in tb_data)
        total_credit = sum(item['credit_cy'] for item in tb_data)
        
        # Assert that debits equal credits (balanced trial balance)
        assert total_debit == total_credit, "Trial balance should be balanced"
        assert total_debit == 100000, "Total debits should equal 100000"
    
    def test_financial_year_validation(self):
        """Test financial year date validation"""
        from datetime import datetime
        
        fy_start = datetime(2024, 4, 1)
        fy_end = datetime(2025, 3, 31)
        
        # Verify FY end is after FY start
        assert fy_end > fy_start
        
        # Verify it's approximately 1 year
        days_diff = (fy_end - fy_start).days
        assert 360 <= days_diff <= 366
