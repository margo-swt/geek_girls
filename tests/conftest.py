import pytest
import os
from dotenv import load_dotenv
from utils.logger import setup_logger
from utils.test_utils import take_screenshot

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
    Setup logger for the test session
    """
    return setup_logger("test_session")

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
    Get browser type from environment variable
    """
    return os.getenv("BROWSER_TYPE", "chrome")

@pytest.fixture(scope="session")
def headless():
    """
    Get headless mode from environment variable
    """
    return os.getenv("HEADLESS", "false").lower() == "true"

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