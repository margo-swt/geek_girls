from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class LoginPage(BasePage):
    """Page object for the Login page"""
    
    # Locators
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "submit")
    ADD_USER_LINK = (By.ID, "signup")
    
    def navigate_to(self):
        """Navigate to the login page"""
        self.driver.get("https://thinking-tester-contact-list.herokuapp.com/login")
    
    def login(self, email, password):
        """Login with the given credentials"""
        self.fill_email(email)
        self.fill_password(password)
        self.click_login()
    
    def fill_email(self, email):
        """Fill in the email field"""
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)
    
    def fill_password(self, password):
        """Fill in the password field"""
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
    
    def click_login(self):
        """Click the login button"""
        self.driver.find_element(*self.LOGIN_BUTTON).click()
    
    def click_add_user(self):
        """Click the Add User link"""
        self.driver.find_element(*self.ADD_USER_LINK).click()
    
    def is_displayed(self):
        """Check if the login page is displayed"""
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.LOGIN_BUTTON)
            )
            return True
        except:
            return False 