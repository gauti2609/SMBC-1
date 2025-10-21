# 🎓 Financial Automation Application - User Training Materials

**Version**: 1.0.0  
**Training Duration**: 4-6 hours (self-paced)  
**Level**: Beginner to Intermediate  
**Prerequisites**: Basic Excel knowledge, accounting fundamentals

---

## 📋 **TRAINING OVERVIEW**

This comprehensive training guide will take you from beginner to proficient user of the Financial Automation Application.

**Learning Objectives**:
- ✅ Install and configure the application
- ✅ Import Trial Balance data from Excel
- ✅ Use the Selection Sheet effectively
- ✅ Generate Schedule III compliant financials
- ✅ Export to formula-linked Excel
- ✅ Troubleshoot common issues

**Training Structure**:
- **Module 1**: Installation & Setup (30 min)
- **Module 2**: Company Management (30 min)
- **Module 3**: Trial Balance Import (45 min)
- **Module 4**: Selection Sheet Mastery (60 min)
- **Module 5**: Financial Statements (45 min)
- **Module 6**: Excel Export & Customization (30 min)
- **Module 7**: Advanced Features (60 min)

---

## 🎯 **MODULE 1: INSTALLATION & SETUP** (30 minutes)

### **1.1 System Preparation**

**Before You Begin**:
- [ ] Windows 10/11 computer available
- [ ] 500 MB free disk space
- [ ] Administrator access (for first install)
- [ ] Excel 2016+ installed (for exports)

**Download Application**:
1. Download `FinancialAutomation_v1.0.zip`
2. Extract to `C:\FinancialAutomation`
3. Verify files present (15 files total)

---

### **1.2 First Launch**

**Step-by-Step**:

1. **Locate Executable**
   ```
   Navigate to: C:\FinancialAutomation
   File: FinancialAutomation.exe
   ```

2. **Run Application**
   - Double-click `FinancialAutomation.exe`
   - If Windows warns: Click "More info" → "Run anyway"
   - Wait for splash screen (2-3 seconds)

3. **Database Creation**
   ```
   ✅ Creating database tables... (10 seconds)
   ✅ Initializing master data...
   ✅ Setup complete!
   ```

**✅ Checkpoint**: Application window appears with login screen

---

### **1.3 Create Admin User**

**First User Setup**:

1. Click **"Create Admin User"** button
2. Fill in details:
   ```
   Username:    admin
   Password:    [Choose strong password, min 8 chars]
   Confirm:     [Repeat password]
   Email:       admin@yourcompany.com
   Full Name:   System Administrator
   ```

3. Click **"Create"**
4. Success message: "Admin user created successfully"

**✅ Checkpoint**: You can now log in with admin/[your password]

---

### **1.4 Login**

1. Enter credentials:
   - Username: `admin`
   - Password: [your password]

2. Click **"Login"**

3. Main window appears with 8 tabs

**✅ Checkpoint**: You see the main application interface

---

### **EXERCISE 1.1**: Installation Verification

**Task**: Complete these steps to verify installation

1. Close and reopen application
2. Log in successfully
3. Check database location:
   ```
   File Explorer → C:\FinancialAutomation
   Look for: financial_automation.db (should exist, ~100 KB)
   ```

4. Verify menu items:
   - File menu (New Company, Backup, Exit)
   - Help menu (User Guide, About)

**Expected Result**: All items present and clickable

---

## 🏢 **MODULE 2: COMPANY MANAGEMENT** (30 minutes)

### **2.1 Create Your First Company**

**Navigate to Company Info Tab**:

1. Click **"Company Info"** tab (first tab)
2. Click **"New Company"** button (if not already shown)

**Fill in Company Details**:

```
┌─ COMPANY INFORMATION ─────────────────────────────────┐
│                                                        │
│ Entity Name:        ABC Manufacturing Ltd            │
│ CIN:                L12345KA2020PLC123456            │
│                                                        │
│ Registered Address:                                    │
│ ┌──────────────────────────────────────────────────┐  │
│ │ 123 Industrial Area, Sector 5                   │  │
│ │ Bangalore - 560001                               │  │
│ │ Karnataka, India                                 │  │
│ └──────────────────────────────────────────────────┘  │
│                                                        │
│ Financial Year:                                        │
│   Start Date:  [01-Apr-2024]  (DD-MMM-YYYY)          │
│   End Date:    [31-Mar-2025]  (auto-calculated)      │
│                                                        │
│ Currency:       [INR ▼]                               │
│ Units:          [Lakhs ▼]                             │
│                                                        │
│ [Save Company]  [Cancel]                              │
└────────────────────────────────────────────────────────┘
```

**Field Explanations**:

- **Entity Name**: Legal company name (as per ROC)
- **CIN**: Corporate Identification Number (21 chars)
- **Address**: Complete registered office address
- **FY Start**: First day of financial year (usually 01-Apr)
- **FY End**: Last day (auto-calculated, usually 31-Mar)
- **Currency**: INR, USD, EUR, GBP (usually INR)
- **Units**: Lakhs (1,00,000) or Crores (1,00,00,000)

**Click "Save Company"**

**✅ Checkpoint**: Success message "Company created successfully"

---

### **2.2 Company Selector**

**Understanding the Company Dropdown**:

```
Top of window: [ABC Manufacturing Ltd ▼]
```

**Purpose**: Switch between multiple companies

**Usage**:
- One company → Always shows that company
- Multiple companies → Dropdown to select
- Current company highlighted
- All data filters to selected company

**Try It**:
1. Note company dropdown at top
2. All tabs now work for this company
3. Create second company (optional) to see dropdown

---

### **2.3 Edit Company Details**

**To Update Company Info**:

1. Go to Company Info tab
2. Edit any field
3. Click "Update Company"
4. Success message confirms

**Common Updates**:
- Change FY dates (for new year)
- Update address
- Change units (Lakhs ↔ Crores)

**✅ Checkpoint**: Company details saved and displayed correctly

---

### **EXERCISE 2.1**: Company Setup

**Task**: Create a practice company

**Company Details**:
```
Entity Name:      Practice Ltd
CIN:              L99999KA2023PLC999999
Address:          Your choice
FY:               01-Apr-2024 to 31-Mar-2025
Currency:         INR
Units:            Lakhs
```

**Verification**:
- Company appears in dropdown (if multiple companies)
- All details correct in Company Info tab
- Can switch to Practice Ltd using dropdown

---

## 📊 **MODULE 3: TRIAL BALANCE IMPORT** (45 minutes)

### **3.1 Prepare Your Trial Balance File**

**Required Excel Format**:

```
Column A: Ledger Name / Account Name
Column B: Opening Balance (Current Year)
Column C: Debit (Current Year)
Column D: Credit (Current Year)
Column E: Closing Balance (Current Year)
Column F: Closing Balance (Previous Year) [Optional]
```

**Example Row**:
```
| Ledger               | Opening | Debit    | Credit   | Closing | Closing PY |
|----------------------|---------|----------|----------|---------|------------|
| Cash at Bank         | 50.00   | 200.00   | 150.00   | 100.00  | 50.00      |
| Trade Receivables    | 150.00  | 500.00   | 450.00   | 200.00  | 150.00     |
| Computer Equipment   | 10.00   | 5.00     | 0.00     | 15.00   | 10.00      |
```

**Important**: 
- First row = Headers
- Units in Lakhs (if company uses Lakhs)
- No formulas in cells (values only)
- No merged cells
- No empty rows in middle

**Using Sample File**:
- File: `Sample_TB.xlsx` (included in package)
- Contains: 271 entries
- Realistic data: Manufacturing company
- Pre-formatted correctly

---

### **3.2 Import Process**

**Step-by-Step Import**:

1. **Go to Trial Balance Tab**
   - Click "Trial Balance" tab (2nd tab)
   - Empty table initially

2. **Click "Import from Excel"** button
   - File browser opens
   - Navigate to your TB file
   - Select file (e.g., Sample_TB.xlsx)
   - Click "Open"

3. **Preview Screen**
   ```
   ┌─ IMPORT PREVIEW ─────────────────────────────────┐
   │                                                   │
   │ File: Sample_TB.xlsx                             │
   │ Rows Found: 271                                   │
   │                                                   │
   │ Mapping:                                          │
   │   Column A → Ledger Name     ✓                   │
   │   Column B → Opening Balance ✓                   │
   │   Column C → Debit           ✓                   │
   │   Column D → Credit          ✓                   │
   │   Column E → Closing Balance ✓                   │
   │   Column F → Closing PY      ✓                   │
   │                                                   │
   │ [Proceed with Import]  [Cancel]                  │
   └───────────────────────────────────────────────────┘
   ```

4. **Click "Proceed with Import"**
   - Progress bar shows
   - "Importing... 50... 100... 150... 200... 271"
   - Auto-mapping to major heads
   - "✅ Import complete! 271 entries imported"

**✅ Checkpoint**: Trial Balance table populated with your data

---

### **3.3 Review Imported Data**

**Table Columns**:

| Ledger Name | Opening | Debit | Credit | Closing | Major Head | Actions |
|-------------|---------|-------|--------|---------|------------|---------|
| Cash at Bank | 50.00 | 200.00 | 150.00 | 100.00 | Note 13: Cash | Edit |
| Trade Receivables | 150.00 | 500.00 | 450.00 | 200.00 | Note 10: Receivables | Edit |
| **UNMAPPED** | 10.00 | 5.00 | 0.00 | 15.00 | **[Assign]** | **Edit** |

**Color Coding**:
- 🟢 **Green row**: Mapped to major head
- 🔴 **Red row**: Unmapped (needs attention)
- ⚪ **White row**: Normal

**Totals Row**:
```
Total: 271 entries | Debit: 10,500.00 | Credit: 10,500.00 | Balanced: ✓
```

---

### **3.4 Manual Mapping**

**For Unmapped Accounts**:

1. **Click "Edit" on red/unmapped row**

2. **Mapping Dialog Appears**:
   ```
   ┌─ MAP ACCOUNT ──────────────────────────────┐
   │                                             │
   │ Ledger: Miscellaneous Expenses             │
   │                                             │
   │ Assign to Major Head:                      │
   │ [Select Major Head ▼]                      │
   │   - Note 1: Share Capital                  │
   │   - Note 2: Reserves & Surplus             │
   │   ...                                       │
   │   - Note 27: Other Expenses                │
   │                                             │
   │ Assign to Minor Head: (Optional)           │
   │ [Select Minor Head ▼]                      │
   │                                             │
   │ [Save Mapping]  [Cancel]                   │
   └─────────────────────────────────────────────┘
   ```

3. **Select appropriate major head**
   - Example: "Miscellaneous Expenses" → "Note 27: Other Expenses"

4. **Click "Save Mapping"**
   - Row turns green
   - Mapping saved

**Auto-Mapping** (Already Done):
- The system auto-maps ~80% using keywords
- "Cash", "Bank" → Note 13: Cash
- "Receivable", "Debtor" → Note 10: Trade Receivables
- "Computer", "Laptop" → Note 1: PPE
- etc.

---

### **3.5 Export Unmapped Items**

**To Review Unmapped**:

1. Click **"Export Unmapped"** button
2. Excel file created: `Unmapped_Accounts_[date].xlsx`
3. Review offline
4. Map manually in application

**Unmapped File Format**:
```
| Ledger Name | Closing Balance | Suggested Major Head |
|-------------|-----------------|----------------------|
| Suspense A/C | 5.00 | [Review Needed] |
```

---

### **EXERCISE 3.1**: Import Sample Trial Balance

**Task**: Import and review sample data

**Steps**:
1. Go to Trial Balance tab
2. Click "Import from Excel"
3. Select `Sample_TB.xlsx`
4. Review preview
5. Import (271 entries)
6. Check totals balance
7. Count unmapped items
8. Map 2-3 unmapped accounts manually

**Verification**:
- ✅ Debit = Credit (balanced)
- ✅ Most accounts mapped (green)
- ✅ Can edit any row
- ✅ Export unmapped works

---

## 📝 **MODULE 4: SELECTION SHEET MASTERY** (60 minutes)

### **4.1 Understanding the Selection Sheet**

**Purpose**:
- Select which notes to include in financials
- 68 predefined Schedule III notes available
- System recommends based on your Trial Balance
- You can override any recommendation

**Access**:
- Click "Selection Sheet" tab (3rd tab)

**What You See**:
```
┌─ SELECTION SHEET ──────────────────────────────────────────────────────┐
│                                                                         │
│ [Update Recommendations]  [Update Auto-Numbering]  [Reset All]        │
│                                                                         │
│ Table: 68 notes across 7 categories                                    │
│                                                                         │
│ Columns:                                                                │
│ - Note Ref: Schedule III reference (A.1, B.2, etc.)                   │
│ - Description: Full note description                                   │
│ - Linked Major Head: Auto-linked account types                        │
│ - System Rec: AI recommendation (Yes/No/Blank)                        │
│ - User Selection: Your choice (Yes/No/Blank)                          │
│ - Final: Combined result (System + User)                              │
│ - Auto-Number: Sequential numbering (1, 2, 3...)                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### **4.2 The 68 Predefined Notes**

**Category A: Share Capital & Reserves** (8 notes)
```
A.1 - Share Capital
A.2 - Reserves and Surplus
A.3 - Money Received Against Share Warrants
A.4 - Share Application Money Pending Allotment
A.5 - Equity Component of Compound Financial Instruments
A.6 - Other Equity
A.7 - Non-Controlling Interests
A.8 - Changes in Equity
```

**Category B: Non-Current Liabilities** (8 notes)
```
B.1 - Long-term Borrowings
B.2 - Deferred Tax Liabilities (Net)
B.3 - Other Long-term Liabilities
B.4 - Long-term Provisions
B.5 - Preference Share Capital
B.6 - Finance Lease Obligations
B.7 - Employee Benefits (Gratuity/Leave)
B.8 - Government Grants
```

**Category C: Current Liabilities** (11 notes)
```
C.1 - Short-term Borrowings
C.2 - Trade Payables
C.3 - Other Current Liabilities
C.4 - Short-term Provisions
C.5 - Current Portion of Long-term Borrowings
C.6 - Current Maturities of Finance Leases
C.7 - Unpaid Dividends
C.8 - Application Money Refundable
C.9 - Unclaimed Dividends
C.10 - Interest Accrued
C.11 - Acceptances
```

**Category D: Non-Current Assets** (13 notes)
```
D.1 - Fixed Assets (PPE)
D.2 - Goodwill
D.3 - Other Intangible Assets
D.4 - Capital Work-in-Progress
D.5 - Intangible Assets under Development
D.6 - Non-current Investments
D.7 - Deferred Tax Assets (Net)
D.8 - Long-term Loans and Advances
D.9 - Other Non-current Assets
D.10 - Investment Property
D.11 - Biological Assets
D.12 - Financial Assets
D.13 - Assets Held for Sale
```

**Category E: Current Assets** (14 notes)
```
E.1 - Current Investments
E.2 - Inventories
E.3 - Trade Receivables
E.4 - Cash and Cash Equivalents
E.5 - Short-term Loans and Advances
E.6 - Other Current Assets
E.7 - Current Financial Assets
E.8 - Assets Classified as Held for Sale
E.9 - Prepaid Expenses
E.10 - Advance Tax (Net)
E.11 - MAT Credit Entitlement
E.12 - Short-term Deposits
E.13 - Unbilled Revenue
E.14 - Contract Assets
```

**Category F: Equity & Liabilities** (7 notes)
```
F.1 - Revenue from Operations
F.2 - Other Income
F.3 - Cost of Materials Consumed
F.4 - Purchases of Stock-in-Trade
F.5 - Changes in Inventories
F.6 - Employee Benefits Expense
F.7 - Finance Costs
```

**Category G: Statement of Changes** (7 notes)
```
G.1 - Earnings Per Share
G.2 - Contingent Liabilities
G.3 - Commitments
G.4 - Related Party Disclosures
G.5 - Segment Reporting
G.6 - Significant Accounting Policies
G.7 - Prior Period Items
```

---

### **4.3 System Recommendations**

**How It Works**:

1. **Analyze Trial Balance**
   - Scans all account names
   - Checks closing balances
   - Identifies patterns

2. **Recommend Notes**
   - If "Cash" accounts found → Recommend E.4 (Cash & Cash Equivalents)
   - If "Receivables" found → Recommend E.3 (Trade Receivables)
   - If "Inventory" found → Recommend E.2 (Inventories)
   - etc.

3. **Mark Recommendations**
   - System Rec column shows "Yes" (green highlight)
   - Empty if not recommended

**Trigger Recommendations**:

1. **From Trial Balance Tab**:
   - After import, click **"Update Note Recommendations"**
   - Message: "System recommended 48 notes"
   - Auto-switches to Selection Sheet tab

2. **From Selection Sheet Tab**:
   - Click **"Update Recommendations"** button
   - Analyzes TB again
   - Updates recommendations

**✅ Checkpoint**: System Rec column populated with Yes/Blank

---

### **4.4 User Overrides**

**You Control Final Selection**:

**Scenario 1: Accept Recommendation**
```
System Rec: Yes → Leave User Selection: Blank
Result: Final = Yes ✓
```

**Scenario 2: Reject Recommendation**
```
System Rec: Yes → Change User Selection to: No
Result: Final = No ✗
```

**Scenario 3: Add Note Manually**
```
System Rec: Blank → Change User Selection to: Yes
Result: Final = Yes ✓
```

**How to Override**:

1. Click dropdown in **User Selection** column
2. Choose: **Yes** / **No** / **Blank**
   ```
   [Yes ▼]
   ```
3. Selection saved automatically
4. **Final** column updates

**Example**:
```
Note: G.2 - Contingent Liabilities
System Rec: Blank (no contingencies found in TB)
User Selection: Yes (you know there are contingencies to disclose)
Final: Yes ✓ (will appear in financials)
```

---

### **4.5 Auto-Numbering**

**Purpose**: Sequential note numbering (1, 2, 3...)

**Before Auto-Numbering**:
```
| Note Ref | Description | Final | Auto-Number |
|----------|-------------|-------|-------------|
| A.1 | Share Capital | Yes | (empty) |
| A.2 | Reserves | Yes | (empty) |
| D.1 | Fixed Assets | Yes | (empty) |
| E.3 | Receivables | Yes | (empty) |
```

**After Auto-Numbering**:
```
| Note Ref | Description | Final | Auto-Number |
|----------|-------------|-------|-------------|
| A.1 | Share Capital | Yes | 1 |
| A.2 | Reserves | Yes | 2 |
| D.1 | Fixed Assets | Yes | 3 |
| E.3 | Receivables | Yes | 4 |
```

**How It Works**:
1. Takes all rows where **Final = Yes**
2. Skips section headers
3. Numbers sequentially: 1, 2, 3...
4. Updates **Auto-Number** column
5. These numbers appear in Balance Sheet!

**To Update Numbering**:
- Click **"Update Auto-Numbering"** button
- Happens instantly
- Can re-run anytime

**Balance Sheet Uses These Numbers**:
```
BALANCE SHEET

Shareholders' Funds
  Share Capital                1        100.00        100.00
  Reserves and Surplus         2        250.00        200.00
                                        -------       -------
                                        350.00        300.00

Non-Current Assets
  Fixed Assets                 3        500.00        450.00

Current Assets
  Trade Receivables            4        200.00        150.00
```

**✅ Checkpoint**: Auto-Number column shows 1, 2, 3... for selected notes

---

### **4.6 Color Coding Guide**

**Understanding Colors**:

| Color | Meaning | Column | Action |
|-------|---------|--------|--------|
| 🟢 Green | System recommended | System Rec | Review & accept/reject |
| 🟡 Gold | User selected | User Selection | Your choices |
| ⚪ White | Not selected | Both | Optional |
| 🔵 Blue (header) | Section header | All | Visual separator |

**Example View**:
```
[🔵 CATEGORY A: SHARE CAPITAL & RESERVES]  ← Blue header

🟢 A.1  Share Capital              System: Yes   User: (blank)  Final: Yes
🟢 A.2  Reserves and Surplus       System: Yes   User: (blank)  Final: Yes
⚪ A.3  Share Warrants             System: (blank) User: (blank)  Final: No
🟡 A.4  Share Application Money    System: (blank) User: Yes     Final: Yes
```

---

### **EXERCISE 4.1**: Selection Sheet Practice

**Task**: Work through complete selection process

**Part A: System Recommendations**
1. Ensure Sample TB already imported
2. Go to Trial Balance tab
3. Click "Update Note Recommendations"
4. Switch to Selection Sheet tab
5. Count green rows (System Rec = Yes)
   - How many? _____

**Part B: User Overrides**
1. Find note "G.2 - Contingent Liabilities"
2. Check System Rec (probably Blank)
3. Change User Selection to "Yes"
4. Verify Final shows "Yes"

**Part C: Reject a Recommendation**
1. Find a green row (System Rec = Yes)
2. Change User Selection to "No"
3. Verify Final shows "No"
4. Change back to "Blank" (to accept again)

**Part D: Auto-Numbering**
1. Click "Update Auto-Numbering"
2. Check Auto-Number column
3. Note first number: ___
4. Note last number: ___
5. Verify sequential (1, 2, 3...)

**Verification Checklist**:
- [ ] Can see all 68 notes
- [ ] System Rec column populated
- [ ] Can change User Selection
- [ ] Final column updates correctly
- [ ] Auto-numbering works

---

## 💰 **MODULE 5: FINANCIAL STATEMENTS** (45 minutes)

### **5.1 Generate Statements**

**Prerequisites**:
- ✅ Company created
- ✅ Trial Balance imported
- ✅ Selection Sheet configured
- ✅ Auto-numbering updated

**Generate Process**:

1. **Go to Financials Tab**
   - Click "Financials" tab (7th tab)

2. **Click "Generate Financial Statements"**
   ```
   [🔄 Generate Financial Statements]
   ```

3. **Processing** (takes 5-10 seconds):
   ```
   Generating Balance Sheet... ✓
   Generating Profit & Loss Statement... ✓
   Generating Cash Flow Statement... ✓
   Creating Note 1... ✓
   Creating Note 2... ✓
   ...
   Creating Note 48... ✓
   
   ✅ Financial statements generated successfully!
   ```

4. **View Results**
   - Sub-tabs appear: BS, P&L, CF, Notes
   - Click each to view

**✅ Checkpoint**: All three statements visible

---

### **5.2 Balance Sheet**

**Format**: Schedule III Vertical Format

```
ABC MANUFACTURING LTD
BALANCE SHEET as at 31-Mar-2025
(All amounts in Lakhs, unless otherwise stated)

                                        Note No.  As at           As at
                                                  31-Mar-2025     31-Mar-2024
                                                  ───────────     ───────────
I. EQUITY AND LIABILITIES

(1) Shareholders' Funds
    (a) Share Capital                   1         100.00          100.00
    (b) Reserves and Surplus            2         250.00          200.00
                                                  ───────         ───────
                                                  350.00          300.00

(2) Non-Current Liabilities
    (a) Long-term Borrowings            3         150.00          180.00
    (b) Long-term Provisions            4          20.00           15.00
                                                  ───────         ───────
                                                  170.00          195.00

(3) Current Liabilities
    (a) Short-term Borrowings           5          80.00           70.00
    (b) Trade Payables                  6         200.00          150.00
    (c) Other Current Liabilities       7          50.00           45.00
    (d) Short-term Provisions           8          15.00           12.00
                                                  ───────         ───────
                                                  345.00          277.00
                                                  ───────         ───────
TOTAL                                             865.00          772.00
                                                  ═══════         ═══════

II. ASSETS

(1) Non-Current Assets
    (a) Fixed Assets                    9         400.00          380.00
    (b) Non-current Investments        10          50.00           50.00
    (c) Long-term Loans & Advances     11          30.00           25.00
                                                  ───────         ───────
                                                  480.00          455.00

(2) Current Assets
    (a) Inventories                    12         150.00          120.00
    (b) Trade Receivables              13         200.00          160.00
    (c) Cash and Cash Equivalents      14          20.00           25.00
    (d) Other Current Assets           15          15.00           12.00
                                                  ───────         ───────
                                                  385.00          317.00
                                                  ───────         ───────
TOTAL                                             865.00          772.00
                                                  ═══════         ═══════
```

**Features**:
- ✅ Schedule III compliant structure
- ✅ Groupings (Shareholders' Funds, etc.)
- ✅ Note numbers match Selection Sheet
- ✅ Comparative (CY vs PY)
- ✅ Proper totals and subtotals
- ✅ Professional formatting

---

### **5.3 Profit & Loss Statement**

**Format**: Schedule III Vertical Format

```
ABC MANUFACTURING LTD
STATEMENT OF PROFIT AND LOSS for the year ended 31-Mar-2025
(All amounts in Lakhs, unless otherwise stated)

                                        Note No.  Year Ended      Year Ended
                                                  31-Mar-2025     31-Mar-2024
                                                  ───────────     ───────────
I. Revenue from Operations              16        1,500.00        1,200.00
II. Other Income                        17           50.00           40.00
                                                  ─────────       ─────────
III. Total Income (I+II)                          1,550.00        1,240.00
                                                  ─────────       ─────────

IV. EXPENSES:
    Cost of Materials Consumed          18          800.00          650.00
    Purchase of Stock-in-Trade          19          100.00           80.00
    Changes in Inventories              20          (30.00)         (20.00)
    Employee Benefits Expense           21          200.00          180.00
    Finance Costs                       22           40.00           45.00
    Depreciation                        23           50.00           48.00
    Other Expenses                      24          140.00          120.00
                                                  ─────────       ─────────
Total Expenses (IV)                               1,300.00        1,103.00
                                                  ─────────       ─────────

V. Profit Before Tax (III-IV)                      250.00          137.00

VI. Tax Expense:
    (1) Current Tax                                  60.00           35.00
    (2) Deferred Tax                                  5.00            3.00
                                                  ─────────       ─────────
Total Tax Expense                                    65.00           38.00
                                                  ─────────       ─────────

VII. Profit for the Period (V-VI)                  185.00           99.00
                                                  ═════════       ═════════

Earnings Per Share (Basic):                          18.50            9.90
```

---

### **5.4 Cash Flow Statement**

**Method**: Indirect Method

```
ABC MANUFACTURING LTD
CASH FLOW STATEMENT for the year ended 31-Mar-2025
(All amounts in Lakhs, unless otherwise stated)

                                                    Year Ended      Year Ended
                                                    31-Mar-2025     31-Mar-2024
                                                    ───────────     ───────────
A. CASH FLOW FROM OPERATING ACTIVITIES

   Profit Before Tax                                  250.00          137.00
   
   Adjustments for:
     Depreciation                                      50.00           48.00
     Interest Expense                                  40.00           45.00
     Interest Income                                   (5.00)          (4.00)
                                                     ────────        ────────
   Operating Profit before Working Capital           335.00          226.00
   
   Changes in Working Capital:
     (Increase)/Decrease in Inventories               (30.00)         (20.00)
     (Increase)/Decrease in Trade Receivables         (40.00)         (30.00)
     Increase/(Decrease) in Trade Payables             50.00           35.00
     Increase/(Decrease) in Other Current Liab         5.00            5.00
                                                     ────────        ────────
   Cash Generated from Operations                    320.00          216.00
   
   Less: Income Tax Paid                              (60.00)         (35.00)
   Less: Interest Paid                                (40.00)         (45.00)
                                                     ────────        ────────
   Net Cash from Operating Activities (A)            220.00          136.00
                                                     ────────        ────────

B. CASH FLOW FROM INVESTING ACTIVITIES

   Purchase of Fixed Assets                           (70.00)         (80.00)
   Interest Received                                    5.00            4.00
                                                     ────────        ────────
   Net Cash used in Investing Activities (B)          (65.00)         (76.00)
                                                     ────────        ────────

C. CASH FLOW FROM FINANCING ACTIVITIES

   Proceeds from Borrowings                            50.00           60.00
   Repayment of Borrowings                            (50.00)         (40.00)
   Dividends Paid                                    (160.00)         (80.00)
                                                     ────────        ────────
   Net Cash from Financing Activities (C)            (160.00)         (60.00)
                                                     ────────        ────────

NET INCREASE/(DECREASE) IN CASH (A+B+C)                (5.00)           0.00

Cash and Cash Equivalents at Beginning                 25.00           25.00
                                                     ────────        ────────
Cash and Cash Equivalents at End                       20.00           25.00
                                                     ════════        ════════
```

---

### **5.5 Notes to Accounts**

**All Selected Notes Generated**:

**Example: Note 1 - Share Capital**
```
NOTE 1: SHARE CAPITAL
                                                As at           As at
                                                31-Mar-2025     31-Mar-2024
                                                ───────────     ───────────
Authorized Capital:
10,000 Equity Shares of Rs. 10 each             100.00          100.00
                                                ───────         ───────
                                                100.00          100.00
                                                ───────         ───────

Issued, Subscribed and Fully Paid-up:
10,000 Equity Shares of Rs. 10 each             100.00          100.00
                                                ───────         ───────
                                                100.00          100.00
                                                ═══════         ═══════

(a) Reconciliation of number of shares:
                                            Number (000s)       Amount
Opening Balance                                 10.00           100.00
Add: Shares issued during the year               0.00             0.00
                                                ──────          ───────
Closing Balance                                 10.00           100.00
                                                ══════          ═══════

(b) Rights, preferences and restrictions:
    Equity shareholders are entitled to one vote per share
    and dividend as declared by the company.

(c) Shareholders holding more than 5%:
    Name                        No. of Shares   % Holding
    XYZ Holdings Ltd                 6,000          60%
```

**Example: Note 13 - Trade Receivables**
```
NOTE 13: TRADE RECEIVABLES
                                                As at           As at
                                                31-Mar-2025     31-Mar-2024
                                                ───────────     ───────────
Unsecured, Considered Good:
  - Outstanding for period less than 6 months     140.00          112.00
  - Outstanding for period more than 6 months      60.00           48.00
                                                ────────        ────────
                                                  200.00          160.00

Unsecured, Considered Doubtful:
  - Outstanding for period more than 6 months      10.00            8.00

Less: Allowance for Doubtful Debts               (10.00)          (8.00)
                                                ────────        ────────
                                                  200.00          160.00
                                                ════════        ════════

AGEING SCHEDULE:
Outstanding for:                          Amount      % of Total
  Less than 6 months                      140.00          70%
  6-12 months                              40.00          20%
  1-2 years                                16.00           8%
  2-3 years                                 4.00           2%
  More than 3 years                         0.00           0%
                                         ────────       ─────
Total                                     200.00         100%
                                         ════════       ═════

Note: Ageing based on estimated distribution. Will be replaced with
actual invoice-level data in future versions.
```

---

### **EXERCISE 5.1**: Generate and Review Financials

**Task**: Generate statements and verify

**Part A: Generation**
1. Go to Financials tab
2. Click "Generate Financial Statements"
3. Wait for completion message
4. Note time taken: _____ seconds

**Part B: Balance Sheet Review**
1. Click BS sub-tab
2. Verify structure matches Schedule III
3. Check note numbers match Selection Sheet
4. Verify CY and PY columns present
5. Check totals balance (Assets = Liabilities)

**Part C: P&L Review**
1. Click P&L sub-tab
2. Verify revenue, expenses, tax, profit
3. Check note numbers
4. Verify profit calculation correct

**Part D: Cash Flow Review**
1. Click CF sub-tab
2. Verify three sections (Operating, Investing, Financing)
3. Check cash reconciliation
4. Verify matches BS cash balance

**Part E: Notes Review**
1. Click Notes sub-tab
2. Scroll through all notes
3. Find Note 1 (Share Capital)
4. Find Note 13 (Trade Receivables)
5. Verify ageing schedule present

**Verification Checklist**:
- [ ] All three statements generated
- [ ] Note numbers sequential (1, 2, 3...)
- [ ] Comparative years shown (CY/PY)
- [ ] Totals match (BS balances, P&L calculations)
- [ ] Professional formatting
- [ ] All selected notes present

---

## 📊 **MODULE 6: EXCEL EXPORT & CUSTOMIZATION** (30 minutes)

### **6.1 Export to Excel**

**From Financials Tab**:

1. **Click "Export to Excel" button**
   ```
   [📊 Export to Excel]
   ```

2. **Save Dialog Appears**:
   ```
   Save As: ABC_Manufacturing_Financials_31Mar2025.xlsx
   Location: [Choose folder]
   ```

3. **Export Progress**:
   ```
   Creating workbook... ✓
   Adding Balance Sheet... ✓
   Adding Profit & Loss... ✓
   Adding Cash Flow... ✓
   Adding Note 1... ✓
   Adding Note 2... ✓
   ...
   Adding Note 48... ✓
   Applying formatting... ✓
   Adding formulas... ✓
   
   ✅ Excel export complete! 30 sheets created.
   File size: 26.4 KB
   
   [Open Excel File]  [Close]
   ```

4. **Click "Open Excel File"**
   - Excel launches
   - Workbook opens automatically

**✅ Checkpoint**: Excel workbook with 30 sheets

---

### **6.2 Excel Workbook Structure**

**Sheet Tabs** (30 total):
```
Balance Sheet | Profit & Loss | Cash Flow | Note_1 | Note_2 | ... | Note_48
```

**Sheet Organization**:
- First 3 sheets: Main statements
- Next N sheets: Notes (one per selected note)
- All professionally formatted
- Formula-linked

---

### **6.3 Formula Linking**

**How It Works**:

**Balance Sheet Cell** (C7):
```excel
='Note_1'!C10
```

**What This Means**:
- Cell C7 in Balance Sheet
- Links to Cell C10 in Note_1 sheet
- If Note_1 changes → Balance Sheet updates automatically
- Real Excel formula, not copy-paste!

**Example**:

1. **Open Balance Sheet**
   - Find "Share Capital" row
   - Note value: 100.00
   - Click cell → Formula bar shows: `='Note_1'!C10`

2. **Navigate to Note_1**
   - Click "Note_1" tab
   - Find cell C10
   - Value: 100.00

3. **Test Formula**:
   - Change C10 to 150.00
   - Go back to Balance Sheet
   - Share Capital now shows 150.00 ✓
   - Formula worked!

4. **Undo** (Ctrl+Z to revert)

**All Linked Cells**:
- Every line item in BS/PL links to a note
- Notes link to sub-schedules
- Totals use SUM formulas
- Percentages calculate automatically

---

### **6.4 Formatting Features**

**Schedule III Formatting Applied**:

1. **Headers**:
   - Company name (Bold, 14pt)
   - Statement title (Bold, 12pt)
   - "As at 31-Mar-2025" (Italic, 10pt)
   - Column headers (Bold, centered)

2. **Colors**:
   - Header row: Blue background (#4472C4)
   - Totals row: Light grey (#D3D3D3)
   - Section headers: Bold
   - Subtotals: Underlined

3. **Borders**:
   - All cells: Thin borders
   - Header: Thick bottom border
   - Totals: Double underline
   - Grand totals: Thick double border

4. **Alignment**:
   - Text: Left aligned
   - Numbers: Right aligned
   - Headers: Center aligned
   - Decimals: 2 places (1.00)

5. **Column Widths**:
   - Description: 40 characters
   - Note No: 10 characters
   - Amounts: 15 characters
   - Auto-adjusted to content

---

### **6.5 Customization in Excel**

**You Can Edit**:

✅ **Formatting**:
- Change colors
- Adjust fonts
- Modify borders
- Add company logo

✅ **Formulas**:
- Add calculated rows
- Insert percentages
- Create ratios
- Add conditional formatting

✅ **Content**:
- Add notes/comments
- Insert explanations
- Include annexures
- Add charts/graphs

⚠️ **Warnings**:
- Don't delete note sheets (breaks formulas)
- Don't rename sheets (breaks links)
- Keep formula structure intact
- Save as new file if major changes

**Best Practice**:
1. Export from application
2. Save as "Original_Export.xlsx"
3. Save As "Working_Copy.xlsx"
4. Edit working copy
5. Keep original for reference

---

### **EXERCISE 6.1**: Excel Export and Formula Testing

**Task**: Export and verify formulas

**Part A: Export**
1. Go to Financials tab
2. Click "Export to Excel"
3. Save as "Practice_Export.xlsx"
4. Wait for completion
5. Click "Open Excel File"

**Part B: Verify Structure**
1. Count sheet tabs: _____ (should be 30)
2. Check first 3 sheets: BS, P&L, CF
3. Check note sheets: Note_1, Note_2, etc.

**Part C: Test Formulas**
1. Go to Balance Sheet
2. Find "Share Capital" (Note 1)
3. Click cell → Note formula: _____________
4. Navigate to Note_1 sheet
5. Verify same value in referenced cell

**Part D: Formula Chain**
1. Balance Sheet → Note 1 → Detailed schedule
2. Change value in detailed schedule
3. Verify Note 1 updates
4. Verify Balance Sheet updates
5. Undo changes (Ctrl+Z)

**Part E: Formatting Check**
- [ ] Company header present
- [ ] Colors applied (blue headers)
- [ ] Borders on all cells
- [ ] Numbers right-aligned
- [ ] Decimals showing (.00)
- [ ] Column widths appropriate

**Part F: Save & Close**
1. Save Excel file
2. Close Excel
3. Re-open in application
4. Export again (new filename)
5. Compare two exports (should be identical)

---

## 🚀 **MODULE 7: ADVANCED FEATURES** (60 minutes)

### **7.1 PPE Schedule**

**Purpose**: Detailed Fixed Assets schedule

**Navigate**: Click "PPE Schedule" tab

**Data Entry**:
```
┌─ PROPERTY, PLANT & EQUIPMENT ─────────────────────────────────┐
│                                                                │
│ [Add Item]  [Edit]  [Delete]  [Import from Excel]            │
│                                                                │
│ Table:                                                         │
│ Asset Description | Gross Block CY | Depreciation CY | Net   │
│ Computer          | 5.00            | 3.00            | 2.00  │
│ Furniture         | 10.00           | 4.00            | 6.00  │
│ Vehicles          | 20.00           | 8.00            | 12.00 │
│                                                                │
│ Total             | 35.00           | 15.00           | 20.00 │
└────────────────────────────────────────────────────────────────┘
```

**Add Item**:
1. Click "Add Item"
2. Fill form:
   ```
   Asset Description:     Office Equipment
   Gross Block Opening:   10.00
   Additions:             5.00
   Deletions:             0.00
   Gross Block Closing:   15.00 (auto-calculated)
   
   Depreciation Opening:  4.00
   Charge for Year:       2.00
   On Deletions:          0.00
   Depreciation Closing:  6.00 (auto-calculated)
   
   Net Block Closing:     9.00 (auto-calculated)
   ```
3. Click "Save"

**Generates**: Note 1 (Fixed Assets) with complete movement schedule

---

### **7.2 CWIP (Capital Work-in-Progress)**

**Navigate**: Click "CWIP" tab

**Data Entry**:
```
Project Name:          Factory Expansion
Opening Balance:       50.00
Additions during year: 30.00
Capitalized:           0.00
Closing Balance:       80.00 (auto-calculated)
Estimated Completion:  Dec-2025
```

**Generates**: Separate CWIP schedule in financials

---

### **7.3 Investments**

**Navigate**: Click "Investments" tab

**Categories**:
- Non-Current Investments
- Current Investments

**Data Entry**:
```
Investment Type:       Equity Shares
Company Name:          XYZ Ltd
Classification:        Non-Current
Quantity:              1,000 shares
Cost per Unit:         50.00
Total Cost:            50.00 Lakhs
Market Value:          55.00 Lakhs
```

**Generates**: Note 10 (Non-Current Investments)

---

### **7.4 Master Data Management**

**Navigate**: Click "Master Data" tab

**Purpose**: Customize major/minor heads

**Major Heads** (12 default):
```
Note 1:  Share Capital
Note 2:  Reserves & Surplus
Note 3:  Fixed Assets (PPE)
Note 5:  Non-Current Investments
Note 6:  Long-term Loans & Advances
Note 7:  Other Non-Current Assets
Note 9:  Inventories
Note 10: Trade Receivables
Note 13: Cash & Cash Equivalents
Note 20: Long-term Borrowings
Note 24: Trade Payables
Note 27: Other Expenses
```

**Edit Major Head**:
1. Click "Edit" on any row
2. Change description (if needed)
3. Cannot change note number
4. Click "Save"

**Minor Heads** (24 default):
- Sub-categories under major heads
- Example: Under "Cash" → "Cash on Hand", "Bank Accounts"

**Add Minor Head**:
1. Click "Add Minor Head"
2. Select major head
3. Enter description
4. Click "Save"

---

### **7.5 Multi-Company Management**

**Scenario**: Managing multiple entities

**Create Second Company**:
1. Company Info tab → "New Company"
2. Fill details for Company B
3. Click "Save"

**Switch Between Companies**:
```
Top dropdown: [ABC Manufacturing Ltd ▼]
              [XYZ Services Ltd      ]
```

**Data Isolation**:
- Each company has separate TB
- Separate selections
- Separate financials
- Own master data (optional)

**Shared Data** (optional):
- Master data can be shared
- User accounts shared
- Settings shared

---

### **7.6 Backup & Restore**

**Backup Database**:
1. File menu → "Backup Database"
2. Choose location
3. Filename: `financial_automation_backup_20251020.db`
4. Click "Save"

**Restore**:
1. File menu → "Restore Database"
2. Select backup file
3. Confirm (overwrites current data)
4. Restart application

**Best Practices**:
- Backup daily before major work
- Keep 7 days of backups
- Store offsite (cloud/USB)
- Test restore periodically

---

### **7.7 Keyboard Shortcuts**

**Navigation**:
- `Ctrl + 1` through `Ctrl + 8`: Switch tabs
- `Ctrl + N`: New company
- `Ctrl + S`: Save current form
- `Ctrl + Q`: Quit application

**Data Entry**:
- `Tab`: Next field
- `Shift + Tab`: Previous field
- `Enter`: Save and next row
- `Esc`: Cancel edit

**Financials**:
- `Ctrl + G`: Generate statements
- `Ctrl + E`: Export to Excel
- `Ctrl + P`: Print (future)

---

### **EXERCISE 7.1**: Advanced Features Practice

**Task A: Add PPE Items**
1. Go to PPE Schedule tab
2. Add 3 assets:
   - Computer: Gross 10.00, Dep 6.00
   - Furniture: Gross 20.00, Dep 8.00
   - Vehicle: Gross 50.00, Dep 20.00
3. Verify totals calculate
4. Regenerate financials
5. Check Note 1 includes PPE data

**Task B: Create Second Company**
1. Company Info → New Company
2. Name: "Practice Company 2"
3. Save company
4. Switch between companies using dropdown
5. Verify data separated

**Task C: Backup**
1. File menu → Backup
2. Save as "Practice_Backup.db"
3. Verify file created (check file size)
4. Optional: Test restore

**Task D: Master Data**
1. Master Data tab
2. Edit description of any major head
3. Save
4. Verify appears in dropdowns

---

## ✅ **FINAL ASSESSMENT** (30 minutes)

### **Comprehensive Test**

Complete this end-to-end workflow to verify learning:

**Scenario**: Your company needs financial statements for FY 2024-25

**Steps**:

1. **Setup** (5 min)
   - [ ] Create company "Assessment Ltd"
   - [ ] FY: 01-Apr-2024 to 31-Mar-2025
   - [ ] Units: Lakhs

2. **Import Data** (5 min)
   - [ ] Import Sample_TB.xlsx
   - [ ] Verify 271 entries imported
   - [ ] Check balance (Debit = Credit)
   - [ ] Map 3 unmapped items manually

3. **Selection** (5 min)
   - [ ] Update note recommendations
   - [ ] Review all 68 notes
   - [ ] Override 2 notes (accept/reject)
   - [ ] Update auto-numbering
   - [ ] Verify sequential numbers

4. **Additional Data** (5 min)
   - [ ] Add 2 PPE items
   - [ ] Add 1 CWIP project
   - [ ] Add 1 investment

5. **Generate** (3 min)
   - [ ] Generate financial statements
   - [ ] Review Balance Sheet
   - [ ] Review Profit & Loss
   - [ ] Review Cash Flow
   - [ ] Review 5 notes

6. **Export** (3 min)
   - [ ] Export to Excel
   - [ ] Open workbook
   - [ ] Verify 30 sheets
   - [ ] Test one formula
   - [ ] Save Excel file

7. **Verify** (4 min)
   - [ ] BS totals balance
   - [ ] Note numbers sequential
   - [ ] Excel formulas work
   - [ ] All selected notes present
   - [ ] Schedule III format correct

**Passing Criteria**: All 25 checkboxes completed ✓

**Time Limit**: 30 minutes

**Result**: _____ / 25 (___%)

---

## 📚 **ADDITIONAL RESOURCES**

### **Documentation**
- **USER_GUIDE.md**: Complete reference (500+ pages)
- **FAQ.md**: Common questions and answers
- **QUICK_REFERENCE.md**: One-page cheat sheet
- **RELEASE_NOTES.md**: Version history

### **Video Tutorials**
- Installation walkthrough (5 min)
- Trial Balance import (10 min)
- Selection Sheet mastery (15 min)
- Excel export deep dive (10 min)
- Complete workflow (20 min)

### **Sample Files**
- Sample_TB.xlsx: 271 entries
- Sample_Company_Data.xlsx: Complete dataset
- Template_TB_Import.xlsx: Blank template

### **Support**
- Email: support@financialautomation.com
- Forum: forum.financialautomation.com
- Knowledge Base: kb.financialautomation.com

---

## 🎓 **CERTIFICATION** (Optional)

Upon completing all modules and passing the final assessment:

1. Take screenshot of final Excel export
2. Email to: training@financialautomation.com
3. Include:
   - Your name
   - Company name
   - Completion date
   - Assessment score

Receive: **Digital Certificate of Completion**

---

## 📝 **TRAINING FEEDBACK**

Help us improve this training:

**Rate Each Module** (1-5 stars):
- Module 1: Installation ⭐⭐⭐⭐⭐
- Module 2: Company Management ⭐⭐⭐⭐⭐
- Module 3: Trial Balance ⭐⭐⭐⭐⭐
- Module 4: Selection Sheet ⭐⭐⭐⭐⭐
- Module 5: Financials ⭐⭐⭐⭐⭐
- Module 6: Excel Export ⭐⭐⭐⭐⭐
- Module 7: Advanced ⭐⭐⭐⭐⭐

**Overall Training**: ⭐⭐⭐⭐⭐

**Comments**: ________________________________

Email to: training@financialautomation.com

---

## 🎉 **CONGRATULATIONS!**

You've completed the Financial Automation Application training!

**You Can Now**:
- ✅ Set up and configure the application
- ✅ Import Trial Balance data
- ✅ Use the Selection Sheet effectively
- ✅ Generate Schedule III financials
- ✅ Export formula-linked Excel workbooks
- ✅ Manage multiple companies
- ✅ Customize master data
- ✅ Handle advanced features

**Next Steps**:
1. Practice with your own company data
2. Train your team using these materials
3. Explore advanced features
4. Provide feedback for improvements

**Welcome to automated financial reporting!** 🚀

---

*Training Materials Version: 1.0*  
*Last Updated: October 20, 2025*  
*Author: Financial Automation Team*

**For support**: support@financialautomation.com  
**For updates**: Check Help → Check for Updates
