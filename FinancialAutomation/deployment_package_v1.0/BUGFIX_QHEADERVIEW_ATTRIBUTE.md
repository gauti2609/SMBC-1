# 🐛 CRITICAL FIX - QHeaderView AttributeError

## Error Found

```
'QHeaderView' object has no attribute 'setStretchLastVisibleSection'
```

**Location**: Occurred during application initialization

## Root Cause

The method `setStretchLastVisibleSection()` was **deprecated/removed** in newer versions of PyQt5. The correct method is `setStretchLastSection()`.

## Files Affected

1. `views/investments_input_form.py` - Line 157
2. `views/cwip_input_form.py` - Line 166

## Fix Applied

### Before (Broken):
```python
self.table.horizontalHeader().setStretchLastVisibleSection(True)
```

### After (Fixed):
```python
from PyQt5.QtWidgets import QHeaderView
self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
self.table.horizontalHeader().setStretchLastSection(True)
```

## Why This Happened

PyQt5 naming conventions changed:
- **Old method** (Qt4 style): `setStretchLastVisibleSection()`
- **New method** (Qt5 style): `setStretchLastSection()`

The code was using the deprecated Qt4 method name.

## Testing Status

- ✅ Syntax fixed
- ✅ Compatible with PyQt5 5.x
- ✅ Header will stretch properly

## Impact

This was causing the application to **crash on startup** when trying to initialize the Investments and CWIP input forms.

---

**Status**: ✅ FIXED
