from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class ContactListPage(BasePage):
    """Page object for the Contact List page"""
    
    # Locators
    CONTACT_LIST_TABLE = (By.ID, "myTable")
    ADD_CONTACT_BUTTON = (By.ID, "add-contact")
    LOGOUT_BUTTON = (By.ID, "logout")
    
    def is_displayed(self, timeout=10):
        """Check if the Contact List page is displayed"""
        try:
            # Wait for both the URL and the table to be present
            self.wait_for_url_contains("/contactList", timeout)
            self.wait_for_element(self.CONTACT_LIST_TABLE, timeout)
            return True
        except:
            return False
    
    def click_add_contact(self):
        """Click the Add Contact button"""
        self.click(self.ADD_CONTACT_BUTTON)
    
    def click_logout(self):
        """Click the Logout button"""
        self.click(self.LOGOUT_BUTTON)
    
    def get_contact_count(self):
        """Get the number of contacts in the list"""
        contacts = self.driver.find_elements(By.CSS_SELECTOR, "#myTable tr")
        return len(contacts) - 1  # Subtract 1 for the header row 