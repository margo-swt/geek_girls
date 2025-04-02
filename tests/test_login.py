import pytest
from webdriver_config import WebDriverConfig
from pages.login_page import LoginPage
from utils.test_utils import generate_test_id

class TestLogin:
    @pytest.fixture(scope="function")
    def setup(self, logger, browser_type, headless):
        """
        Setup fixture to initialize driver and page objects
        """
        logger.info(f"Initializing {browser_type} browser (headless: {headless})")
        driver = WebDriverConfig.get_driver(browser_type=browser_type, headless=headless)
        login_page = LoginPage(driver)
        yield driver, login_page
        logger.info("Closing browser")
        driver.quit()

    @pytest.mark.smoke
    @pytest.mark.critical
    def test_successful_login(self, setup, logger, test_data):
        """
        Test successful login with valid credentials
        """
        driver, login_page = setup
        test_id = generate_test_id("successful_login")
        logger.info(f"Starting test: {test_id}")
        
        try:
            # Test steps
            logger.info("Navigating to login page")
            login_page.navigate_to()
            assert login_page.is_login_page_displayed(), "Login page should be displayed"
            
            logger.info("Attempting login with valid credentials")
            login_page.login(test_data["valid_user"], test_data["valid_password"])
            # Add assertions for successful login (e.g., check if redirected to dashboard)
            
            logger.info("Test completed successfully")
        except Exception as e:
            logger.error(f"Test failed: {str(e)}")
            raise

    @pytest.mark.regression
    def test_invalid_credentials(self, setup, logger, test_data):
        """
        Test login with invalid credentials
        """
        driver, login_page = setup
        test_id = generate_test_id("invalid_credentials")
        logger.info(f"Starting test: {test_id}")
        
        try:
            # Test steps
            logger.info("Navigating to login page")
            login_page.navigate_to()
            assert login_page.is_login_page_displayed(), "Login page should be displayed"
            
            logger.info("Attempting login with invalid credentials")
            login_page.login(test_data["invalid_user"], test_data["invalid_password"])
            error_message = login_page.get_error_message()
            assert "Invalid credentials" in error_message, "Error message should indicate invalid credentials"
            
            logger.info("Test completed successfully")
        except Exception as e:
            logger.error(f"Test failed: {str(e)}")
            raise

    @pytest.mark.regression
    def test_empty_credentials(self, setup, logger):
        """
        Test login with empty credentials
        """
        driver, login_page = setup
        test_id = generate_test_id("empty_credentials")
        logger.info(f"Starting test: {test_id}")
        
        try:
            # Test steps
            logger.info("Navigating to login page")
            login_page.navigate_to()
            assert login_page.is_login_page_displayed(), "Login page should be displayed"
            
            logger.info("Attempting login with empty credentials")
            login_page.login("", "")
            error_message = login_page.get_error_message()
            assert "Please enter your credentials" in error_message, "Error message should indicate empty credentials"
            
            logger.info("Test completed successfully")
        except Exception as e:
            logger.error(f"Test failed: {str(e)}")
            raise

    @pytest.mark.regression
    def test_signup_link(self, setup, logger):
        """
        Test signup link functionality
        """
        driver, login_page = setup
        test_id = generate_test_id("signup_link")
        logger.info(f"Starting test: {test_id}")
        
        try:
            # Test steps
            logger.info("Navigating to login page")
            login_page.navigate_to()
            assert login_page.is_login_page_displayed(), "Login page should be displayed"
            
            logger.info("Clicking signup link")
            assert login_page.click_signup_link(), "Signup link should be clickable"
            # Add assertions for signup page
            
            logger.info("Test completed successfully")
        except Exception as e:
            logger.error(f"Test failed: {str(e)}")
            raise 