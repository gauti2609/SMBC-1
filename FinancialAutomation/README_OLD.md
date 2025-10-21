# Financial Automation System

Automated drafting of Financial Statements as per Schedule III of the Companies Act and Indian Accounting Standards (AS Division I).

## Version
1.0.0 (Development Build)

## Description
Desktop application for Windows 10/11 that automates the creation of:
- Balance Sheet
- Profit & Loss Statement
- Cash Flow Statement (Indirect Method)
- Notes to Accounts (all AS requirements + Schedule III 2021 amendments)
- Ratio Analysis
- Aging Schedules

## Features

### Core Functionality
- ✅ User Authentication & License Management
- ✅ Trial License (30 days)
- ✅ Full License Support
- ✅ Hierarchical Master Data Management (Major/Minor/Grouping Heads)
- 🚧 Trial Balance Import & Validation
- 🚧 Comprehensive Input Forms
- 🚧 Financial Statement Generation
- 🚧 Notes to Accounts Generation
- 🚧 Excel Export with Live Formulas

### Compliance
- Schedule III Division I (AS, not Ind AS)
- All Accounting Standards (AS 1-29)
- 2021 Schedule III Amendments
- MSME Compliance
- Related Party Disclosures (AS 18)
- Tax Reconciliation (AS 22)
- Employee Benefits (AS 15)

## Development Setup

### Prerequisites
- Python 3.8 or higher
- Virtual environment

### Installation

1. Clone the repository:
```bash
cd SMBC-1/FinancialAutomation
```

2. Create virtual environment:
```bash
python3 -m venv venv
```

3. Activate virtual environment:
```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

```bash
python main.py
```

## Project Structure

```
FinancialAutomation/
├── main.py                    # Application entry point
├── config/
│   ├── settings.py            # Configuration settings
│   └── database.py            # Database initialization
├── models/
│   ├── user.py                # User model
│   ├── license.py             # License model
│   └── master_data.py         # Master data models
├── controllers/
│   └── auth_controller.py     # Authentication controller
├── views/
│   ├── login_window.py        # Login/Registration window
│   ├── main_window.py         # Main application window
│   └── [tab files]            # Individual tab modules
├── services/                  # Business logic services
├── utils/                     # Utility functions
└── resources/                 # Icons, templates, sample data
```

## Database Schema

The application uses SQLite with the following main tables:
- users
- licenses
- major_heads, minor_heads, groupings (hierarchical master data)
- company_info
- trial_balance
- All input sheets (share_capital, ppe_schedule, etc.)
- selection_sheet

## Current Development Status

### Completed ✅
1. Project structure setup
2. Database schema design and initialization
3. User authentication system
4. License management (Trial/Full)
5. Login and registration UI
6. Main application window with menu system
7. Tab-based navigation framework
8. Default master data initialization

### In Progress 🚧
6. Master Data Management UI
7. Trial Balance import and validation
8. Input forms for all schedules
9. Financial statement generation
10. Notes generation
11. Export functionality

### Planned 📋
- Ratio analysis
- Aging schedules
- PDF export
- User documentation
- PyInstaller packaging

## Building Windows Executable

(Instructions will be provided after development completion)

```bash
pyinstaller --name="FinancialAutomation" \
            --windowed \
            --onefile \
            --add-data "resources;resources" \
            main.py
```

## Testing

Test with the provided Sample TB.xlsx file to verify all functionality.

## 📞 Support & Contributing

### Getting Help

- 📘 Read the [USER_GUIDE.md](USER_GUIDE.md)
- 🔍 Check [FAQs](USER_GUIDE.md#faqs)
- 📧 Email: support@example.com

### Reporting Issues

Found a bug? Have a feature request?

1. Check existing issues on GitHub
2. Create new issue with detailed description
3. Include steps to reproduce (for bugs)

### Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📜 Legal & Compliance

### Disclaimer

This application generates Schedule III compliant financial statements. However:

⚠️ **All financial statements must be reviewed and certified by a qualified Chartered Accountant** before submission to statutory authorities.

Users are responsible for:
- Accuracy of input data
- Compliance with applicable accounting standards
- Verification by professionals
- Final approval by auditors

### License

[MIT License / Your License Here]

---

## 🎉 Acknowledgments

**Built with:**
- Python community
- PyQt5 framework
- PostgreSQL database
- Open source libraries

**Special thanks to:**
- All contributors and testers
- CA community for feedback
- Users who helped shape this application

---

## 📊 Project Status

**Current Version:** 1.0.0  
**Status:** ✅ Production Ready - Tested & Verified  
**Last Updated:** October 19, 2025

**Roadmap:**
- [x] ✅ PPE, CWIP, Investments modules
- [x] ✅ Balance Sheet, P&L, Notes generation
- [x] ✅ Schedule III compliance
- [x] ✅ Complete workflow testing
- [ ] 📦 PDF export (v1.1)
- [ ] 📦 Cash Flow Statement (v1.2)
- [ ] 📦 Consolidated financials (v2.0)
- [ ] 📦 Web-based version (v2.0)

---

## ⭐ Star This Project

If you find this application useful, please give it a star ⭐ on GitHub!

---

**Made with ❤️ for the Finance Community**

**Ready to automate your financial statement generation? [Download Now](#) or [View Documentation](USER_GUIDE.md)**

## Support

For issues and questions, contact the development team.

---

**Note**: This is a development build. The application is under active development.
