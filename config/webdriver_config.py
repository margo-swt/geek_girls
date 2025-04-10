from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
from dotenv import load_dotenv

load_dotenv()

class WebDriverConfig:
    @staticmethod
    def get_chrome_driver():
        """
        Initialize and return a Chrome WebDriver instance
        :return: Chrome WebDriver instance
        """
        chrome_options = Options()
        # chrome_options.add_argument('--headless=new')  # Commented out to see the browser
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(20)  # Increased wait time to 20 seconds
        
        return driver 