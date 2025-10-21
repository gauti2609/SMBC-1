# 📘 Financial Automation Application - User Guide

**Version:** 1.0.0  
**Date:** October 19, 2025  
**For:** CA Firms, CFOs, and Finance Departments

---

## 📖 Table of Contents

1. [Introduction](#introduction)
2. [System Requirements](#system-requirements)
3. [Installation](#installation)
4. [Getting Started](#getting-started)
5. [Complete Workflow](#complete-workflow)
6. [Module Guide](#module-guide)
7. [Tips & Best Practices](#tips--best-practices)
8. [Troubleshooting](#troubleshooting)
9. [FAQs](#faqs)

---

## 🎯 Introduction

### What is this Application?

The Financial Automation Application is a comprehensive tool designed to automate the generation of **Schedule III compliant financial statements** for Indian companies as per the Companies Act, 2013.

### Key Features

✅ **Schedule III Compliance** - Fully compliant with Indian accounting standards  
✅ **Comparative Analysis** - Current Year vs Previous Year throughout  
✅ **Auto-Calculations** - Automatic depreciation, totals, and balance sheet balancing  
✅ **Professional Output** - Statutory-ready Balance Sheet, P&L, and Notes  
✅ **Multi-Company Support** - Manage multiple companies in one application  
✅ **Excel Integration** - Import Trial Balance, Export schedules  
✅ **Database-Backed** - Secure data storage with SQLite/PostgreSQL  

### Who Should Use This?

- 📊 **Chartered Accountants** preparing statutory financial statements
- 💼 **Chief Financial Officers** managing company financials
- 🏢 **Finance Departments** in medium to large companies
- 📈 **Auditors** reviewing financial statements

---

## 💻 System Requirements

### Minimum Requirements

- **Operating System:** Windows 10/11, macOS 10.14+, Linux (Ubuntu 18.04+)
- **RAM:** 4 GB (8 GB recommended)
- **Storage:** 500 MB free space
- **Python:** 3.8 or higher (for development)
- **Display:** 1366x768 or higher resolution

### Software Dependencies

- Python 3.8+
- PyQt5 (GUI framework)
- openpyxl (Excel integration)
- psycopg2 (PostgreSQL support - optional)

---

## 🚀 Installation

### Option 1: Using Executable (Recommended for End Users)

1. Download the latest release from the releases page
2. Extract the ZIP file to your desired location
3. Run `FinancialAutomation.exe` (Windows) or `FinancialAutomation` (macOS/Linux)
4. The application will start with a login screen

### Option 2: From Source (For Developers)

```bash
# Clone the repository
git clone <repository-url>
cd FinancialAutomation

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### First-Time Setup

1. **Create Admin User:**
   - On first launch, create an admin user account
   - Username: Choose a unique username
   - Password: Use a strong password (minimum 8 characters)
   - Email: Your email address
   - Full Name: Your full name

2. **Database Configuration:**
   - For single-user: SQLite (default, no configuration needed)
   - For multi-user: PostgreSQL (see `.env` file configuration)

---

## 🎬 Getting Started

### Step 1: Login

1. Launch the application
2. Enter your username and password
3. Click "Login"

### Step 2: Create/Select Company

1. Click "Company Info" tab
2. Click "Add New Company" button
3. Fill in company details:
   - Company Name
   - Registration Number
   - PAN Number
   - Address
   - Financial Year dates (Start and End)
4. Click "Save"
5. Select the company from the dropdown to work on it

### Step 3: Set Up Master Data (One-Time)

1. Go to "Master Data" tab
2. Define your account code structure:
   - Major Heads (Assets, Liabilities, Income, Expenses)
   - Minor Heads (sub-categories)
   - Groupings for reporting
3. Save the configuration

---

## 📋 Complete Workflow

### Typical Month-End/Year-End Workflow

```
1. Import Trial Balance
   ↓
2. Map Accounts to Schedule III
   ↓
3. Enter PPE Details
   ↓
4. Enter CWIP Projects
   ↓
5. Enter Investments
   ↓
6. Enter Inventories (if needed)
   ↓
7. Generate Financial Statements
   ↓
8. Review & Export
```

### Detailed Steps

#### 1️⃣ Import Trial Balance

**Purpose:** Load your trial balance data from Tally or Excel

**Steps:**
1. Go to "Trial Balance" tab
2. Click "Import from Excel/CSV"
3. Select your file (ensure format matches template)
4. Review imported data
5. Click "Save"

**File Format:**
```
Account Code | Account Name | Debit CY | Credit CY | Debit PY | Credit PY
1001        | Cash on Hand  | 500000   | 0         | 400000   | 0
```

#### 2️⃣ Map Accounts to Schedule III

**Purpose:** Tell the system how to categorize accounts

**Steps:**
1. Go to "Selection Sheet" tab
2. For each Trial Balance account:
   - Select the Schedule III category (Assets/Liabilities/Income/Expenses)
   - Choose the specific line item (e.g., "Trade Receivables", "Revenue from Operations")
3. Click "Save Mapping"

**Example Mappings:**
- Account "Trade Debtors" → Current Assets → Trade Receivables
- Account "Sales Revenue" → Income → Revenue from Operations
- Account "Salaries Expense" → Expenses → Employee Benefit Expense

#### 3️⃣ Enter PPE Details (Property, Plant & Equipment)

**Purpose:** Create detailed depreciation schedule for fixed assets

**Steps:**
1. Go to "Input Forms" tab
2. Select "PPE (Notes 1, 7)" sub-tab
3. Click "Add Asset" button
4. Fill in asset details:

**For Each Asset:**
- **Asset Class:** Building, Plant & Machinery, Computers, etc.
- **Gross Block (Opening):** CY and PY
- **Additions during the year:** CY and PY
- **Disposals during the year:** CY and PY
- **Accumulated Depreciation (Opening):** CY and PY
- **Depreciation for the year:** CY and PY
- **Depreciation Rate:** e.g., 5%, 15%, 40%
- **Useful Life:** in years

5. Click "Save"
6. Repeat for all asset classes
7. Click "Save All" when complete

**Auto-Calculations:**
- Closing Gross Block = Opening + Additions - Disposals
- Closing Acc. Depreciation = Opening + For the Year - On Disposals
- Net Block = Gross Block - Accumulated Depreciation

**Export:** Click "Export to Excel" to save PPE schedule

#### 4️⃣ Enter CWIP Projects (Capital Work-in-Progress)

**Purpose:** Track ongoing capital projects

**Steps:**
1. Go to "Input Forms" → "CWIP (Note 2)" sub-tab
2. Click "Add Project"
3. Fill in project details:
   - **Project Name:** e.g., "New Factory Building"
   - **Opening Balance:** CY and PY
   - **Additions during year:** CY and PY
   - **Capitalized (transferred to PPE):** CY and PY
   - **Start Date:** When project began
   - **Expected Completion:** Target date
4. Click "Save"

**Auto-Calculations:**
- Closing Balance = Opening + Additions - Capitalized

**Tip:** When a CWIP project completes, capitalize it and add to PPE

#### 5️⃣ Enter Investments

**Purpose:** Track investments in subsidiaries, associates, equity, debt, etc.

**Steps:**
1. Go to "Input Forms" → "Investments (Notes 3, 4, 13, 14)" sub-tab
2. You'll see two tabs: **Non-Current** and **Current**

**For Non-Current Investments:**
1. Select "Non-Current Investments" tab
2. Click "Add Investment"
3. Fill in details:
   - **Particulars:** e.g., "ABC Subsidiary Ltd (100% holding)"
   - **Investment Type:** Subsidiaries, Associates, Joint Ventures, Government Securities, etc.
   - **Quoted/Unquoted:** Check if quoted on stock exchange
   - **Quantity:** CY and PY
   - **Cost:** CY and PY
   - **Fair Value:** CY and PY
   - **Carrying Amount:** CY and PY (book value)
   - **Market Value:** CY and PY (if quoted)
4. Click "OK"

**For Current Investments:**
1. Select "Current Investments" tab
2. Same process as Non-Current
3. Typically includes: Mutual Funds, Listed Equity, Short-term Bonds

**Investment Types Available:**
- Subsidiaries (>50% holding)
- Associates (20-50% holding)
- Joint Ventures
- Government Securities
- Debentures or Bonds
- Equity Instruments (shares)
- Preference Shares
- Mutual Funds
- Other Investments

**Auto-Calculations:**
- Summary totals for Non-Current and Current
- Total investments value

#### 6️⃣ Enter Inventories (Optional - if using detailed inventory tracking)

**Purpose:** Track inventory by category

**Steps:**
1. Create inventory records directly in database or via custom form
2. Categories available:
   - Raw Materials
   - Work-in-Progress
   - Finished Goods
   - Stock-in-Trade
   - Stores and Spares
   - Loose Tools

**Alternative:** Use Trial Balance for inventory totals

#### 7️⃣ Generate Financial Statements

**Purpose:** Create Schedule III compliant Balance Sheet, P&L, and Notes

**Steps:**
1. Go to "Financial Statements" tab
2. Ensure company is selected
3. Click "Generate/Refresh" button
4. View generated statements in three tabs:

**Tab 1: Balance Sheet**
- Complete Schedule III format
- I. ASSETS (Non-Current + Current)
- II. EQUITY AND LIABILITIES
- Note references (Note 1, 2, 3, etc.)
- CY vs PY comparative columns
- Auto-balanced

**Tab 2: Profit & Loss**
- Revenue from Operations
- Other Income
- Total Income
- Expenses (Employee Benefits, Finance Costs, Depreciation, Other)
- Profit before Tax
- Tax Expense (@ 25%)
- Profit after Tax

**Tab 3: Notes to Accounts**
- Note 1: Property, Plant and Equipment (detailed schedule)
- Note 2: Capital Work-in-Progress
- Note 3: Non-Current Investments
- Note 8: Inventories
- Note 9: Current Investments
- And more...

#### 8️⃣ Review & Export

**Review Checklist:**
- ✅ Balance Sheet balances (Assets = Liabilities + Equity)
- ✅ All note references correct
- ✅ Depreciation from PPE matches P&L depreciation expense
- ✅ Investment totals match between Balance Sheet and Notes
- ✅ CY vs PY figures are consistent
- ✅ All amounts are in correct format (₹)

**Export Options:**
- Click "Export to Excel" (coming soon for consolidated report)
- Individual forms (PPE, CWIP, Investments) can be exported from their tabs
- Print or Save as PDF (coming soon)

---

## 📚 Module Guide

### Company Info Tab

**Purpose:** Manage company master data

**Features:**
- Add/Edit/Delete companies
- Company Name, Registration Number, PAN
- Financial Year dates
- Address details

**Best Practice:** Create separate company for each legal entity

---

### Master Data Tab

**Purpose:** Define account code structure

**Features:**
- Major Heads (Assets, Liabilities, Revenue, Expenses)
- Minor Heads (sub-categories)
- Groupings for reporting
- Current Year vs Previous Year setup

**Best Practice:** Define once, reuse across financial years

---

### Trial Balance Tab

**Purpose:** Import and manage trial balance

**Features:**
- Import from Excel/CSV
- Manual entry/edit
- Debit/Credit for CY and PY
- Account code mapping
- Category assignment

**Best Practice:** Import from Tally/accounting system, then review

---

### Selection Sheet Tab

**Purpose:** Map Trial Balance to Schedule III

**Features:**
- Account-wise mapping
- Category selection
- Schedule III line item assignment
- Save mapping configuration

**Best Practice:** Map once, adjust as needed for new accounts

---

### Input Forms Tab

**Sub-Tab 1: PPE (Notes 1, 7)**
- Detailed depreciation schedule
- 23-column table
- Auto-calculate closing balances
- Export to Excel

**Sub-Tab 2: CWIP (Note 2)**
- Project-wise tracking
- Opening + Additions - Capitalized = Closing
- Date tracking
- Export to Excel

**Sub-Tab 3: Investments (Notes 3, 4, 13, 14)**
- Tabbed interface: Non-Current | Current
- 15-column table
- Investment type dropdown
- Quoted/Unquoted checkbox
- Summary totals
- Export to Excel

---

### Financial Statements Tab

**Sub-Tab 1: Balance Sheet**
- Schedule III format
- CY vs PY columns
- Note references
- Color-coded sections
- Auto-balanced

**Sub-Tab 2: P&L Statement**
- Schedule III format
- Revenue and expense categorization
- Auto-depreciation from PPE
- Tax calculation
- Profit margin

**Sub-Tab 3: Notes to Accounts**
- Auto-generated from input forms
- Detailed schedules
- Linked to Balance Sheet/P&L

---

## 💡 Tips & Best Practices

### Data Entry Tips

1. **Work Systematically**
   - Complete Trial Balance first
   - Then PPE, CWIP, Investments
   - Finally generate statements

2. **Use Consistent Naming**
   - Asset classes: Use standard names (Building, Plant and Machinery)
   - Investment names: Include holding % (e.g., "ABC Ltd - 75%")
   - Account codes: Follow your organization's coding system

3. **Verify as You Go**
   - Check auto-calculated totals after each entry
   - Verify closing balances match your records
   - Cross-check with previous year's audited financials

4. **Save Frequently**
   - Click "Save" or "Save All" regularly
   - Don't rely on auto-save
   - Make backups of database file

### Accuracy Tips

1. **Depreciation**
   - Ensure depreciation rates match company policy
   - Verify opening accumulated depreciation
   - Check that depreciation for the year is calculated correctly
   - Depreciation should auto-appear in P&L - verify it matches

2. **Investments**
   - Classify correctly (Non-Current vs Current)
   - Update fair values from market prices (if quoted)
   - Carrying amount should reflect book value as per accounting policy

3. **Trial Balance Mapping**
   - Review all "Unmapped" accounts
   - Ensure revenue accounts don't end up in expenses
   - Check that all Balance Sheet accounts are mapped

### Performance Tips

1. **For Large Datasets**
   - Use PostgreSQL instead of SQLite
   - Filter data by company/year
   - Export to Excel for complex analysis

2. **Regular Maintenance**
   - Archive old companies/years
   - Clean up test data
   - Backup database monthly

---

## 🔧 Troubleshooting

### Common Issues

#### Issue: "Balance Sheet doesn't balance"

**Cause:** Missing data in Trial Balance or input forms

**Solution:**
1. Check Total Debit = Total Credit in Trial Balance
2. Verify all assets/liabilities are mapped
3. Ensure equity section includes retained earnings
4. Review current year profit/loss is included in equity

---

#### Issue: "Depreciation not showing in P&L"

**Cause:** PPE data not entered or incorrect

**Solution:**
1. Go to PPE input form
2. Verify "Depreciation for the Year (CY)" is filled
3. Click "Save All"
4. Regenerate financial statements

---

#### Issue: "Investments total doesn't match"

**Cause:** Data not saved or formula issue

**Solution:**
1. Check both Non-Current and Current tabs in Investments form
2. Verify all rows are saved (check for unsaved red cells)
3. Click "Save All from Both Tabs"
4. Regenerate financial statements

---

#### Issue: "Import Excel failed"

**Cause:** File format doesn't match expected structure

**Solution:**
1. Download the Excel template from the application
2. Ensure columns are in correct order
3. Check for special characters in account names
4. Verify numeric fields contain only numbers

---

#### Issue: "Application crashes on startup"

**Cause:** Database corruption or missing dependencies

**Solution:**
1. Check `financial_automation.db` file exists
2. Try renaming DB file (creates fresh database)
3. Reinstall dependencies: `pip install -r requirements.txt`
4. Check error logs in application folder

---

## ❓ FAQs

### General Questions

**Q: Is this application suitable for all company sizes?**

A: Yes! It's designed for small to large companies. Small companies can use basic features, while large companies can leverage multi-company and PostgreSQL support.

**Q: Does it support standalone financial statements?**

A: Yes, you can generate standalone financial statements for any single company.

**Q: Can I generate consolidated financial statements?**

A: Not in v1.0, but this feature is planned for future releases.

**Q: Is the application compliant with Companies Act, 2013?**

A: Yes, the output follows Schedule III format as per Companies Act, 2013.

---

### Technical Questions

**Q: Can I use this on multiple computers?**

A: 
- SQLite (default): Copy database file to each computer
- PostgreSQL: Multiple users can access same database simultaneously

**Q: How do I backup my data?**

A: 
- SQLite: Copy `financial_automation.db` file
- PostgreSQL: Use `pg_dump` utility

**Q: Can I customize the output format?**

A: The Schedule III format is standardized. Custom reports can be added in future versions.

**Q: Does it support IFRS or IndAS?**

A: Currently supports Schedule III format (applicable to IndAS). IFRS support can be added.

---

### Data Questions

**Q: How far back can I track previous years?**

A: The application supports Current Year (CY) and Previous Year (PY). For more years, create separate company records or extend the database schema.

**Q: Can I import data from Tally?**

A: Yes! Export Trial Balance from Tally to Excel, then import into the application.

**Q: What if I make a mistake in entered data?**

A: You can edit any entry by clicking on it, modifying values, and clicking Save.

**Q: How do I delete incorrect entries?**

A: Select the row and click "Delete Selected" button. Confirm the deletion.

---

### Financial Questions

**Q: How is depreciation calculated?**

A: 
- SLM (Straight Line Method): (Cost - Salvage) / Useful Life
- WDV (Written Down Value): Opening WDV × Depreciation Rate

The application shows depreciation for the year as entered/calculated.

**Q: Can I change financial year dates?**

A: Yes, but it's recommended to create a new company for each financial year to maintain historical data.

**Q: How is tax calculated in P&L?**

A: Currently at fixed 25% of Profit before Tax. Can be customized for different tax rates.

---

## 📞 Support & Contact

### Getting Help

1. **Documentation:** Refer to this User Guide
2. **FAQs:** Check the FAQs section above
3. **Issue Tracker:** Report bugs on GitHub
4. **Email Support:** [Contact the development team]

### Feature Requests

Have ideas for new features? 
- Submit on GitHub Issues
- Email the team with "Feature Request" in subject
- Join the community forum

---

## 📜 Legal & Compliance

### Disclaimer

This application is provided as-is for generating financial statements. Users are responsible for:
- Accuracy of input data
- Compliance with accounting standards
- Verification by qualified professionals
- Final approval by auditors/statutory authorities

### Audit Note

While this application generates Schedule III compliant statements, **all financial statements should be reviewed and certified by a qualified Chartered Accountant** before submission to statutory authorities.

---

## 🔄 Version History

**v1.0.0** (October 19, 2025)
- Initial release
- PPE, CWIP, Investments modules
- Balance Sheet, P&L, Notes generation
- Schedule III compliance
- Excel import/export
- Multi-company support

---

## 🎓 Learning Resources

### Recommended Reading

1. **Schedule III, Companies Act 2013** - Understanding the format
2. **AS/Ind AS Standards** - Accounting standards reference
3. **Fixed Assets Management** - Depreciation calculation methods
4. **Investment Accounting** - Classification and valuation

### Video Tutorials (Coming Soon)

- Getting Started Tutorial
- Trial Balance Import
- PPE Schedule Creation
- Investment Management
- Generating Financial Statements

---

## ✨ Quick Reference Card

### Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Save | Ctrl+S |
| New Entry | Ctrl+N |
| Delete | Delete |
| Refresh | F5 |
| Export | Ctrl+E |

### Common Tasks Quick Guide

| Task | Location | Time |
|------|----------|------|
| Add New Company | Company Info → Add New | 2 min |
| Import Trial Balance | Trial Balance → Import | 5 min |
| Add PPE Asset | Input Forms → PPE → Add Asset | 3 min |
| Add Investment | Input Forms → Investments → Add | 2 min |
| Generate Statements | Financial Statements → Generate | Instant |
| Export to Excel | Any Form → Export to Excel | 1 min |

---

**🎉 You're now ready to use the Financial Automation Application!**

**Happy Financial Reporting!** 📊✨
