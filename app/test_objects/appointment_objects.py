from selenium.webdriver.common.by import By

class AppointmentObjects:
    select_facility = (By.XPATH, "//select[@name='facility']")  # Hamburger menu button
    check_box_apply_readmission = (By.ID, "chk_hospotal_readmission")
    input_radio_program = (By.NAME, "programs")
    date_visite_date = (By.ID, "txt_visit_date")
    text_area_comment = (By.NAME, "comment")
    button_submit = (By.ID, "btn-book-appointment")
    p_confirmation_subtitle = (By.XPATH, "//p[@class='lead']")