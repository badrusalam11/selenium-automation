# this environment act as test_listener like Katalon
import os
import json
from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from test.utils.session_manager import session_manager  # Import the session manager
from webdriver_manager.chrome import ChromeDriverManager
from test.utils.report import Report
from test.utils.event import EventUtil
from selenium.webdriver.chrome.options import Options
from test import CONFIG_DATA


def before_scenario(context, scenario):
    print("Before Scenario Hook")
    chrome_service = Service(ChromeDriverManager().install())
    chrome_options = Options()
    if CONFIG_DATA['environment']=='stagging':
        chrome_options.add_argument("--no-sandbox")  # Required inside Docker
        chrome_options.add_argument("--disable-dev-shm-usage")  # Helps avoid memory issues
        chrome_options.add_argument("--headless")  # Optional: Run Chrome in headless mode
        chrome_options.add_argument("--remote-debugging-port=9222")  # Debugging
        chrome_options.add_argument("--user-data-dir=/tmp/chrome-user-data")  # Unique profile
    context.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    context.driver.maximize_window()
    # Store feature, scenario details
    context.feature_name = scenario.feature.name
    context.scenario_name = scenario.name
    context.start_time = int(time.time() * 1000)  # Start time in milliseconds
    context.steps = []
    context.images = []
    # Manage sessions
    session_manager.append_session(context.driver.session_id)
    context.session_id = context.driver.session_id

def before_step(context, step):
    # Capture the start time of the step in milliseconds
    context.step_start_time = int(time.time() * 1000)

def after_step(context, step):
    print("after step", context.images)
    # Log step details with time in milliseconds
    step_data = Report.construct_step_data(step, context.step_start_time, context.images)
    context.steps.append(step_data)
    # Clear images for the next step
    context.images = []

def after_scenario(context, scenario):
    print("After Scenario Hook")
    context.driver.quit()
    # Prepare scenario data
    scenario_data = Report.create_scenario_data(context, scenario)
    # Save scenario data to a session file
    Report.save_scenario_data(context.session_id, scenario_data)

def before_test_suite():
    session_manager.clear_session_files()
    session_manager.generate_running_id()
    running_data = session_manager.load_running_id()
    print("Before Test Suite Hook")
    print("Running test for id: ", running_data['running_id'] + "...")

def after_test_suite():
    print("After Test Suite Hook")
    # Collect all scenario data, but exclude 'current_session.json'
    all_scenarios = Report.collect_all_scenarios_excluding_current()
    # Save consolidated report
    event = EventUtil()
    event.after_test_suite(all_scenarios)
    # Optionally clear session files after generating the report
    session_manager.clear_session_files()
    session_manager.clear_running_id()