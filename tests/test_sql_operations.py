import pytest
import sqlite3
import os
from datetime import datetime
import logging

logger = logging.getLogger('test_logger')

@pytest.fixture(scope="function")
def db_connection():
    """Create a temporary SQLite database connection"""
    # Create a temporary database file
    db_path = "test.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create a test table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert some test data
    test_data = [
        ('John', 'Doe', 'john.doe@example.com'),
        ('Jane', 'Smith', 'jane.smith@example.com'),
        ('Bob', 'Johnson', 'bob.johnson@example.com')
    ]
    cursor.executemany('''
        INSERT INTO users (first_name, last_name, email)
        VALUES (?, ?, ?)
    ''', test_data)
    conn.commit()
    
    yield conn
    
    # Cleanup: close connection and remove the database file
    conn.close()
    if os.path.exists(db_path):
        os.remove(db_path)

def test_sql_operations(db_connection):
    """Test various SQL operations"""
    logger.info("Starting SQL operations test")
    cursor = db_connection.cursor()
    
    # 1. SELECT - Basic query
    logger.info("Executing SELECT query")
    cursor.execute('SELECT * FROM users')
    all_users = cursor.fetchall()
    logger.info(f"Found {len(all_users)} users in the database")
    
    # 2. SELECT with WHERE clause
    logger.info("Executing SELECT with WHERE clause")
    cursor.execute('SELECT * FROM users WHERE first_name = ?', ('John',))
    john = cursor.fetchone()
    logger.info(f"Found user: {john}")
    
    # 3. INSERT - Add new user
    logger.info("Executing INSERT operation")
    cursor.execute('''
        INSERT INTO users (first_name, last_name, email)
        VALUES (?, ?, ?)
    ''', ('Alice', 'Brown', 'alice.brown@example.com'))
    db_connection.commit()
    
    # 4. UPDATE - Modify existing user
    logger.info("Executing UPDATE operation")
    cursor.execute('''
        UPDATE users 
        SET last_name = 'Smith-Jones'
        WHERE email = ?
    ''', ('john.doe@example.com',))
    db_connection.commit()
    
    # 5. DELETE - Remove a user
    logger.info("Executing DELETE operation")
    cursor.execute('DELETE FROM users WHERE email = ?', ('bob.johnson@example.com',))
    db_connection.commit()
    
    # 6. Complex query with JOIN (if we had another table)
    logger.info("Creating and querying related tables")
    cursor.execute('''
        CREATE TABLE user_profiles (
            user_id INTEGER PRIMARY KEY,
            bio TEXT,
            location TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Add some profile data
    cursor.execute('''
        INSERT INTO user_profiles (user_id, bio, location)
        VALUES (?, ?, ?)
    ''', (1, 'Software Engineer', 'San Francisco'))
    db_connection.commit()
    
    # Perform a JOIN query
    logger.info("Executing JOIN query")
    cursor.execute('''
        SELECT u.first_name, u.last_name, up.bio, up.location
        FROM users u
        LEFT JOIN user_profiles up ON u.id = up.user_id
    ''')
    user_profiles = cursor.fetchall()
    logger.info(f"Found {len(user_profiles)} user profiles")
    
    # 7. Aggregate functions
    logger.info("Executing aggregate functions")
    cursor.execute('SELECT COUNT(*) FROM users')
    total_users = cursor.fetchone()[0]
    logger.info(f"Total number of users: {total_users}")
    
    # 8. GROUP BY with HAVING
    logger.info("Executing GROUP BY query")
    cursor.execute('''
        SELECT location, COUNT(*) as count
        FROM user_profiles
        GROUP BY location
        HAVING count > 0
    ''')
    location_stats = cursor.fetchall()
    logger.info(f"Location statistics: {location_stats}")
    
    # Verify our operations
    cursor.execute('SELECT * FROM users')
    final_users = cursor.fetchall()
    logger.info(f"Final user count: {len(final_users)}")
    
    # Clean up the user_profiles table
    cursor.execute('DROP TABLE user_profiles')
    db_connection.commit()
    
    logger.info("SQL operations test completed successfully") 