# Test Fixes Instructions

## Problem
The test files in your Windows directory still have old code. You need to apply these fixes.

## Option 1: Copy Fixed Files (RECOMMENDED)

Copy these 4 fixed files from this workspace to your Windows test directory:

```
Source (this workspace):
/workspaces/SMBC-1/FinancialAutomation/deployment_package_v1.0/tests/

Destination (your Windows):
C:\Financials Automation_Github\FinancialAutomation_v1.0_Complete\deployment_package_v1.0\tests\

Files to copy:
1. test_backend_database.py
2. test_gui_company_creation.py  
3. test_gui_main_window.py
4. conftest.py
```

## Option 2: Manual Edits

If you can't copy files, apply these manual edits to your Windows test files:

---

### File: `tests\conftest.py`

**Line 215** - Change:
```python
window.update_company_selection()
```
To:
```python
window.populate_company_selector()
```

---

### File: `tests\test_backend_database.py`

**Lines 30-47** - Already correct, but verify test_create_company uses:
```python
company_id = CompanyInfo.create(...)  # Not company.save()
companies = CompanyInfo.get_all_by_user(test_user.user_id)  # Not get_user_companies
```

**Lines 49-54** - Change test_get_user_companies:
```python
companies = CompanyInfo.get_all_by_user(test_user.user_id)  # Not get_user_companies
```

**Lines 56-64** - Change test_create_major_head:
```python
major_head = MajorHead(
    company_id=test_company.company_id,
    major_head_name='Current Assets',  # Not 'name'
    category='Assets'  # Not 'head_type', remove 'code'
)
```

**Lines 66-87** - Change test_create_minor_head:
```python
# Create major head first
major_head = MajorHead(
    company_id=test_company.company_id,
    major_head_name='Current Assets',  # Not 'name'
    category='Assets'  # Not 'head_type', remove 'code'
)
major_head.save()

# Create minor head
minor_head = MinorHead(
    company_id=test_company.company_id,
    major_head_id=major_head.major_head_id,
    minor_head_name='Cash and Bank',  # Not 'name'
    category='Assets'  # Not 'head_type', remove 'code'
)
```

**Lines 130-147** - Change test_trial_balance_validation:
```python
tb1 = TrialBalance(
    tb_id=None,  # ADD THIS
    company_id=test_company.company_id,
    ledger_name='Cash',
    debit_cy=100000,  # Not 'debit'
    credit_cy=0  # Not 'credit'
)
tb1.save()

tb2 = TrialBalance(
    tb_id=None,  # ADD THIS
    company_id=test_company.company_id,
    ledger_name='Capital',
    debit_cy=0,  # Not 'debit'
    credit_cy=100000  # Not 'credit'
)
```

---

### File: `tests\test_gui_company_creation.py`

**Line 159** - Change:
```python
assert hasattr(company_tab, 'cin_input'), "CIN input should exist"  # Not 'pan_input'
```

**Lines 175-183** - Change test_save_company_with_valid_data (remove pan_input, py_start/end):
```python
# Fill in required fields
company_tab.entity_name_input.setText("Test Company Ltd")
company_tab.cin_input.setText("L12345MH2020PLC123456")
# REMOVE: company_tab.pan_input.setText("ABCDE1234F")

# Set financial year dates
from PyQt5.QtCore import QDate
company_tab.fy_start_input.setDate(QDate(2024, 4, 1))
company_tab.fy_end_input.setDate(QDate(2025, 3, 31))
# REMOVE: company_tab.py_start_input.setDate(QDate(2023, 4, 1))
# REMOVE: company_tab.py_end_input.setDate(QDate(2024, 3, 31))
```

**Lines 233-240** - Change test_company_selector_updates_after_save (remove py_start/end):
```python
company_tab.fy_start_input.setDate(QDate(2024, 4, 1))
company_tab.fy_end_input.setDate(QDate(2025, 3, 31))
# REMOVE: company_tab.py_start_input.setDate(QDate(2023, 4, 1))
# REMOVE: company_tab.py_end_input.setDate(QDate(2024, 3, 31))
```

**Lines 283-290** - Change test_complete_company_creation_workflow (remove pan_input, py_start/end):
```python
company_tab.entity_name_input.setText("Complete Test Company")
company_tab.cin_input.setText("L12345KA2020PLC123456")
# REMOVE: company_tab.pan_input.setText("ABCDE1234F")

from PyQt5.QtCore import QDate
company_tab.fy_start_input.setDate(QDate(2024, 4, 1))
company_tab.fy_end_input.setDate(QDate(2025, 3, 31))
# REMOVE: company_tab.py_start_input.setDate(QDate(2023, 4, 1))
# REMOVE: company_tab.py_end_input.setDate(QDate(2024, 3, 31))
```

---

### File: `tests\test_gui_main_window.py`

**Lines 37-44** - Change test_all_tabs_exist:
```python
required_tabs = [
    "Company Information",
    "Master Data",
    "Trial Balance",
    "Input Forms",  # NOT "PPE Schedule"
    "Financial Statements"
]
```

---

## Verification

After applying fixes, search for these patterns in your test files - they should NOT exist:

❌ `get_user_companies` (should be `get_all_by_user`)
❌ `pan_input` (should be `cin_input`)
❌ `py_start_input` (should be `fy_start_input`)
❌ `py_end_input` (should be `fy_end_input`)
❌ `update_company_selection()` (should be `populate_company_selector()`)
❌ `MajorHead(..., code=..., name=..., head_type=...)` (should be `major_head_name=..., category=...`)
❌ `TrialBalance(..., debit=..., credit=...)` (should be `debit_cy=..., credit_cy=...`)
❌ `"PPE Schedule"` in tab list (should be `"Input Forms"`)

## Expected Results

After fixes: **~30-32 tests should PASS** (85-90% pass rate)
