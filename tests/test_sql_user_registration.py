import pytest
import sqlite3
import os
import shutil
from datetime import datetime
import logging
from faker import Faker
from pages.add_user_page import AddUserPage
from pages.contact_list_page import ContactListPage
from pages.login_page import LoginPage
from tests.base_test import BaseTest
import time

logger = logging.getLogger('test_logger')
fake = Faker()

def clear_screenshots():
    """Clear the screenshots directory before test run"""
    screenshots_dir = 'screenshots'
    if os.path.exists(screenshots_dir):
        shutil.rmtree(screenshots_dir)
        os.makedirs(screenshots_dir)
        logger.info("Cleared screenshots directory")
    else:
        os.makedirs(screenshots_dir)
        logger.info("Created screenshots directory")

def take_screenshot(driver, name):
    """Take a screenshot and save it to the screenshots directory"""
    try:
        # Create screenshots directory if it doesn't exist
        os.makedirs('screenshots', exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"screenshots/{timestamp}_{name}.png"
        
        # Take screenshot
        driver.save_screenshot(filename)
        logger.info(f"Screenshot saved: {filename}")
    except Exception as e:
        logger.error(f"Failed to take screenshot: {str(e)}")

@pytest.fixture(scope="function")
def db_connection():
    """Create a temporary SQLite database connection"""
    # Clear screenshots before test
    clear_screenshots()
    
    # Create a temporary database file
    db_path = "test_users.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create a test table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Generate and insert test data using Faker
    test_data = []
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    for i in range(5):  # Generate 5 test users
        test_data.append((
            fake.first_name(),
            fake.last_name(),
            f"{fake.user_name()}_{timestamp}_{i}@example.com",  # Add timestamp and index to email
            fake.password(length=10)
        ))
    
    cursor.executemany('''
        INSERT INTO test_users (first_name, last_name, email, password)
        VALUES (?, ?, ?, ?)
    ''', test_data)
    conn.commit()
    
    # Verify table creation and data
    logger.info("Verifying SQL table creation and data...")
    
    # Check table structure
    cursor.execute("PRAGMA table_info(test_users)")
    columns = cursor.fetchall()
    logger.info("Table structure:")
    for col in columns:
        logger.info(f"Column: {col[1]}, Type: {col[2]}, NotNull: {col[3]}, Default: {col[4]}")
    
    # Check number of rows
    cursor.execute("SELECT COUNT(*) FROM test_users")
    count = cursor.fetchone()[0]
    logger.info(f"Number of rows in table: {count}")
    
    # Display sample data
    cursor.execute("SELECT * FROM test_users LIMIT 3")
    sample_data = cursor.fetchall()
    logger.info("Sample data:")
    for row in sample_data:
        logger.info(f"ID: {row[0]}, Name: {row[1]} {row[2]}, Email: {row[3]}, Created: {row[5]}")
    
    yield conn
    
    # Cleanup: close connection and remove the database file
    conn.close()
    if os.path.exists(db_path):
        os.remove(db_path)
        logger.info("Database file cleaned up")

class TestSQLUserRegistration(BaseTest):
    """Test class for SQL-based user registration"""
    
    def test_register_user_from_sql(self, db_connection):
        """Test registering a user using data from SQL database"""
        logger.info("Starting SQL-based user registration test")
        
        # Get test data from SQL database
        cursor = db_connection.cursor()
        cursor.execute('SELECT first_name, last_name, email, password FROM test_users LIMIT 1')
        user_data = cursor.fetchone()
        
        if not user_data:
            pytest.fail("No test data found in database")
            
        first_name, last_name, email, password = user_data
        logger.info(f"Retrieved test user data: {first_name} {last_name} ({email})")
        
        # Navigate to Add User page and fill form
        add_user_page = AddUserPage(self.driver)
        add_user_page.navigate_to()
        logger.info("Navigated to Add User page")
        
        # Fill in the form with data from SQL
        add_user_page.fill_first_name(first_name)
        add_user_page.fill_last_name(last_name)
        add_user_page.fill_email(email)
        add_user_page.fill_password(password)
        logger.info("Filled in user registration form with SQL data")
        
        # Take screenshot of filled form
        take_screenshot(self.driver, "registration_form_filled")
        
        # Get the actual values from the form fields
        actual_first_name = add_user_page.get_first_name()
        actual_last_name = add_user_page.get_last_name()
        actual_email = add_user_page.get_email()
        logger.info("Retrieved actual values from form:")
        logger.info(f"First Name: Expected '{first_name}', Got '{actual_first_name}'")
        logger.info(f"Last Name: Expected '{last_name}', Got '{actual_last_name}'")
        logger.info(f"Email: Expected '{email}', Got '{actual_email}'")
        
        # Verify form values match database values
        assert actual_first_name == first_name, f"First name mismatch in form. Expected: {first_name}, Got: {actual_first_name}"
        assert actual_last_name == last_name, f"Last name mismatch in form. Expected: {last_name}, Got: {actual_last_name}"
        assert actual_email == email, f"Email mismatch in form. Expected: {email}, Got: {actual_email}"
        logger.info("Form values match database values")
        
        # Prepare API request payload using actual form values
        payload = {
            "firstName": actual_first_name,
            "lastName": actual_last_name,
            "email": actual_email,
            "password": password  # We can't get password from form for security reasons
        }
        
        # Submit form
        add_user_page.submit_form()
        logger.info("Submitted user registration form")
        time.sleep(2)  # Wait for any error messages
        
        # Take screenshot after submission
        take_screenshot(self.driver, "registration_form_submitted")
        
        # Check for error messages
        error_message = add_user_page.get_error_message()
        if error_message:
            logger.info(f"Registration error: {error_message}")
            # Take screenshot of error message
            take_screenshot(self.driver, "registration_error")
        
        # Verify API request payload
        try:
            logger.info("Sending API request with form values:")
            logger.info(f"First Name: {payload['firstName']}")
            logger.info(f"Last Name: {payload['lastName']}")
            logger.info(f"Email: {payload['email']}")
            logger.info(f"Password: {'*' * len(payload['password'])}")  # Mask password
            
            response = self.session.post(
                'https://thinking-tester-contact-list.herokuapp.com/users',
                json=payload,
                headers={
                    'Accept': '*/*',
                    'Content-Type': 'application/json',
                    'Origin': 'https://thinking-tester-contact-list.herokuapp.com',
                    'Referer': 'https://thinking-tester-contact-list.herokuapp.com/addUser'
                }
            )
            
            logger.info(f"API Response Status Code: {response.status_code}")
            if response.status_code != 201:
                logger.error(f"API Response Body: {response.text}")
            
            # Verify status code is 400 (Bad Request) for duplicate email
            assert response.status_code == 400, f"Expected status code 400 for duplicate email, got {response.status_code}"
            assert "Email address is already in use" in response.text, "Expected error message about duplicate email"
            logger.info("API request correctly rejected duplicate email")

        except Exception as e:
            # Take screenshot on failure
            take_screenshot(self.driver, "registration_failure")
            logger.error(f"API verification failed: {str(e)}")
            raise
        
        logger.info("SQL-based user registration test completed successfully") 
        