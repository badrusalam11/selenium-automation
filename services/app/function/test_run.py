
import json
import os
import subprocess
import sys
import time

from app import RUNNING_ID_FILE


def execute_selenium_tests(testsuite_id):
    """
    Execute the Selenium tests. You can implement your Selenium
    testing logic here or trigger a separate script that runs the tests.
    """
    try:
        # Run an external script (modify the command as needed)
        command = [sys.executable, "run.py", testsuite_id]
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )

        # Log output for debugging
        print("Selenium Test Output:", result.stdout)
        if result.stderr:
            print("Selenium Test Error:", result.stderr)
    except Exception as e:
        print(f"Error while running Selenium tests: {e}")

def load_running_id():
    """ Load running_id.json if it exists """
    if os.path.exists(RUNNING_ID_FILE):
        with open(RUNNING_ID_FILE, "r") as file:
            return json.load(file)
    return None

def wait_for_running_id(timeout=10, interval=0.5):
    """ Wait for the running_id.json file to be available """
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        running_data = load_running_id()
        if running_data and "running_id" in running_data:
            return running_data
        time.sleep(interval)  # Wait before retrying
    return None  # Timeout reached