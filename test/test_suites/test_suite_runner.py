# test_suite_runner.py
import os
import sys

from test.environment import after_test_suite, before_test_suite

def run_test_suite(test_suite_name):
    before_test_suite()
    # Define the path to the test suites directory
    test_suites_dir = os.path.join(os.path.dirname(__file__))
    print(test_suites_dir)
    # Construct the test suite file path dynamically
    test_suite_file = os.path.join(test_suites_dir, f"{test_suite_name}.py")
    
    if not os.path.exists(test_suite_file):
        print(f"Test suite '{test_suite_name}' not found.")
        return
    
    # Dynamically import and run the selected test suite
    sys.path.insert(0, test_suites_dir)  # Add test_suites directory to Python path
    
    test_suite_module = __import__(test_suite_name)
    test_suite_module.run_suite()
    after_test_suite()
