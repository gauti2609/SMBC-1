#!/bin/bash
#
# Quick Build Script for Financial Automation Application
# Creates Windows/macOS/Linux executable using PyInstaller
#

echo "════════════════════════════════════════════════════════════════"
echo "   Financial Automation - Quick Build Script"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Check if PyInstaller is installed
if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo "❌ PyInstaller not found!"
    echo "Installing PyInstaller..."
    pip install pyinstaller
fi

echo "✅ PyInstaller found"
echo ""

# Determine platform
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    PLATFORM="Linux"
    ICON="resources/icons/app_icon.png"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    PLATFORM="macOS"
    ICON="resources/icons/app_icon.icns"
else
    PLATFORM="Windows"
    ICON="resources/icons/app_icon.ico"
fi

echo "🖥️  Platform: $PLATFORM"
echo "📦 Building executable..."
echo ""

# Build with PyInstaller
pyinstaller \
    --name="FinancialAutomation" \
    --onefile \
    --windowed \
    --add-data="config:config" \
    --add-data="models:models" \
    --add-data="views:views" \
    --add-data="controllers:controllers" \
    --add-data="utils:utils" \
    --hidden-import=PyQt5 \
    --hidden-import=openpyxl \
    --hidden-import=bcrypt \
    --hidden-import=sqlite3 \
    --clean \
    --noconfirm \
    main.py

if [ $? -eq 0 ]; then
    echo ""
    echo "════════════════════════════════════════════════════════════════"
    echo "✅ BUILD SUCCESSFUL!"
    echo "════════════════════════════════════════════════════════════════"
    echo ""
    echo "📂 Executable location: dist/FinancialAutomation"
    echo ""
    
    # Show file size
    if [ -f "dist/FinancialAutomation" ]; then
        SIZE=$(du -h "dist/FinancialAutomation" | cut -f1)
        echo "📊 Size: $SIZE"
    fi
    
    echo ""
    echo "📋 Next steps:"
    echo "   1. Test: ./dist/FinancialAutomation"
    echo "   2. Package with documentation"
    echo "   3. Distribute to users"
    echo ""
else
    echo ""
    echo "════════════════════════════════════════════════════════════════"
    echo "❌ BUILD FAILED"
    echo "════════════════════════════════════════════════════════════════"
    echo ""
    echo "Check the error messages above"
    exit 1
fi
