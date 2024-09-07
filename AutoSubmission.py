from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from dotenv import load_dotenv
import os

load_dotenv()

url = "https://waterlooworks.uwaterloo.ca/waterloo.htm?action=login"
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

driver = webdriver.Firefox()
driver.get(url)

driver.implicitly_wait(10)

# Login Page
driver.find_element(By.ID, "userNameInput").send_keys(username)
driver.find_element(By.ID, "nextButton").click()
driver.find_element(By.ID, "passwordInput").send_keys(password)
driver.find_element(By.ID, "submitButton").click()

# DUO Verification Page
DUO_passcode = driver.find_element(By.CSS_SELECTOR, "div.row:nth-child(3)").text

print("Please use passcode to verify through DUO Mobile within 10 minute: ", DUO_passcode);

# Trust Browser Page
WebDriverWait(driver, 600).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#dont-trust-browser-button"))
)
driver.find_element(By.CSS_SELECTOR, "#dont-trust-browser-button").click()

# WaterlooWorks Homepage
WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/header/div[2]/div/div/div/div/a"))
)
driver.fullscreen_window()
# driver.find_element(By.XPATH, "/html").screenshot("homepage.png")

# Open Jobs Page
driver.get("https://waterlooworks.uwaterloo.ca/myAccount/co-op/full/jobs.htm")
# driver.find_element(By.XPATH, "/html").screenshot("jobs_page.png")

