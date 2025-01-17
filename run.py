import sys
import os

# Add the project root directory to PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.test_suites.test_suite_runner import run_test_suite

if __name__ == "__main__":
    run_test_suite()
