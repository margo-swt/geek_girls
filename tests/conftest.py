import pytest
import os
from dotenv import load_dotenv
from utils.logger import setup_logger
from utils.test_utils import take_screenshot
import logging
from datetime import datetime

# Load environment variables
load_dotenv()

def pytest_configure(config):
    """
    Configure pytest
    """
    # Add custom markers
    config.addinivalue_line(
        "markers",
        "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers",
        "regression: mark test as regression test"
    )
    config.addinivalue_line(
        "markers",
        "critical: mark test as critical"
    )

@pytest.fixture(scope="session")
def logger():
    """
    Fixture to provide logging functionality
    """
    # Create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    # Create a file handler
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"logs/test_{timestamp}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    
    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

@pytest.fixture(scope="session")
def base_url():
    """
    Get base URL from environment variable
    """
    return os.getenv("BASE_URL", "https://example.com")

@pytest.fixture(scope="session")
def test_data():
    """
    Load test data
    """
    return {
        "valid_user": os.getenv("VALID_USER", "test_user"),
        "valid_password": os.getenv("VALID_PASSWORD", "test_password"),
        "invalid_user": "invalid_user",
        "invalid_password": "invalid_password"
    }

@pytest.fixture(scope="session")
def browser_type():
    """
    Fixture to specify the browser type
    Default is 'chrome'
    """
    return 'chrome'

# @pytest.fixture(scope="session")
# def headless():
#     """
#     Fixture to specify if browser should run in headless mode
#     Default is False (non-headless)
#     """
#     return False

@pytest.fixture(scope="session")
def download_dir():
    """
    Create and return download directory path
    """
    download_dir = os.path.join(os.getcwd(), "downloads")
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    return download_dir

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test results and take screenshots on failure
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call":
        if report.failed:
            driver = item.funcargs.get("setup")[0] if "setup" in item.funcargs else None
            if driver:
                take_screenshot(driver, f"failure_{item.name}")

@pytest.fixture(scope="function")
def test_id():
    """
    Generate unique test ID for each test
    """
    return None  # Will be set by individual tests 