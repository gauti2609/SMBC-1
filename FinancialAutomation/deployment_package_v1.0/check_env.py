"""
Environment Configuration Checker
Helps diagnose .env file issues
"""
import os
from pathlib import Path

print("=" * 80)
print("ENVIRONMENT CONFIGURATION CHECKER")
print("=" * 80)

# Check current directory
print(f"\n1. Current Directory: {os.getcwd()}")

# Check if .env file exists
env_file = Path('.env')
print(f"\n2. .env File Check:")
print(f"   Path: {env_file.absolute()}")
print(f"   Exists: {env_file.exists()}")

if env_file.exists():
    print(f"   Size: {env_file.stat().st_size} bytes")
    print(f"\n3. .env File Contents:")
    print("   " + "-" * 76)
    with open('.env', 'r') as f:
        for i, line in enumerate(f, 1):
            # Mask password
            if 'PASSWORD' in line.upper() and '=' in line:
                key, value = line.split('=', 1)
                print(f"   {i:2}. {key}=***HIDDEN***")
            else:
                print(f"   {i:2}. {line.rstrip()}")
    print("   " + "-" * 76)
else:
    print("   ❌ .env file NOT FOUND!")
    print("\n   Expected location: " + str(env_file.absolute()))
    print("\n   SOLUTION: Create .env file with this content:")
    print("   " + "-" * 76)
    print("""
# Database Configuration
DB_TYPE=postgresql

# PostgreSQL Settings
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=financial_automation
POSTGRES_USER=fin_app_user
POSTGRES_PASSWORD=FinApp@2025

# Connection Pool Settings
POSTGRES_MIN_CONN=2
POSTGRES_MAX_CONN=10
""")
    print("   " + "-" * 76)

# Check environment variables
print(f"\n4. Environment Variables (from settings.py):")
try:
    from config import settings
    print(f"   DB_TYPE: {settings.DB_TYPE}")
    print(f"   POSTGRES_HOST: {settings.POSTGRES_HOST}")
    print(f"   POSTGRES_PORT: {settings.POSTGRES_PORT}")
    print(f"   POSTGRES_DB: {settings.POSTGRES_DB}")
    print(f"   POSTGRES_USER: {settings.POSTGRES_USER}")
    print(f"   POSTGRES_PASSWORD: {'***' + settings.POSTGRES_PASSWORD[-4:] if settings.POSTGRES_PASSWORD else 'NOT SET'}")
except Exception as e:
    print(f"   ❌ Error loading settings: {e}")

print("\n" + "=" * 80)
print("DIAGNOSIS COMPLETE")
print("=" * 80)
