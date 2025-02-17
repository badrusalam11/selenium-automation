from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from test.test_objects.web_objects import WebObjects
from test.global_variables.global_variables import GlobalVariables
from test.utils.capture import Capture

@given("I am on the login page")
def step_open_login_page(context):
    context.driver.get(GlobalVariables.BASE_URL)
    Capture.capture_screenshot(context, "login_page")

@when("I log in with valid credentials")
def step_login_with_valid_credentials(context):
    context.driver.find_element(*WebObjects.MENU_BUTTON).click()
    context.driver.find_element(*WebObjects.LOGIN_LINK).click()
    context.driver.find_element(*WebObjects.USERNAME_FIELD).send_keys(GlobalVariables.USERNAME)
    context.driver.find_element(*WebObjects.PASSWORD_FIELD).send_keys(GlobalVariables.PASSWORD)
    Capture.capture_screenshot(context, "fill_all_field")
    context.driver.find_element(*WebObjects.LOGIN_BUTTON).click()

@then("I should see the appointment page")
def step_verify_appointment_page(context):
    assert "Make Appointment" in context.driver.page_source
    Capture.capture_screenshot(context, "make_appointment")
