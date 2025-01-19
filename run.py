# run.py
import sys
import os

# Add the project root directory to PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from test.test_suites.test_suite_runner import run_test_suite

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a test suite name (e.g. test_suite_regression).")
        sys.exit(1)
    
    test_suite_name = sys.argv[1]
    run_test_suite(test_suite_name)
