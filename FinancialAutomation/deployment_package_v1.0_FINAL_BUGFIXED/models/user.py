"""User model for authentication and user management"""

import hashlib
import secrets
from datetime import datetime
from config.database import get_connection

class User:
    """User model class"""
    
    def __init__(self, user_id=None, username=None, email=None, full_name=None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.full_name = full_name
        self.created_at = None
        self.last_login = None
        self.is_active = True
    
    @staticmethod
    def hash_password(password):
        """Hash a password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def create_user(username, password, email, full_name):
        """Create a new user"""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            password_hash = User.hash_password(password)
            cursor.execute('''
                INSERT INTO users (username, password_hash, email, full_name)
                VALUES (%s, %s, %s, %s)
            ''', (username, password_hash, email, full_name))
            
            user_id = cursor.fetchone()[0]
            conn.commit()
            conn.close()
            
            return user_id
        except Exception as e:
            conn.close()
            raise e
    
    @staticmethod
    def authenticate(username, password):
        """Authenticate a user"""
        conn = get_connection()
        cursor = conn.cursor()
        
        password_hash = User.hash_password(password)
        cursor.execute('''
            SELECT user_id, username, email, full_name, is_active
            FROM users
            WHERE username = %s AND password_hash = %s
        ''', (username, password_hash))
        
        result = cursor.fetchone()
        conn.close()
        
        if result and result[4]:  # Check if user exists and is active
            user = User(
                user_id=result[0],
                username=result[1],
                email=result[2],
                full_name=result[3]
            )
            user.is_active = result[4]
            
            # Update last login
            User.update_last_login(user.user_id)
            
            return user
        return None
    
    @staticmethod
    def update_last_login(user_id):
        """Update the last login timestamp"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users
            SET last_login = NOW()
            WHERE user_id = %s
        ''', (user_id,))
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id, username, email, full_name, is_active
            FROM users
            WHERE user_id = %s
        ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            user = User(
                user_id=result[0],
                username=result[1],
                email=result[2],
                full_name=result[3]
            )
            user.is_active = result[4]
            return user
        return None
    
    @staticmethod
    def username_exists(username):
        """Check if username already exists"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM users WHERE username = %s', (username,))
        count = cursor.fetchone()[0]
        conn.close()
        
        return count > 0
    
    @staticmethod
    def email_exists(email):
        """Check if email already exists"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM users WHERE email = %s', (email,))
        count = cursor.fetchone()[0]
        conn.close()
        
        return count > 0
