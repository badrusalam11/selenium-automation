from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def before_scenario(context, scenario):
    print("Before Scenario Hook")
    chrome_service = Service(ChromeDriverManager().install())
    context.driver = webdriver.Chrome(service=chrome_service)

def after_scenario(context, scenario):
    print("After Scenario Hook")
    context.driver.quit()

