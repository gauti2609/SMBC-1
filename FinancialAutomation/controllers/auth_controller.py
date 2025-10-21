"""Authentication controller"""

from models.user import User
from models.license import License

class AuthController:
    """Controller for authentication operations"""
    
    @staticmethod
    def register_user(username, password, email, full_name, create_trial=False):
        """
        Register a new user
        
        Args:
            username: Username
            password: Password
            email: Email address
            full_name: Full name
            create_trial: Whether to create a trial license (deprecated, kept for compatibility)
        
        Returns:
            (success, message, user_id)
        """
        # Validate inputs
        if not username or len(username) < 3:
            return False, "Username must be at least 3 characters", None
        
        if not password or len(password) < 6:
            return False, "Password must be at least 6 characters", None
        
        if not email or '@' not in email:
            return False, "Invalid email address", None
        
        # Check if username exists
        if User.username_exists(username):
            return False, "Username already exists", None
        
        # Check if email exists
        if User.email_exists(email):
            return False, "Email already exists", None
        
        try:
            # Create user
            user_id = User.create_user(username, password, email, full_name)
            
            # License creation disabled for v1.0 (re-enabled in v1.1)
            # if create_trial:
            #     License.create_trial_license(user_id)
            
            return True, "User registered successfully", user_id
        except Exception as e:
            return False, f"Error during registration: {str(e)}", None
    
    @staticmethod
    def login_user(username, password):
        """
        Authenticate and login a user
        
        Args:
            username: Username
            password: Password
        
        Returns:
            (success, message, user_object)
        """
        if not username or not password:
            return False, "Username and password are required", None
        
        user = User.authenticate(username, password)
        
        if user:
            # License validation disabled for v1.0 (re-enabled in v1.1)
            # is_valid, license_msg = License.validate_license(user.user_id)
            # 
            # if not is_valid:
            #     return False, f"Login failed: {license_msg}", None
            # 
            # return True, license_msg, user
            
            return True, "Login successful", user
        else:
            return False, "Invalid username or password", None
    
    @staticmethod
    def activate_license(user_id, license_key):
        """
        Activate a license key for a user
        
        Args:
            user_id: User ID
            license_key: License key to activate
        
        Returns:
            (success, message)
        """
        return License.activate_license_key(user_id, license_key)
    
    @staticmethod
    def get_license_info(user_id):
        """
        Get license information for a user
        
        Args:
            user_id: User ID
        
        Returns:
            License object or None
        """
        return License.get_user_license(user_id)
