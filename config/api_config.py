import requests
import logging

logger = logging.getLogger(__name__)

class APIConfig:
    """Configuration for API requests."""
    
    BASE_URL = "https://thinking-tester-contact-list.herokuapp.com"
    
    @staticmethod
    def register_user(first_name, last_name, email, password):
        """Register a new user via API."""
        url = f"{APIConfig.BASE_URL}/users"
        payload = {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "password": password
        }
        headers = {
            'Accept': '*/*',
            'Content-Type': 'application/json',
            'Origin': APIConfig.BASE_URL,
            'Referer': f"{APIConfig.BASE_URL}/addUser"
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            return response
        except Exception as e:
            logger.error(f"API request failed: {e}")
            raise 