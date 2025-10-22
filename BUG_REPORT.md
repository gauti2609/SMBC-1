# Bug Report for SMBC-1 Repository

## Executive Summary
This document lists all identified bugs found in the Python code within the FinancialAutomation module. The bugs are categorized by severity and file location.

**Note:** VBA_Module1.bas was excluded from this analysis as it is a reference file, not part of the active codebase.

---

## Critical Bugs

### 1. SQL Injection Vulnerability in Trial Balance Model
**File:** `FinancialAutomation/models/trial_balance.py`  
**Lines:** 152-158  
**Severity:** CRITICAL  

**Description:**  
The `update_mapping()` method uses mixed placeholder styles in SQL query - both `?` (SQLite style) and `%s` (PostgreSQL style) which will cause a syntax error.

**Current Code:**
```python
cursor.execute('''
    UPDATE trial_balance
    SET major_head_id = ?, minor_head_id = ?, grouping_id = ?,
        type_bs_pl = %s, is_mapped = 1, updated_at = %s
    WHERE tb_id = %s
''', (major_head_id, minor_head_id, grouping_id, type_bs_pl,
      datetime.now(), tb_id))
```

**Issue:**  
- Mixed placeholder styles (`?` and `%s`) in the same query
- Will fail when executed against PostgreSQL database
- The first three placeholders use `?` while the rest use `%s`

**Impact:**  
- Application crash when trying to update trial balance mappings
- Data cannot be saved properly

---

## High Priority Bugs

### 2. Missing RETURNING Clause in INSERT Statement
**File:** `FinancialAutomation/models/trial_balance.py`  
**Lines:** 53-68  
**Severity:** HIGH  

**Description:**  
The `create()` method executes an INSERT statement but tries to fetch the inserted ID without a RETURNING clause for PostgreSQL.

**Current Code:**
```python
cursor.execute('''
    INSERT INTO trial_balance (
        company_id, ledger_name,
        opening_balance_cy, debit_cy, credit_cy, closing_balance_cy,
        opening_balance_py, debit_py, credit_py, closing_balance_py,
        type_bs_pl, major_head_id, minor_head_id, grouping_id,
        is_mapped, import_batch_id, created_at, updated_at
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
''', (company_id, ledger_name,
      opening_balance_cy, debit_cy, credit_cy, closing_balance_cy,
      opening_balance_py, debit_py, credit_py, closing_balance_py,
      type_bs_pl, major_head_id, minor_head_id, grouping_id,
      is_mapped, import_batch_id,
      datetime.now(), datetime.now()))

tb_id = cursor.fetchone()[0]  # This will fail - no RETURNING clause
```

**Issue:**  
- PostgreSQL INSERT without RETURNING clause doesn't return any rows
- `cursor.fetchone()` will fail with "no results to fetch" error
- Should add `RETURNING tb_id` to the INSERT statement

**Impact:**  
- Cannot create new trial balance entries
- Function will crash with exception

---

### 3. Connection Not Released on Error
**File:** `FinancialAutomation/models/trial_balance.py`  
**Lines:** 48-75  
**Severity:** HIGH  

**Description:**  
Multiple methods in the trial balance model don't properly release database connections on errors, leading to connection pool exhaustion.

**Current Code Pattern:**
```python
try:
    cursor.execute(...)
    conn.commit()
    conn.close()
    return tb_id

except Exception as e:
    conn.close()  # Only closes on exception
    raise e
```

**Issue:**  
- If an error occurs before the try block completes, connection might not be closed
- Connection pool can be exhausted over time
- No use of context managers or proper cleanup

**Impact:**  
- Connection pool exhaustion after repeated errors
- Application becomes unresponsive
- Database locks and performance degradation

---

## Medium Priority Bugs

### 4. Inconsistent Master Data Model Constructor
**File:** `FinancialAutomation/models/master_data.py`  
**Lines:** 88-92  
**Severity:** MEDIUM  

**Description:**  
The `get_by_name()` static method creates a MajorHead object with wrong parameter order.

**Current Code:**
```python
if result:
    return MajorHead(result[0], result[1], result[2], result[3])
return None
```

**Issue:**  
- Constructor expects: `(major_head_id, company_id, major_head_name, category, ...)`
- Result tuple contains: `(major_head_id, major_head_name, category, display_order)`
- Missing `company_id` parameter
- `display_order` passed as wrong parameter

**Impact:**  
- Runtime errors when using this method
- Data corruption if object is used

---

### 5. Deprecated Method Still Referenced
**File:** `FinancialAutomation/models/master_data.py`  
**Lines:** 52-55  
**Severity:** MEDIUM  

**Description:**  
The `get_all()` method is deprecated but returns empty list instead of raising proper deprecation warning.

**Current Code:**
```python
@staticmethod
def get_all():
    """DEPRECATED: Use get_all_by_company() instead. Kept for backward compatibility."""
    return []
```

**Issue:**  
- Method silently returns empty list which may cause bugs
- No deprecation warning to alert developers
- Should either raise DeprecationWarning or be completely removed

**Impact:**  
- Silent failures when legacy code calls this method
- Difficult to debug issues

---

## Low Priority Bugs / Code Quality Issues

### 6. Missing Input Validation in Database Initialization
**File:** `FinancialAutomation/config/database.py`  
**Lines:** 5-418  
**Severity:** LOW  

**Description:**  
The `initialize_database()` function doesn't check if tables already exist before attempting to create them.

**Issue:**  
- While using `CREATE TABLE IF NOT EXISTS` prevents errors, it doesn't validate table structure
- If schema changes are made, existing tables won't be updated
- No migration system in place

**Impact:**  
- Schema drift between environments
- Difficult to upgrade database structure

---

## Summary Statistics

- **Total Bugs Found:** 6
- **Critical:** 1
- **High Priority:** 3
- **Medium Priority:** 2
- **Low Priority:** 1

## Recommendations

### Immediate Actions Required:
1. Fix the SQL placeholder bug in `trial_balance.py` (Bug #1) - CRITICAL
2. Add RETURNING clause to INSERT statement (Bug #2)
3. Implement proper connection management with context managers (Bug #3)

### Short-term Improvements:
1. Fix constructor parameter issues in master_data.py (Bug #4)
2. Add proper deprecation warnings or remove deprecated methods (Bug #5)
3. Implement database migration system (Bug #6)

### Long-term Code Quality:
1. Add comprehensive input validation throughout
2. Implement database migrations system
3. Add unit tests to catch these types of bugs early
4. Implement proper error handling with context managers

---

## Testing Recommendations

To verify these bugs:

1. **Bug #1 (SQL Placeholder):** Try to map a trial balance entry and observe SQL error
2. **Bug #2 (INSERT RETURNING):** Try to create a new trial balance entry and observe error
3. **Bug #3 (Connection Leak):** Run stress test creating many trial balance entries and monitor connection pool
4. **Bug #4 (Constructor):** Call `MajorHead.get_by_name()` and try to use the returned object
5. **Bug #5 (Deprecated Method):** Call `MajorHead.get_all()` and verify behavior
6. **Bug #6 (Database Validation):** Modify database schema and verify migration handling

---

**Report Generated:** October 22, 2025  
**Repository:** gauti2609/SMBC-1  
**Analysis Scope:** Python files in FinancialAutomation/ directory only
