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
        
        # Prepare API request payload
        payload = {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "password": password
        }
        
        # Verify API request payload
        try:
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
            
            logger.info(f"API Request Payload: {payload}")
            logger.info(f"API Response Status Code: {response.status_code}")
            
            # Verify the payload matches our database values
            assert payload['firstName'] == first_name, "First name mismatch in payload"
            assert payload['lastName'] == last_name, "Last name mismatch in payload"
            assert payload['email'] == email, "Email mismatch in payload"
            assert payload['password'] == password, "Password mismatch in payload"
            logger.info("Payload verification successful")
            
            # Verify status code is 201 (Created)
            assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"
            logger.info("Status code verification successful")
            
        except Exception as e:
            logger.error(f"API verification failed: {str(e)}")
            raise
        
        logger.info("SQL-based user registration test completed successfully") 