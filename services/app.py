from datetime import datetime
import os
from flask import Flask, request

from app.controller.test_suites import test_suite_detail, test_suites
from app.controller.test_run import clear_test_run, test_run
from app import logger

app = Flask(__name__)

@app.route('/selenium/run', methods=['POST'])
def selenium_run():
    # Parse JSON payload.
    payload = request.get_json()
    logger.info('payload', payload)
    print(payload)
    result = test_run(payload)
    return result
    

@app.route('/selenium/testsuites', methods=['GET'])
def selenium_testsuites():
    result = test_suites()
    return result

@app.route('/selenium/testsuite/detail', methods=['POST'])
def selenium_testsuite_detail():
    payload = request.get_json()
    print(payload)
    result = test_suite_detail(payload)
    return result

@app.route('/selenium/reset', methods=['DELETE'])
def selenium_reset_run():
    result = clear_test_run()    
    return result

# Bind to 0.0.0.0 and use dynamic port
if __name__ == "__main__":
    port = int(os.environ.get("FLASK_PORT", 5000))  # Default to 5000 if not set
    app.run(host="0.0.0.0", port=port, debug=True)