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

def before_scenario(context, scenario):
    print("Before Scenario Hook")
    chrome_service = Service(ChromeDriverManager().install())
    context.driver = webdriver.Chrome(service=chrome_service)
    context.driver.maximize_window()
    # Store feature, scenario details
    context.feature_name = scenario.feature.name
    context.scenario_name = scenario.name
    context.start_time = int(time.time() * 1000)  # Start time in milliseconds
    context.steps = []
    # Manage sessions
    session_manager.append_session(context.driver.session_id)
    context.session_id = context.driver.session_id

def before_step(context, step):
    # Capture the start time of the step in milliseconds
    context.step_start_time = int(time.time() * 1000)

def after_step(context, step):
    # Log step details with time in milliseconds
    step_data = step_data = Report.construct_step_data(step, context.step_start_time)
    context.steps.append(step_data)

def after_scenario(context, scenario):
    print("After Scenario Hook")
    context.driver.quit()
    # Prepare scenario data
    scenario_data = Report.create_scenario_data(context, scenario)
    # Save scenario data to a session file
    Report.save_scenario_data(context.session_id, scenario_data)

def before_test_suite():
    session_manager.clear_session_files()

def after_test_suite():
    print("After Test Suite Hook")
    # Collect all scenario data, but exclude 'current_session.json'
    all_scenarios = Report.collect_all_scenarios_excluding_current()
    # Save consolidated report
    Report.generate_json_report(all_scenarios)
    Report.generate_pdf_report(session_manager.load_sessions())
    # Optionally clear session files after generating the report
    session_manager.clear_session_files()