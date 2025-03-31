import logging
import os
from datetime import datetime

def setup_logger(name: str) -> logging.Logger:
    """
    Setup a logger with file and console handlers
    :param name: Name of the logger
    :return: Logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # File handler
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_handler = logging.FileHandler(f'logs/test_run_{timestamp}.log')
    file_handler.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger 