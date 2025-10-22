# Quick Reference: All Bugs Found in SMBC-1

**Date:** October 22, 2025  
**Total Bugs:** 11  
**Status:** Analysis Complete - No Code Changes Made

---

## Critical Bugs (Fix Immediately) ⚠️

| # | File | Line | Issue | Quick Fix |
|---|------|------|-------|-----------|
| 1 | company_info.py | 227-238 | Mixed `?` and `%s` placeholders in UPDATE | Change all `?` to `%s` |
| 2 | ppe.py | 202-215 | Mixed placeholders + `NOW()` in UPDATE | Change `?` to `%s`, replace `NOW()` with `%s` + `datetime.now()` |
| 3 | cwip.py | 195-201 | Mixed `?` and `%s` placeholders in UPDATE | Change all `?` to `%s` |
| 4 | investments.py | 232-240 | Mixed placeholders + `NOW()` in UPDATE | Change `?` to `%s`, replace `NOW()` with `%s` + `datetime.now()` |

**Time to Fix:** ~20 minutes  
**Impact:** Application crashes on UPDATE operations

---

## High Priority Bugs (Fix This Week) 🔥

| # | File | Line | Issue | Quick Fix |
|---|------|------|-------|-----------|
| 5 | company_info.py | 182-194 | Missing RETURNING in INSERT | Add `RETURNING company_id` after VALUES |
| 6 | ppe.py | 151-171 | Missing RETURNING in INSERT | Add `RETURNING ppe_id` after VALUES |
| 7 | cwip.py | 154-168 | Missing RETURNING in INSERT | Add `RETURNING cwip_id` after VALUES |
| 8 | investments.py | 188-204 | Missing RETURNING in INSERT | Add `RETURNING investment_id` after VALUES |

**Time to Fix:** ~8 minutes  
**Impact:** Cannot create new records

---

## Medium Priority Bugs (Next Sprint) ⚡

| # | File | Issue | Time to Fix |
|---|------|-------|-------------|
| 9 | company_info.py | Improper connection cleanup in create() | 15 min |
| 10 | Multiple files | Inconsistent connection management | 30 min |

**Impact:** Connection pool exhaustion over time

---

## Low Priority (Long-term) 📋

| # | File | Issue | Time to Fix |
|---|------|-------|-------------|
| 11 | database.py | No migration system | 1-2 days |

**Impact:** Difficult to manage schema changes

---

## Files Requiring Fixes

### Immediate Attention Required:
- ✅ `models/company_info.py` (3 bugs: #1, #5, #9)
- ✅ `models/ppe.py` (2 bugs: #2, #6)
- ✅ `models/cwip.py` (2 bugs: #3, #7)
- ✅ `models/investments.py` (2 bugs: #4, #8)

### Later:
- ⬜ `config/database.py` (1 bug: #11)
- ⬜ Multiple model files (Bug #10)

---

## Quick Fix Examples

### Bug #1 Example (Mixed Placeholders):
**Before:**
```python
SET entity_name = ?, address = ?, cin_no = ?, rounding_level = %s
```

**After:**
```python
SET entity_name = %s, address = %s, cin_no = %s, rounding_level = %s
```

### Bug #2 Example (NOW() Function):
**Before:**
```python
SET asset_class = ?, updated_at = NOW() WHERE ppe_id = %s
```

**After:**
```python
SET asset_class = %s, updated_at = %s WHERE ppe_id = %s
# And add datetime.now() to the parameters tuple
```

### Bug #5 Example (Missing RETURNING):
**Before:**
```python
INSERT INTO company_info (...) VALUES (%s, %s, ...)
company_id = cursor.fetchone()[0]  # FAILS!
```

**After:**
```python
INSERT INTO company_info (...) VALUES (%s, %s, ...) RETURNING company_id
company_id = cursor.fetchone()[0]  # Works!
```

---

## Testing Checklist

After fixing bugs, test:
- [ ] Update company information (Bug #1)
- [ ] Update PPE entry (Bug #2)
- [ ] Update CWIP project (Bug #3)
- [ ] Update investment (Bug #4)
- [ ] Create new company (Bug #5)
- [ ] Create new PPE entry (Bug #6)
- [ ] Create new CWIP project (Bug #7)
- [ ] Create new investment (Bug #8)
- [ ] Connection cleanup under errors (Bug #9-10)

---

## Priority Order for Fixes

1. **Day 1:** Fix Bugs #1-4 (Critical - Mixed Placeholders)
2. **Day 1:** Fix Bugs #5-8 (High - Missing RETURNING)
3. **Day 2-3:** Add unit tests
4. **Week 2:** Fix Bugs #9-10 (Connection Management)
5. **Next Sprint:** Bug #11 (Migration System)

---

## Status vs Previous Reports

### Previously Identified Bugs (Now Fixed):
- ✅ Mixed placeholders in trial_balance.py
- ✅ Missing RETURNING in trial_balance.py
- ✅ Constructor issues in master_data.py
- ✅ Deprecated method warnings

### New Bugs Found (This Report):
- 🆕 4 CRITICAL bugs (mixed placeholders in other files)
- 🆕 4 HIGH bugs (missing RETURNING in other files)
- 🆕 2 MEDIUM bugs (connection management)

**Total New Bugs Discovered:** 10

---

For detailed analysis, see: `COMPREHENSIVE_BUG_REPORT.md`

**Note:** VBA_Module1.bas excluded from analysis (reference file)
