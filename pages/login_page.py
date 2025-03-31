from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    # Locators
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot Password?")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://example.com/login"  # Replace with your actual login page URL

    def navigate_to(self):
        """
        Navigate to the login page
        """
        self.driver.get(self.url)

    def login(self, username: str, password: str) -> bool:
        """
        Perform login action
        :param username: Username to enter
        :param password: Password to enter
        :return: True if login successful, False otherwise
        """
        try:
            self.input_text(self.USERNAME_INPUT, username)
            self.input_text(self.PASSWORD_INPUT, password)
            return self.click_element(self.LOGIN_BUTTON)
        except Exception:
            return False

    def get_error_message(self) -> str:
        """
        Get error message if login fails
        :return: Error message text
        """
        return self.get_text(self.ERROR_MESSAGE) or ""

    def click_forgot_password(self) -> bool:
        """
        Click on forgot password link
        :return: True if clicked, False otherwise
        """
        return self.click_element(self.FORGOT_PASSWORD_LINK)

    def is_login_page_displayed(self) -> bool:
        """
        Check if login page is displayed
        :return: True if login page is displayed, False otherwise
        """
        return bool(self.find_element(self.USERNAME_INPUT) and 
                   self.find_element(self.PASSWORD_INPUT) and 
                   self.find_element(self.LOGIN_BUTTON)) 