import os

TEST_DIR = os.path.join(os.getcwd(), "test")

# Path constants
REPORTS_PDF_FOLDER = os.path.join(TEST_DIR, "reports", "pdf")
SCREENSHOTS_DIR = os.path.join(TEST_DIR, "screenshots")
RESULTS_FILE = os.path.join(TEST_DIR, "csv", "test_results.csv")
RUNNING_ID_FILE = os.path.join(TEST_DIR, "sessions", "running_id.json")
SESSION_FILE = os.path.join(TEST_DIR, "sessions", "current_session.json")
SESSIONS_FOLDER = os.path.join(TEST_DIR, "sessions")
REPORTS_JSON_FOLDER = os.path.join(TEST_DIR, "reports", "json")
PROPERTIES_FILE = os.path.join(os.getcwd(), "test.properties")
CONFIG_FILE = os.path.join(os.getcwd(), "config.json")
BIND_TEST_CASE_FOLDER = os.path.join(TEST_DIR, "bind_test_case")

from test.utils.config import Config
Config.ensure_folders_exist()
PROPERTIES_DATA=Config.load_properties()
CONFIG_DATA=Config.load_config(CONFIG_FILE)
print(CONFIG_DATA)