# Financial Automation Application - Video Walkthrough Script

**Duration**: 10-12 minutes  
**Target Audience**: Accountants, Finance Professionals, CFOs  
**Format**: Screen recording with voiceover

---

## 📋 **VIDEO STRUCTURE**

### **INTRO (0:00 - 0:30)**

**[Screen: Application logo/splash screen]**

**Voiceover:**
> "Welcome to the Financial Automation Application - your complete solution for generating Schedule III compliant financial statements for Indian companies. In this walkthrough, we'll show you how to go from a Trial Balance spreadsheet to professionally formatted, audit-ready financial statements in minutes."

**[Show title card]:**
- Financial Automation v1.0
- Schedule III Compliance Made Easy
- www.yourcompany.com

---

### **PART 1: INSTALLATION & SETUP (0:30 - 2:00)**

**[Screen: File explorer showing installation files]**

**Voiceover:**
> "Let's start with installation. The application comes as a simple executable - no complex setup required."

**Demo Steps:**
1. Show the distribution folder
   - FinancialAutomation.exe
   - README.txt
   - USER_GUIDE.md
   
2. Double-click the executable
   
**Voiceover:**
> "On first launch, the application automatically creates a local database and sets up all required tables. This takes just a few seconds."

**[Screen: Login window appears]**

**Voiceover:**
> "You'll see the login screen. For first-time setup, use the default credentials."

**Demo Steps:**
3. Enter credentials:
   - Username: admin
   - Password: admin123
   
4. Click "Login"

**[Screen: Main dashboard loads]**

**Voiceover:**
> "And we're in! The application opens to the main dashboard. Notice the clean, intuitive interface with all major functions accessible from the left sidebar."

---

### **PART 2: COMPANY SETUP (2:00 - 3:30)**

**[Screen: Company Info tab]**

**Voiceover:**
> "Let's set up a company. Click on 'Company Info' in the sidebar."

**Demo Steps:**
1. Click "Company Info" tab
2. Click "Add New Company"
3. Fill in details:
   - **Entity Name**: Demo Manufacturing Ltd
   - **CIN**: L12345KA2020PLC123456
   - **Registered Address**: 123 Industrial Area, Bangalore - 560001
   - **Financial Year Start**: 2024-04-01
   - **Financial Year End**: 2025-03-31
   - **Currency**: INR
   - **Unit of Measurement**: Lakhs

**Voiceover:**
> "Enter your company details. The CIN number, financial year dates, and unit of measurement are particularly important as they appear throughout your financial statements."

**Demo Steps:**
4. Click "Save"

**[Screen: Success message]**

**Voiceover:**
> "Perfect! Your company is now configured. The application automatically initializes the master data - that's your chart of accounts with all Schedule III major and minor heads."

---

### **PART 3: TRIAL BALANCE IMPORT (3:30 - 5:30)**

**[Screen: Trial Balance tab]**

**Voiceover:**
> "Now for the magic - importing your Trial Balance. This is where automation really shines."

**Demo Steps:**
1. Click "Trial Balance" tab
2. Click "Import TB"
3. Select file: "Sample TB.xlsx"

**[Screen: Show Excel file preview]**

**Voiceover:**
> "Your Trial Balance can be in Excel or CSV format. Our sample file has 271 entries with opening balances, debits, credits, and closing balances for both current and prior year."

**Demo Steps:**
4. Click "Import"
5. Show import progress

**[Screen: Import complete dialog showing "271 entries imported"]**

**Voiceover:**
> "Import complete! All 271 accounts are now in the system. Notice the application has automatically attempted to map accounts to major heads based on keywords."

**[Screen: Trial Balance table view]**

**Demo Steps:**
6. Scroll through entries
7. Show the "Mapping Status" summary:
   - Total: 271
   - Mapped: 245 (90%)
   - Unmapped: 26 (10%)

**Voiceover:**
> "The intelligent mapping engine has already classified 90% of your accounts. For any unmapped items, you can manually assign them using the dropdown in each row."

**Demo Steps:**
8. Click on an unmapped entry
9. Show dropdown with major heads
10. Select "Trade Receivables" for an accounts receivable entry
11. Click "Save Mapping"

**Voiceover:**
> "Quick and intuitive. Once all accounts are mapped, we're ready for the next step."

---

### **PART 4: SELECTION SHEET (5:30 - 7:00)**

**[Screen: Trial Balance tab]**

**Voiceover:**
> "Here's a unique feature - the Selection Sheet. Click this green button."

**Demo Steps:**
1. Click "Update Note Recommendations"

**[Screen: Processing animation]**

**Voiceover:**
> "The application analyzes your Trial Balance and intelligently recommends which Schedule III notes are relevant for your company."

**[Screen: Confirmation dialog: "System has recommended 28 notes based on your Trial Balance data"]**

**Demo Steps:**
2. Click "OK"

**[Screen: Selection Sheet tab opens automatically]**

**Voiceover:**
> "We're automatically switched to the Selection Sheet. This shows all 68 available Schedule III notes across seven categories."

**[Screen: Selection Sheet table]**

**Demo Steps:**
3. Scroll through the table showing:
   - Note Reference (A.1, A.2, B.1, etc.)
   - Description
   - Linked Major Head
   - System Recommendation (highlighted in green)
   - User Selection dropdown
   - Final Selection
   - Auto Number

**Voiceover:**
> "Green rows are system recommendations based on your data. You have full control - use the User Selection dropdown to override any recommendation."

**Demo Steps:**
4. Show a few notes:
   - A.1 Corporate Information - Recommended
   - B.1 Property, Plant & Equipment - Recommended
   - B.10 Trade Receivables - Recommended
   - B.24 Trade Payables - Recommended

5. Override one recommendation:
   - Click dropdown on a "No" recommendation
   - Change to "Yes"

**Voiceover:**
> "Maybe you want to include additional notes. Just change the selection to Yes."

**Demo Steps:**
6. Click "Update Auto-Numbering"

**[Screen: Auto numbers populate in last column: 1, 2, 3, 4...]**

**Voiceover:**
> "The auto-numbering feature sequences your selected notes. These numbers will appear in your final financial statements, keeping everything organized and cross-referenced."

---

### **PART 5: ADDITIONAL DATA ENTRY (7:00 - 8:00)**

**[Screen: Input Forms tab]**

**Voiceover:**
> "For detailed schedules, you'll need to enter additional data. Let's look at the PPE schedule."

**Demo Steps:**
1. Click "Input Forms" tab
2. Select "PPE (Property, Plant & Equipment)"

**[Screen: PPE data entry form]**

**Demo Steps:**
3. Click "Add New Asset"
4. Fill in sample data:
   - **Asset Name**: Computer Systems
   - **Gross Block Opening**: 50.00 lakhs
   - **Additions**: 10.00 lakhs
   - **Disposals**: 5.00 lakhs
   - **Accumulated Depreciation Opening**: 20.00 lakhs
   - **Depreciation for the Year**: 8.00 lakhs
   - **Depreciation Rate**: 40%

5. Click "Save"

**Voiceover:**
> "Similar forms are available for CWIP, Investments, Inventories, and other detailed schedules. The application automatically calculates closing balances and prepares the complete Schedule III format."

---

### **PART 6: GENERATING FINANCIALS (8:00 - 9:30)**

**[Screen: Financial Statements tab]**

**Voiceover:**
> "Now for the moment of truth - generating your financial statements."

**Demo Steps:**
1. Click "Financial Statements" tab
2. Click "Generate Statements"

**[Screen: Processing animation: "Generating Balance Sheet, P&L, Cash Flow, and all Notes..."]**

**[Screen: Generated statements display]**

**Voiceover:**
> "In seconds, you have complete financial statements!"

**Demo Steps:**
3. Show Balance Sheet:
   - Schedule III format
   - Current Year and Prior Year columns
   - Note references linked

4. Scroll to show sections:
   - ASSETS section with all major heads
   - EQUITY section
   - LIABILITIES section

5. Click on a note reference (e.g., "Note 1")

**[Screen: Note 1 detail view]**

**Demo Steps:**
6. Show detailed note breakdown

**Voiceover:**
> "Each note is fully populated with data from your Trial Balance and input forms. Notice the statutory breakdowns - for example, Trade Receivables shows the required ageing schedule and classification."

**Demo Steps:**
7. Navigate back
8. Show Profit & Loss Statement
9. Show Cash Flow Statement (Indirect Method)

**Voiceover:**
> "The Cash Flow Statement is automatically prepared using the indirect method, starting from profit before tax and adjusting for non-cash items and working capital changes."

---

### **PART 7: EXCEL EXPORT (9:30 - 10:30)**

**[Screen: Financial Statements tab]**

**Voiceover:**
> "Finally, let's export to Excel - this is where you'll really appreciate the power of this application."

**Demo Steps:**
1. Click "Export to Excel"
2. Choose save location
3. Enter filename: "Demo_Manufacturing_Financials_FY2024-25.xlsx"
4. Click "Save"

**[Screen: Export progress: "Creating 30-sheet workbook..."]**

**[Screen: Success message: "Export complete! File saved successfully."]**

**Demo Steps:**
5. Open the Excel file

**[Screen: Excel opens showing 30 sheets]**

**Voiceover:**
> "Look at this - a professional 30-sheet workbook with your complete financials."

**Demo Steps:**
6. Show sheet tabs:
   - Balance Sheet
   - Profit & Loss
   - Cash Flow
   - Note_1, Note_2... through Note_27

7. Click on Balance Sheet
8. Click on a cell with a note reference (e.g., cell with PPE amount)

**[Screen: Show formula bar: =Note_1!C10]**

**Voiceover:**
> "Here's the best part - every number in your financial statements is formula-linked to the detailed notes. Change a value in a note, and your Balance Sheet updates automatically. Perfect for audit trails and what-if analysis."

**Demo Steps:**
9. Navigate to Note_1 (PPE)
10. Show the detailed schedule with all calculations
11. Return to Balance Sheet
12. Show professional formatting:
    - Schedule III compliant headers
    - Color-coded sections
    - Proper borders and alignment
    - Company logo placeholder

**Voiceover:**
> "The formatting is Schedule III compliant, professional, and ready for board presentations or audit submissions."

---

### **PART 8: FEATURES SUMMARY (10:30 - 11:30)**

**[Screen: Feature highlights with icons/animations]**

**Voiceover:**
> "Let's recap what makes Financial Automation special:"

**[Show bullet points appearing one by one]**

✅ **Automated Trial Balance Import**
- Support for Excel and CSV
- Intelligent auto-mapping
- 90%+ accuracy out of the box

✅ **Smart Selection Sheet**
- 68 predefined Schedule III notes
- AI-powered recommendations
- Complete user control

✅ **Complete Financial Statements**
- Balance Sheet with CY/PY comparison
- Profit & Loss Statement
- Cash Flow Statement (Indirect Method)
- All 27 Notes to Accounts

✅ **Formula-Linked Excel Export**
- 30-sheet professional workbook
- Dynamic formula linking
- Audit-ready formatting
- ~26 KB file size

✅ **Time Savings**
- What used to take days now takes minutes
- Reduce errors with automation
- Focus on analysis, not formatting

**Voiceover:**
> "Whether you're a CFO, accountant, or audit firm, this application transforms your financial reporting workflow."

---

### **PART 9: ADDITIONAL FEATURES (11:30 - 12:00)**

**[Screen: Quick overview of other features]**

**Voiceover:**
> "We didn't cover everything today. The application also includes:"

**Demo Steps - Quick flythrough:**
1. Show Investments tab
2. Show CWIP tab
3. Show user management
4. Show company selection dropdown

**Voiceover:**
> "Multiple company management, detailed input forms for all schedules, user access control, and comprehensive reporting capabilities."

---

### **OUTRO (12:00 - 12:30)**

**[Screen: Summary slide]**

**Voiceover:**
> "Financial Automation v1.0 is production-ready today. With 22,000 lines of tested code, 100% Schedule III compliance, and a proven workflow, it's the complete solution for Indian financial reporting."

**[Screen: Call to action]**

**Contact Information:**
- 📧 Email: support@yourcompany.com
- 🌐 Website: www.yourcompany.com
- 📱 Phone: +91-XXXXX-XXXXX

**Voiceover:**
> "Get started today with a free trial. Thank you for watching, and happy financial reporting!"

**[Screen: Fade to logo]**

---

## 🎬 **PRODUCTION NOTES**

### Recording Settings
- **Resolution**: 1920x1080 (Full HD)
- **Frame Rate**: 30 fps
- **Audio**: 48 kHz, Stereo
- **Screen Capture**: Full application window (no desktop clutter)

### Editing Checklist
- [ ] Add intro/outro music (professional, upbeat)
- [ ] Add transitions between sections (smooth, not distracting)
- [ ] Highlight cursor movements
- [ ] Zoom in on important UI elements (buttons, dropdowns)
- [ ] Add text overlays for key points
- [ ] Include closed captions
- [ ] Add chapter markers in YouTube/Vimeo
- [ ] Color grade for consistency
- [ ] Audio normalization and noise reduction

### Video Assets Needed
- Company logo animation
- Feature icons/graphics
- Background music (royalty-free)
- Lower thirds for contact information
- End screen with links

### Distribution Channels
- YouTube (unlisted for clients)
- Vimeo (password protected)
- Company website embed
- Email campaigns
- Sales presentations

### Follow-up Videos (Suggested)
1. "Advanced Features Deep Dive" (15 min)
2. "Tips & Tricks for Power Users" (10 min)
3. "Common Questions Answered" (8 min)
4. "Version 1.1 New Features" (upcoming)

---

## 📝 **SCRIPT VARIATIONS**

### Short Version (5 minutes)
For social media and quick demos:
1. Intro (30s)
2. Import TB (1:30)
3. Selection Sheet (1:00)
4. Generate & Export (1:30)
5. Outro (30s)

### Long Version (20 minutes)
For training sessions:
- Include all sections above
- Add troubleshooting segment
- Show user management features
- Demonstrate multi-company workflow
- Include Q&A segment

---

**Script Version**: 1.0  
**Date**: October 19, 2025  
**Author**: Financial Automation Team  
**Review Status**: ✅ Ready for Production
