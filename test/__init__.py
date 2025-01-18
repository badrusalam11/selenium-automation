import os


FEATURE_DIR = os.path.join(os.getcwd(), "test")

# Path constants
REPORTS_PDF_DIR = os.path.join(FEATURE_DIR, "reports", "pdf")
SCREENSHOTS_DIR = os.path.join(FEATURE_DIR, "screenshots")
RESULTS_FILE = os.path.join(FEATURE_DIR, "csv", "test_results.csv")
SESSION_FILE = os.path.join(FEATURE_DIR, "sessions", "current_session.json")