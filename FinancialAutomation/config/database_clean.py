"""Database initialization and management"""

import os
from datetime import datetime
# Delegate connection handling to the db_connection abstraction which supports
# both SQLite (development) and PostgreSQL (production).
from .db_connection import get_connection, execute_query, adapt_sql, close_pool, release_connection
from config.settings import DB_TYPE, DB_PATH

def initialize_database():
    """Initialize the database with all required tables"""
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Users table - MUST BE FIRST (referenced by company_info)
    sql = adapt_sql('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            full_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
    ''')
    cursor.execute(sql)
    
    # Licenses table
    sql = adapt_sql('''
        CREATE TABLE IF NOT EXISTS licenses (
            license_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            license_key TEXT UNIQUE NOT NULL,
            license_type TEXT NOT NULL,
            issue_date DATE NOT NULL,
            expiry_date DATE,
            is_active BOOLEAN DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    cursor.execute(sql)
    
    # Company Info table - MUST BE BEFORE major_heads/minor_heads/groupings
    sql = adapt_sql('''
        CREATE TABLE IF NOT EXISTS company_info (
            company_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            entity_name TEXT NOT NULL,
            address TEXT,
            cin_no TEXT,
            fy_start_date DATE NOT NULL,
            fy_end_date DATE NOT NULL,
            currency TEXT DEFAULT 'INR',
            units TEXT DEFAULT 'Millions',
            number_format TEXT DEFAULT 'Accounting',
            negative_format TEXT DEFAULT 'Brackets',
            default_font TEXT DEFAULT 'Bookman Old Style',
            default_font_size INTEGER DEFAULT 11,
            show_zeros_as_blank BOOLEAN DEFAULT 0,
            decimal_places INTEGER DEFAULT 2,
            turnover REAL DEFAULT 0,
            rounding_level TEXT DEFAULT '100000',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    cursor.execute(sql)
    
    # Major Heads table
    sql = adapt_sql('''
        CREATE TABLE IF NOT EXISTS major_heads (
            major_head_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            major_head_name TEXT NOT NULL,
            category TEXT NOT NULL,
            -- Opening balances for comparative financial statements
            opening_balance_cy REAL DEFAULT 0,
            opening_balance_py REAL DEFAULT 0,
            display_order INTEGER,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (company_id) REFERENCES company_info(company_id),
            UNIQUE(company_id, major_head_name)
        )
    ''')
    cursor.execute(sql)
    
    # Minor Heads table
    sql = adapt_sql('''
        CREATE TABLE IF NOT EXISTS minor_heads (
            minor_head_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            minor_head_name TEXT NOT NULL,
            major_head_id INTEGER NOT NULL,
            -- Opening balances for comparative financial statements
            opening_balance_cy REAL DEFAULT 0,
            opening_balance_py REAL DEFAULT 0,
            display_order INTEGER,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (company_id) REFERENCES company_info(company_id),
            FOREIGN KEY (major_head_id) REFERENCES major_heads(major_head_id),
            UNIQUE(company_id, minor_head_name, major_head_id)
        )
    ''')
    cursor.execute(sql)
    
    # Groupings table
    sql = adapt_sql('''
        CREATE TABLE IF NOT EXISTS groupings (
            grouping_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            grouping_name TEXT NOT NULL,
            minor_head_id INTEGER NOT NULL,
            major_head_id INTEGER NOT NULL,
            -- Opening balances for comparative financial statements
            opening_balance_cy REAL DEFAULT 0,
            opening_balance_py REAL DEFAULT 0,
            display_order INTEGER,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (company_id) REFERENCES company_info(company_id),
            FOREIGN KEY (minor_head_id) REFERENCES minor_heads(minor_head_id),
            FOREIGN KEY (major_head_id) REFERENCES major_heads(major_head_id),
            UNIQUE(company_id, grouping_name, minor_head_id, major_head_id)
        )
    ''')
    cursor.execute(sql)
    
    # Trial Balance table
    sql = adapt_sql('''
        CREATE TABLE IF NOT EXISTS trial_balance (
            tb_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            ledger_name TEXT NOT NULL,
            -- Current Year (CY) figures
            opening_balance_cy REAL DEFAULT 0,
            debit_cy REAL DEFAULT 0,
            credit_cy REAL DEFAULT 0,
            closing_balance_cy REAL DEFAULT 0,
            -- Previous Year (PY) figures for comparatives
            opening_balance_py REAL DEFAULT 0,
            debit_py REAL DEFAULT 0,
            credit_py REAL DEFAULT 0,
            closing_balance_py REAL DEFAULT 0,
            -- Classification and mapping
            type_bs_pl TEXT NOT NULL,  -- 'BS' or 'PL'
            major_head_id INTEGER,
            minor_head_id INTEGER,
            grouping_id INTEGER,
            is_mapped INTEGER DEFAULT 0,  -- 0 = unmapped, 1 = mapped
            import_batch_id INTEGER,  -- Track which import batch
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (company_id) REFERENCES company_info(company_id),
            FOREIGN KEY (major_head_id) REFERENCES major_heads(major_head_id),
            FOREIGN KEY (minor_head_id) REFERENCES minor_heads(minor_head_id),
            FOREIGN KEY (grouping_id) REFERENCES groupings(grouping_id)
        )
    ''')
    cursor.execute(sql)
    
    # Share Capital table
    sql = adapt_sql('''
        CREATE TABLE IF NOT EXISTS share_capital (
            share_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            class_of_share TEXT NOT NULL,
            authorized_shares REAL DEFAULT 0,
            face_value REAL DEFAULT 0,
            opening_shares_cy REAL DEFAULT 0,
            shares_issued_cy REAL DEFAULT 0,
            closing_shares_cy REAL DEFAULT 0,
            opening_shares_py REAL DEFAULT 0,
            shares_issued_py REAL DEFAULT 0,
            closing_shares_py REAL DEFAULT 0,
            FOREIGN KEY (company_id) REFERENCES company_info(company_id)
        )
    ''')
    cursor.execute(sql)
    
    # Shareholders table
    sql = adapt_sql('''
        CREATE TABLE IF NOT EXISTS shareholders (
            shareholder_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            shareholder_name TEXT NOT NULL,
            shares_cy REAL DEFAULT 0,
            shares_py REAL DEFAULT 0,
            is_promoter BOOLEAN DEFAULT 0,
            FOREIGN KEY (company_id) REFERENCES company_info(company_id)
        )
    ''')
    cursor.execute(sql)
    
    # PPE Schedule table
    sql = adapt_sql('''
        CREATE TABLE IF NOT EXISTS ppe_schedule (
            ppe_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            asset_class TEXT NOT NULL,
            -- Current Year (CY) - Gross Block
            opening_gross_block_cy REAL DEFAULT 0,
            additions_cy REAL DEFAULT 0,
            disposals_gross_cy REAL DEFAULT 0,
            closing_gross_block_cy REAL DEFAULT 0,
            -- Current Year (CY) - Accumulated Depreciation
            opening_acc_depreciation_cy REAL DEFAULT 0,
            depreciation_for_year_cy REAL DEFAULT 0,
            acc_depr_on_disposals_cy REAL DEFAULT 0,
            closing_acc_depreciation_cy REAL DEFAULT 0,
            -- Previous Year (PY) - Gross Block
            opening_gross_block_py REAL DEFAULT 0,
            additions_py REAL DEFAULT 0,
            disposals_gross_py REAL DEFAULT 0,
            closing_gross_block_py REAL DEFAULT 0,
            -- Previous Year (PY) - Accumulated Depreciation
            opening_acc_depreciation_py REAL DEFAULT 0,
            depreciation_for_year_py REAL DEFAULT 0,
            acc_depr_on_disposals_py REAL DEFAULT 0,
            closing_acc_depreciation_py REAL DEFAULT 0,
            -- Metadata
            depreciation_rate REAL DEFAULT 0,
            useful_life_years INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (company_id) REFERENCES company_info(company_id)
        )
    ''')
    cursor.execute(sql)
    
    # CWIP Schedule table
    sql = adapt_sql('''
        CREATE TABLE IF NOT EXISTS cwip_schedule (
            cwip_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            project_name TEXT NOT NULL,
            opening_balance_cy REAL DEFAULT 0,
            additions_cy REAL DEFAULT 0,
            capitalized_cy REAL DEFAULT 0,
            closing_balance_cy REAL DEFAULT 0,
            opening_balance_py REAL DEFAULT 0,
            additions_py REAL DEFAULT 0,
            capitalized_py REAL DEFAULT 0,
            closing_balance_py REAL DEFAULT 0,
            project_start_date DATE,
            expected_completion_date DATE,
            FOREIGN KEY (company_id) REFERENCES company_info(company_id)
        )
    ''')
    cursor.execute(sql)
    
    # Intangible Assets table
    sql = adapt_sql('''
        CREATE TABLE IF NOT EXISTS intangible_assets (
            intangible_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            asset_class TEXT NOT NULL,
            is_under_development BOOLEAN DEFAULT 0,
            opening_gross_block REAL DEFAULT 0,
            additions REAL DEFAULT 0,
            disposals_gross REAL DEFAULT 0,
            opening_acc_amortization REAL DEFAULT 0,
            amortization_for_year REAL DEFAULT 0,
            acc_amort_on_disposals REAL DEFAULT 0,
            FOREIGN KEY (company_id) REFERENCES company_info(company_id)
        )
    ''')
    cursor.execute(sql)
    
    # Investments table - Schedule III compliant
    sql = adapt_sql('''
        CREATE TABLE IF NOT EXISTS investments (
            investment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            investment_particulars TEXT NOT NULL,
            classification TEXT NOT NULL,  -- Non-Current / Current
            investment_type TEXT,  -- Subsidiaries / Associates / JV / Equity / Preference / Debt / Mutual Funds / Others
            is_quoted BOOLEAN DEFAULT 0,
            quantity_cy INTEGER DEFAULT 0,
            quantity_py INTEGER DEFAULT 0,
            cost_cy REAL DEFAULT 0,
            cost_py REAL DEFAULT 0,
            fair_value_cy REAL DEFAULT 0,
            fair_value_py REAL DEFAULT 0,
            carrying_amount_cy REAL DEFAULT 0,
            carrying_amount_py REAL DEFAULT 0,
            market_value_cy REAL DEFAULT 0,
            market_value_py REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (company_id) REFERENCES company_info(company_id)
        )
    ''')
    cursor.execute(sql)
    
    # Inventories table - Schedule III Note 8
    sql = adapt_sql('''
        CREATE TABLE IF NOT EXISTS inventories (
            inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            category TEXT NOT NULL,  -- Raw Materials / WIP / Finished Goods / Stock-in-Trade / Stores & Spares
            particulars TEXT NOT NULL,
            quantity_cy REAL DEFAULT 0,
            quantity_py REAL DEFAULT 0,
            unit TEXT,
            value_cy REAL DEFAULT 0,
            value_py REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (company_id) REFERENCES company_info(company_id)
        )
    ''')
    cursor.execute(sql)
    
    # Employee Benefits table
    sql = adapt_sql('''
        CREATE TABLE IF NOT EXISTS employee_benefits (
            eb_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            pf_contribution_cy REAL DEFAULT 0,
            pf_contribution_py REAL DEFAULT 0,
            gratuity_current_service_cost_cy REAL DEFAULT 0,
            gratuity_current_service_cost_py REAL DEFAULT 0,
            gratuity_interest_cost_cy REAL DEFAULT 0,
            gratuity_interest_cost_py REAL DEFAULT 0,
            gratuity_actuarial_gain_loss_cy REAL DEFAULT 0,
            gratuity_actuarial_gain_loss_py REAL DEFAULT 0,
            gratuity_obligation_cy REAL DEFAULT 0,
            gratuity_obligation_py REAL DEFAULT 0,
            gratuity_plan_assets_cy REAL DEFAULT 0,
            gratuity_plan_assets_py REAL DEFAULT 0,
            FOREIGN KEY (company_id) REFERENCES company_info(company_id)
        )
    ''')
    cursor.execute(sql)
    
    # Tax Information table
    sql = adapt_sql('''
        CREATE TABLE IF NOT EXISTS tax_information (
            tax_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            current_tax_cy REAL DEFAULT 0,
            current_tax_py REAL DEFAULT 0,
            deferred_tax_cy REAL DEFAULT 0,
            deferred_tax_py REAL DEFAULT 0,
            applicable_tax_rate REAL DEFAULT 0,
            non_deductible_expenses REAL DEFAULT 0,
            other_differences REAL DEFAULT 0,
            FOREIGN KEY (company_id) REFERENCES company_info(company_id)
        )
    ''')
    cursor.execute(sql)
    
    # Related Parties table
    sql = adapt_sql('''
        CREATE TABLE IF NOT EXISTS related_parties (
            rp_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            party_name TEXT NOT NULL,
            relationship TEXT NOT NULL,
            FOREIGN KEY (company_id) REFERENCES company_info(company_id)
        )
    ''')
    cursor.execute(sql)
    
    # Related Party Transactions table
    sql = adapt_sql('''
        CREATE TABLE IF NOT EXISTS related_party_transactions (
            rpt_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            rp_id INTEGER NOT NULL,
            transaction_type TEXT NOT NULL,
            amount_cy REAL DEFAULT 0,
            amount_py REAL DEFAULT 0,
            balance_outstanding_cy REAL DEFAULT 0,
            balance_outstanding_py REAL DEFAULT 0,
            FOREIGN KEY (company_id) REFERENCES company_info(company_id),
            FOREIGN KEY (rp_id) REFERENCES related_parties(rp_id)
        )
    ''')
    cursor.execute(sql)
    
    # Contingent Liabilities table
    sql = adapt_sql('''
        CREATE TABLE IF NOT EXISTS contingent_liabilities (
            cl_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            particulars TEXT NOT NULL,
            type TEXT NOT NULL,
            amount_cy REAL DEFAULT 0,
            amount_py REAL DEFAULT 0,
            FOREIGN KEY (company_id) REFERENCES company_info(company_id)
        )
    ''')
    cursor.execute(sql)
    
    # Receivables Ledger table
    sql = adapt_sql('''
        CREATE TABLE IF NOT EXISTS receivables_ledger (
            receivable_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            customer_name TEXT NOT NULL,
            invoice_no TEXT,
            invoice_date DATE,
            invoice_amount REAL DEFAULT 0,
            amount_settled REAL DEFAULT 0,
            outstanding_amount REAL DEFAULT 0,
            is_disputed BOOLEAN DEFAULT 0,
            FOREIGN KEY (company_id) REFERENCES company_info(company_id)
        )
    ''')
    cursor.execute(sql)
    
    # Payables Ledger table
    sql = adapt_sql('''
        CREATE TABLE IF NOT EXISTS payables_ledger (
            payable_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            vendor_name TEXT NOT NULL,
            invoice_no TEXT,
            invoice_date DATE,
            invoice_amount REAL DEFAULT 0,
            amount_settled REAL DEFAULT 0,
            outstanding_amount REAL DEFAULT 0,
            is_disputed BOOLEAN DEFAULT 0,
            is_msme BOOLEAN DEFAULT 0,
            FOREIGN KEY (company_id) REFERENCES company_info(company_id)
        )
    ''')
    cursor.execute(sql)
    
    # Selection Sheet table
    sql = adapt_sql('''
        CREATE TABLE IF NOT EXISTS selection_sheet (
            selection_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            note_ref TEXT NOT NULL,
            note_description TEXT NOT NULL,
            linked_major_head TEXT,
            system_recommendation TEXT DEFAULT 'No',
            user_selection TEXT DEFAULT 'No',
            final_selection TEXT DEFAULT 'No',
            auto_number TEXT,
            FOREIGN KEY (company_id) REFERENCES company_info(company_id)
        )
    ''')
    cursor.execute(sql)
    cursor.execute(sql)
    
    conn.commit()
    conn.close()
    
    # Note: Default master data is now company-specific and should be created per company
    # Use initialize_default_master_data_for_company(company_id) after creating a company

def initialize_default_master_data():
    """Initialize default master data for Major/Minor/Grouping heads"""
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if master data already exists
    cursor.execute("SELECT COUNT(*) FROM major_heads")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return  # Already initialized
    
    # Default Major Heads (from VBA code)
    major_heads_data = [
        ("Property, Plant and Equipment", "Assets", 1),
        ("Intangible Assets", "Assets", 2),
        ("Non-current Investments", "Assets", 3),
        ("Long-term Loans and Advances", "Assets", 4),
        ("Other Non-current Assets", "Assets", 5),
        ("Current Investments", "Assets", 6),
        ("Inventories", "Assets", 7),
        ("Trade Receivables", "Assets", 8),
        ("Cash and Cash Equivalents", "Assets", 9),
        ("Short-term Loans and Advances", "Assets", 10),
        ("Other Current Assets", "Assets", 11),
        ("Equity Share Capital", "Equity", 12),
        ("Other Equity", "Equity", 13),
        ("Long-term Borrowings", "Liabilities", 14),
        ("Deferred Tax Liabilities (Net)", "Liabilities", 15),
        ("Other Long-term Liabilities", "Liabilities", 16),
        ("Long-term Provisions", "Liabilities", 17),
        ("Short-term Borrowings", "Liabilities", 18),
        ("Trade Payables", "Liabilities", 19),
        ("Other Current Liabilities", "Liabilities", 20),
        ("Short-term Provisions", "Liabilities", 21),
        ("Revenue from Operations", "Income", 22),
        ("Other Income", "Income", 23),
        ("Cost of Materials Consumed", "Expenses", 24),
        ("Purchases of Stock-in-Trade", "Expenses", 25),
        ("Changes in Inventories", "Expenses", 26),
        ("Employee Benefits Expense", "Expenses", 27),
        ("Finance Costs", "Expenses", 28),
        ("Depreciation and Amortization", "Expenses", 29),
        ("Other Expenses", "Expenses", 30),
        ("Exceptional Items", "Special", 31),
        ("Extraordinary Items", "Special", 32),
        ("Taxes on Income", "Special", 33),
        ("Prior Period Items", "Special", 34)
    ]
    
    cursor.executemany(
        "INSERT INTO major_heads (major_head_name, category, display_order) VALUES (?, ?, ?)",
        major_heads_data
    )
    
    # Default Minor Heads (sample - would need full list from VBA)
    minor_heads_data = [
        ("Tangible Assets", 1, 1),
        ("Intangible Assets", 2, 1),
        ("Financial Assets - Investments", 3, 1),
        ("Financial Assets - Loans", 4, 1),
        ("Other Non-current Assets", 5, 1),
        ("Inventories", 7, 1),
        ("Financial Assets - Trade Receivables", 8, 1),
        ("Cash and Cash Equivalents", 9, 1),
        ("Financial Assets - Loans", 10, 1),
        ("Other financial assets", 11, 1),
        ("Equity Share Capital", 12, 1),
        ("Other Equity", 13, 1),
        ("Financial Liabilities - Borrowings", 14, 1),
        ("Provisions", 17, 1),
        ("Other financial liabilities", 16, 1),
        ("Financial Liabilities - Borrowings", 18, 1),
        ("Financial Liabilities - Trade Payables", 19, 1),
        ("Other financial liabilities", 20, 1),
        ("Provisions", 21, 1),
        ("Revenue from Operations", 22, 1),
        ("Other Income", 23, 1),
        ("Cost of Materials Consumed", 24, 1),
        ("Purchases of Stock-in-Trade", 25, 1),
        ("Changes in inventories", 26, 1),
        ("Employee Benefit Expense", 27, 1),
        ("Finance Costs", 28, 1),
        ("Depreciation and Amortization Expense", 29, 1),
        ("Other Expenses", 30, 1)
    ]
    
    cursor.executemany(
        "INSERT INTO minor_heads (minor_head_name, major_head_id, display_order) VALUES (?, ?, ?)",
        minor_heads_data
    )
    
    # Default Groupings (sample - would need full list from VBA)
    groupings_data = [
        ("Land", 1, 1, 1),
        ("Building", 1, 1, 2),
        ("Plant and Machinery", 1, 1, 3),
        ("Furniture and Fixtures", 1, 1, 4),
        ("Vehicles", 1, 1, 5),
        ("Office Equipment", 1, 1, 6),
        ("Capital Work-in-Progress", 1, 1, 7),
        ("Goodwill", 2, 2, 1),
        ("Patents, Copyrights, Trademarks", 2, 2, 2),
        ("Intangible assets under development", 2, 2, 3),
        ("Raw materials", 7, 6, 1),
        ("Work-in-progress", 7, 6, 2),
        ("Finished goods", 7, 6, 3),
        ("Stock-in-trade", 7, 6, 4),
        ("Stores and spares", 7, 6, 5),
        ("Cash on hand", 9, 8, 1),
        ("Balances with banks", 9, 8, 2),
        ("Retained Earnings", 13, 12, 1),
        ("General Reserve", 13, 12, 2),
        ("Securities Premium", 13, 12, 3),
        ("Sale of products", 22, 20, 1),
        ("Sale of services", 22, 20, 2),
        ("Interest Income", 23, 21, 1),
        ("Dividend Income", 23, 21, 2),
        ("Salaries and wages", 27, 25, 1),
        ("Contribution to provident and other funds", 27, 25, 2),
        ("Staff welfare expenses", 27, 25, 3),
        ("Interest expense", 28, 26, 1),
        ("Other borrowing costs", 28, 26, 2),
        ("Depreciation on tangible assets", 29, 27, 1),
        ("Amortization on intangible assets", 29, 27, 2)
    ]
    
    cursor.executemany(
        "INSERT INTO groupings (grouping_name, minor_head_id, major_head_id, display_order) VALUES (?, ?, ?, ?)",
        groupings_data
    )
    
    conn.commit()
    conn.close()
    print("Database initialized successfully with default master data!")
