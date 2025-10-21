# Financial Automation v1.0 - User Training Guide

**Training Duration**: 4-6 hours  
**Target Audience**: Accountants, Finance Teams, CFOs  
**Prerequisites**: Basic accounting knowledge, Excel proficiency  
**Format**: Self-paced with hands-on exercises

---

## 📚 **TABLE OF CONTENTS**

1. [Introduction](#module-1-introduction)
2. [Installation & Setup](#module-2-installation--setup)
3. [Company Configuration](#module-3-company-configuration)
4. [Trial Balance Import](#module-4-trial-balance-import)
5. [Selection Sheet](#module-5-selection-sheet)
6. [Input Forms & Data Entry](#module-6-input-forms--data-entry)
7. [Financial Statements](#module-7-financial-statements)
8. [Excel Export](#module-8-excel-export)
9. [Advanced Features](#module-9-advanced-features)
10. [Best Practices & Tips](#module-10-best-practices--tips)

---

## MODULE 1: INTRODUCTION (30 minutes)

### 1.1 What is Financial Automation?

Financial Automation is a desktop application designed to automate the preparation of Schedule III compliant financial statements for Indian companies under the Companies Act, 2013.

**Key Benefits:**
- ⏱️ **95% Time Savings**: What took days now takes minutes
- ✅ **100% Compliance**: Built-in Schedule III format
- 🔗 **Formula Linking**: Dynamic Excel workbooks
- 🎯 **Accuracy**: Eliminates manual errors
- 📊 **Professional Output**: Audit-ready statements

### 1.2 Application Overview

**Main Components:**
1. **Company Info** - Manage company details
2. **Trial Balance** - Import and map accounts
3. **Master Data** - Chart of accounts (Major/Minor heads)
4. **Selection Sheet** - Choose applicable notes
5. **Input Forms** - Enter detailed data (PPE, CWIP, etc.)
6. **Financial Statements** - Generate BS, P&L, CF
7. **Reports** - Export and review

### 1.3 Workflow Summary

```
Trial Balance Import
        ↓
Account Mapping
        ↓
Selection Sheet Configuration
        ↓
Additional Data Entry
        ↓
Generate Financial Statements
        ↓
Export to Excel
```

### 1.4 Learning Objectives

By the end of this training, you will be able to:
- ✅ Install and configure the application
- ✅ Import and map Trial Balance data
- ✅ Configure the Selection Sheet
- ✅ Generate complete financial statements
- ✅ Export professional Excel workbooks
- ✅ Troubleshoot common issues

### 📝 Exercise 1.1: Self-Assessment

**Before starting, rate your knowledge (1-5):**
- [ ] Schedule III requirements: ___/5
- [ ] Trial Balance preparation: ___/5
- [ ] Financial statement format: ___/5
- [ ] Excel proficiency: ___/5
- [ ] Computer software installation: ___/5

---

## MODULE 2: INSTALLATION & SETUP (45 minutes)

### 2.1 System Requirements

**Check your system:**
- ✅ Operating System: Windows 10/11, macOS, or Linux
- ✅ RAM: 4 GB minimum (8 GB recommended)
- ✅ Disk Space: 500 MB free
- ✅ Display: 1366x768 minimum (1920x1080 recommended)
- ✅ Internet: For initial download (not required for operation)

### 2.2 Installation Steps

**Method 1: Executable (Recommended)**

1. Extract the deployment ZIP file
2. Navigate to `Application` folder
3. Run `FinancialAutomation.exe` (Windows) or equivalent
4. Wait for first-time database initialization

**Method 2: Python Source (Advanced Users)**

```bash
# Install Python 3.10+
# Extract deployment package
cd Application

# Install dependencies
pip install -r requirements.txt

# Run setup demo
python demo_db_setup_simple.py

# Launch application
python main.py
```

### 2.3 First Launch

**What happens:**
1. Database (`financial_automation.db`) is created automatically
2. All 23 tables are initialized
3. Default admin user is created
4. Master data (chart of accounts) is populated
5. Login window appears

**Default Credentials:**
- Username: `admin`
- Password: `admin123`

⚠️ **IMPORTANT**: Change password immediately after first login!

### 2.4 Verifying Installation

**Check these indicators:**
- ✅ Login window displays correctly
- ✅ Can login with default credentials
- ✅ Main dashboard loads without errors
- ✅ All tabs are visible (Company Info, Trial Balance, etc.)
- ✅ Database file exists in application directory

### 📝 Exercise 2.1: Installation Practice

**Complete these tasks:**
1. [ ] Install the application on your system
2. [ ] Perform first login with default credentials
3. [ ] Navigate to each main tab
4. [ ] Change admin password (Settings → User Management)
5. [ ] Verify database file location
6. [ ] Take a screenshot of the main dashboard

**Troubleshooting Checklist:**
- [ ] Application won't start → Check Python version
- [ ] Login fails → Verify credentials (case-sensitive)
- [ ] Tabs not loading → Check error log
- [ ] Slow performance → Check system resources

---

## MODULE 3: COMPANY CONFIGURATION (30 minutes)

### 3.1 Understanding Company Info

Each company in the system has:
- **Basic Details**: Name, CIN, address
- **Financial Year**: Start and end dates
- **Presentation Settings**: Currency, units, logo
- **Master Data**: Automatically initialized chart of accounts

### 3.2 Creating Your First Company

**Step-by-Step:**

1. **Navigate to Company Info Tab**
   - Click "Company Info" in left sidebar
   - You'll see an empty list (or existing companies)

2. **Click "Add New Company"**
   - A form appears with multiple fields

3. **Fill Required Fields**
   ```
   Entity Name:           ABC Manufacturing Ltd
   CIN:                   L12345KA2020PLC123456
   Registered Address:    Plot 123, Industrial Area
                         Bangalore - 560001, Karnataka
   FY Start Date:         2024-04-01
   FY End Date:           2025-03-31
   Currency:              INR
   Unit of Measurement:   Lakhs
   Company Logo:          [Optional - Upload image]
   ```

4. **Click "Save"**
   - System creates company record
   - Initializes 12 major heads
   - Initializes 24 minor heads
   - Creates 68 Selection Sheet notes
   - Shows success message

5. **Verify Creation**
   - Company appears in company list
   - Company ID is assigned
   - Master data populated (check Master Data tab)

### 3.3 Field Explanations

| Field | Purpose | Format | Example |
|-------|---------|--------|---------|
| Entity Name | Legal company name | Text | ABC Manufacturing Ltd |
| CIN | Corporate Identity Number | L12345XX2020PLCNNNNNN | L12345KA2020PLC123456 |
| Registered Address | Legal address | Multi-line text | As shown above |
| FY Start | Financial year start | YYYY-MM-DD | 2024-04-01 |
| FY End | Financial year end | YYYY-MM-DD | 2025-03-31 |
| Currency | Reporting currency | 3-letter code | INR, USD, EUR |
| Units | Amount denomination | Dropdown | Lakhs, Crores, Thousands |
| Logo | Company logo | Image file | .png, .jpg (optional) |

### 3.4 Multi-Company Management

**Switching Between Companies:**
1. Use the dropdown at top of window
2. Select desired company
3. All tabs update to show that company's data

**Use Cases:**
- Accounting firms managing multiple clients
- Group companies (parent + subsidiaries)
- Comparative analysis across entities

### 📝 Exercise 3.1: Create Practice Company

**Create a company with these details:**
```
Entity Name:           Tech Solutions Pvt Ltd
CIN:                   L72900KA2019PTC987654
Address:               456 Tech Park, Electronic City
                      Bangalore - 560100
FY Start:              2024-04-01
FY End:                2025-03-31
Currency:              INR
Units:                 Lakhs
```

**Verification Steps:**
1. [ ] Company saved successfully
2. [ ] Appears in company list
3. [ ] Can select from dropdown
4. [ ] Master Data tab shows 12 major heads
5. [ ] Selection Sheet tab shows 68 notes

**Common Mistakes to Avoid:**
- ❌ Invalid CIN format
- ❌ FY end before FY start
- ❌ Special characters in company name
- ❌ Missing required fields

---

## MODULE 4: TRIAL BALANCE IMPORT (60 minutes)

### 4.1 Preparing Your Trial Balance File

**Supported Formats:**
- ✅ Excel (.xlsx, .xls)
- ✅ CSV (.csv)

**Required Columns:**
1. **Ledger** (Account Name) - Text
2. **Opening Balance CY** - Number
3. **Debit CY** - Number
4. **Credit CY** - Number
5. **Closing Balance CY** - Number
6. **Closing Balance PY** - Number (optional)

**Excel File Structure:**
```
Row 1: Headers
Row 2+: Data

Column A: Ledger
Column B: Opening Balance CY
Column C: Debit CY
Column D: Credit CY
Column E: Closing Balance CY
Column F: Closing Balance PY
```

**Sample Data:**
```
Ledger              | Opening | Debit    | Credit   | Closing  | PY Closing
--------------------|---------|----------|----------|----------|-----------
Cash in Hand        | 50.00   | 1000.00  | 800.00   | 250.00   | 50.00
Bank - HDFC         | 1000.00 | 5000.00  | 4500.00  | 1500.00  | 1000.00
Accounts Receivable | 2000.00 | 3000.00  | 2500.00  | 2500.00  | 2000.00
Computer - Laptop   | 100.00  | 20.00    | 5.00     | 115.00   | 100.00
```

**Best Practices:**
- ✅ Remove any formulas (convert to values)
- ✅ Remove subtotals and totals rows
- ✅ Use consistent naming for accounts
- ✅ Ensure debits equal credits
- ✅ Check for negative signs (use proper columns)
- ✅ Remove any merged cells

### 4.2 Importing Trial Balance

**Step-by-Step Process:**

**Step 1: Navigate to Trial Balance Tab**
- Click "Trial Balance" in sidebar
- You'll see an empty table (or existing entries)

**Step 2: Click "Import TB"**
- File browser opens
- Navigate to your Excel/CSV file
- Select file
- Click "Open"

**Step 3: Review Import Preview**
- Application shows first 5 rows
- Verify columns are detected correctly
- Check data types
- Click "Confirm Import"

**Step 4: Wait for Import**
- Progress bar appears
- Each row is validated and imported
- Duration depends on file size
  - 100 rows: ~2 seconds
  - 500 rows: ~10 seconds
  - 1000+ rows: ~20 seconds

**Step 5: Review Import Summary**
```
✅ Import Complete!

Total Rows:        271
Successfully Imported: 271
Skipped (Blank):      0
Errors:               0

Opening Balance: 1,234,567.89
Debit Total:     5,678,901.23
Credit Total:    5,678,901.23
Closing Balance: 1,234,567.89

Balance Check: ✅ Balanced (difference: 0.00)
```

### 4.3 Understanding Auto-Mapping

**What is Auto-Mapping?**
The application automatically assigns accounts to major heads based on keywords in the ledger name.

**Mapping Rules:**
```
Keywords in Ledger Name → Major Head

computer, laptop, mobile → Property, Plant & Equipment
receivable, debtor, outstanding → Trade Receivables
cash, bank → Cash and Cash Equivalents
payable, creditor, vendor → Trade Payables
loan, borrowing → Borrowings
capital, equity, reserve → Equity
salary, wages, rent, expense → Expense accounts
sales, revenue, income → Revenue accounts
```

**Auto-Mapping Success Rate:**
- Typical: 85-95%
- Well-structured TB: 95-100%
- Poorly named accounts: 60-80%

### 4.4 Manual Mapping

**For Unmapped Accounts:**

1. **Identify Unmapped Entries**
   - Highlighted in yellow/orange
   - "Major Head" column shows "Unmapped"
   - Filter by: Status = "Unmapped"

2. **Map Individual Account**
   - Click on the row
   - Find "Major Head" dropdown
   - Select appropriate major head from list
   - Click "Save" or press Enter

3. **Bulk Mapping (Similar Accounts)**
   - Select multiple rows (Ctrl+Click)
   - Right-click → "Bulk Map"
   - Choose major head
   - Click "Apply to Selected"

4. **Verify Mapping**
   - Check mapping status summary
   - Review each major head total
   - Ensure all accounts are classified

**Example Mapping Decisions:**
```
Account Name              → Recommended Major Head
Security Deposit - Rent   → Other Non-Current Assets
Advance to Suppliers      → Other Current Assets
TDS Receivable           → Other Current Assets
GST Input Credit         → Other Current Assets
Provision for Gratuity   → Non-Current Liabilities
Outstanding Expenses     → Other Current Liabilities
```

### 4.5 Validation & Corrections

**Check These:**
1. ✅ Debit = Credit (Trial Balance property)
2. ✅ All accounts mapped
3. ✅ No duplicate ledger names
4. ✅ Balances look reasonable
5. ✅ PY data imported correctly

**Common Issues & Fixes:**

| Issue | Symptom | Solution |
|-------|---------|----------|
| Unbalanced TB | Debit ≠ Credit | Check Excel formulas, find difference |
| Import fails | Error message | Check file format, remove special chars |
| Duplicate names | Warning dialog | Rename duplicates in Excel, re-import |
| Wrong amounts | Values don't match | Check decimal places, unit conversion |
| Missing PY data | PY column empty | Add PY column to Excel, re-import |

### 📝 Exercise 4.1: Import Sample TB

**Use the provided Sample TB.xlsx file:**

1. [ ] Navigate to Trial Balance tab
2. [ ] Click "Import TB"
3. [ ] Select "Sample TB.xlsx" from SampleData folder
4. [ ] Review import preview
5. [ ] Complete import
6. [ ] Verify summary:
   - Total entries: 271
   - Balance check: Passed
   - Auto-mapped: ~90%
7. [ ] Map any unmapped accounts
8. [ ] Take screenshot of completed import

**Challenge:** Map these unmapped accounts correctly:
- Security Deposit → Other Non-Current Assets
- Advance to Suppliers → Other Current Assets
- Outstanding Expenses → Other Current Liabilities

### 📝 Exercise 4.2: Prepare Your Own TB

**Convert your company's Trial Balance:**

1. [ ] Export TB from your accounting software
2. [ ] Open in Excel
3. [ ] Format as per required structure:
   - Column A: Ledger names
   - Column B: Opening Balance CY
   - Column C: Debit CY
   - Column D: Credit CY
   - Column E: Closing Balance CY
   - Column F: Closing Balance PY
4. [ ] Remove formulas (copy → paste values)
5. [ ] Remove subtotals/totals
6. [ ] Verify debit = credit
7. [ ] Save as .xlsx file
8. [ ] Import into application
9. [ ] Complete mapping

---

## MODULE 5: SELECTION SHEET (45 minutes)

### 5.1 Understanding the Selection Sheet

**What is it?**
The Selection Sheet determines which Schedule III notes will be included in your financial statements.

**Why is it needed?**
Not all companies need all 27 notes. For example:
- Service company doesn't need "Inventories" note
- Company without borrowings doesn't need "Borrowings" note
- Company without related party transactions doesn't need that note

**How it works:**
1. System analyzes your Trial Balance
2. Recommends relevant notes based on data
3. You review and override as needed
4. Selected notes get sequential numbers (1, 2, 3...)
5. These numbers appear in final statements

### 5.2 Selection Sheet Categories

**68 Notes Across 7 Categories:**

**Category A: Accounting Policies (Mandatory)**
- A.1 - Corporate information
- A.2 - Significant accounting policies
- A.2.1 to A.2.14 - Policy details

**Category B: Balance Sheet Notes (27 notes)**
- B.1 to B.27 - All Schedule III notes

**Category C-G: Additional Notes**
- C.1 to C.4 - Contingent liabilities
- D.1 to D.3 - Related parties
- E.1 to E.5 - Employee benefits
- F.1 to F.3 - Segment reporting
- G.1 to G.4 - Other disclosures

### 5.3 System Recommendations

**How Recommendations Work:**

After Trial Balance import, click "Update Note Recommendations" button:

```
Analyzing Trial Balance...
✓ Found PPE accounts → Recommend Note B.1
✓ Found Receivables → Recommend Note B.10
✓ Found Cash/Bank → Recommend Note B.13
✓ Found Payables → Recommend Note B.24
✓ Found Borrowings → Recommend Note B.20
✓ Found Equity accounts → Recommend Notes B.3-B.4
```

**Recommendation Logic:**
- Account balance > 0 → Note recommended
- Specific keywords → Related note recommended
- Zero balance → Note not recommended (but can override)

### 5.4 Using the Selection Sheet Interface

**Table Columns:**

1. **Note Ref** - Schedule III reference (A.1, B.1, etc.)
2. **Description** - Full note description
3. **Linked Major Head** - Related account category
4. **System Recommendation** - Yes/No (green if Yes)
5. **User Selection** - Your override (dropdown: Yes/No/Blank)
6. **Final Selection** - Computed result
7. **Auto Number** - Sequential number for selected notes

**Workflow:**

**Step 1: Generate Recommendations**
```
Trial Balance tab → Click "Update Note Recommendations"
→ Auto-switches to Selection Sheet tab
→ Dialog: "28 notes recommended"
```

**Step 2: Review Recommendations**
- Green rows = Recommended by system
- White rows = Not recommended
- Scroll through all 68 notes

**Step 3: Override as Needed**
- Click dropdown in "User Selection" column
- Choose "Yes" to force include
- Choose "No" to force exclude
- Choose "Blank" to use system recommendation

**Step 4: Update Auto-Numbering**
```
Click "Update Auto-Numbering" button
→ Selected notes get numbers: 1, 2, 3, 4...
→ Numbers appear in "Auto Number" column
```

**Step 5: Verify Selection**
- Count: Should be 15-30 notes typically
- Check all mandatory notes included
- Review numbering sequence

### 5.5 Common Selection Scenarios

**Manufacturing Company:**
- ✅ B.1 - PPE (Yes - have machinery)
- ✅ B.8 - CWIP (Yes - have construction)
- ✅ B.9 - Inventories (Yes - raw materials, WIP, FG)
- ✅ B.10 - Trade Receivables (Yes)
- ✅ B.13 - Cash (Yes)
- ✅ B.20 - Borrowings (Yes - term loans)
- ✅ B.24 - Trade Payables (Yes)
- ❌ B.5 - Investments (No - none)
- ❌ C.2 - Biological Assets (No - not applicable)

**Service Company:**
- ✅ B.1 - PPE (Yes - computers, furniture)
- ✅ B.10 - Trade Receivables (Yes)
- ✅ B.13 - Cash (Yes)
- ✅ B.24 - Trade Payables (Yes - vendors)
- ❌ B.8 - CWIP (No)
- ❌ B.9 - Inventories (No - service business)
- ❌ B.20 - Borrowings (Maybe - if have loans)

**Trading Company:**
- ✅ B.1 - PPE (Limited - office equipment)
- ✅ B.9 - Inventories (Yes - stock in trade)
- ✅ B.10 - Trade Receivables (Yes)
- ✅ B.13 - Cash (Yes)
- ✅ B.20 - Borrowings (Yes - working capital loans)
- ✅ B.24 - Trade Payables (Yes)
- ❌ B.8 - CWIP (No)
- ❌ B.5 - Investments (Rarely)

### 📝 Exercise 5.1: Configure Selection Sheet

**Using your imported Trial Balance:**

1. [ ] Navigate to Trial Balance tab
2. [ ] Click "Update Note Recommendations"
3. [ ] Review recommendations dialog (count)
4. [ ] Switched to Selection Sheet automatically
5. [ ] Review each recommended note (green rows)
6. [ ] Override at least 2 recommendations:
   - Force include one not recommended
   - Force exclude one recommended
7. [ ] Click "Update Auto-Numbering"
8. [ ] Verify numbering is sequential
9. [ ] Count final selections: _____ notes
10. [ ] Take screenshot

**Reflection Questions:**
- How many notes were recommended? _____
- How many did you override? _____
- Why did you make those overrides? _____
- Are all mandatory notes included? _____

### 📝 Exercise 5.2: Selection Sheet Challenge

**Scenario:** You're preparing statements for:
- ABC Manufacturing Ltd
- Has factory building and machinery
- Manufactures widgets
- Sells to distributors on credit
- Has bank overdraft facility
- No investments or subsidiaries

**Task:** Which notes would you select?

Mark ✅ or ❌ for each:
- [ ] B.1 - PPE
- [ ] B.2 - Intangible Assets
- [ ] B.5 - Investments
- [ ] B.8 - CWIP
- [ ] B.9 - Inventories
- [ ] B.10 - Trade Receivables
- [ ] B.13 - Cash
- [ ] B.20 - Borrowings
- [ ] B.24 - Trade Payables

**Answer Key:** (Review after completing)

---

## MODULE 6: INPUT FORMS & DATA ENTRY (60 minutes)

### 6.1 Understanding Input Forms

**Why Needed?**
Some Schedule III notes require detailed breakdowns beyond Trial Balance data:
- PPE: Gross block, additions, disposals, depreciation
- CWIP: Project-wise details
- Investments: Classification, fair value
- Inventories: Category-wise breakdown
- Borrowings: Terms, security, maturity

**Available Forms:**
1. PPE Schedule
2. CWIP (Capital Work in Progress)
3. Investments
4. Inventories
5. [Additional forms as needed]

### 6.2 PPE (Property, Plant & Equipment) Schedule

**Schedule Format Required:**
```
Description | Gross Block |            | Accumulated Depreciation |            | Net Block |
           | Opening |Additions|Disposals| Opening |Current Year| Closing |Opening|Closing
-----------+---------+---------+---------+---------+------------+---------+-------+-------
Land       | 1000.00 |    0.00 |    0.00 |    0.00 |       0.00 |    0.00 |1000.00|1000.00
Buildings  |  500.00 |   50.00 |    0.00 |  100.00 |      25.00 |  125.00 | 400.00| 425.00
Plant      |  800.00 |  100.00 |   50.00 |  300.00 |      80.00 |  330.00 | 500.00| 520.00
Computers  |  150.00 |   30.00 |   20.00 |   90.00 |      32.00 |  102.00 |  60.00|  58.00
Vehicles   |  300.00 |    0.00 |   30.00 |  150.00 |      54.00 |  174.00 | 150.00|  96.00
```

**Step-by-Step Entry:**

1. **Navigate to Input Forms Tab**
   - Click "Input Forms" in sidebar
   - Select "PPE Schedule" from dropdown

2. **Add New Asset Class**
   - Click "Add New"
   - Fill in form:
   ```
   Asset Description:  Buildings
   
   Gross Block (Opening):      500.00
   Additions during year:       50.00
   Disposals during year:        0.00
   
   Depreciation (Opening):     100.00
   Depreciation for year:       25.00
   Depreciation Rate (%):        5.00
   
   Useful Life (years):         60
   ```

3. **System Auto-Calculates**
   - Gross Block Closing = Opening + Additions - Disposals
   - Accumulated Depreciation Closing = Opening + Current Year
   - Net Block Opening = Gross Block Opening - Depreciation Opening
   - Net Block Closing = Gross Block Closing - Depreciation Closing

4. **Repeat for Each Asset Class**
   - Land
   - Buildings
   - Plant & Machinery
   - Furniture & Fixtures
   - Vehicles
   - Office Equipment
   - Computers

5. **Save & Verify**
   - Click "Save All"
   - View summary totals
   - Check against Trial Balance

**Validation Checks:**
- ✅ Net Block Closing matches TB PPE balance
- ✅ Depreciation for year matches P&L expense
- ✅ All calculations correct
- ✅ No negative values (except disposals)

### 6.3 CWIP (Capital Work-in-Progress)

**When Needed:**
- Construction projects ongoing
- Machinery under installation
- Software under development

**Data Required:**
- Project name
- Opening balance
- Additions during year
- Capitalized to PPE
- Closing balance

**Entry Process:**

1. Click "CWIP" in Input Forms
2. Add New Project:
   ```
   Project Name:         Factory Expansion
   Opening Balance:      250.00
   Additions:            100.00
   Capitalization:        50.00
   Closing Balance:      300.00  [Auto-calculated]
   
   Expected Completion:  2025-12-31
   % Complete:           60%
   ```

3. Save each project
4. Total closing balance should match TB CWIP account

### 6.4 Investments Schedule

**Classification Required:**
1. **Current vs Non-Current**
2. **Type:**
   - Equity instruments
   - Debt instruments (bonds, debentures)
   - Mutual funds
   - Government securities
3. **Valuation:**
   - Cost
   - Fair value
   - Amortized cost

**Entry Form:**
```
Investment Name:       ABC Ltd Equity Shares
Classification:        Non-Current
Type:                  Equity Instrument
Quantity:              10,000 shares
Cost per unit:         150.00
Total Cost:            1,500.00  [Auto]
Fair Value per unit:   180.00
Total Fair Value:      1,800.00  [Auto]
Valuation Method:      Fair Value through P&L

Opening Balance:       1,500.00
Purchases:             0.00
Sales:                 0.00
Fair Value Change:     300.00
Closing Balance:       1,800.00
```

### 6.5 Other Input Forms

**Inventories:**
- Raw Materials: ___
- Work-in-Progress: ___
- Finished Goods: ___
- Stock-in-Trade: ___
- Stores & Spares: ___

**Borrowings:**
- Term Loans
- Working Capital Loans
- Debentures
- Interest rates, maturity dates, security details

**Trade Receivables (Detailed Ageing):**
- [Deferred to v1.1]
- Currently uses estimated percentages

### 📝 Exercise 6.1: PPE Entry

**Enter this PPE data:**

| Asset | Gross Opening | Additions | Disposals | Dep Opening | Dep Rate |
|-------|---------------|-----------|-----------|-------------|----------|
| Land | 500.00 | 0.00 | 0.00 | 0.00 | 0% |
| Buildings | 300.00 | 50.00 | 0.00 | 60.00 | 10% |
| Plant | 200.00 | 30.00 | 10.00 | 80.00 | 40% |
| Computers | 50.00 | 20.00 | 5.00 | 30.00 | 40% |

**Verify these calculated values:**
1. Buildings Net Block Closing: _____
2. Plant Depreciation for Year: _____
3. Computers Closing Gross Block: _____
4. Total Net Block (all assets): _____

### 📝 Exercise 6.2: Complete Input Forms

**For your company, complete:**
1. [ ] PPE Schedule (at least 3 asset classes)
2. [ ] CWIP (if applicable)
3. [ ] Investments (if any)
4. [ ] Inventories breakdown
5. [ ] Verify totals match Trial Balance
6. [ ] Take screenshot of each completed form

---

## MODULE 7: FINANCIAL STATEMENTS (45 minutes)

### 7.1 Generating Statements

**Pre-Generation Checklist:**
- ✅ Trial Balance imported and mapped
- ✅ Selection Sheet configured
- ✅ Input forms completed
- ✅ Company info verified
- ✅ Data validated

**Generation Process:**

1. **Navigate to Financial Statements Tab**
   - Click "Financial Statements" in sidebar

2. **Click "Generate Statements"**
   - Processing dialog appears
   - Status updates:
     ```
     Generating Balance Sheet...
     Generating Profit & Loss...
     Generating Cash Flow Statement...
     Generating Notes 1-27...
     Applying formatting...
     ```

3. **Wait for Completion** (5-15 seconds)
   - Depends on data volume
   - Progress bar indicates status

4. **View Results**
   - Statements display in tab
   - Use sub-tabs to switch between:
     - Balance Sheet
     - Profit & Loss
     - Cash Flow
     - Individual Notes

### 7.2 Balance Sheet

**Structure:**
```
[Company Name]
Balance Sheet as at [FY End Date]
(All amounts in [Units] unless otherwise stated)

                                    Note No.  Current Year  Previous Year
ASSETS
I. Non-Current Assets
   (a) Property, Plant & Equipment      1      12,345.67     11,234.56
   (b) Capital Work-in-Progress         2         234.56        345.67
   (c) Intangible Assets                3         123.45        134.56
   (d) Financial Assets
       (i) Investments                  4       1,234.56      1,111.11
       (ii) Trade Receivables           5         111.11        100.00
       (iii) Loans                      6         222.22        200.00
       (iv) Other Financial Assets      7         333.33        300.00
   (e) Deferred Tax Assets (Net)        8         444.44        400.00
   (f) Other Non-Current Assets         9         555.55        500.00

II. Current Assets
   (a) Inventories                     10       2,345.67      2,222.22
   (b) Financial Assets
       (i) Investments                 11       1,111.11      1,000.00
       (ii) Trade Receivables          12       3,456.78      3,000.00
       (iii) Cash & Cash Equivalents   13       1,234.56      1,111.11
       (iv) Bank Balances              14         234.56        200.00
       (v) Loans                       15         345.67        300.00
       (vi) Other Financial Assets     16         456.78        400.00
   (c) Current Tax Assets              17         111.11        100.00
   (d) Other Current Assets            18         222.22        200.00

TOTAL ASSETS                                   24,222.29     22,320.02

EQUITY AND LIABILITIES
I. Equity
   (a) Equity Share Capital            19       5,000.00      5,000.00
   (b) Other Equity                    20      10,111.11      9,222.22

II. Non-Current Liabilities
   (a) Financial Liabilities
       (i) Borrowings                  21       3,456.78      3,111.11
       (ii) Other Financial Liab.      22         234.56        200.00
   (b) Provisions                      23         345.67        311.11
   (c) Deferred Tax Liabilities        24         222.22        200.00

III. Current Liabilities
   (a) Financial Liabilities
       (i) Borrowings                  25       1,234.56      1,111.11
       (ii) Trade Payables             26       2,345.67      2,222.22
       (iii) Other Financial Liab.     27         567.89        511.11
   (b) Other Current Liabilities       28         345.67        311.11
   (c) Provisions                      29         222.22        200.00
   (d) Current Tax Liabilities         30         111.11        100.00

TOTAL EQUITY AND LIABILITIES                   24,222.29     22,320.02
```

**Review Checklist:**
- ✅ Total Assets = Total Equity & Liabilities
- ✅ All note numbers populated
- ✅ No negative values (except specific items)
- ✅ CY and PY columns both filled
- ✅ Headers and formatting correct

### 7.3 Profit & Loss Statement

**Structure:**
```
[Company Name]
Statement of Profit and Loss for the year ended [FY End Date]

                                           Note No.  Current Year  Previous Year

I. Revenue from Operations                    31      50,000.00     45,000.00
II. Other Income                              32       1,000.00        900.00

III. Total Income (I + II)                            51,000.00     45,900.00

IV. Expenses
   Cost of Materials Consumed                 33      20,000.00     18,000.00
   Purchases of Stock-in-Trade                34       5,000.00      4,500.00
   Changes in Inventories                     35        (500.00)      (400.00)
   Employee Benefit Expense                   36      10,000.00      9,000.00
   Finance Costs                              37       1,500.00      1,400.00
   Depreciation & Amortization                38       2,000.00      1,800.00
   Other Expenses                             39       8,000.00      7,200.00

   Total Expenses (IV)                               46,000.00     41,500.00

V. Profit Before Tax (III - IV)                       5,000.00      4,400.00

VI. Tax Expense
   Current Tax                                        1,400.00      1,232.00
   Deferred Tax                                        (200.00)      (168.00)
   Tax Adjustment - Earlier Years                        50.00         44.00

   Total Tax Expense                                  1,250.00      1,108.00

VII. Profit After Tax (V - VI)                        3,750.00      3,292.00

VIII. Other Comprehensive Income                            -             -

IX. Total Comprehensive Income (VII + VIII)           3,750.00      3,292.00

X. Earnings Per Equity Share
   Basic                                                   0.75          0.66
   Diluted                                                 0.75          0.66
```

**Validation:**
- ✅ Revenue matches TB income accounts
- ✅ Expenses match TB expense accounts
- ✅ Depreciation matches PPE schedule
- ✅ Tax expense reasonable (25-30% of PBT)
- ✅ PAT flows to Balance Sheet (retained earnings)

### 7.4 Cash Flow Statement

**Format (Indirect Method):**
```
[Company Name]
Cash Flow Statement for the year ended [FY End Date]

A. Cash Flow from Operating Activities
   Profit Before Tax                                   5,000.00
   
   Adjustments for:
   Depreciation & Amortization                         2,000.00
   Interest Expense                                    1,500.00
   Interest Income                                      (200.00)
   (Profit)/Loss on Sale of Assets                       50.00
   
   Operating Profit before Working Capital Changes     8,350.00
   
   Changes in Working Capital:
   (Increase)/Decrease in Trade Receivables             (456.78)
   (Increase)/Decrease in Inventories                   (123.45)
   (Increase)/Decrease in Other Assets                  (111.11)
   Increase/(Decrease) in Trade Payables                 123.45
   Increase/(Decrease) in Other Liabilities               89.12
   
   Cash Generated from Operations                      7,871.23
   
   Less: Income Taxes Paid                            (1,400.00)
   
   Net Cash from Operating Activities (A)              6,471.23

B. Cash Flow from Investing Activities
   Purchase of PPE                                      (500.00)
   Sale of PPE                                            50.00
   Purchase of Investments                              (200.00)
   Sale of Investments                                   100.00
   Interest Received                                     200.00
   
   Net Cash used in Investing Activities (B)            (350.00)

C. Cash Flow from Financing Activities
   Proceeds from Borrowings                             500.00
   Repayment of Borrowings                             (400.00)
   Interest Paid                                      (1,500.00)
   Dividends Paid                                     (1,000.00)
   
   Net Cash used in Financing Activities (C)          (2,400.00)

D. Net Increase/(Decrease) in Cash (A+B+C)            3,721.23

E. Cash & Cash Equivalents - Opening                  1,111.11

F. Cash & Cash Equivalents - Closing (D+E)            4,832.34
```

**Reconciliation:**
- ✅ Closing cash matches Balance Sheet
- ✅ PAT + Depreciation is positive (generally)
- ✅ Working capital changes reflect BS movements
- ✅ Investing activities match PPE/Investment changes
- ✅ Financing activities match Borrowings/Equity changes

### 7.5 Notes to Accounts

**Each Note Contains:**
1. **Header**: Note number, title
2. **Table**: CY and PY amounts
3. **Sub-breakdowns**: As required
4. **Footnotes**: Additional disclosures

**Example - Note 1: Property, Plant & Equipment**
```
Note 1 - Property, Plant & Equipment

Particulars        | Gross Block |            | Accum. Depreciation |           | Net Block |
                  | Opening |Additions|Closing| Opening |Current|Closing|Opening|Closing|
------------------+---------+---------+-------+---------+-------+-------+-------+-------|
Land              | 1000.00 |    0.00 |1000.00|    0.00 |  0.00 |  0.00 |1000.00|1000.00|
Buildings         |  500.00 |   50.00 | 550.00|  100.00 | 25.00 | 125.00| 400.00| 425.00|
Plant & Machinery |  800.00 |  100.00 | 900.00|  300.00 | 80.00 | 380.00| 500.00| 520.00|
Furniture         |  100.00 |   10.00 | 110.00|   50.00 | 10.00 |  60.00|  50.00|  50.00|
Vehicles          |  300.00 |    0.00 | 300.00|  150.00 | 54.00 | 204.00| 150.00|  96.00|
Computers         |  150.00 |   30.00 | 180.00|   90.00 | 32.00 | 122.00|  60.00|  58.00|
------------------+---------+---------+-------+---------+-------+-------+-------+-------|
Total             | 2850.00 |  190.00 |3040.00|  690.00 |201.00 | 891.00|2160.00|2149.00|

Previous Year     | 2700.00 |  150.00 |2850.00|  490.00 |200.00 | 690.00|2210.00|2160.00|
```

**Review All Notes:**
- Go through notes 1-27 (or selected notes)
- Verify calculations
- Check formatting
- Ensure completeness

### 📝 Exercise 7.1: Generate & Review

**Complete these steps:**

1. [ ] Generate financial statements
2. [ ] Review Balance Sheet:
   - Total Assets = Total Equity & Liabilities? _____
   - All notes populated? _____
3. [ ] Review Profit & Loss:
   - Total Income: _____
   - Total Expenses: _____
   - Profit After Tax: _____
4. [ ] Review Cash Flow:
   - Operating Activities: _____
   - Investing Activities: _____
   - Financing Activities: _____
   - Net Cash Increase: _____
5. [ ] Review at least 5 notes:
   - Note 1 (PPE): Complete? _____
   - Note 10 (Receivables): Complete? _____
   - Note 13 (Cash): Complete? _____
   - Note 20 (Borrowings): Complete? _____
   - Note 24 (Payables): Complete? _____
6. [ ] Take screenshots of each statement

**Quality Checks:**
- [ ] No #REF errors
- [ ] No blank cells where data expected
- [ ] Formatting consistent
- [ ] Headers correct
- [ ] Company name and dates accurate

---

## MODULE 8: EXCEL EXPORT (45 minutes)

### 8.1 Understanding Excel Export

**What You Get:**
- 30-sheet Excel workbook
- Balance Sheet, P&L, Cash Flow + 27 Notes
- Formula linking between sheets
- Schedule III compliant formatting
- Professional styling
- Ready for printing/distribution

**File Size:** ~26 KB (lightweight!)

### 8.2 Export Process

**Step-by-Step:**

1. **Ensure Statements Generated**
   - Must generate before exporting
   - Check all statements display correctly

2. **Click "Export to Excel"**
   - Button in Financial Statements tab
   - File save dialog appears

3. **Choose Location & Name**
   ```
   Suggested naming:
   [CompanyName]_Financials_[FYEnd].xlsx
   
   Example:
   ABC_Manufacturing_Financials_FY2024-25.xlsx
   Tech_Solutions_Financials_2025-03-31.xlsx
   ```

4. **Click "Save"**
   - Export progress dialog
   - Creating 30 sheets...
   - Applying formulas...
   - Formatting...

5. **Success Message**
   ```
   ✅ Export Complete!
   
   File: ABC_Manufacturing_Financials_FY2024-25.xlsx
   Location: C:\Documents\Financials\
   Size: 26.8 KB
   Sheets: 30
   
   Click "Open File" to view
   ```

### 8.3 Excel File Structure

**Sheet Tabs (30 total):**
```
1. Balance Sheet
2. Profit & Loss
3. Cash Flow
4-30. Note_1 through Note_27
```

**Navigation:**
- Click sheet tabs to switch
- Use hyperlinks in Balance Sheet (if implemented)
- Ctrl+Page Down/Up to move between sheets

### 8.4 Formula Linking

**How It Works:**

In Balance Sheet, cell C7 (PPE amount) contains:
```excel
='Note_1'!C10
```

This means:
- Value comes from Note_1 sheet
- Cell C10 (PPE total)
- Changes in Note_1 auto-update Balance Sheet

**Benefits:**
- ✅ Single source of truth
- ✅ No manual copy-paste
- ✅ Instant updates
- ✅ Audit trail
- ✅ What-if analysis enabled

**Example Scenario:**
```
User opens Excel file
Goes to Note_1 (PPE)
Changes "Computers - Additions" from 30.00 to 40.00
Gross Block increases by 10.00
Net Block increases by 10.00 (assuming no depreciation change)
Returns to Balance Sheet
PPE line item automatically shows new total
Total Assets automatically recalculates
```

**Verify Formula Linking:**
1. Open exported file
2. Go to Balance Sheet
3. Click on any amount with note reference
4. Check formula bar (shows ='Note_X'!CellRef)
5. Go to that note sheet
6. Verify the referenced cell
7. Change value in note
8. Return to Balance Sheet
9. Confirm Balance Sheet updated

### 8.5 Schedule III Formatting

**Professional Formatting Applied:**

**Headers:**
- Company name (bold, size 14)
- Statement title (bold, size 12)
- Date (size 10)
- Units disclosure (size 9, italic)

**Tables:**
- Column headers (bold, bottom border)
- Data rows (right-aligned numbers)
- Subtotals (bold, top border)
- Grand totals (bold, double top border)

**Colors:**
- Headers: Light blue background
- Subtotals: Light gray background
- Notes section: Light yellow background
- Negative values: Red font

**Column Widths:**
- Description: 40-50 characters
- Note No.: 10 characters
- Current Year: 15 characters
- Previous Year: 15 characters

**Number Formatting:**
- Amounts: #,##0.00 (with comma separator)
- Percentages: 0.00%
- No currency symbols in body (stated in header)

### 8.6 Using the Excel File

**Common Tasks:**

**1. Print Financial Statements**
```
Select Balance Sheet
File → Print
Settings:
  - Orientation: Portrait
  - Scaling: Fit to 1 page wide
  - Margins: Normal
Print
Repeat for P&L and Cash Flow
```

**2. Email to Auditors**
```
- Single file (all 30 sheets)
- No need to attach individual notes
- Auditors can navigate easily
- Formula traceability intact
```

**3. Modify for What-If Analysis**
```
Example: Increase depreciation rate
1. Go to Note_1 (PPE)
2. Change depreciation rate from 40% to 45%
3. Depreciation amount auto-recalculates
4. Balance Sheet Net Block updates
5. P&L Depreciation Expense updates
6. Cash Flow Operating Activities updates
7. See impact on Profit After Tax
```

**4. Create PDF for Board Meeting**
```
Select all sheets (Shift+Click last sheet)
File → Export → Create PDF
Check "Entire Workbook"
Save as: ABC_Manufacturing_Board_Pack_Mar2025.pdf
```

### 8.7 Troubleshooting Excel Export

**Issue: Export Fails**
- Check disk space (need ~1 MB)
- Close any file with same name
- Check write permissions in target folder
- Retry export

**Issue: Formulas Show #REF**
- Sheet names may have changed
- Re-export from application
- Don't manually rename sheets

**Issue: Formatting Lost**
- Don't save in .xls format (use .xlsx)
- Check Excel version (2010+)
- Re-export if necessary

**Issue: Values Don't Match Application**
- Ensure you generated latest statements
- Check if you edited Excel after export
- Re-export to get fresh copy

### 📝 Exercise 8.1: Export & Explore

**Complete these tasks:**

1. [ ] Export your financial statements
2. [ ] Open the Excel file
3. [ ] Count sheets: _____ (should be 30)
4. [ ] Check file size: _____ KB
5. [ ] Go to Balance Sheet
6. [ ] Click on cell with PPE amount
7. [ ] Note the formula: __________
8. [ ] Go to the referenced Note sheet
9. [ ] Verify the cell value matches
10. [ ] Change a value in the note
11. [ ] Return to Balance Sheet
12. [ ] Confirm auto-update occurred
13. [ ] Undo changes (Ctrl+Z)
14. [ ] Take screenshots of:
    - Balance Sheet
    - One complete note
    - Formula bar showing formula link

### 📝 Exercise 8.2: Advanced Excel Tasks

**Try these:**

1. **Print Preview**
   - Set up Balance Sheet for printing
   - Adjust page breaks if needed
   - Save printer settings

2. **Create PDF**
   - Export Balance Sheet to PDF
   - Export P&L to PDF
   - Combine into single PDF (if tools available)

3. **What-If Analysis**
   - Scenario: Increase sales by 10%
   - Go to Note 31 (Revenue)
   - Increase revenue by 10%
   - Observe impact on:
     - P&L Total Income
     - P&L Profit Before Tax
     - P&L Profit After Tax
     - Balance Sheet Retained Earnings
   - Document changes:
     - Original PAT: _____
     - New PAT: _____
     - Difference: _____

4. **Share with Team**
   - Email Excel file to colleague
   - Verify they can open and view
   - Check formulas work on their system

---

## MODULE 9: ADVANCED FEATURES (45 minutes)

### 9.1 Multi-Company Management

**Switching Companies:**
1. Use dropdown at top of window
2. Select company from list
3. All tabs refresh with that company's data

**Copying Data Between Companies:**
- Export from Company A
- Import to Company B (if similar structure)
- Useful for group companies

**Best Practices:**
- Use consistent naming conventions
- Keep separate financial years
- Don't mix data between companies

### 9.2 User Management

**Adding Users:**
1. Settings → User Management
2. Click "Add User"
3. Enter: Username, Password, Full Name, Email
4. Set permissions (Admin/User)
5. Save

**User Roles:**
- **Admin**: Full access, can add users, delete data
- **User**: Can view and edit, cannot delete

**Security:**
- Change default admin password
- Use strong passwords
- Don't share credentials

### 9.3 Database Backup & Restore

**Manual Backup:**
```
1. Close application
2. Locate database file:
   - Windows: C:\Users\[You]\AppData\Local\FinancialAutomation\
   - Or: Application directory
   - File: financial_automation.db
3. Copy file to backup location
4. Rename with date: financial_automation_2025-03-31_backup.db
```

**Restore Backup:**
```
1. Close application
2. Replace current .db file with backup
3. Restart application
4. Verify data integrity
```

**Automated Backup (Recommended):**
- Set up daily backup script
- Use cloud storage (Dropbox, OneDrive)
- Keep multiple versions (7-day rotation)

### 9.4 Importing from Accounting Software

**Supported Sources:**
- Tally (Export to Excel, then import)
- Quickbooks (Export to CSV)
- SAP (Export Trial Balance)
- Any software that exports to Excel/CSV

**Export Settings from Source:**
```
Tally Example:
Gateway → Display → Trial Balance
Press Alt+E (Excel)
Save as: TB_Export.xlsx

Ensure columns are:
- Ledger Name
- Opening Balance
- Debit
- Credit
- Closing Balance
```

### 9.5 Customization Options

**Company Logo:**
- Upload in Company Info
- Appears on exported statements
- Recommended: 200x100 px, PNG format

**Number Formatting:**
- Change units (Lakhs/Crores)
- Decimal places
- Currency symbol

**Report Templates:**
- Modify CSS for printing
- Adjust column widths
- Change color schemes

### 9.6 Troubleshooting Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| Slow performance | Application laggy | Close other apps, restart application |
| Database locked | Can't save changes | Close application, reopen |
| Import hangs | Excel import stuck | Check for merged cells, formulas in Excel |
| Export fails | Error on export | Check disk space, close Excel files |
| Login issues | Can't login | Verify username/password (case-sensitive) |
| Missing data | Data not showing | Check company selection dropdown |

### 📝 Exercise 9.1: Advanced Tasks

**Complete at least 3:**

1. [ ] Create a second company
2. [ ] Switch between companies
3. [ ] Add a new user account
4. [ ] Create database backup
5. [ ] Upload company logo
6. [ ] Change unit of measurement
7. [ ] Export statements for both companies

---

## MODULE 10: BEST PRACTICES & TIPS (30 minutes)

### 10.1 Data Preparation Best Practices

**Before Importing Trial Balance:**
1. ✅ Reconcile all accounts
2. ✅ Ensure debits = credits
3. ✅ Remove formulas (convert to values)
4. ✅ Check for special characters
5. ✅ Use consistent naming
6. ✅ Include prior year data
7. ✅ Remove blank rows
8. ✅ Keep header row only

**During Account Mapping:**
1. ✅ Map high-value accounts first
2. ✅ Use bulk mapping for similar accounts
3. ✅ Verify each major head total
4. ✅ Document mapping decisions
5. ✅ Review unmapped items carefully

**Input Forms:**
1. ✅ Complete all applicable schedules
2. ✅ Cross-check with Trial Balance
3. ✅ Verify calculations
4. ✅ Save frequently
5. ✅ Review totals

### 10.2 Quality Assurance Checklist

**Before Finalizing Statements:**

**Data Validation:**
- [ ] Trial Balance balanced
- [ ] All accounts mapped
- [ ] Selection Sheet configured
- [ ] PPE schedule complete
- [ ] All input forms filled
- [ ] Company info accurate

**Statement Review:**
- [ ] Balance Sheet totals match
- [ ] All note numbers populated
- [ ] No #REF or #ERROR values
- [ ] Prior year data present
- [ ] Headers correct (company name, dates)
- [ ] Formatting consistent

**Cash Flow Validation:**
- [ ] Closing cash matches Balance Sheet
- [ ] Operating activities positive (typically)
- [ ] Working capital changes explained
- [ ] PAT + Depreciation = approximate operating cash

**Notes Verification:**
- [ ] PPE schedule calculations correct
- [ ] Trade Receivables ageing shown
- [ ] Trade Payables MSME compliance
- [ ] All selected notes have data
- [ ] No selected notes are blank

### 10.3 Workflow Efficiency Tips

**Time-Saving Techniques:**

1. **Template Your Trial Balance**
   - Create standard Excel template
   - Use for every period
   - Reduces import errors

2. **Document Your Mappings**
   - First time: 30-60 minutes
   - Save mapping reference
   - Next time: 5-10 minutes (reuse)

3. **Batch Data Entry**
   - Complete all PPE at once
   - Do all investments together
   - More efficient than switching

4. **Keyboard Shortcuts**
   - Tab: Next field
   - Shift+Tab: Previous field
   - Ctrl+S: Save
   - Ctrl+Enter: Save and next

5. **Use Demos for Training**
   - Practice with Sample TB.xlsx
   - Train team on test company
   - Don't practice on live data

### 10.4 Common Mistakes to Avoid

**❌ DON'T:**
1. Import TB without checking balance
2. Skip account mapping
3. Ignore unmapped accounts
4. Leave input forms incomplete
5. Generate statements without review
6. Edit Excel after export (breaks formulas)
7. Delete database file accidentally
8. Share admin password
9. Work without backups
10. Rush through data entry

**✅ DO:**
1. Follow workflow sequence
2. Validate at each step
3. Save frequently
4. Back up regularly
5. Review before finalizing
6. Document processes
7. Train team properly
8. Test on sample data first
9. Keep prior periods for reference
10. Seek help when needed

### 10.5 Continuous Improvement

**After Each Period:**
1. Review what worked well
2. Identify bottlenecks
3. Update templates
4. Refine mappings
5. Train on new features

**Feedback Loop:**
- Document issues encountered
- Note resolution steps
- Share with team
- Suggest improvements
- Track time savings

### 10.6 Getting Help

**Resources:**
1. **USER_GUIDE.md** - Comprehensive reference
2. **FAQ Section** - Common questions
3. **Video Tutorials** - Visual walkthroughs
4. **Demo Scripts** - Hands-on practice
5. **Support Email** - support@yourcompany.com

**When Contacting Support:**
- Describe issue clearly
- Include screenshots
- Note error messages
- Specify software version
- Mention steps to reproduce

### 📝 Exercise 10.1: Create Your Checklist

**Customize this workflow checklist for your company:**

**Weekly/Monthly Close:**
- [ ] _____________________
- [ ] _____________________
- [ ] _____________________

**Quarter End:**
- [ ] _____________________
- [ ] _____________________
- [ ] _____________________

**Year End:**
- [ ] _____________________
- [ ] _____________________
- [ ] _____________________

### 📝 Final Assessment

**Rate your confidence (1-5) after training:**
- [ ] Installation & setup: ___/5
- [ ] Company configuration: ___/5
- [ ] Trial Balance import: ___/5
- [ ] Account mapping: ___/5
- [ ] Selection Sheet: ___/5
- [ ] Input forms: ___/5
- [ ] Generating statements: ___/5
- [ ] Excel export: ___/5
- [ ] Troubleshooting: ___/5

**Overall:**
- [ ] Ready to use independently: Yes / Need more practice

---

## 🎓 TRAINING COMPLETION CERTIFICATE

**Congratulations!**

You have completed the Financial Automation v1.0 User Training.

**Skills Acquired:**
- ✅ Application installation and configuration
- ✅ Company and master data setup
- ✅ Trial Balance import and mapping
- ✅ Selection Sheet configuration
- ✅ Detailed data entry (PPE, CWIP, etc.)
- ✅ Financial statement generation
- ✅ Excel export with formula linking
- ✅ Best practices and troubleshooting

**Next Steps:**
1. Complete hands-on practice with your company data
2. Generate your first real financial statements
3. Share knowledge with your team
4. Provide feedback for v1.1 improvements

**Training Completion Date:** __________________

**Trainee Signature:** __________________

---

## 📞 SUPPORT & FEEDBACK

**Questions or Feedback?**
- 📧 Email: support@yourcompany.com
- 🌐 Website: www.yourcompany.com
- 📱 Phone: +91-XXXXX-XXXXX

**Share Your Success Story:**
We'd love to hear how Financial Automation has helped your business!

---

**Training Guide Version**: 1.0  
**Last Updated**: October 19, 2025  
**For Application Version**: 1.0.0  
**Total Training Time**: 4-6 hours

**© 2025 Financial Automation. All rights reserved.**
