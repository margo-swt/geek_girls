import pytest
import requests
import logging
from config.webdriver_config import WebDriverConfig

class BaseTest:
    """Base class for all test classes"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test environment before each test"""
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('test_logger')
        
        # Initialize WebDriver using WebDriverConfig
        self.driver = WebDriverConfig.get_chrome_driver()
        
        # Initialize requests session
        self.session = requests.Session()
        
        # Setup complete
        self.logger.info("Test setup completed")
        
        yield
        
        # Cleanup after test
        if self.driver:
            self.driver.quit()
        if self.session:
            self.session.close()
        
        self.logger.info("Test cleanup completed") 