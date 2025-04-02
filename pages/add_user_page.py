from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class AddUserPage(BasePage):
    """Page object for the Add User page"""
    
    # Locators
    FIRST_NAME_INPUT = (By.ID, "firstName")
    LAST_NAME_INPUT = (By.ID, "lastName")
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    SUBMIT_BUTTON = (By.ID, "submit")
    CANCEL_BUTTON = (By.ID, "cancel")
    ERROR_MESSAGE = (By.ID, "error")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{self.base_url}/addUser"

    def open(self):
        """Open Add User page"""
        self.driver.get(self.url)
        return self

    def navigate_to(self):
        """Navigate to the Add User page"""
        self.driver.get("https://thinking-tester-contact-list.herokuapp.com/addUser")

    def fill_first_name(self, first_name):
        """Fill in the first name field"""
        self.input_text(self.FIRST_NAME_INPUT, first_name)

    def fill_last_name(self, last_name):
        """Fill in the last name field"""
        self.input_text(self.LAST_NAME_INPUT, last_name)

    def fill_email(self, email):
        """Fill in the email field"""
        self.input_text(self.EMAIL_INPUT, email)

    def fill_password(self, password):
        """Fill in the password field"""
        self.input_text(self.PASSWORD_INPUT, password)

    def submit_form(self):
        """Submit the add user form"""
        self.click(self.SUBMIT_BUTTON)
        return self

    def click_cancel(self):
        """Click the cancel button"""
        self.click(self.CANCEL_BUTTON)
        return self

    def is_displayed(self):
        """Check if the Add User page is displayed"""
        try:
            self.wait_for_element(self.SUBMIT_BUTTON)
            return True
        except:
            return False

    def clear_form(self):
        """Clear all form fields"""
        self.driver.find_element(*self.FIRST_NAME_INPUT).clear()
        self.driver.find_element(*self.LAST_NAME_INPUT).clear()
        self.driver.find_element(*self.EMAIL_INPUT).clear()
        self.driver.find_element(*self.PASSWORD_INPUT).clear()

    def get_error_message(self):
        """Get error message if present"""
        try:
            error_element = self.wait_for_element_visible(self.ERROR_MESSAGE, timeout=5)
            return error_element.text
        except:
            return None 