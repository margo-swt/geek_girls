import pytest
import requests
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.add_user_page import AddUserPage
import os
import json
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger('test_logger')

class TestAddUser:
    @pytest.mark.ui
    @pytest.mark.negative
    def test_empty_fields_validation(self, driver):
        """Test validation messages when submitting empty fields"""
        logger.info("Starting empty fields validation test")
        
        add_user_page = AddUserPage(driver)
        add_user_page.open()
        add_user_page.submit_form()
        
        error_message = add_user_page.get_error_message()
        assert "User validation failed: firstName: Path `firstName` is required., lastName: Path `lastName` is required., email: Email is invalid, password: Path `password` is required." in error_message
        
        logger.info("Empty fields validation test completed successfully")

    @pytest.mark.api
    @pytest.mark.negative
    def test_empty_fields_api(self, empty_user_data, api_headers, request):
        """Test API response when submitting empty fields"""
        logger.info("Starting empty fields API validation test")
        
        # Transform the data to match API expectations
        api_data = {
            "firstName": empty_user_data["first_name"],
            "lastName": empty_user_data["last_name"],
            "email": empty_user_data["email"],
            "password": empty_user_data["password"]
        }
        
        response = requests.post(
            f"{os.getenv('BASE_URL')}/users",
            headers=api_headers,
            json=api_data
        )
        
        # Store response for reporting
        request.node.api_response = response
        
        # Log response details
        logger.info(f"Response status code: {response.status_code}")
        logger.info(f"Response body: {response.json()}")
        
        assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
        error_data = response.json()
        assert "firstName" in error_data["errors"]
        assert "lastName" in error_data["errors"]
        assert "email" in error_data["errors"]
        assert "password" in error_data["errors"]
        
        logger.info("Empty fields API validation test completed successfully") 