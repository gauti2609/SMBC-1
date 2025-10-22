"""
Application settings and configuration - PostgreSQL only
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Application Info
APP_NAME = "Financial Automation"
APP_VERSION = "1.0.0"
ORGANIZATION = "SMBC"

# PostgreSQL Configuration (ONLY database type supported)
POSTGRES_CONFIG = {
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'port': int(os.getenv('POSTGRES_PORT', 5432)),
    'database': os.getenv('POSTGRES_DB', 'financial_automation'),
    'user': os.getenv('POSTGRES_USER', 'fin_app_user'),
    'password': os.getenv('POSTGRES_PASSWORD', '')
}

# Connection Pool Settings
POOL_MIN_CONN = int(os.getenv('POSTGRES_MIN_CONN', 2))
POOL_MAX_CONN = int(os.getenv('POSTGRES_MAX_CONN', 10))

# Default Font Settings
DEFAULT_FONT = "Bookman Old Style"
DEFAULT_FONT_SIZE = 11

# Financial Statement Settings
DEFAULT_CURRENCY = "INR"
DEFAULT_UNITS = "Millions"
DEFAULT_NUMBER_FORMAT = "Accounting"
DEFAULT_NEGATIVE_FORMAT = "Brackets"
DEFAULT_ROUNDING_LEVEL = "100000"
DEFAULT_DECIMAL_PLACES = 2

# UI Settings
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
