"""Configuration settings for the Financial Automation application"""

import os
try:
    from dotenv import load_dotenv
    # Load environment variables from .env file if available
    load_dotenv()
except Exception:
    # dotenv is optional in the development environment
    load_dotenv = None

# Application Settings
APP_NAME = "Financial Automation"
APP_VERSION = "1.0.0"
COMPANY_NAME = "SMBC"

# Database Settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database Type: 'sqlite' for local/development, 'postgresql' for network/production
DB_TYPE = os.getenv('DB_TYPE', 'postgresql').lower()  # Changed default to postgresql

# SQLite Configuration (Local/Development)
DB_NAME = "financial_automation.db"

# Use AppData folder for SQLite database to ensure persistence across sessions
# This is critical for .exe builds where the app folder might be read-only
if os.name == 'nt':  # Windows
    APP_DATA_DIR = os.path.join(os.getenv('APPDATA'), 'FinancialAutomation')
else:  # Linux/Mac
    APP_DATA_DIR = os.path.join(os.path.expanduser('~'), '.financialautomation')

# Create directory if it doesn't exist (for SQLite)
if DB_TYPE == 'sqlite' and not os.path.exists(APP_DATA_DIR):
    os.makedirs(APP_DATA_DIR)

DB_PATH = os.path.join(APP_DATA_DIR, DB_NAME) if DB_TYPE == 'sqlite' else None

# PostgreSQL Configuration (Network/Production)
# Support both DB_* and POSTGRES_* environment variable naming
POSTGRES_CONFIG = {
    'host': os.getenv('POSTGRES_HOST') or os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('POSTGRES_PORT') or os.getenv('DB_PORT', '5432')),
    'database': os.getenv('POSTGRES_DB') or os.getenv('POSTGRES_DATABASE') or os.getenv('DB_NAME', 'financial_automation'),
    'user': os.getenv('POSTGRES_USER') or os.getenv('DB_USER', 'app_user'),
    'password': os.getenv('POSTGRES_PASSWORD') or os.getenv('DB_PASSWORD', ''),
    'sslmode': os.getenv('DB_SSLMODE', 'prefer'),  # prefer, require, disable
    'connect_timeout': int(os.getenv('DB_TIMEOUT', '10'))
}

# Connection Pool Settings - Support both naming conventions
POOL_MIN_CONN = int(os.getenv('POSTGRES_MIN_CONN') or os.getenv('POOL_MIN_CONN', '1'))
POOL_MAX_CONN = int(os.getenv('POSTGRES_MAX_CONN') or os.getenv('POOL_MAX_CONN', '20'))

# License Settings
LICENSE_FILE = "licenses.db"
LICENSE_PATH = os.path.join(BASE_DIR, LICENSE_FILE)

# License Server (for network deployment)
LICENSE_SERVER_URL = os.getenv('LICENSE_SERVER', None)  # e.g., https://192.168.1.100:8443
LICENSE_VALIDATION_TIMEOUT = int(os.getenv('LICENSE_TIMEOUT', '5'))  # seconds
LICENSE_OFFLINE_GRACE_DAYS = int(os.getenv('LICENSE_GRACE_DAYS', '7'))  # days

# Default Formatting
DEFAULT_FONT = "Bookman Old Style"
DEFAULT_FONT_SIZE = 11
DEFAULT_CURRENCY = "INR"
DEFAULT_UNITS = "Millions"
NUMBER_FORMAT = "Accounting"
NEGATIVE_FORMAT = "Brackets"

# Date Format
DATE_FORMAT = "yyyy-MM-dd"
DISPLAY_DATE_FORMAT = "dd-MMM-yyyy"

# Accounting Standards
AS_DIVISION = "Division I"  # Not Ind AS

# Trial Balance Columns (for validation)
TB_REQUIRED_COLUMNS = [
    "Ledger Name",
    "Opening Balance (CY)",
    "Debit (CY)",
    "Credit (CY)",
    "Closing Balance (CY)",
    "Closing Balance (PY)",
    "Type (BS/PL)",
    "Major Head",
    "Minor Head",
    "Grouping"
]

# Cash Flow Method
CASH_FLOW_METHOD = "Indirect"

# Aging Buckets (in days)
AGING_BUCKETS = [
    ("< 6 Months", 0, 182),
    ("6 Months - 1 Year", 182, 365),
    ("1-2 Years", 365, 730),
    ("2-3 Years", 730, 1095),
    ("> 3 Years", 1095, 999999)
]

# Ratio Variance Threshold
RATIO_VARIANCE_THRESHOLD = 0.25  # 25%

# License Types
LICENSE_TYPE_TRIAL = "Trial"
LICENSE_TYPE_FULL = "Full"
TRIAL_PERIOD_DAYS = 30

# Export Formats
EXPORT_FORMAT_EXCEL = "Excel (.xlsx)"
EXPORT_FORMAT_PDF = "PDF (.pdf)"

# UI Theme
THEME_COLOR_PRIMARY = "#2c3e50"
THEME_COLOR_SECONDARY = "#34495e"
THEME_COLOR_ACCENT = "#3498db"
THEME_COLOR_SUCCESS = "#27ae60"
THEME_COLOR_WARNING = "#f39c12"
THEME_COLOR_DANGER = "#e74c3c"
