from faker import Faker
import random
import string

class TestDataGenerator:
    def __init__(self):
        self.fake = Faker()
        
    def generate_user_data(self):
        """
        Generate valid user data for signup
        """
        return {
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "email": self.fake.email(),
            "password": self._generate_password()
        }
    
    def _generate_password(self, length=12):
        """
        Generate a secure password
        """
        # Combine different character types
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special_chars = "!@#$%^&*"
        
        # Ensure at least one of each type
        password = [
            random.choice(lowercase),
            random.choice(uppercase),
            random.choice(digits),
            random.choice(special_chars)
        ]
        
        # Fill the rest with random characters
        all_chars = lowercase + uppercase + digits + special_chars
        password.extend(random.choice(all_chars) for _ in range(length - 4))
        
        # Shuffle the password
        random.shuffle(password)
        return ''.join(password)
    
    def generate_invalid_email(self):
        """
        Generate invalid email formats
        """
        invalid_emails = [
            "test@",  # Missing domain
            "@example.com",  # Missing username
            "test@example",  # Missing TLD
            "test@.com",  # Missing domain name
            "test@example..com",  # Double dot
            "test@example.com.",  # Trailing dot
            "test@example@com",  # Multiple @
            "test example.com",  # Space instead of @
            "test@example com",  # Space in domain
        ]
        return random.choice(invalid_emails)
    
    def generate_short_password(self):
        """
        Generate a password that's too short
        """
        return self._generate_password(length=5)  # Less than minimum required length 