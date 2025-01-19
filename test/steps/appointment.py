from behave import given, when, then
from test.test_objects.web_objects import WebObjects
from test.test_objects.appointment_objects import AppointmentObjects
from test.global_variables.global_variables import GlobalVariables
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import time
from test.data_files.script.appointment_datafile import AppointmentData
from utils.capture import Capture

appointment_data = AppointmentData.get_appointment_data()
print(appointment_data)

@given("I am already the logged in")
def step_already_logged_in(context):
    context.driver.get(GlobalVariables.BASE_URL)
    context.driver.find_element(*WebObjects.MENU_BUTTON).click()
    context.driver.find_element(*WebObjects.LOGIN_LINK).click()
    context.driver.find_element(*WebObjects.USERNAME_FIELD).send_keys(GlobalVariables.USERNAME)
    context.driver.find_element(*WebObjects.PASSWORD_FIELD).send_keys(GlobalVariables.PASSWORD)
    Capture.capture_screenshot(context, "login")
    context.driver.find_element(*WebObjects.LOGIN_BUTTON).click()

@when("I fill all the required field with data in {row}")
def step_fill_appointment_field(context, row):
    data = appointment_data[int(row)]
    select_facility = context.driver.find_element(*AppointmentObjects.select_facility)
    dropdown = Select(select_facility)
    # Select an option by visible text
    dropdown.select_by_visible_text(data['facility'])
    context.driver.find_element(*AppointmentObjects.check_box_apply_readmission).click()
    radio_buttons = context.driver.find_elements(*AppointmentObjects.input_radio_program)
    for radio_button in radio_buttons:
        if radio_button.get_attribute("value") == data['healthcare_program']:
            radio_button.click()
            break
    context.driver.find_element(*AppointmentObjects.date_visite_date).send_keys(data['visit_date'])
    context.driver.find_element(*AppointmentObjects.text_area_comment).click()
    context.driver.find_element(*AppointmentObjects.text_area_comment).send_keys(data['comment'])
    Capture.capture_screenshot(context, "fill")
    context.driver.find_element(*AppointmentObjects.button_submit).click()

@then("I see 'Appointment Confirmation' page")
def step_verify_appointment_confirmation(context):
    Capture.capture_screenshot(context, "confirmation_page")
    assert "Appointment Confirmation" in context.driver.page_source
