import pytest
from config.webdriver_config import WebDriverConfig
from faker import Faker
import json
import os
import logging
from datetime import datetime
from py.xml import html
from dotenv import load_dotenv

load_dotenv()

# Configure logging
@pytest.fixture(scope='session', autouse=True)
def setup_logging():
    # Create a logger
    logger = logging.getLogger('test_logger')
    logger.setLevel(logging.INFO)
    
    # Create handlers
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler('reports/test.log')
    
    # Create formatters and add it to handlers
    log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(log_format)
    file_handler.setFormatter(log_format)
    
    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

def pytest_html_report_title(report):
    report.title = "Contact List App - Test Automation Report"

def pytest_configure(config):
    config._metadata = {
        'Project Name': 'Contact List App',
        'Test Environment': os.getenv('BASE_URL'),
        'Browser': os.getenv('BROWSER', 'Chrome'),
        'Platform': 'macOS',
        'Python Version': '3.12'
    }

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    # Add timestamp to the report
    report.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Get the test log content
    log_content = None
    try:
        with open('reports/test.log', 'r') as f:
            log_content = f.read()
    except:
        log_content = "No log file found"
    
    # Add logs to the report for all tests
    if report.when == "call":
        extras = []
        
        # Add log output
        if log_content:
            extras.append({
                "content": str(html.div(
                    html.h3("Test Logs"),
                    html.pre(log_content),
                    class_="log"
                )),
                "name": "Test Logs",
                "format": "html",
                "format_type": "raw",
                "extension": "html"
            })
        
        # Add API response details if it's an API test
        if "test_empty_fields_api" in item.name and hasattr(item, "api_response"):
            try:
                response_json = item.api_response.json()
                # Format JSON with proper indentation and syntax highlighting
                formatted_json = json.dumps(response_json, indent=2)
                extras.append({
                    "content": str(html.div(
                        html.h3("API Response Details"),
                        html.table(
                            [
                                html.tr([html.td("Status Code"), html.td(str(item.api_response.status_code))]),
                                html.tr([html.td("Response Body"), html.td(
                                    html.pre(
                                        html.code(
                                            formatted_json,
                                            class_="json"
                                        ),
                                        class_="json-container"
                                    )
                                )]),
                                html.tr([html.td("Request URL"), html.td(item.api_response.url)]),
                                html.tr([html.td("Request Headers"), html.td(
                                    html.pre(
                                        html.code(
                                            json.dumps(dict(item.api_response.request.headers), indent=2),
                                            class_="json"
                                        ),
                                        class_="json-container"
                                    )
                                )])
                            ]
                        ),
                        class_="api-response"
                    )),
                    "name": "API Response",
                    "format": "html",
                    "format_type": "raw",
                    "extension": "html"
                })
            except Exception as e:
                extras.append({
                    "content": str(html.div(f"Error processing API response: {str(e)}", class_="error")),
                    "name": "API Error",
                    "format": "html",
                    "format_type": "raw",
                    "extension": "html"
                })
        
        # Use the new extras attribute instead of the deprecated extra
        report.extras = extras

@pytest.fixture(scope="function")
def driver():
    """
    Create and return a WebDriver instance for each test
    """
    driver = WebDriverConfig.get_chrome_driver()
    yield driver
    
    # Capture screenshot on test failure
    if driver is not None:
        try:
            driver.save_screenshot('reports/screenshots/last_test.png')
        except:
            pass
        driver.quit()

@pytest.fixture(scope="session")
def faker():
    """
    Create and return a Faker instance
    """
    return Faker()

@pytest.fixture
def valid_user_data(faker):
    """
    Generate valid user data using Faker
    """
    return {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "email": faker.email(),
        "password": faker.password(length=10)
    }

@pytest.fixture
def empty_user_data():
    """
    Return empty user data for negative testing
    """
    return {
        "first_name": "",
        "last_name": "",
        "email": "",
        "password": ""
    }

@pytest.fixture
def api_headers():
    """
    Return headers for API requests
    """
    return {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Content-Type': 'application/json',
        'Origin': os.getenv('BASE_URL'),
        'Referer': f"{os.getenv('BASE_URL')}/addUser",
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
    } 