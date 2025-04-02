import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests
import logging

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
        
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in headless mode
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # Initialize WebDriver
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        
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