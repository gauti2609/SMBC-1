"""Company Information Model - CRUD operations for company details and preferences"""

from config.database import get_connection
from datetime import datetime

class CompanyInfo:
    """Company Information model"""
    
    def __init__(self, company_id=None, user_id=None, entity_name=None, address=None,
                 cin_no=None, fy_start_date=None, fy_end_date=None, currency='INR',
                 units='Millions', number_format='Accounting', negative_format='Brackets',
                 default_font='Bookman Old Style', default_font_size=11, 
                 show_zeros_as_blank=0, decimal_places=2, turnover=0, 
                 rounding_level='100000'):
        self.company_id = company_id
        self.user_id = user_id
        self.entity_name = entity_name
        self.address = address
        self.cin_no = cin_no
        self.fy_start_date = fy_start_date
        self.fy_end_date = fy_end_date
        self.currency = currency
        self.units = units
        self.number_format = number_format
        self.negative_format = negative_format
        self.default_font = default_font
        self.default_font_size = default_font_size
        self.show_zeros_as_blank = show_zeros_as_blank
        self.decimal_places = decimal_places
        self.turnover = turnover
        self.rounding_level = rounding_level
    
    @staticmethod
    def get_by_user_id(user_id):
        """Get company info for a specific user"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT company_id, user_id, entity_name, address, cin_no,
                   fy_start_date, fy_end_date, currency, units, number_format,
                   negative_format, default_font, default_font_size, 
                   show_zeros_as_blank, decimal_places, turnover, rounding_level
            FROM company_info
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT 1
        ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return CompanyInfo(
                company_id=result[0],
                user_id=result[1],
                entity_name=result[2],
                address=result[3],
                cin_no=result[4],
                fy_start_date=result[5],
                fy_end_date=result[6],
                currency=result[7],
                units=result[8],
                number_format=result[9],
                negative_format=result[10],
                default_font=result[11],
                default_font_size=result[12],
                show_zeros_as_blank=result[13],
                decimal_places=result[14] if result[14] is not None else 2,
                turnover=float(result[15]) if result[15] is not None else 0.0,
                rounding_level=result[16] if result[16] is not None else '100000'
            )
        return None
    
    @staticmethod
    def get_by_id(company_id):
        """Get company info by company ID"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT company_id, user_id, entity_name, address, cin_no,
                   fy_start_date, fy_end_date, currency, units, number_format,
                   negative_format, default_font, default_font_size, 
                   show_zeros_as_blank, decimal_places, turnover, rounding_level
            FROM company_info
            WHERE company_id = ?
        ''', (company_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return CompanyInfo(
                company_id=result[0],
                user_id=result[1],
                entity_name=result[2],
                address=result[3],
                cin_no=result[4],
                fy_start_date=result[5],
                fy_end_date=result[6],
                currency=result[7],
                units=result[8],
                number_format=result[9],
                negative_format=result[10],
                default_font=result[11],
                default_font_size=result[12],
                show_zeros_as_blank=result[13],
                decimal_places=result[14] if result[14] is not None else 2,
                turnover=float(result[15]) if result[15] is not None else 0.0,
                rounding_level=result[16] if result[16] is not None else '100000'
            )
        return None
    
    @staticmethod
    def get_all_by_user(user_id):
        """Get all companies for a specific user"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT company_id, user_id, entity_name, address, cin_no,
                   fy_start_date, fy_end_date, currency, units, number_format,
                   negative_format, default_font, default_font_size, 
                   show_zeros_as_blank, decimal_places, turnover, rounding_level
            FROM company_info
            WHERE user_id = ?
            ORDER BY entity_name
        ''', (user_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        companies = []
        for result in results:
            companies.append(CompanyInfo(
                company_id=result[0],
                user_id=result[1],
                entity_name=result[2],
                address=result[3],
                cin_no=result[4],
                fy_start_date=result[5],
                fy_end_date=result[6],
                currency=result[7],
                units=result[8],
                number_format=result[9],
                negative_format=result[10],
                default_font=result[11],
                default_font_size=result[12],
                show_zeros_as_blank=result[13],
                decimal_places=result[14] if result[14] is not None else 2,
                turnover=float(result[15]) if result[15] is not None else 0.0,
                rounding_level=result[16] if result[16] is not None else '100000'
            ))
        
        return companies
    
    @staticmethod
    def create(user_id, entity_name, fy_start_date, fy_end_date, address=None,
               cin_no=None, currency='INR', units='Millions', number_format='Accounting',
               negative_format='Brackets', default_font='Bookman Old Style', 
               default_font_size=11, show_zeros_as_blank=0, decimal_places=2,
               turnover=0, rounding_level='100000'):
        """Create new company information"""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            # Validate CIN format if provided
            if cin_no:
                if not CompanyInfo.validate_cin(cin_no):
                    raise ValueError("Invalid CIN format. Expected format: L12345AB2020PLC123456")
            
            # Validate date range
            if not CompanyInfo.validate_dates(fy_start_date, fy_end_date):
                raise ValueError("FY End Date must be after FY Start Date")
            
            # Validate rounding level based on turnover (Schedule III compliance)
            if not CompanyInfo.validate_rounding_level(turnover, rounding_level):
                raise ValueError("Invalid rounding level for the given turnover as per Schedule III")
            
            cursor.execute('''
                INSERT INTO company_info (
                    user_id, entity_name, address, cin_no, fy_start_date, fy_end_date,
                    currency, units, number_format, negative_format, default_font,
                    default_font_size, show_zeros_as_blank, decimal_places, turnover, 
                    rounding_level, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, entity_name, address, cin_no, fy_start_date, fy_end_date,
                  currency, units, number_format, negative_format, default_font,
                  default_font_size, show_zeros_as_blank, decimal_places, turnover,
                  rounding_level, datetime.now(), datetime.now()))
            
            company_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return company_id
        
        except Exception as e:
            conn.close()
            raise e
    
    @staticmethod
    def update(company_id, entity_name, fy_start_date, fy_end_date, address=None,
               cin_no=None, currency='INR', units='Millions', number_format='Accounting',
               negative_format='Brackets', default_font='Bookman Old Style', 
               default_font_size=11, show_zeros_as_blank=0, decimal_places=2,
               turnover=0, rounding_level='100000'):
        """Update company information"""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            # Validate CIN format if provided
            if cin_no:
                if not CompanyInfo.validate_cin(cin_no):
                    raise ValueError("Invalid CIN format. Expected format: L12345AB2020PLC123456")
            
            # Validate date range
            if not CompanyInfo.validate_dates(fy_start_date, fy_end_date):
                raise ValueError("FY End Date must be after FY Start Date")
            
            # Validate rounding level based on turnover
            if not CompanyInfo.validate_rounding_level(turnover, rounding_level):
                raise ValueError("Invalid rounding level for the given turnover as per Schedule III")
            
            cursor.execute('''
                UPDATE company_info
                SET entity_name = ?, address = ?, cin_no = ?, fy_start_date = ?,
                    fy_end_date = ?, currency = ?, units = ?, number_format = ?,
                    negative_format = ?, default_font = ?, default_font_size = ?,
                    show_zeros_as_blank = ?, decimal_places = ?, turnover = ?,
                    rounding_level = ?, updated_at = ?
                WHERE company_id = ?
            ''', (entity_name, address, cin_no, fy_start_date, fy_end_date,
                  currency, units, number_format, negative_format, default_font,
                  default_font_size, show_zeros_as_blank, decimal_places, turnover,
                  rounding_level, datetime.now(), company_id))
            
            conn.commit()
            conn.close()
        
        except Exception as e:
            conn.close()
            raise e
    
    @staticmethod
    def delete(company_id):
        """Delete company information"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM company_info WHERE company_id = ?', (company_id,))
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def validate_cin(cin):
        """
        Validate CIN (Corporate Identity Number) format
        Format: L12345AB2020PLC123456
        - First character: Letter (L/U/N etc.)
        - Next 5 digits: Registration number
        - Next 2 letters: State code
        - Next 4 digits: Year
        - Next 3 letters: Company type
        - Last 6 digits: Sequential number
        """
        if not cin or len(cin) != 21:
            return False
        
        # Check pattern
        if not (cin[0].isalpha() and 
                cin[1:6].isdigit() and 
                cin[6:8].isalpha() and 
                cin[8:12].isdigit() and 
                cin[12:15].isalpha() and 
                cin[15:21].isdigit()):
            return False
        
        return True
    
    @staticmethod
    def validate_dates(start_date, end_date):
        """Validate that end date is after start date"""
        from datetime import datetime
        
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        
        return end_date > start_date
    
    @staticmethod
    def validate_rounding_level(turnover, rounding_level):
        """
        Validate rounding level as per Schedule III requirements
        
        As per Schedule III (Part I, Point 4):
        - Turnover < Rs. 100 Crores: Can present in '100s, '1000s, '100000s (Lakhs), or '1000000s (Millions)
        - Turnover >= Rs. 100 Crores: Can present in '100000s (Lakhs), '1000000s (Millions), or '10000000s (Crores)
        - Absolute values ('1') are always allowed
        """
        turnover_threshold = 100_00_00_000  # Rs. 100 Crores
        
        # Absolute values always allowed
        if rounding_level == '1':
            return True
        
        # Allowed rounding levels for turnover < 100 Crores
        low_turnover_levels = ['100', '1000', '100000', '1000000']
        
        # Allowed rounding levels for turnover >= 100 Crores
        high_turnover_levels = ['100000', '1000000', '10000000']
        
        if turnover < turnover_threshold:
            return rounding_level in low_turnover_levels
        else:
            return rounding_level in high_turnover_levels
    
    @staticmethod
    def get_rounding_options(turnover):
        """
        Get allowed rounding options based on turnover (Schedule III compliance)
        
        Returns list of tuples: (value, display_text)
        """
        turnover_threshold = 100_00_00_000  # Rs. 100 Crores
        
        if turnover < turnover_threshold:
            # Turnover < 100 Crores
            return [
                ('1', 'Absolute Values (No Rounding)'),
                ('100', 'Hundreds (\'100s)'),
                ('1000', 'Thousands (\'1000s)'),
                ('100000', 'Lakhs (\'100000s)'),
                ('1000000', 'Millions (\'1000000s)')
            ]
        else:
            # Turnover >= 100 Crores
            return [
                ('1', 'Absolute Values (No Rounding)'),
                ('100000', 'Lakhs (\'100000s)'),
                ('1000000', 'Millions (\'1000000s)'),
                ('10000000', 'Crores (\'10000000s)')
            ]
    
    @staticmethod
    def get_rounding_display_name(rounding_level):
        """Get display name for rounding level"""
        mapping = {
            '1': 'Absolute Values',
            '100': 'Hundreds',
            '1000': 'Thousands',
            '100000': 'Lakhs',
            '1000000': 'Millions',
            '10000000': 'Crores'
        }
        return mapping.get(str(rounding_level), 'Unknown')
    
    def to_dict(self):
        """Convert to dictionary for export"""
        return {
            'company_id': self.company_id,
            'user_id': self.user_id,
            'entity_name': self.entity_name,
            'address': self.address,
            'cin_no': self.cin_no,
            'fy_start_date': self.fy_start_date,
            'fy_end_date': self.fy_end_date,
            'currency': self.currency,
            'units': self.units,
            'number_format': self.number_format,
            'negative_format': self.negative_format,
            'default_font': self.default_font,
            'default_font_size': self.default_font_size,
            'show_zeros_as_blank': self.show_zeros_as_blank,
            'decimal_places': self.decimal_places,
            'turnover': self.turnover,
            'rounding_level': self.rounding_level
        }
