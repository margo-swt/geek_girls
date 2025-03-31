from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import Optional, List

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find_element(self, locator: tuple, timeout: int = 10) -> Optional[object]:
        """
        Find element with explicit wait
        :param locator: Tuple of locator strategy and value (e.g., (By.ID, "example"))
        :param timeout: Time to wait for element
        :return: WebElement if found, None otherwise
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            return None

    def find_elements(self, locator: tuple, timeout: int = 10) -> List[object]:
        """
        Find all elements matching the locator
        :param locator: Tuple of locator strategy and value
        :param timeout: Time to wait for elements
        :return: List of WebElements
        """
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
            return elements
        except TimeoutException:
            return []

    def click_element(self, locator: tuple, timeout: int = 10) -> bool:
        """
        Click on element with explicit wait
        :param locator: Tuple of locator strategy and value
        :param timeout: Time to wait for element
        :return: True if clicked, False otherwise
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def input_text(self, locator: tuple, text: str, timeout: int = 10) -> bool:
        """
        Input text into element
        :param locator: Tuple of locator strategy and value
        :param text: Text to input
        :param timeout: Time to wait for element
        :return: True if text entered, False otherwise
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            element.clear()
            element.send_keys(text)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def get_text(self, locator: tuple, timeout: int = 10) -> Optional[str]:
        """
        Get text from element
        :param locator: Tuple of locator strategy and value
        :param timeout: Time to wait for element
        :return: Text if found, None otherwise
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element.text
        except (TimeoutException, NoSuchElementException):
            return None

    def select_dropdown(self, locator: tuple, value: str, timeout: int = 10) -> bool:
        """
        Select option from dropdown
        :param locator: Tuple of locator strategy and value
        :param value: Value to select
        :param timeout: Time to wait for element
        :return: True if selected, False otherwise
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            Select(element).select_by_value(value)
            return True
        except (TimeoutException, NoSuchElementException):
            return False 