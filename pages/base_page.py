from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
from dotenv import load_dotenv

load_dotenv()

class BasePage:
    """Base class for all page objects"""
    
    def __init__(self, driver):
        """Initialize the base page"""
        self.driver = driver
        self.base_url = os.getenv('BASE_URL')
        self.wait = WebDriverWait(driver, 10)

    def wait_for_element(self, locator, timeout=10):
        """Wait for an element to be present"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            raise TimeoutException(f"Element {locator} not found after waiting {timeout} seconds")

    def wait_for_element_clickable(self, locator, timeout=10):
        """Wait for an element to be clickable"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
        except TimeoutException:
            raise TimeoutException(f"Element {locator} not clickable after waiting {timeout} seconds")

    def wait_for_element_visible(self, locator, timeout=10):
        """Wait for an element to be visible"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            raise TimeoutException(f"Element {locator} not visible after waiting {timeout} seconds")

    def wait_for_element_invisible(self, locator, timeout=10):
        """Wait for an element to be invisible"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
        except TimeoutException:
            raise TimeoutException(f"Element {locator} still visible after waiting {timeout} seconds")

    def wait_for_url_contains(self, text, timeout=10):
        """Wait for URL to contain specific text"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.url_contains(text)
            )
        except TimeoutException:
            raise TimeoutException(f"URL does not contain '{text}' after waiting {timeout} seconds")

    def wait_for_url_to_be(self, url, timeout=10):
        """Wait for URL to be exactly as specified"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.url_to_be(url)
            )
        except TimeoutException:
            raise TimeoutException(f"URL is not '{url}' after waiting {timeout} seconds")

    def is_element_present(self, locator):
        """Check if an element is present on the page"""
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False

    def get_element_text(self, locator):
        """Get text of an element"""
        element = self.wait_for_element_visible(locator)
        return element.text

    def input_text(self, locator, text):
        """Input text into an element"""
        element = self.wait_for_element_visible(locator)
        element.clear()
        element.send_keys(text)

    def click(self, locator):
        """Click an element"""
        element = self.wait_for_element_clickable(locator)
        element.click()

    def get_current_url(self):
        """Get the current URL"""
        return self.driver.current_url

    def find_element(self, locator: tuple):
        """Find element with explicit wait"""
        return self.wait_for_element(locator)

    def find_elements(self, locator: tuple):
        """Find elements with explicit wait"""
        return self.wait_for_element(locator)

    def is_element_visible(self, locator: tuple, timeout: int = None) -> bool:
        """Check if element is visible"""
        try:
            wait = WebDriverWait(self.driver, timeout or 10)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def wait_for_url_contains(self, partial_url: str, timeout: int = None) -> bool:
        """Wait for URL to contain specific text"""
        try:
            wait = WebDriverWait(self.driver, timeout or 10)
            return wait.until(EC.url_contains(partial_url))
        except TimeoutException:
            return False 