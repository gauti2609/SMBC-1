"""
Build Script for Financial Automation Application
Creates platform-specific executables using PyInstaller
"""

import os
import sys
import platform
import shutil
from pathlib import Path

def get_platform_settings():
    """Get platform-specific build settings"""
    system = platform.system()
    
    if system == "Windows":
        return {
            'name': 'FinancialAutomation',
            'extension': '.exe',
            'icon': 'resources/icons/app_icon.ico',
            'separator': ';'
        }
    elif system == "Darwin":  # macOS
        return {
            'name': 'FinancialAutomation',
            'extension': '.app',
            'icon': 'resources/icons/app_icon.icns',
            'separator': ':'
        }
    else:  # Linux
        return {
            'name': 'FinancialAutomation',
            'extension': '',
            'icon': 'resources/icons/app_icon.png',
            'separator': ':'
        }

def create_spec_file(settings):
    """Create PyInstaller spec file"""
    
    # Determine icon path - check if it exists at build time
    icon_path = settings.get('icon', '')
    icon_line = f"icon='{icon_path}'," if icon_path and os.path.exists(icon_path) else "icon=None,"
    
    spec_content = f"""# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None

# Only include directories that exist
datas = []
for item in [('config', 'config'), ('models', 'models'), ('views', 'views'), ('controllers', 'controllers')]:
    if os.path.exists(item[0]):
        datas.append(item)

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'PyQt5',
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'PyQt5.sip',
        'openpyxl',
        'openpyxl.cell',
        'openpyxl.cell._writer',
        'psycopg2',
        'psycopg2.pool',
        'python-dotenv',
        'dotenv',
        'views',
        'views.login_window',
        'views.main_window',
        'views.company_info_tab',
        'views.trial_balance_tab',
        'views.master_data_tab',
        'views.selection_sheet_tab',
        'views.financials_tab',
        'views.input_forms_tab',
        'views.trial_balance_mapping_dialog',
        'views.ppe_input_form',
        'views.cwip_input_form',
        'views.investments_input_form',
        'models',
        'models.user',
        'models.license',
        'models.company_info',
        'models.master_data',
        'models.trial_balance',
        'models.ppe',
        'models.cwip',
        'models.inventories',
        'models.investments',
        'models.selection_sheet',
        'config',
        'config.database',
        'config.db_connection',
        'config.settings',
        'controllers',
        'controllers.auth_controller',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{settings['name']}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    {icon_line}
)
"""
    
    with open('FinancialAutomation.spec', 'w') as f:
        f.write(spec_content)
    
    print("✅ Created FinancialAutomation.spec")

def build_executable(settings):
    """Build the executable using PyInstaller"""
    
    print("\n" + "="*80)
    print(f"Building {settings['name']} for {platform.system()}")
    print("="*80 + "\n")
    
    # Create spec file
    create_spec_file(settings)
    
    # Run PyInstaller
    cmd = f"pyinstaller --clean --noconfirm FinancialAutomation.spec"
    
    print(f"\n📦 Running PyInstaller...")
    print(f"Command: {cmd}\n")
    
    result = os.system(cmd)
    
    if result == 0:
        print("\n" + "="*80)
        print("✅ BUILD SUCCESSFUL!")
        print("="*80)
        print(f"\n📂 Executable location: dist/{settings['name']}{settings['extension']}")
        print("\n📋 Next steps:")
        print("   1. Test the executable")
        print("   2. Package with USER_GUIDE.md")
        print("   3. Create installer (optional)")
        print("   4. Distribute to users")
        
        # Show size
        exe_path = Path(f"dist/{settings['name']}{settings['extension']}")
        if exe_path.exists():
            if exe_path.is_file():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"\n📊 Executable size: {size_mb:.1f} MB")
        
        return True
    else:
        print("\n" + "="*80)
        print("❌ BUILD FAILED")
        print("="*80)
        print("\nCommon issues:")
        print("   • PyInstaller not installed: pip install pyinstaller")
        print("   • Missing dependencies: pip install -r requirements.txt")
        print("   • Icon file missing: Create resources/icons/ directory")
        return False

def create_distribution_package(settings):
    """Create distribution package with executable and documentation"""
    
    try:
        dist_dir = Path('distribution')
        dist_dir.mkdir(exist_ok=True)
        
        package_name = f"FinancialAutomation_{platform.system()}"
        package_dir = dist_dir / package_name
        
        # Clean and create package directory
        if package_dir.exists():
            shutil.rmtree(package_dir)
        package_dir.mkdir()
        
        print(f"\n📦 Creating distribution package: {package_name}")
        
        # Copy executable
        exe_name = f"{settings['name']}{settings['extension']}"
        exe_src = Path('dist') / exe_name
        
        if exe_src.exists():
            if exe_src.is_dir():  # macOS .app bundle
                shutil.copytree(exe_src, package_dir / exe_name)
            else:
                shutil.copy2(exe_src, package_dir / exe_name)
            print(f"   ✅ Copied {exe_name}")
        else:
            print(f"   ⚠️  Executable not found: {exe_src}")
            print(f"   Skipping distribution package creation")
            return False
        
        # Copy documentation
        docs = [
            'USER_GUIDE.md',
            '00_START_HERE.md',
            'README.md',
        ]
        
        for doc in docs:
            if Path(doc).exists():
                shutil.copy2(doc, package_dir / doc)
                print(f"   ✅ Copied {doc}")
        
        # Create README.txt for package
        readme_content = f"""
Financial Automation Application
================================

Thank you for downloading Financial Automation Application!

QUICK START:
1. Run {exe_name}
2. Create admin user on first launch
3. Read USER_GUIDE.md for complete instructions

DOCUMENTATION:
- 00_START_HERE.md - Quick orientation guide
- USER_GUIDE.md - Complete user manual (500+ pages)
- README.md - Project overview

SYSTEM REQUIREMENTS:
- Windows 10/11 (64-bit)
- 4 GB RAM minimum
- 500 MB disk space

SUPPORT:
- Check USER_GUIDE.md FAQ section first
- Email: support@example.com

Version: 1.0.0
Date: October 19, 2025

© 2025 Financial Automation. All rights reserved.
"""
        
        with open(package_dir / 'README.txt', 'w') as f:
            f.write(readme_content)
        print("   ✅ Created README.txt")
        
        # Create ZIP archive
        print(f"\n📦 Creating ZIP archive...")
        shutil.make_archive(
            str(dist_dir / package_name),
            'zip',
            dist_dir,
            package_name
        )
        
        zip_path = dist_dir / f"{package_name}.zip"
        if zip_path.exists():
            size_mb = zip_path.stat().st_size / (1024 * 1024)
            print(f"   ✅ Created {package_name}.zip ({size_mb:.1f} MB)")
        
        print(f"\n✅ Distribution package ready: {zip_path}")
        print(f"\n📂 Package contents:")
        print(f"   • {exe_name}")
        if Path(package_dir / 'USER_GUIDE.md').exists():
            print(f"   • USER_GUIDE.md")
        if Path(package_dir / '00_START_HERE.md').exists():
            print(f"   • 00_START_HERE.md")
        if Path(package_dir / 'README.md').exists():
            print(f"   • README.md")
        print(f"   • README.txt")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error creating distribution package: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main build process"""
    
    print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                                                                                ║
║           FINANCIAL AUTOMATION APPLICATION - EXECUTABLE BUILDER                ║
║                                                                                ║
║                           Version 1.0.0                                        ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")
    
    # Get platform settings
    settings = get_platform_settings()
    
    print(f"\n🖥️  Platform: {platform.system()} ({platform.machine()})")
    print(f"🐍 Python: {sys.version.split()[0]}")
    print(f"📦 Target: {settings['name']}{settings['extension']}")
    
    # Check PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller: {PyInstaller.__version__}")
    except ImportError:
        print("\n❌ PyInstaller not found!")
        print("Install with: pip install pyinstaller")
        return False
    
    # Build executable
    if build_executable(settings):
        
        # Check if running in CI environment
        is_ci = os.environ.get('CI') == 'true' or os.environ.get('GITHUB_ACTIONS') == 'true'
        
        # Ask to create distribution package (skip in CI)
        if is_ci:
            pkg_result = create_distribution_package(settings)
            if not pkg_result:
                print("\n⚠️  Warning: Distribution package creation failed, but executable was built successfully")
        else:
            print("\n" + "="*80)
            response = input("\n📦 Create distribution package (ZIP)? [Y/n]: ").strip().lower()
            
            if response in ['', 'y', 'yes']:
                pkg_result = create_distribution_package(settings)
                if not pkg_result:
                    print("\n⚠️  Warning: Distribution package creation failed, but executable was built successfully")
        
        print("\n" + "="*80)
        print("🎉 BUILD PROCESS COMPLETE!")
        print("="*80)
        print("\n✅ Your application is ready for distribution!")
        
        return True
    
    return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
