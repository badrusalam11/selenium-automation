# this environment act as test_listener like Katalon
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def before_scenario(context, scenario):
    print("Before Scenario Hook")
    chrome_service = Service(ChromeDriverManager().install())
    context.driver = webdriver.Chrome(service=chrome_service)
    context.driver.maximize_window()

def after_scenario(context, scenario):
    print("After Scenario Hook")
    context.driver.quit()


def before_test_suite():
    pass

def after_test_suite():
    pass