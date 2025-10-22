"""Database initialization and management - PostgreSQL only"""

from .db_connection import get_connection, release_connection

def initialize_database():
    """Initialize the PostgreSQL database with all required tables"""
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Users table - MUST BE FIRST (referenced by company_info)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            full_name VARCHAR(255),
            created_at TIMESTAMP DEFAULT NOW(),
            last_login TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE
        )
    ''')
    
    # Licenses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS licenses (
            license_id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            license_key VARCHAR(255) UNIQUE NOT NULL,
            license_type VARCHAR(50) NOT NULL,
            issue_date DATE NOT NULL,
            expiry_date DATE,
            is_active BOOLEAN DEFAULT TRUE,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    # Company Info table - MUST BE BEFORE major_heads/minor_heads/groupings
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS company_info (
            company_id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            entity_name VARCHAR(500) NOT NULL,
            address TEXT,
            cin_no VARCHAR(50),
            fy_start_date DATE NOT NULL,
            fy_end_date DATE NOT NULL,
            currency VARCHAR(10) DEFAULT 'INR',
            units VARCHAR(50) DEFAULT 'Millions',
            number_format VARCHAR(50) DEFAULT 'Accounting',
            negative_format VARCHAR(50) DEFAULT 'Brackets',
            default_font VARCHAR(100) DEFAULT 'Bookman Old Style',
            default_font_size INTEGER DEFAULT 11,
            show_zeros_as_blank BOOLEAN DEFAULT FALSE,
            decimal_places INTEGER DEFAULT 2,
            turnover DECIMAL(15,2) DEFAULT 0,
            rounding_level VARCHAR(50) DEFAULT '100000',
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW(),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    # Major Heads table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS major_heads (
            major_head_id SERIAL PRIMARY KEY,
            company_id INTEGER NOT NULL,
            major_head_name VARCHAR(500) NOT NULL,
            category VARCHAR(100) NOT NULL,
            opening_balance_cy DECIMAL(15,2) DEFAULT 0,
            opening_balance_py DECIMAL(15,2) DEFAULT 0,
            display_order INTEGER,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT NOW(),
            FOREIGN KEY (company_id) REFERENCES company_info(company_id),
            UNIQUE(company_id, major_head_name)
        )
    ''')
    
    # Minor Heads table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS minor_heads (
            minor_head_id SERIAL PRIMARY KEY,
            company_id INTEGER NOT NULL,
            minor_head_name VARCHAR(500) NOT NULL,
            major_head_id INTEGER NOT NULL,
            opening_balance_cy DECIMAL(15,2) DEFAULT 0,
            opening_balance_py DECIMAL(15,2) DEFAULT 0,
            display_order INTEGER,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT NOW(),
            FOREIGN KEY (company_id) REFERENCES company_info(company_id),
            FOREIGN KEY (major_head_id) REFERENCES major_heads(major_head_id),
            UNIQUE(company_id, minor_head_name, major_head_id)
        )
    ''')
    
    # Groupings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groupings (
            grouping_id SERIAL PRIMARY KEY,
            company_id INTEGER NOT NULL,
            grouping_name VARCHAR(500) NOT NULL,
            minor_head_id INTEGER NOT NULL,
            major_head_id INTEGER NOT NULL,
            opening_balance_cy DECIMAL(15,2) DEFAULT 0,
            opening_balance_py DECIMAL(15,2) DEFAULT 0,
            display_order INTEGER,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT NOW(),
            FOREIGN KEY (company_id) REFERENCES company_info(company_id),
            FOREIGN KEY (minor_head_id) REFERENCES minor_heads(minor_head_id),
            FOREIGN KEY (major_head_id) REFERENCES major_heads(major_head_id),
            UNIQUE(company_id, grouping_name, minor_head_id, major_head_id)
        )
    ''')
    
    # Trial Balance table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trial_balance (
            tb_id SERIAL PRIMARY KEY,
            company_id INTEGER NOT NULL,
            ledger_name VARCHAR(500) NOT NULL,
            opening_balance_cy DECIMAL(15,2) DEFAULT 0,
            debit_cy DECIMAL(15,2) DEFAULT 0,
            credit_cy DECIMAL(15,2) DEFAULT 0,
            closing_balance_cy DECIMAL(15,2) DEFAULT 0,
            opening_balance_py DECIMAL(15,2) DEFAULT 0,
            debit_py DECIMAL(15,2) DEFAULT 0,
            credit_py DECIMAL(15,2) DEFAULT 0,
            closing_balance_py DECIMAL(15,2) DEFAULT 0,
            type_bs_pl VARCHAR(10) NOT NULL,
            major_head_id INTEGER,
            minor_head_id INTEGER,
            grouping_id INTEGER,
            is_mapped INTEGER DEFAULT 0,
            import_batch_id INTEGER,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW(),
            FOREIGN KEY (company_id) REFERENCES company_info(company_id),
            FOREIGN KEY (major_head_id) REFERENCES major_heads(major_head_id),
            FOREIGN KEY (minor_head_id) REFERENCES minor_heads(minor_head_id),
            FOREIGN KEY (grouping_id) REFERENCES groupings(grouping_id)
        )
    ''')
    
    # Share Capital table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS share_capital (
            share_id SERIAL PRIMARY KEY,
            company_id INTEGER NOT NULL,
            class_of_share VARCHAR(255) NOT NULL,
            authorized_shares DECIMAL(15,2) DEFAULT 0,
            face_value DECIMAL(15,2) DEFAULT 0,
            opening_shares_cy DECIMAL(15,2) DEFAULT 0,
            shares_issued_cy DECIMAL(15,2) DEFAULT 0,
            closing_shares_cy DECIMAL(15,2) DEFAULT 0,
            opening_shares_py DECIMAL(15,2) DEFAULT 0,
            shares_issued_py DECIMAL(15,2) DEFAULT 0,
            closing_shares_py DECIMAL(15,2) DEFAULT 0,
            FOREIGN KEY (company_id) REFERENCES company_info(company_id)
        )
    ''')
    
    # Shareholders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shareholders (
            shareholder_id SERIAL PRIMARY KEY,
            company_id INTEGER NOT NULL,
            shareholder_name VARCHAR(500) NOT NULL,
            shares_cy DECIMAL(15,2) DEFAULT 0,
            shares_py DECIMAL(15,2) DEFAULT 0,
            is_promoter BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (company_id) REFERENCES company_info(company_id)
        )
    ''')
    
    # PPE Schedule table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ppe_schedule (
            ppe_id SERIAL PRIMARY KEY,
            company_id INTEGER NOT NULL,
            asset_class VARCHAR(255) NOT NULL,
            opening_gross_block_cy DECIMAL(15,2) DEFAULT 0,
            additions_cy DECIMAL(15,2) DEFAULT 0,
            disposals_gross_cy DECIMAL(15,2) DEFAULT 0,
            closing_gross_block_cy DECIMAL(15,2) DEFAULT 0,
            opening_acc_depreciation_cy DECIMAL(15,2) DEFAULT 0,
            depreciation_for_year_cy DECIMAL(15,2) DEFAULT 0,
            acc_depr_on_disposals_cy DECIMAL(15,2) DEFAULT 0,
            closing_acc_depreciation_cy DECIMAL(15,2) DEFAULT 0,
            opening_gross_block_py DECIMAL(15,2) DEFAULT 0,
            additions_py DECIMAL(15,2) DEFAULT 0,
            disposals_gross_py DECIMAL(15,2) DEFAULT 0,
            closing_gross_block_py DECIMAL(15,2) DEFAULT 0,
            opening_acc_depreciation_py DECIMAL(15,2) DEFAULT 0,
            depreciation_for_year_py DECIMAL(15,2) DEFAULT 0,
            acc_depr_on_disposals_py DECIMAL(15,2) DEFAULT 0,
            closing_acc_depreciation_py DECIMAL(15,2) DEFAULT 0,
            depreciation_rate DECIMAL(5,2) DEFAULT 0,
            useful_life_years INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW(),
            FOREIGN KEY (company_id) REFERENCES company_info(company_id)
        )
    ''')
    
    # CWIP Schedule table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cwip_schedule (
            cwip_id SERIAL PRIMARY KEY,
            company_id INTEGER NOT NULL,
            project_name VARCHAR(500) NOT NULL,
            opening_balance_cy DECIMAL(15,2) DEFAULT 0,
            additions_cy DECIMAL(15,2) DEFAULT 0,
            capitalized_cy DECIMAL(15,2) DEFAULT 0,
            closing_balance_cy DECIMAL(15,2) DEFAULT 0,
            opening_balance_py DECIMAL(15,2) DEFAULT 0,
            additions_py DECIMAL(15,2) DEFAULT 0,
            capitalized_py DECIMAL(15,2) DEFAULT 0,
            closing_balance_py DECIMAL(15,2) DEFAULT 0,
            project_start_date DATE,
            expected_completion_date DATE,
            FOREIGN KEY (company_id) REFERENCES company_info(company_id)
        )
    ''')
    
    # Intangible Assets table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS intangible_assets (
            intangible_id SERIAL PRIMARY KEY,
            company_id INTEGER NOT NULL,
            asset_class VARCHAR(255) NOT NULL,
            is_under_development BOOLEAN DEFAULT FALSE,
            opening_gross_block DECIMAL(15,2) DEFAULT 0,
            additions DECIMAL(15,2) DEFAULT 0,
            disposals_gross DECIMAL(15,2) DEFAULT 0,
            opening_acc_amortization DECIMAL(15,2) DEFAULT 0,
            amortization_for_year DECIMAL(15,2) DEFAULT 0,
            acc_amort_on_disposals DECIMAL(15,2) DEFAULT 0,
            FOREIGN KEY (company_id) REFERENCES company_info(company_id)
        )
    ''')
    
    # Investments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS investments (
            investment_id SERIAL PRIMARY KEY,
            company_id INTEGER NOT NULL,
            investment_particulars TEXT NOT NULL,
            classification VARCHAR(50) NOT NULL,
            investment_type VARCHAR(100),
            is_quoted BOOLEAN DEFAULT FALSE,
            quantity_cy INTEGER DEFAULT 0,
            quantity_py INTEGER DEFAULT 0,
            cost_cy DECIMAL(15,2) DEFAULT 0,
            cost_py DECIMAL(15,2) DEFAULT 0,
            fair_value_cy DECIMAL(15,2) DEFAULT 0,
            fair_value_py DECIMAL(15,2) DEFAULT 0,
            carrying_amount_cy DECIMAL(15,2) DEFAULT 0,
            carrying_amount_py DECIMAL(15,2) DEFAULT 0,
            market_value_cy DECIMAL(15,2) DEFAULT 0,
            market_value_py DECIMAL(15,2) DEFAULT 0,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW(),
            FOREIGN KEY (company_id) REFERENCES company_info(company_id)
        )
    ''')
    
    # Inventories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventories (
            inventory_id SERIAL PRIMARY KEY,
            company_id INTEGER NOT NULL,
            category VARCHAR(100) NOT NULL,
            particulars VARCHAR(500) NOT NULL,
            quantity_cy DECIMAL(15,2) DEFAULT 0,
            quantity_py DECIMAL(15,2) DEFAULT 0,
            unit VARCHAR(50),
            value_cy DECIMAL(15,2) DEFAULT 0,
            value_py DECIMAL(15,2) DEFAULT 0,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW(),
            FOREIGN KEY (company_id) REFERENCES company_info(company_id)
        )
    ''')
    
    # Employee Benefits table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employee_benefits (
            eb_id SERIAL PRIMARY KEY,
            company_id INTEGER NOT NULL,
            pf_contribution_cy DECIMAL(15,2) DEFAULT 0,
            pf_contribution_py DECIMAL(15,2) DEFAULT 0,
            gratuity_current_service_cost_cy DECIMAL(15,2) DEFAULT 0,
            gratuity_current_service_cost_py DECIMAL(15,2) DEFAULT 0,
            gratuity_interest_cost_cy DECIMAL(15,2) DEFAULT 0,
            gratuity_interest_cost_py DECIMAL(15,2) DEFAULT 0,
            gratuity_actuarial_gain_loss_cy DECIMAL(15,2) DEFAULT 0,
            gratuity_actuarial_gain_loss_py DECIMAL(15,2) DEFAULT 0,
            gratuity_obligation_cy DECIMAL(15,2) DEFAULT 0,
            gratuity_obligation_py DECIMAL(15,2) DEFAULT 0,
            gratuity_plan_assets_cy DECIMAL(15,2) DEFAULT 0,
            gratuity_plan_assets_py DECIMAL(15,2) DEFAULT 0,
            FOREIGN KEY (company_id) REFERENCES company_info(company_id)
        )
    ''')
    
    # Tax Information table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tax_information (
            tax_id SERIAL PRIMARY KEY,
            company_id INTEGER NOT NULL,
            current_tax_cy DECIMAL(15,2) DEFAULT 0,
            current_tax_py DECIMAL(15,2) DEFAULT 0,
            deferred_tax_cy DECIMAL(15,2) DEFAULT 0,
            deferred_tax_py DECIMAL(15,2) DEFAULT 0,
            applicable_tax_rate DECIMAL(5,2) DEFAULT 0,
            non_deductible_expenses DECIMAL(15,2) DEFAULT 0,
            other_differences DECIMAL(15,2) DEFAULT 0,
            FOREIGN KEY (company_id) REFERENCES company_info(company_id)
        )
    ''')
    
    # Related Parties table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS related_parties (
            rp_id SERIAL PRIMARY KEY,
            company_id INTEGER NOT NULL,
            party_name VARCHAR(500) NOT NULL,
            relationship VARCHAR(100) NOT NULL,
            FOREIGN KEY (company_id) REFERENCES company_info(company_id)
        )
    ''')
    
    # Related Party Transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS related_party_transactions (
            rpt_id SERIAL PRIMARY KEY,
            company_id INTEGER NOT NULL,
            rp_id INTEGER NOT NULL,
            transaction_type VARCHAR(100) NOT NULL,
            amount_cy DECIMAL(15,2) DEFAULT 0,
            amount_py DECIMAL(15,2) DEFAULT 0,
            balance_outstanding_cy DECIMAL(15,2) DEFAULT 0,
            balance_outstanding_py DECIMAL(15,2) DEFAULT 0,
            FOREIGN KEY (company_id) REFERENCES company_info(company_id),
            FOREIGN KEY (rp_id) REFERENCES related_parties(rp_id)
        )
    ''')
    
    # Contingent Liabilities table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contingent_liabilities (
            cl_id SERIAL PRIMARY KEY,
            company_id INTEGER NOT NULL,
            particulars TEXT NOT NULL,
            type VARCHAR(100) NOT NULL,
            amount_cy DECIMAL(15,2) DEFAULT 0,
            amount_py DECIMAL(15,2) DEFAULT 0,
            FOREIGN KEY (company_id) REFERENCES company_info(company_id)
        )
    ''')
    
    # Receivables Ledger table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS receivables_ledger (
            receivable_id SERIAL PRIMARY KEY,
            company_id INTEGER NOT NULL,
            customer_name VARCHAR(500) NOT NULL,
            invoice_no VARCHAR(100),
            invoice_date DATE,
            invoice_amount DECIMAL(15,2) DEFAULT 0,
            amount_settled DECIMAL(15,2) DEFAULT 0,
            outstanding_amount DECIMAL(15,2) DEFAULT 0,
            is_disputed BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (company_id) REFERENCES company_info(company_id)
        )
    ''')
    
    # Payables Ledger table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payables_ledger (
            payable_id SERIAL PRIMARY KEY,
            company_id INTEGER NOT NULL,
            vendor_name VARCHAR(500) NOT NULL,
            invoice_no VARCHAR(100),
            invoice_date DATE,
            invoice_amount DECIMAL(15,2) DEFAULT 0,
            amount_settled DECIMAL(15,2) DEFAULT 0,
            outstanding_amount DECIMAL(15,2) DEFAULT 0,
            is_disputed BOOLEAN DEFAULT FALSE,
            is_msme BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (company_id) REFERENCES company_info(company_id)
        )
    ''')
    
    # Selection Sheet table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS selection_sheet (
            selection_id SERIAL PRIMARY KEY,
            company_id INTEGER NOT NULL,
            note_ref VARCHAR(50) NOT NULL,
            note_description VARCHAR(500) NOT NULL,
            linked_major_head VARCHAR(500),
            system_recommendation VARCHAR(10) DEFAULT 'No',
            user_selection VARCHAR(10) DEFAULT 'No',
            final_selection VARCHAR(10) DEFAULT 'No',
            auto_number VARCHAR(50),
            FOREIGN KEY (company_id) REFERENCES company_info(company_id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✓ PostgreSQL database initialized successfully!")


def initialize_default_master_data():
    """Initialize default master data - not used in v1.0"""
    pass
