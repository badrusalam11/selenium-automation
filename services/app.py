from datetime import datetime
import json
import os
from pathlib import Path
import sys
import time
from flask import Flask, request, jsonify
import subprocess
import threading

app = Flask(__name__)
FEATURE_DIR = os.path.join(os.getcwd(), "test")
RUNNING_ID_FILE = os.path.join(FEATURE_DIR, "sessions", "running_id.json")
TEST_SUITES_DIR = os.path.join(FEATURE_DIR, "test_suites")
SESSION_FILE = os.path.join(FEATURE_DIR, "sessions", "current_session.json")
SESSIONS_FOLDER = os.path.join(FEATURE_DIR, "sessions")

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

def get_testsuites(directory=TEST_SUITES_DIR):
    """
    Recursively get all .py filenames inside the given directory without the .py extension.
    
    Args:
        directory (str): The base directory to search in.
        
    Returns:
        list: A list of Python filenames without .py extension (e.g., ['regression', 'list'])
    """
    python_files = set()  # Use a set to avoid duplicates
    
    # Walk through all directories and subdirectories
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                if file == "test_suite_runner.py":
                    continue
                filename_without_ext = os.path.splitext(file)[0]  # Remove .py extension
                python_files.add(filename_without_ext)
    return sorted(list(python_files))  # Sort for consistency


@app.route('/selenium/run', methods=['POST'])
def selenium_run():
    # Parse JSON payload.
    payload = request.get_json()
    testsuite_id = payload.get('testsuite_id') if payload else None
    
    # check if testsuite_id is empty
    if not testsuite_id:
        return jsonify({
            "status": "error",
            "errorCode": "INVALID_REQUEST",
            "message": "testsuite_id is required"
        }), 400
    
    #check if the testsuite exist
    testsuite_list = get_testsuites()
    if testsuite_id not in testsuite_list:
        return jsonify({
            "status": "error",
            "errorCode": "INVALID_TESTSUITE",
            "message": "testsuite_id is not valid"
        }), 404
    
    # check running id first
    running_data = load_running_id()
    if running_data and "running_id" in running_data:
        return jsonify({
            "status": "error",
            "errorCode": "TEST_ALREADY_RUNNING",
            "message": "A Selenium test is already running. Please wait for it to complete before starting a new one.",
            "data": {
                "running_id": running_data["running_id"]
            }
        }), 429  # HTTP 429 Too Many Requests
    
    # Run Selenium tests in a background thread
    threading.Thread(target=execute_selenium_tests, args=(testsuite_id,)).start()

    # Wait and retry for running_id to become available
    running_data = wait_for_running_id(timeout=10)

    if not running_data:
        return jsonify({
            'status': 'error',
            'errorCode': 'RUNNING_ID_NOT_READY',
            'message': 'Running ID not available after waiting period'
        }), 500  # Internal Server Error

    return jsonify({
        'status': 'success',
        'message': 'Selenium test triggered',
        'data': {
            'testsuite_id': testsuite_id,
            'running_id': running_data['running_id']
        }
    }), 200

@app.route('/selenium/testsuites', methods=['GET'])
def selenium_testsuites():
    testsuites_list = get_testsuites()
    return jsonify({
    'status': 'success',
    'message': 'Selenium test triggered',
    'data': {
        'testsuites': testsuites_list 
    }
}), 200


def clear_sessions():
        session_file=SESSION_FILE
        """Clears the session data by deleting the session file."""
        if os.path.exists(session_file):
            os.remove(session_file)
        session = []  # Clear the in-memory session list

def clear_session_files():
    sessions_path = Path(SESSIONS_FOLDER)
    for session_file in sessions_path.glob("*.json"):
        session_file.unlink()
        
@app.route('/selenium/reset', methods=['DELETE'])
def selenium_reset_run():
    clear_session_files()
    clear_sessions()
    return jsonify({
        'status':'success',
        'message':'Success to reset selenium run'
    }), 200

# Bind to 0.0.0.0 and use dynamic port
if __name__ == "__main__":
    port = int(os.environ.get("FLASK_PORT", 5000))  # Default to 5000 if not set
    app.run(host="0.0.0.0", port=port, debug=True)