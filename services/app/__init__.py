import os

from app.function.log import setup_log

TEST_DIR = os.path.join(os.getcwd(), "test")
SERVICES_DIR = os.path.join(os.getcwd(), "services")
APP_DIR = os.path.join(SERVICES_DIR,"app")
RUNNING_ID_FILE = os.path.join(TEST_DIR, "sessions", "running_id.json")
TEST_SUITES_DIR = os.path.join(TEST_DIR, "test_suites")
SESSION_FILE = os.path.join(TEST_DIR, "sessions", "current_session.json")
SESSIONS_FOLDER = os.path.join(TEST_DIR, "sessions")
BIND_TEST_CASE_FOLDER = os.path.join(TEST_DIR, "bind_test_case")
FEATURE_DIR = os.path.join(TEST_DIR, "features")
PROPERTIES_FILE = os.path.join(os.getcwd(), "test.properties")

LOG_FOLDER = os.path.join(APP_DIR, 'logs')
logger, LOG_FILE_NAME = setup_log(LOG_FOLDER)
