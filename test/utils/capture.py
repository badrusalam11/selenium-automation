import os
import time
from test import FEATURE_DIR

class Capture:
    def capture_screenshot(driver, name):
        # timestamp = time.strftime("%Y%m%d-%H%M%S")
        timestamp = str(time.time())
        session_id = driver.session_id
        screenshot_folder = FEATURE_DIR + "/screenshots/" + session_id
        # Create a folder to save screenshots if it doesn't exist
        if not os.path.exists(screenshot_folder):
            os.makedirs(screenshot_folder)
        
        # Generate timestamped screenshot filename
        screenshot_path = os.path.join(screenshot_folder, f"{timestamp}_{name}.png")
        
        # Capture and save the screenshot
        driver.get_screenshot_as_file(screenshot_path)
        print(f"Screenshot saved at {screenshot_path}")