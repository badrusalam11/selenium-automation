# this environment act as test_listener like Katalon
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from test.utils.report import Report
from test.utils.session_manager import session_manager  # Import the session manager

def before_scenario(context, scenario):
    print("Before Scenario Hook")
    chrome_service = Service(ChromeDriverManager().install())
    context.driver = webdriver.Chrome(service=chrome_service)
    context.driver.maximize_window()

    # Append session_id using the singleton
    session_manager.append_session(context.driver.session_id)
    print(f"SESSION after appending: {session_manager.get_sessions()}")

def after_scenario(context, scenario):
    print("After Scenario Hook")
    context.driver.quit()

def before_test_suite():
    session_manager.clear_sessions()

def after_test_suite():
    print("After Test Suite SESSION: ", session_manager.load_sessions())
    Report.generate_pdf_report(session_manager.load_sessions())
    session_manager.clear_sessions()  # Optionally clear session after the suite
