"""License model for managing user licenses"""

import secrets
from datetime import datetime, timedelta
from config.database import get_connection
from config.settings import LICENSE_TYPE_TRIAL, LICENSE_TYPE_FULL, TRIAL_PERIOD_DAYS

class License:
    """License model class"""
    
    def __init__(self, license_id=None, user_id=None, license_key=None, 
                 license_type=None, issue_date=None, expiry_date=None, is_active=True):
        self.license_id = license_id
        self.user_id = user_id
        self.license_key = license_key
        self.license_type = license_type
        self.issue_date = issue_date
        self.expiry_date = expiry_date
        self.is_active = is_active
    
    @staticmethod
    def generate_license_key():
        """Generate a random license key"""
        return secrets.token_hex(16).upper()
    
    @staticmethod
    def create_trial_license(user_id):
        """Create a trial license for a user"""
        conn = get_connection()
        cursor = conn.cursor()
        
        license_key = License.generate_license_key()
        issue_date = datetime.now().date()
        expiry_date = issue_date + timedelta(days=TRIAL_PERIOD_DAYS)
        
        cursor.execute('''
            INSERT INTO licenses (user_id, license_key, license_type, issue_date, expiry_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, license_key, LICENSE_TYPE_TRIAL, issue_date, expiry_date))
        
        license_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return license_id, license_key
    
    @staticmethod
    def create_full_license(user_id, expiry_date=None):
        """Create a full license for a user"""
        conn = get_connection()
        cursor = conn.cursor()
        
        license_key = License.generate_license_key()
        issue_date = datetime.now().date()
        
        cursor.execute('''
            INSERT INTO licenses (user_id, license_key, license_type, issue_date, expiry_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, license_key, LICENSE_TYPE_FULL, issue_date, expiry_date))
        
        license_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return license_id, license_key
    
    @staticmethod
    def validate_license(user_id):
        """Validate if user has an active license"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT license_id, license_key, license_type, issue_date, expiry_date, is_active
            FROM licenses
            WHERE user_id = ? AND is_active = 1
            ORDER BY license_id DESC
            LIMIT 1
        ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return False, "No active license found"
        
        license_type = result[2]
        expiry_date = result[4]
        
        # Check if license has expired
        if expiry_date:
            expiry = datetime.strptime(expiry_date, '%Y-%m-%d').date()
            if datetime.now().date() > expiry:
                return False, f"{license_type} license expired on {expiry_date}"
        
        # Calculate days remaining for trial
        if license_type == LICENSE_TYPE_TRIAL and expiry_date:
            expiry = datetime.strptime(expiry_date, '%Y-%m-%d').date()
            days_remaining = (expiry - datetime.now().date()).days
            return True, f"Trial license valid ({days_remaining} days remaining)"
        
        return True, f"{license_type} license active"
    
    @staticmethod
    def get_user_license(user_id):
        """Get the active license for a user"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT license_id, user_id, license_key, license_type, issue_date, expiry_date, is_active
            FROM licenses
            WHERE user_id = ? AND is_active = 1
            ORDER BY license_id DESC
            LIMIT 1
        ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return License(
                license_id=result[0],
                user_id=result[1],
                license_key=result[2],
                license_type=result[3],
                issue_date=result[4],
                expiry_date=result[5],
                is_active=result[6]
            )
        return None
    
    @staticmethod
    def activate_license_key(user_id, license_key):
        """Activate a license key for a user"""
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if license key exists and is not already activated
        cursor.execute('''
            SELECT license_id, user_id, license_type, expiry_date
            FROM licenses
            WHERE license_key = ?
        ''', (license_key,))
        
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return False, "Invalid license key"
        
        # If license already assigned to another user, reject
        if result[1] and result[1] != user_id:
            conn.close()
            return False, "License key already in use"
        
        # Update license to assign to this user
        cursor.execute('''
            UPDATE licenses
            SET user_id = ?, is_active = 1
            WHERE license_key = ?
        ''', (user_id, license_key))
        
        conn.commit()
        conn.close()
        
        return True, "License activated successfully"
