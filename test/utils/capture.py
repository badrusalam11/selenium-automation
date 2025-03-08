import os
import time
from test import TEST_DIR

class Capture:
    def capture_screenshot(context, name=""):
        # timestamp = time.strftime("%Y%m%d-%H%M%S")
        timestamp = str(time.time())
        session_id = context.driver.session_id
        screenshot_folder = os.path.join(TEST_DIR, "sessions", session_id)
        # Create a folder to save screenshots if it doesn't exist
        if not os.path.exists(screenshot_folder):
            os.makedirs(screenshot_folder)
        
        # Generate timestamped screenshot filename
        screenshot_path = os.path.join(screenshot_folder, f"{timestamp}_{name}.png")
        # Set context images for report
        # Ensure context.images exists and append the screenshot path
        if not hasattr(context, "images"):
            context.images = []
        context.images.append(screenshot_path)
        # Capture and save the screenshot
        context.driver.get_screenshot_as_file(screenshot_path)
        print(f"Screenshot saved at {screenshot_path}")