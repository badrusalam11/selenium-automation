from datetime import datetime
import os
import sys
from flask import Flask, request, jsonify
import subprocess
import threading

app = Flask(__name__)

def execute_selenium_tests(testsuite_id):
    """
    Execute the Selenium tests. You can implement your Selenium
    testing logic here or trigger a separate script that runs the tests.
    For example, you might run a script like:
    
        python run.py <testsuite_id>
    
    This example uses subprocess to run an external script.
    """
    try:
        # Build the command. Adjust this command as needed for your setup.
        command = [sys.executable, "run.py", testsuite_id]
        current_directory = os.getcwd()
        print("Current directory:", current_directory)
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=current_directory
        )
        
        # Log output for debugging purposes.
        print("Selenium Test Output:", result.stdout)
        if result.stderr:
            print("Selenium Test Error:", result.stderr)
    except Exception as e:
        print(f"Error while running Selenium tests: {e}")

@app.route('/selenium/run', methods=['POST'])
def selenium_run():
    # Parse JSON payload.
    payload = request.get_json()
    testsuite_id = payload.get('testsuite_id') if payload else None

    if not testsuite_id:
        return jsonify({'error': 'testsuite_id is required'}), 400

    # Run the selenium test in a background thread so the API response is not delayed.
    threading.Thread(target=execute_selenium_tests, args=(testsuite_id,)).start()
    running_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return jsonify({'message': 'Selenium test triggered', 'testsuite_id': testsuite_id, 'running_id':running_id}), 200

if __name__ == '__main__':
    # Note: Flask's built-in server is for development only.
    app.run(debug=True)
