import threading
from flask import jsonify, make_response

from app.function.test_run import execute_selenium_tests, load_running_id, wait_for_running_id
from app.function.test_suites import get_testsuites
from app.function.session import clear_session_files, clear_sessions


def test_run(payload):
    testsuite_id = payload.get('testsuite_id') if payload else None
    email = payload.get('email') if payload else None
    
    # check if testsuite_id is empty
    if not testsuite_id:
        return make_response(jsonify({
            "status": "error",
            "errorCode": "INVALID_REQUEST",
            "message": "testsuite_id is required"
        }), 400)
    
    #check if the testsuite exist
    testsuite_list = get_testsuites()
    if testsuite_id not in testsuite_list:
        return make_response(jsonify({
            "status": "error",
            "errorCode": "INVALID_TESTSUITE",
            "message": "testsuite_id is not valid"
        }), 404)
    
    # check running id first
    running_data = load_running_id()
    if running_data and "running_id" in running_data:
        return make_response(jsonify({
            "status": "error",
            "errorCode": "TEST_ALREADY_RUNNING",
            "message": "A Selenium test is already running. Please wait for it to complete before starting a new one.",
            "data": {
                "running_id": running_data["running_id"]
            }
        }), 429) # HTTP 429 Too Many Requests
    # Run Selenium tests in a background thread
    threading.Thread(target=execute_selenium_tests, args=(testsuite_id,)).start()

    # Wait and retry for running_id to become available
    running_data = wait_for_running_id(timeout=10)

    if not running_data:
        return make_response(jsonify({
            'status': 'error',
            'errorCode': 'RUNNING_ID_NOT_READY',
            'message': 'Running ID not available after waiting period'
        }), 500) # Internal Server Error

    return make_response(jsonify({
        'status': 'success',
        'message': 'Selenium test triggered',
        'data': {
            'testsuite_id': testsuite_id,
            'running_id': running_data['running_id']
        }
    }), 200)

def clear_test_run():
    clear_session_files()
    clear_sessions()
    return make_response(jsonify({
        'status':'success',
        'message':'Success to reset selenium run'
    }), 200)