import pytest
from webdriver_config import WebDriverConfig
from pages.signup_page import SignupPage
from utils.data_generator import TestDataGenerator
from utils.test_utils import generate_test_id

class TestSignup:
    @pytest.fixture(scope="function")
    def setup(self, logger, browser_type, headless):
        """
        Setup fixture to initialize driver and page objects
        """
        logger.info(f"Initializing {browser_type} browser (headless: {headless})")
        driver = WebDriverConfig.get_driver(browser_type=browser_type, headless=headless)
        signup_page = SignupPage(driver)
        data_generator = TestDataGenerator()
        yield driver, signup_page, data_generator
        logger.info("Closing browser")
        driver.quit()

    @pytest.mark.smoke
    @pytest.mark.critical
    def test_successful_signup(self, setup, logger):
        """
        Test successful signup with valid data
        """
        driver, signup_page, data_generator = setup
        test_id = generate_test_id("successful_signup")
        logger.info(f"Starting test: {test_id}")
        
        try:
            # Generate test data
            user_data = data_generator.generate_user_data()
            logger.info(f"Generated test data: {user_data}")
            
            # Test steps
            logger.info("Navigating to signup page")
            signup_page.navigate_to()
            assert signup_page.is_signup_page_displayed(), "Signup page should be displayed"
            
            logger.info("Attempting signup with valid data")
            signup_page.signup(
                user_data["first_name"],
                user_data["last_name"],
                user_data["email"],
                user_data["password"]
            )
            # Add assertions for successful signup (e.g., check if redirected to login page)
            
            logger.info("Test completed successfully")
        except Exception as e:
            logger.error(f"Test failed: {str(e)}")
            raise

    @pytest.mark.regression
    def test_invalid_email_signup(self, setup, logger):
        """
        Test signup with invalid email format
        """
        driver, signup_page, data_generator = setup
        test_id = generate_test_id("invalid_email_signup")
        logger.info(f"Starting test: {test_id}")
        
        try:
            # Generate test data with invalid email
            user_data = data_generator.generate_user_data()
            user_data["email"] = data_generator.generate_invalid_email()
            logger.info(f"Generated test data with invalid email: {user_data}")
            
            # Test steps
            logger.info("Navigating to signup page")
            signup_page.navigate_to()
            assert signup_page.is_signup_page_displayed(), "Signup page should be displayed"
            
            logger.info("Attempting signup with invalid email")
            signup_page.signup(
                user_data["first_name"],
                user_data["last_name"],
                user_data["email"],
                user_data["password"]
            )
            error_message = signup_page.get_error_message()
            assert "Invalid email" in error_message, "Error message should indicate invalid email"
            
            logger.info("Test completed successfully")
        except Exception as e:
            logger.error(f"Test failed: {str(e)}")
            raise

    @pytest.mark.regression
    def test_short_password_signup(self, setup, logger):
        """
        Test signup with password that's too short
        """
        driver, signup_page, data_generator = setup
        test_id = generate_test_id("short_password_signup")
        logger.info(f"Starting test: {test_id}")
        
        try:
            # Generate test data with short password
            user_data = data_generator.generate_user_data()
            user_data["password"] = data_generator.generate_short_password()
            logger.info(f"Generated test data with short password: {user_data}")
            
            # Test steps
            logger.info("Navigating to signup page")
            signup_page.navigate_to()
            assert signup_page.is_signup_page_displayed(), "Signup page should be displayed"
            
            logger.info("Attempting signup with short password")
            signup_page.signup(
                user_data["first_name"],
                user_data["last_name"],
                user_data["email"],
                user_data["password"]
            )
            error_message = signup_page.get_error_message()
            assert "Password too short" in error_message, "Error message should indicate password is too short"
            
            logger.info("Test completed successfully")
        except Exception as e:
            logger.error(f"Test failed: {str(e)}")
            raise 