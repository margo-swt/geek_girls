import pytest
import sqlite3
import os
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

@pytest.fixture(scope="function")
def db_connection():
    """Create a temporary SQLite database connection"""
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
    for _ in range(5):  # Generate 5 test users
        test_data.append((
            fake.first_name(),
            fake.last_name(),
            fake.email(),
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
    
    def test_empty_fields_validation(self):
        """Test validation messages when submitting empty fields"""
        logger.info("Starting empty fields validation test")
        
        # Navigate to Add User page
        add_user_page = AddUserPage(self.driver)
        add_user_page.navigate_to()
        logger.info("Navigated to Add User page")
        
        # Submit empty form
        add_user_page.submit_form()
        logger.info("Submitted empty form")
        
        # Wait a moment for the error message to appear
        time.sleep(2)
        
        # Check error message
        error_message = add_user_page.get_error_message()
        expected_error = "User validation failed: firstName: Path `firstName` is required., lastName: Path `lastName` is required., email: Email is invalid, password: Path `password` is required."
        assert error_message == expected_error, f"Expected error message not found. Got: {error_message}"
        
        logger.info("Empty fields validation test completed successfully") 