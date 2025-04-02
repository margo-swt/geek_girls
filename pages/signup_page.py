from selenium.webdriver.common.by import By
from .base_page import BasePage

class SignupPage(BasePage):
    # Locators
    FIRST_NAME_INPUT = (By.ID, "firstName")
    LAST_NAME_INPUT = (By.ID, "lastName")
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    SIGNUP_BUTTON = (By.ID, "submit")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://thinking-tester-contact-list.herokuapp.com/addUser"

    def navigate_to(self):
        """
        Navigate to the signup page
        """
        self.driver.get(self.url)

    def signup(self, first_name: str, last_name: str, email: str, password: str) -> bool:
        """
        Perform signup action
        :param first_name: First name to enter
        :param last_name: Last name to enter
        :param email: Email to enter
        :param password: Password to enter
        :return: True if signup successful, False otherwise
        """
        try:
            self.input_text(self.FIRST_NAME_INPUT, first_name)
            self.input_text(self.LAST_NAME_INPUT, last_name)
            self.input_text(self.EMAIL_INPUT, email)
            self.input_text(self.PASSWORD_INPUT, password)
            return self.click_element(self.SIGNUP_BUTTON)
        except Exception:
            return False

    def get_error_message(self) -> str:
        """
        Get error message if signup fails
        :return: Error message text
        """
        return self.get_text(self.ERROR_MESSAGE) or ""

    def is_signup_page_displayed(self) -> bool:
        """
        Check if signup page is displayed
        :return: True if signup page is displayed, False otherwise
        """
        return bool(self.find_element(self.FIRST_NAME_INPUT) and 
                   self.find_element(self.LAST_NAME_INPUT) and 
                   self.find_element(self.EMAIL_INPUT) and 
                   self.find_element(self.PASSWORD_INPUT) and 
                   self.find_element(self.SIGNUP_BUTTON)) 