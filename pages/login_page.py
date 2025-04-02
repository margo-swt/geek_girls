from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    # Locators
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "submit")
    SIGNUP_LINK = (By.LINK_TEXT, "Not yet a user? Click here to sign up!")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://thinking-tester-contact-list.herokuapp.com/"

    def navigate_to(self):
        """
        Navigate to the login page
        """
        self.driver.get(self.url)

    def login(self, email: str, password: str) -> bool:
        """
        Perform login action
        :param email: Email to enter
        :param password: Password to enter
        :return: True if login successful, False otherwise
        """
        try:
            self.input_text(self.EMAIL_INPUT, email)
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

    def click_signup_link(self) -> bool:
        """
        Click on signup link
        :return: True if clicked, False otherwise
        """
        return self.click_element(self.SIGNUP_LINK)

    def is_login_page_displayed(self) -> bool:
        """
        Check if login page is displayed
        :return: True if login page is displayed, False otherwise
        """
        return bool(self.find_element(self.EMAIL_INPUT) and 
                   self.find_element(self.PASSWORD_INPUT) and 
                   self.find_element(self.LOGIN_BUTTON)) 