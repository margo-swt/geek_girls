import os
import time
from datetime import datetime
from typing import Optional
import uuid

def take_screenshot(driver, name: str) -> Optional[str]:
    """
    Take a screenshot and save it with timestamp
    :param driver: WebDriver instance
    :param name: Name of the screenshot
    :return: Path to the screenshot file
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_dir = "screenshots"
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        
        filename = f"{screenshot_dir}/{name}_{timestamp}.png"
        driver.save_screenshot(filename)
        return filename
    except Exception as e:
        print(f"Failed to take screenshot: {str(e)}")
        return None

def wait_for_file_download(directory: str, timeout: int = 30) -> bool:
    """
    Wait for a file to be downloaded
    :param directory: Directory to check for downloads
    :param timeout: Timeout in seconds
    :return: True if file was downloaded, False otherwise
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        files = os.listdir(directory)
        if any(file.endswith('.crdownload') or file.endswith('.part') for file in files):
            time.sleep(1)
            continue
        return True
    return False

def generate_test_id(test_name: str) -> str:
    """
    Generate a unique test ID combining timestamp and UUID
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    return f"{test_name}_{timestamp}_{unique_id}" 