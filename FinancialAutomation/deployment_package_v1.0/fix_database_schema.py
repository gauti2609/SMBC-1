"""
Quick script to replace AUTOINCREMENT with database-agnostic syntax
"""
import re

# Read the file
with open('config/database.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace AUTOINCREMENT with SERIAL for PostgreSQL compatibility
# But we need to keep it conditional based on database type

# Add import for DB_TYPE at the top if not present
if 'from config.settings import DB_TYPE' not in content:
    content = content.replace(
        'from config.settings import DB_TYPE, DB_PATH',
        'from config.settings import DB_TYPE, DB_PATH, POSTGRES_HOST'
    )

# Replace INTEGER PRIMARY KEY AUTOINCREMENT with database-agnostic version
content = re.sub(
    r'(\w+_id) INTEGER PRIMARY KEY AUTOINCREMENT',
    r'\1 SERIAL PRIMARY KEY',
    content
)

# Replace TEXT with VARCHAR for better PostgreSQL compatibility
# But keep TEXT for longer fields
replacements = {
    'username TEXT': 'username VARCHAR(255)',
    'password_hash TEXT': 'password_hash VARCHAR(255)',
    'email TEXT': 'email VARCHAR(255)',
    'full_name TEXT': 'full_name VARCHAR(255)',
    'license_key TEXT': 'license_key VARCHAR(255)',
    'license_type TEXT': 'license_type VARCHAR(50)',
    'category TEXT': 'category VARCHAR(100)',
    'major_head_name TEXT': 'major_head_name VARCHAR(255)',
    'minor_head_name TEXT': 'minor_head_name VARCHAR(255)',
    'grouping_name TEXT': 'grouping_name VARCHAR(255)',
}

for old, new in replacements.items():
    content = content.replace(old, new)

# Replace BOOLEAN with BOOLEAN (same in both)
# Replace REAL with NUMERIC for better precision
content = re.sub(r'(\w+) REAL', r'\1 NUMERIC(15,2)', content)

# Replace TEXT NOT NULL with VARCHAR where appropriate
content = re.sub(
    r'account_code TEXT',
    'account_code VARCHAR(50)',
    content
)
content = re.sub(
    r'ledger_name TEXT',
    'ledger_name VARCHAR(255)',
    content
)

# Write back
with open('config/database.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Database schema updated for PostgreSQL compatibility!")
print("Changes made:")
print("  - AUTOINCREMENT → SERIAL")
print("  - REAL → NUMERIC(15,2)")
print("  - TEXT → VARCHAR (for most fields)")
