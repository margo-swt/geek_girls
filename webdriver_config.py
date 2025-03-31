from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from typing import Optional

class WebDriverConfig:
    @staticmethod
    def get_chrome_driver(headless: bool = False) -> webdriver.Chrome:
        """
        Initialize and return a Chrome WebDriver instance
        :param headless: Run browser in headless mode if True
        :return: Chrome WebDriver instance
        """
        chrome_options = ChromeOptions()
        if headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)

    @staticmethod
    def get_firefox_driver(headless: bool = False) -> webdriver.Firefox:
        """
        Initialize and return a Firefox WebDriver instance
        :param headless: Run browser in headless mode if True
        :return: Firefox WebDriver instance
        """
        firefox_options = FirefoxOptions()
        if headless:
            firefox_options.add_argument('--headless')
        firefox_options.add_argument('--width=1920')
        firefox_options.add_argument('--height=1080')
        
        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=firefox_options)

    @staticmethod
    def get_driver(browser_name: str = 'chrome', headless: bool = False) -> Optional[webdriver.Remote]:
        """
        Get WebDriver instance based on browser name
        :param browser_name: Name of the browser ('chrome' or 'firefox')
        :param headless: Run browser in headless mode if True
        :return: WebDriver instance
        """
        browser_name = browser_name.lower()
        if browser_name == 'chrome':
            return WebDriverConfig.get_chrome_driver(headless)
        elif browser_name == 'firefox':
            return WebDriverConfig.get_firefox_driver(headless)
        else:
            raise ValueError(f"Unsupported browser: {browser_name}") 