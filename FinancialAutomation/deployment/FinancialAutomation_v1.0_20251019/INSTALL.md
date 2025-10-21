# Financial Automation v1.0 - Installation Guide

## 📋 System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11 (64-bit), macOS 10.14+, or Linux
- **RAM**: 4 GB
- **Disk Space**: 500 MB
- **Python**: 3.8 or higher (if running from source)

### Recommended Requirements
- **Operating System**: Windows 11 (64-bit)
- **RAM**: 8 GB or more
- **Disk Space**: 1 GB
- **Python**: 3.10 or higher
- **Display**: 1920x1080 or higher resolution

---

## 🚀 Installation Options

### Option 1: Executable (Recommended for End Users)

**Windows Users:**
1. Extract the deployment package
2. Navigate to the `Application` folder
3. Double-click `FinancialAutomation.exe`
4. The application will launch automatically

**First Launch:**
- The application creates a local database (`financial_automation.db`)
- Default login credentials:
  - Username: `admin`
  - Password: `admin123`
- ⚠️ **Change the default password immediately after first login**

---

### Option 2: Python Source (For Developers)

**Step 1: Install Python**
- Download Python 3.10+ from python.org
- Ensure "Add Python to PATH" is checked during installation

**Step 2: Install Dependencies**
```bash
cd Application
pip install -r requirements.txt
```

**Step 3: Configure Environment**
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings (optional)
nano .env
```

**Step 4: Initialize Database**
```bash
python demo_db_setup_simple.py
```

**Step 5: Run Application**
```bash
python main.py
```

---

## 📊 Quick Start Guide

### 1. First Login
- Launch the application
- Login with `admin` / `admin123`
- Change password in User Settings

### 2. Create Company
- Click "Company Info" tab
- Click "Add New Company"
- Fill in company details:
  - Entity Name
  - CIN number
  - Financial Year dates
  - Currency and units
- Click "Save"

### 3. Import Trial Balance
- Click "Trial Balance" tab
- Click "Import TB"
- Select your Excel/CSV file
- Review imported data
- Map any unmapped accounts

### 4. Configure Selection Sheet
- Click "Update Note Recommendations"
- Review system recommendations
- Override selections as needed
- Click "Update Auto-Numbering"

### 5. Enter Additional Data
- Navigate to "Input Forms" tab
- Enter PPE, CWIP, Investments data
- Save each schedule

### 6. Generate Statements
- Click "Financial Statements" tab
- Click "Generate Statements"
- Review Balance Sheet, P&L, Cash Flow

### 7. Export to Excel
- Click "Export to Excel"
- Choose save location
- Open the 30-sheet workbook

---

## 🗂️ Package Contents

```
FinancialAutomation_v1.0_YYYYMMDD/
├── Application/
│   ├── main.py
│   ├── requirements.txt
│   ├── config/
│   ├── models/
│   ├── views/
│   ├── controllers/
│   ├── utils/
│   └── resources/
├── Documentation/
│   ├── README.md
│   ├── USER_GUIDE.md
│   ├── RELEASE_NOTES_v1.0.md
│   ├── INTEGRATION_TEST_REPORT.md
│   ├── SELECTION_SHEET_IMPLEMENTATION.md
│   ├── MVP_COMPLETION_SUMMARY.md
│   ├── VIDEO_WALKTHROUGH_SCRIPT.md
│   └── DEPLOYMENT_GUIDE.md
├── SampleData/
│   └── Sample TB.xlsx
├── Demos/
│   ├── demo_db_setup_simple.py
│   ├── demo_complete_workflow.py
│   └── test_integration_complete.py
├── Training/
│   ├── USER_TRAINING_GUIDE.md
│   └── QUICK_REFERENCE.pdf
└── INSTALL.md (this file)
```

---

## 🔧 Troubleshooting

### Issue: Application won't start
**Solution:**
- Ensure Python 3.8+ is installed
- Run `pip install -r requirements.txt`
- Check for error messages in console

### Issue: Database error on startup
**Solution:**
- Delete `financial_automation.db` if corrupted
- Restart application (database will recreate)
- Run `python demo_db_setup_simple.py`

### Issue: Import TB fails
**Solution:**
- Ensure Excel file has headers: Ledger, Opening Balance, Debit, Credit, Closing Balance
- Check for formula errors in Excel (convert formulas to values)
- Try CSV format instead

### Issue: Excel export fails
**Solution:**
- Ensure write permissions in save directory
- Close any open Excel files with same name
- Check disk space

---

## 📞 Support

### Documentation
- **User Guide**: See `Documentation/USER_GUIDE.md`
- **Video Tutorial**: See `Documentation/VIDEO_WALKTHROUGH_SCRIPT.md`
- **FAQ**: See USER_GUIDE.md Section 10

### Contact
- 📧 Email: support@yourcompany.com
- 🌐 Website: www.yourcompany.com
- 📱 Phone: +91-XXXXX-XXXXX

### Updates
- Check website for latest version
- Subscribe to release notifications
- Join user community forum

---

## 📄 License

Copyright © 2025 Financial Automation.  
All rights reserved.

This software is licensed for use by authorized users only.  
See LICENSE.txt for complete terms and conditions.

---

## ✅ Installation Checklist

- [ ] System requirements verified
- [ ] Python installed (if using source)
- [ ] Dependencies installed
- [ ] Application launched successfully
- [ ] Default password changed
- [ ] First company created
- [ ] Sample TB imported
- [ ] Documentation reviewed
- [ ] User training completed

---

**Installation Guide Version**: 1.0  
**Last Updated**: October 19, 2025  
**For Application Version**: 1.0.0
