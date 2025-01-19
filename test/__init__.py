import os

FEATURE_DIR = os.path.join(os.getcwd(), "test")

# Path constants
REPORTS_PDF_FOLDER = os.path.join(FEATURE_DIR, "reports", "pdf")
SCREENSHOTS_DIR = os.path.join(FEATURE_DIR, "screenshots")
RESULTS_FILE = os.path.join(FEATURE_DIR, "csv", "test_results.csv")
SESSION_FILE = os.path.join(FEATURE_DIR, "sessions", "current_session.json")
SESSIONS_FOLDER = os.path.join(FEATURE_DIR, "sessions")
REPORTS_JSON_FOLDER = os.path.join(FEATURE_DIR, "reports", "json")
PROPERTIES_FILE = os.path.join(os.getcwd(), "test.properties")

from test.utils.config import Config
Config.ensure_folders_exist()
PROPERTIES_DATA=Config.load_properties()