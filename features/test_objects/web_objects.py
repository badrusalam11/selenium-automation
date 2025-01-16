from selenium.webdriver.common.by import By

class WebObjects:
    MENU_BUTTON = (By.ID, "menu-toggle")  # Hamburger menu button
    LOGIN_LINK = (By.LINK_TEXT, "Login")  # Login link
    USERNAME_FIELD = (By.ID, "txt-username")  # Username input
    PASSWORD_FIELD = (By.ID, "txt-password")  # Password input
    LOGIN_BUTTON = (By.ID, "btn-login")  # Login button
