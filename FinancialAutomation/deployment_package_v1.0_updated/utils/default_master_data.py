"""Default Master Data Template for Schedule III Compliance"""

from models.master_data import MajorHead, MinorHead, Grouping

def initialize_default_master_data_for_company(company_id):
    """
    Initialize default Schedule III compliant master data for a new company.
    This creates a standard Chart of Accounts with Major Heads, Minor Heads, and Groupings.
    
    Args:
        company_id: The company ID to create master data for
        
    Returns:
        dict: Statistics about created items
    """
    
    stats = {"major_heads": 0, "minor_heads": 0, "groupings": 0}
    
    try:
        # ASSETS
        assets_id = MajorHead.create(
            company_id=company_id,
            major_head_name="Non-Current Assets",
            category="Assets",
            description="Assets held for long-term use"
        )
        stats["major_heads"] += 1
        
        # Property, Plant & Equipment
        ppe_id = MinorHead.create(
            company_id=company_id,
            major_head_id=assets_id,
            minor_head_name="Property, Plant and Equipment",
            code="PPE"
        )
        stats["minor_heads"] += 1
        
        ppe_groupings = [
            "Land - Freehold",
            "Land - Leasehold",
            "Buildings",
            "Plant and Machinery",
            "Furniture and Fixtures",
            "Vehicles",
            "Office Equipment",
            "Computers"
        ]
        for grouping_name in ppe_groupings:
            Grouping.create(company_id=company_id, minor_head_id=ppe_id, grouping_name=grouping_name)
            stats["groupings"] += 1
        
        # Capital Work-in-Progress
        cwip_id = MinorHead.create(
            company_id=company_id,
            major_head_id=assets_id,
            minor_head_name="Capital Work-in-Progress",
            code="CWIP"
        )
        stats["minor_heads"] += 1
        
        # Intangible Assets
        intangible_id = MinorHead.create(
            company_id=company_id,
            major_head_id=assets_id,
            minor_head_name="Intangible Assets",
            code="IA"
        )
        stats["minor_heads"] += 1
        
        intangible_groupings = [
            "Goodwill",
            "Brands/Trademarks",
            "Computer Software",
            "Patents",
            "Copyrights",
            "Licenses"
        ]
        for grouping_name in intangible_groupings:
            Grouping.create(company_id=company_id, minor_head_id=intangible_id, grouping_name=grouping_name)
            stats["groupings"] += 1
        
        # Financial Assets - Investments
        investments_id = MinorHead.create(
            company_id=company_id,
            major_head_id=assets_id,
            minor_head_name="Financial Assets - Investments",
            code="NCA-INV"
        )
        stats["minor_heads"] += 1
        
        investment_groupings = [
            "Investment in Subsidiaries",
            "Investment in Associates",
            "Investment in Joint Ventures",
            "Other Investments - Equity Instruments",
            "Other Investments - Debt Instruments"
        ]
        for grouping_name in investment_groupings:
            Grouping.create(company_id=company_id, minor_head_id=investments_id, grouping_name=grouping_name)
            stats["groupings"] += 1
        
        # Other Non-Current Assets
        other_nca_id = MinorHead.create(
            company_id=company_id,
            major_head_id=assets_id,
            minor_head_name="Other Non-Current Assets",
            code="ONCA"
        )
        stats["minor_heads"] += 1
        
        # CURRENT ASSETS
        current_assets_id = MajorHead.create(
            company_id=company_id,
            major_head_name="Current Assets",
            category="Assets"
        )
        stats["major_heads"] += 1
        
        # Inventories
        inventories_id = MinorHead.create(
            company_id=company_id,
            major_head_id=current_assets_id,
            minor_head_name="Inventories",
            code="INV"
        )
        stats["minor_heads"] += 1
        
        inventory_groupings = [
            "Raw Materials",
            "Work-in-Progress",
            "Finished Goods",
            "Stock-in-Trade (Traded Goods)",
            "Stores and Spares",
            "Loose Tools",
            "Packing Materials"
        ]
        for grouping_name in inventory_groupings:
            Grouping.create(company_id=company_id, minor_head_id=inventories_id, grouping_name=grouping_name)
            stats["groupings"] += 1
        
        # Trade Receivables
        trade_receivables_id = MinorHead.create(
            company_id=company_id,
            major_head_id=current_assets_id,
            minor_head_name="Trade Receivables",
            code="TR"
        )
        stats["minor_heads"] += 1
        
        tr_groupings = [
            "Unsecured - Considered Good",
            "Unsecured - Credit Impaired",
            "Unsecured - Doubtful"
        ]
        for grouping_name in tr_groupings:
            Grouping.create(company_id=company_id, minor_head_id=trade_receivables_id, grouping_name=grouping_name)
            stats["groupings"] += 1
        
        # Cash and Cash Equivalents
        cash_id = MinorHead.create(
            company_id=company_id,
            major_head_id=current_assets_id,
            minor_head_name="Cash and Cash Equivalents",
            code="CASH"
        )
        stats["minor_heads"] += 1
        
        cash_groupings = [
            "Cash on Hand",
            "Balances with Banks - Current Accounts",
            "Balances with Banks - Deposit Accounts",
            "Cheques on Hand"
        ]
        for grouping_name in cash_groupings:
            Grouping.create(company_id=company_id, minor_head_id=cash_id, grouping_name=grouping_name)
            stats["groupings"] += 1
        
        # Other Current Assets
        other_ca_id = MinorHead.create(
            company_id=company_id,
            major_head_id=current_assets_id,
            minor_head_name="Other Current Assets",
            code="OCA"
        )
        stats["minor_heads"] += 1
        
        # EQUITY
        equity_id = MajorHead.create(
            company_id=company_id,
            major_head_name="Equity",
            category="Equity"
        )
        stats["major_heads"] += 1
        
        # Share Capital
        share_capital_id = MinorHead.create(
            company_id=company_id,
            major_head_id=equity_id,
            minor_head_name="Share Capital",
            code="SC"
        )
        stats["minor_heads"] += 1
        
        sc_groupings = [
            "Equity Share Capital",
            "Preference Share Capital"
        ]
        for grouping_name in sc_groupings:
            Grouping.create(company_id=company_id, minor_head_id=share_capital_id, grouping_name=grouping_name)
            stats["groupings"] += 1
        
        # Other Equity
        other_equity_id = MinorHead.create(
            company_id=company_id,
            major_head_id=equity_id,
            minor_head_name="Other Equity",
            code="OE"
        )
        stats["minor_heads"] += 1
        
        oe_groupings = [
            "Securities Premium",
            "Retained Earnings",
            "General Reserve",
            "Capital Reserve",
            "Other Reserves"
        ]
        for grouping_name in oe_groupings:
            Grouping.create(company_id=company_id, minor_head_id=other_equity_id, grouping_name=grouping_name)
            stats["groupings"] += 1
        
        # LIABILITIES - NON-CURRENT
        ncl_id = MajorHead.create(
            company_id=company_id,
            major_head_name="Non-Current Liabilities",
            category="Liabilities"
        )
        stats["major_heads"] += 1
        
        # Long-term Borrowings
        lt_borrowings_id = MinorHead.create(
            company_id=company_id,
            major_head_id=ncl_id,
            minor_head_name="Long-term Borrowings",
            code="LTB"
        )
        stats["minor_heads"] += 1
        
        ltb_groupings = [
            "Term Loans from Banks",
            "Term Loans from Financial Institutions",
            "Debentures",
            "Bonds"
        ]
        for grouping_name in ltb_groupings:
            Grouping.create(company_id=company_id, minor_head_id=lt_borrowings_id, grouping_name=grouping_name)
            stats["groupings"] += 1
        
        # Long-term Provisions
        lt_provisions_id = MinorHead.create(
            company_id=company_id,
            major_head_id=ncl_id,
            minor_head_name="Long-term Provisions",
            code="LTP"
        )
        stats["minor_heads"] += 1
        
        ltp_groupings = [
            "Provision for Employee Benefits - Gratuity",
            "Provision for Employee Benefits - Leave Encashment"
        ]
        for grouping_name in ltp_groupings:
            Grouping.create(company_id=company_id, minor_head_id=lt_provisions_id, grouping_name=grouping_name)
            stats["groupings"] += 1
        
        # LIABILITIES - CURRENT
        cl_id = MajorHead.create(
            company_id=company_id,
            major_head_name="Current Liabilities",
            category="Liabilities"
        )
        stats["major_heads"] += 1
        
        # Short-term Borrowings
        st_borrowings_id = MinorHead.create(
            company_id=company_id,
            major_head_id=cl_id,
            minor_head_name="Short-term Borrowings",
            code="STB"
        )
        stats["minor_heads"] += 1
        
        stb_groupings = [
            "Loans from Banks - Cash Credit",
            "Loans from Banks - Working Capital Demand Loan",
            "Loans from Others"
        ]
        for grouping_name in stb_groupings:
            Grouping.create(company_id=company_id, minor_head_id=st_borrowings_id, grouping_name=grouping_name)
            stats["groupings"] += 1
        
        # Trade Payables
        trade_payables_id = MinorHead.create(
            company_id=company_id,
            major_head_id=cl_id,
            minor_head_name="Trade Payables",
            code="TP"
        )
        stats["minor_heads"] += 1
        
        tp_groupings = [
            "Due to Micro and Small Enterprises",
            "Due to Others"
        ]
        for grouping_name in tp_groupings:
            Grouping.create(company_id=company_id, minor_head_id=trade_payables_id, grouping_name=grouping_name)
            stats["groupings"] += 1
        
        # Other Current Liabilities
        ocl_id = MinorHead.create(
            company_id=company_id,
            major_head_id=cl_id,
            minor_head_name="Other Current Liabilities",
            code="OCL"
        )
        stats["minor_heads"] += 1
        
        ocl_groupings = [
            "Statutory Dues Payable",
            "Advances from Customers",
            "Other Payables"
        ]
        for grouping_name in ocl_groupings:
            Grouping.create(company_id=company_id, minor_head_id=ocl_id, grouping_name=grouping_name)
            stats["groupings"] += 1
        
        # Short-term Provisions
        st_provisions_id = MinorHead.create(
            company_id=company_id,
            major_head_id=cl_id,
            minor_head_name="Short-term Provisions",
            code="STP"
        )
        stats["minor_heads"] += 1
        
        # INCOME
        income_id = MajorHead.create(
            company_id=company_id,
            major_head_name="Revenue from Operations",
            category="Income"
        )
        stats["major_heads"] += 1
        
        # Revenue
        revenue_id = MinorHead.create(
            company_id=company_id,
            major_head_id=income_id,
            minor_head_name="Sale of Products/Services",
            code="REV"
        )
        stats["minor_heads"] += 1
        
        revenue_groupings = [
            "Sale of Products",
            "Sale of Services",
            "Other Operating Revenues"
        ]
        for grouping_name in revenue_groupings:
            Grouping.create(company_id=company_id, minor_head_id=revenue_id, grouping_name=grouping_name)
            stats["groupings"] += 1
        
        # Other Income
        other_income_id = MajorHead.create(
            company_id=company_id,
            major_head_name="Other Income",
            category="Income"
        )
        stats["major_heads"] += 1
        
        oi_minor_id = MinorHead.create(
            company_id=company_id,
            major_head_id=other_income_id,
            minor_head_name="Other Income",
            code="OI"
        )
        stats["minor_heads"] += 1
        
        oi_groupings = [
            "Interest Income",
            "Dividend Income",
            "Profit on Sale of Investments",
            "Miscellaneous Income"
        ]
        for grouping_name in oi_groupings:
            Grouping.create(company_id=company_id, minor_head_id=oi_minor_id, grouping_name=grouping_name)
            stats["groupings"] += 1
        
        # EXPENSES
        expenses_id = MajorHead.create(
            company_id=company_id,
            major_head_name="Cost of Materials Consumed",
            category="Expenses"
        )
        stats["major_heads"] += 1
        
        cmc_id = MinorHead.create(
            company_id=company_id,
            major_head_id=expenses_id,
            minor_head_name="Raw Material Consumption",
            code="CMC"
        )
        stats["minor_heads"] += 1
        
        # Employee Benefits
        emp_exp_id = MajorHead.create(
            company_id=company_id,
            major_head_name="Employee Benefits Expense",
            category="Expenses"
        )
        stats["major_heads"] += 1
        
        emp_minor_id = MinorHead.create(
            company_id=company_id,
            major_head_id=emp_exp_id,
            minor_head_name="Employee Costs",
            code="EMP"
        )
        stats["minor_heads"] += 1
        
        emp_groupings = [
            "Salaries and Wages",
            "Contribution to Provident Fund",
            "Gratuity",
            "Staff Welfare Expenses"
        ]
        for grouping_name in emp_groupings:
            Grouping.create(company_id=company_id, minor_head_id=emp_minor_id, grouping_name=grouping_name)
            stats["groupings"] += 1
        
        # Finance Costs
        finance_id = MajorHead.create(
            company_id=company_id,
            major_head_name="Finance Costs",
            category="Expenses"
        )
        stats["major_heads"] += 1
        
        fc_minor_id = MinorHead.create(
            company_id=company_id,
            major_head_id=finance_id,
            minor_head_name="Interest and Finance Charges",
            code="FC"
        )
        stats["minor_heads"] += 1
        
        fc_groupings = [
            "Interest on Term Loans",
            "Interest on Working Capital",
            "Interest on Others",
            "Bank Charges"
        ]
        for grouping_name in fc_groupings:
            Grouping.create(company_id=company_id, minor_head_id=fc_minor_id, grouping_name=grouping_name)
            stats["groupings"] += 1
        
        # Depreciation
        dep_id = MajorHead.create(
            company_id=company_id,
            major_head_name="Depreciation and Amortization",
            category="Expenses"
        )
        stats["major_heads"] += 1
        
        dep_minor_id = MinorHead.create(
            company_id=company_id,
            major_head_id=dep_id,
            minor_head_name="Depreciation",
            code="DEP"
        )
        stats["minor_heads"] += 1
        
        # Other Expenses
        other_exp_id = MajorHead.create(
            company_id=company_id,
            major_head_name="Other Expenses",
            category="Expenses"
        )
        stats["major_heads"] += 1
        
        oe_minor_id = MinorHead.create(
            company_id=company_id,
            major_head_id=other_exp_id,
            minor_head_name="Administrative and Operating Expenses",
            code="AOE"
        )
        stats["minor_heads"] += 1
        
        aoe_groupings = [
            "Rent",
            "Electricity and Water",
            "Repairs and Maintenance",
            "Insurance",
            "Printing and Stationery",
            "Telephone and Internet",
            "Legal and Professional Fees",
            "Travelling and Conveyance",
            "Advertisement and Publicity"
        ]
        for grouping_name in aoe_groupings:
            Grouping.create(company_id=company_id, minor_head_id=oe_minor_id, grouping_name=grouping_name)
            stats["groupings"] += 1
        
        return stats
    
    except Exception as e:
        raise Exception(f"Failed to initialize default master data: {str(e)}")
