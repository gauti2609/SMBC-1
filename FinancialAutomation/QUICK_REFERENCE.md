# 📋 Financial Automation - Quick Reference Guide

**Version**: 1.0.0 | **Date**: October 20, 2025

---

## ⚡ QUICK START (5 Minutes)

```
1. Run FinancialAutomation.exe
2. Login: admin / admin123
3. Create Company
4. Import Trial Balance (Sample_TB.xlsx)
5. Generate Statements
6. Export to Excel
```

---

## 🔑 LOGIN

| Action | Credentials |
|--------|-------------|
| **First Time** | Create admin user |
| **Default** | admin / admin123 |
| **Forgot Password** | Contact administrator |

---

## 🏢 COMPANY MANAGEMENT

### Create Company
```
Company Info tab → New Company button
Required: Entity Name, CIN, FY Dates
Optional: Logo, Address
```

### Switch Company
```
Dropdown at top: [Company Name ▼]
All data filters to selected company
```

---

## 📊 TRIAL BALANCE IMPORT

### Prepare Excel File
```
Column A: Ledger Name
Column B: Opening Balance (CY)
Column C: Debit (CY)
Column D: Credit (CY)
Column E: Closing Balance (CY)
Column F: Closing Balance (PY) [Optional]
```

### Import Steps
```
1. Trial Balance tab
2. Click "Import from Excel"
3. Select file → Import
4. Review totals (Debit should = Credit)
5. Map unmapped items (red rows)
```

### Auto-Mapping Keywords
| Keyword | Maps To |
|---------|---------|
| cash, bank | Note 13: Cash |
| receivable, debtor | Note 10: Receivables |
| payable, creditor | Note 24: Payables |
| computer, laptop | Note 1: PPE |
| inventory, stock | Note 9: Inventories |

---

## 📝 SELECTION SHEET

### Get Recommendations
```
Trial Balance tab → "Update Note Recommendations"
→ Auto-switches to Selection Sheet
```

### Review 68 Notes
| Category | Notes | Example |
|----------|-------|---------|
| A | 8 | Share Capital, Reserves |
| B | 8 | Long-term Borrowings |
| C | 11 | Trade Payables |
| D | 13 | Fixed Assets, CWIP |
| E | 14 | Inventories, Receivables |
| F | 7 | Revenue, Expenses |
| G | 7 | Contingencies, EPS |

### User Override
```
System Rec = Yes → System recommends
User Selection = Yes/No/Blank → Your choice
Final = Combined result
```

### Auto-Numbering
```
Click "Update Auto-Numbering" button
Selected notes numbered: 1, 2, 3...
Numbers appear in Balance Sheet
```

---

## 💰 GENERATE FINANCIALS

### Generate All Statements
```
Financials tab → "Generate Financial Statements"
Wait 5-10 seconds
View: BS, P&L, CF, Notes
```

### Verify Output
```
✓ Balance Sheet totals balance
✓ P&L calculations correct
✓ Cash Flow reconciles
✓ All selected notes present
✓ Note numbers sequential
```

---

## 📊 EXCEL EXPORT

### Export Process
```
Financials tab → "Export to Excel"
Choose filename and location
Wait for completion (10-20 seconds)
30 sheets created (BS + P&L + CF + Notes)
```

### Excel Features
| Feature | Description |
|---------|-------------|
| **Formulas** | BS/PL link to Notes: ='Note_1'!C10 |
| **Format** | Schedule III compliant |
| **Sheets** | 30 total (3 statements + 27 notes) |
| **Size** | ~26 KB |
| **Editable** | Yes, full Excel functionality |

### Test Formulas
```
1. Balance Sheet → Find note reference
2. Note formula bar: ='Note_1'!C10
3. Go to Note_1 sheet → Find cell C10
4. Change value → BS updates automatically
```

---

## 🏢 PPE SCHEDULE

### Add Fixed Asset
```
PPE Schedule tab → Add Item
Enter:
  - Asset Description (e.g., Computer)
  - Gross Block figures
  - Depreciation figures
Net Block = Auto-calculated
```

### Columns
| Column | Description |
|--------|-------------|
| Gross Block | Original cost |
| Additions | Purchases this year |
| Deletions | Sales/disposals |
| Depreciation | Accumulated |
| Net Block | Gross - Depreciation |

---

## 🔢 MASTER DATA

### Major Heads (12 default)
```
Note 1: Share Capital
Note 2: Reserves & Surplus
Note 3: Fixed Assets
Note 9: Inventories
Note 10: Trade Receivables
Note 13: Cash
Note 20: Borrowings
Note 24: Trade Payables
... + 4 more
```

### Edit Master Data
```
Master Data tab → Edit button
Change descriptions (not note numbers)
Save changes
```

---

## ⌨️ KEYBOARD SHORTCUTS

| Shortcut | Action |
|----------|--------|
| **Ctrl + 1 to 8** | Switch tabs |
| **Ctrl + N** | New company |
| **Ctrl + S** | Save current form |
| **Ctrl + G** | Generate statements |
| **Ctrl + E** | Export to Excel |
| **Ctrl + Q** | Quit |
| **Tab** | Next field |
| **Enter** | Save & next row |
| **Esc** | Cancel edit |

---

## 🔧 COMMON TASKS

### Task: Import Your Own TB
```
1. Prepare Excel: Columns A-F
2. Trial Balance tab → Import
3. Select file → Import
4. Review totals → Map unmapped
```

### Task: Select Notes
```
1. Import TB first
2. Trial Balance → "Update Recommendations"
3. Selection Sheet → Review green rows
4. Override as needed (User Selection)
5. "Update Auto-Numbering"
```

### Task: Generate & Export
```
1. Financials → "Generate Statements"
2. Review BS, P&L, CF
3. "Export to Excel"
4. Save file
5. Open in Excel
```

### Task: Add Company
```
1. Company Info → New Company
2. Fill details (Name, CIN, FY)
3. Save
4. Use dropdown to switch
```

### Task: Backup Data
```
1. File menu → Backup Database
2. Choose location
3. Save as: backup_YYYYMMDD.db
4. Keep in safe location
```

---

## 🆘 TROUBLESHOOTING

### Issue: Can't Login
```
Solution:
1. Verify credentials (case-sensitive)
2. Check Caps Lock
3. Reset password (contact admin)
4. Reinstall if needed
```

### Issue: Import Fails
```
Solution:
1. Check Excel format (A-F columns)
2. No formulas in cells
3. No merged cells
4. Save as .xlsx not .xls
5. Close Excel before import
```

### Issue: TB Doesn't Balance
```
Solution:
1. Check totals in Excel first
2. Verify all rows imported
3. Look for missing entries
4. Check decimal places
5. Re-import if needed
```

### Issue: Missing Notes
```
Solution:
1. Selection Sheet → Verify "Final" = Yes
2. "Update Auto-Numbering"
3. Regenerate statements
4. Check Selection Sheet settings
```

### Issue: Excel Formulas Broken
```
Solution:
1. Don't rename sheets
2. Don't delete note sheets
3. Re-export from application
4. Use original export as backup
```

### Issue: Slow Performance
```
Solution:
1. Close other programs
2. Backup & compact database
3. Clear old companies (if many)
4. Restart application
5. Check system resources
```

---

## 💡 TIPS & TRICKS

### Tip 1: Use Sample Data First
```
Practice with Sample_TB.xlsx before real data
Learn features risk-free
Understand workflow
```

### Tip 2: Backup Before Major Changes
```
File → Backup before:
  - Importing large TB
  - Regenerating statements
  - Changing master data
```

### Tip 3: Keep Original Excel Export
```
Export → Save as "Original_Export.xlsx"
Make edits in copy: "Working_Copy.xlsx"
Always have clean version to reference
```

### Tip 4: Use Unmapped Export
```
After TB import:
Export unmapped → Review offline
Map in bulk → Reimport if needed
```

### Tip 5: Name Files Descriptively
```
Good: ABC_Mfg_Financials_31Mar2025.xlsx
Bad: Export1.xlsx

Include: Company name, Type, Date
```

### Tip 6: Verify Before Export
```
Check before exporting:
✓ TB balanced
✓ Selections finalized
✓ Auto-numbering updated
✓ Statements generated
✓ All notes present
```

---

## 📊 SCHEDULE III COMPLIANCE

### Required Sections
```
✓ Balance Sheet (Vertical format)
✓ Profit & Loss Statement
✓ Cash Flow Statement (Indirect method)
✓ Notes to Accounts (1-27 as applicable)
✓ Comparative figures (CY vs PY)
```

### Ageing Requirements (2021 Amendment)
```
Trade Receivables (Note 10):
  ✓ 5-bucket ageing (0-6m, 6-12m, 1-2y, 2-3y, >3y)
  ✓ Good vs Doubtful classification
  ✓ Allowance for bad debts

Trade Payables (Note 24):
  ✓ MSME vs Others split
  ✓ Ageing schedule
  ✓ Disclosure requirements
```

---

## 📁 FILE LOCATIONS

### Windows
```
Application: C:\FinancialAutomation\FinancialAutomation.exe
Database: C:\FinancialAutomation\financial_automation.db
Backups: C:\FinancialAutomation\backups\
Exports: Documents\Financial_Exports\
```

### Database Files
```
Main: financial_automation.db (100-500 KB typical)
Backup: backup_YYYYMMDD.db
Temp: financial_automation.db-journal (auto-deleted)
```

---

## 🔢 UNITS & FORMATS

### Units of Measurement
```
Lakhs: 1,00,000 (default)
Crores: 1,00,00,000
Thousands: 1,000
```

### Date Formats
```
DD-MMM-YYYY: 31-Mar-2025 (default)
DD/MM/YYYY: 31/03/2025
YYYY-MM-DD: 2025-03-31
```

### Number Formats
```
Decimals: 2 places (100.00)
Thousands separator: Comma (1,00,000)
Negative: Brackets (100.00)
```

---

## 📞 SUPPORT

### Getting Help
```
1. Check FAQ.md first
2. Review USER_GUIDE.md
3. Watch video tutorials
4. Email: support@financialautomation.com
5. Forum: forum.financialautomation.com
```

### Reporting Bugs
```
Include:
- Version (1.0.0)
- OS (Windows 10/11)
- Error message (screenshot)
- Steps to reproduce
- Expected vs actual behavior
```

---

## 🔄 UPDATES

### Check for Updates
```
Help menu → Check for Updates
Download new version
Backup database first
Install to new folder
Copy database from old folder
```

### Version History
```
Current: v1.0.0 (October 2025)
Next: v1.0.1 (Bug fixes)
Future: v1.1 (Detailed ageing)
```

---

## ✅ DAILY WORKFLOW CHECKLIST

### Morning Setup
- [ ] Open application
- [ ] Login
- [ ] Select company
- [ ] Backup database

### Data Entry
- [ ] Import/update Trial Balance
- [ ] Map unmapped items
- [ ] Verify TB balances
- [ ] Update note recommendations

### Statement Generation
- [ ] Review Selection Sheet
- [ ] Update auto-numbering
- [ ] Generate financial statements
- [ ] Verify all statements
- [ ] Check totals

### Export & Distribute
- [ ] Export to Excel
- [ ] Verify formulas work
- [ ] Save with descriptive name
- [ ] Share with stakeholders
- [ ] Backup final version

---

## 🎯 SUCCESS METRICS

### Quality Checks
```
✓ TB Balanced: Debit = Credit
✓ BS Balanced: Assets = Liabilities
✓ Notes Sequential: 1, 2, 3... (no gaps)
✓ All Required Notes Present
✓ Comparative Figures Shown (CY/PY)
✓ Ageing Schedules Included
✓ Excel Formulas Working
✓ Schedule III Format Correct
```

### Time Benchmarks
```
Setup: < 5 minutes
TB Import (500 entries): < 2 minutes
Selection Sheet: < 5 minutes
Generate Statements: < 30 seconds
Excel Export: < 30 seconds
Total Workflow: < 15 minutes
```

---

## 🔐 SECURITY BEST PRACTICES

### Data Protection
```
✓ Use strong passwords (8+ chars)
✓ Backup daily
✓ Keep backups offsite (cloud/USB)
✓ Don't share login credentials
✓ Close application when not in use
```

### File Security
```
✓ Database stays on your computer (local)
✓ No cloud sync (unless you configure)
✓ Excel exports can be encrypted
✓ Set file permissions on exports
✓ Delete old/unnecessary exports
```

---

## 📈 SYSTEM LIMITS

| Item | Limit | Notes |
|------|-------|-------|
| Companies | Unlimited | Performance may vary |
| TB Entries | 10,000+ | Tested up to 500 |
| Notes | 68 | Predefined |
| Users | Unlimited | Admin creates |
| File Size (DB) | < 100 MB | Typical |
| Excel Sheets | 30 | BS + PL + CF + Notes |

---

**Print this page for your desk reference!**

*Quick Reference v1.0 | October 20, 2025*  
*Financial Automation Team*
