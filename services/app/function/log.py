from datetime import datetime
import os

import logging


def setup_log(log_dir="logs"):
    """Setup a daily rotating logger that appends logs."""
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_filename = os.path.join(log_dir, f"log-{datetime.now().strftime('%Y-%m-%d')}.log")

    logger = logging.getLogger("daily_logger")
    logger.setLevel(logging.INFO)

    # Prevent multiple handlers from being added
    if not logger.handlers:
        file_handler = logging.FileHandler(log_filename, mode='a')  # Append mode
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger, log_filename