from behave import given, when, then
from app.test_objects.web_objects import WebObjects
from app.test_objects.appointment_objects import AppointmentObjects
from app.global_variables.global_variables import GlobalVariables
from selenium.webdriver.support.ui import Select


@given("I am already the logged in")
def step_already_logged_in(context):
    context.driver.get(GlobalVariables.BASE_URL)
    context.driver.find_element(*WebObjects.MENU_BUTTON).click()
    context.driver.find_element(*WebObjects.LOGIN_LINK).click()
    context.driver.find_element(*WebObjects.USERNAME_FIELD).send_keys(GlobalVariables.USERNAME)
    context.driver.find_element(*WebObjects.PASSWORD_FIELD).send_keys(GlobalVariables.PASSWORD)
    context.driver.find_element(*WebObjects.LOGIN_BUTTON).click()

@when("I fill all the required field")
def step_fill_appointment_field(context):
    select_facility = context.driver.find_element(*AppointmentObjects.select_facility)
    dropdown = Select(select_facility)
    # Select an option by visible text
    dropdown.select_by_visible_text("Hongkong CURA Healthcare Center")
    context.driver.find_element(*AppointmentObjects.check_box_apply_readmission).click()
    context.driver.find_element(*AppointmentObjects.input_radio_program).click()
    context.driver.find_element(*AppointmentObjects.date_visite_date).send_keys("17/01/2024")
    context.driver.find_element(*AppointmentObjects.text_area_comment).send_keys("This is the appointment")
    context.driver.find_element(*AppointmentObjects.button_submit).click()

@then("I see 'Appointment Confirmation' page")
def step_verify_appointment_confirmation(context):
    assert "Appointment Confirmation" in context.driver.page_source
