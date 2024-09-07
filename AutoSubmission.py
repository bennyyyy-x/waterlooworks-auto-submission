from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
import time
from dotenv import load_dotenv
import os
import re

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

print("Please use passcode to verify through DUO Mobile within 10 minute: ", DUO_passcode)

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

# Open Jobs Page
driver.get("https://waterlooworks.uwaterloo.ca/myAccount/co-op/full/jobs.htm")

# Open Shortlist Page
driver.find_element(By.XPATH, "/html/body/main/div[2]/div/div/div/div[2]/div[3]/div[1]/div/div[2]/div/div/div/div/table[2]/tbody/tr[3]/td[2]/a").click()

# Find the "Current tab/New tab" dropdown
postings = driver.find_elements(By.CSS_SELECTOR, ".btn-group")

print(f"postings: {postings}")

for posting in postings:
    view_button = posting.find_element(By.TAG_NAME, 'a')
    driver.execute_script("arguments[0].scrollIntoView();", view_button)
    view_button.click()

    new_tab_button = posting.find_element(By.CSS_SELECTOR, 'ul.dropdown-menu li:nth-child(2) a')
    new_tab_button.click()

    all_tabs = driver.window_handles

    # Switch to new tab
    driver.switch_to.window(all_tabs[1])

    required_documents = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "np-posting-documents-required"))
    ).get_attribute("innerHTML")
    print(f"Required Documents: {required_documents}")

    need_resume = "Resume" in required_documents or "Résumé" in required_documents
    need_cover_letter = "Cover Letter" in required_documents

    if not need_cover_letter:
        # Go to the application page
        apply_button = driver.find_element(By.CSS_SELECTOR, ".btn__default--text.btn--default.applyButton.clickGuard")
        driver.execute_script("arguments[0].scrollIntoView();", apply_button)

        try:
            apply_button.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].click();", apply_button)

        # Select the default package
        try:
            default_package_button = driver.find_element(By.CSS_SELECTOR, "div.panel:nth-child(1) > div:nth-child(1) > label:nth-child(1) > input:nth-child(1)")
        except NoSuchElementException:
            print("No default package button found")
            driver.close()
            driver.switch_to.window(all_tabs[0])
            continue
        driver.execute_script("arguments[0].scrollIntoView();", default_package_button)
        default_package_button.click()

        # Submit the application
        submit_button = driver.find_element(By.CLASS_NAME, "sel_SubmitApplications")
        driver.execute_script("arguments[0].scrollIntoView();", submit_button)
        submit_button.click()
        print("Successfully submitted application")

    # Close this job posting and go back to the shortlist page
    driver.close()
    driver.switch_to.window(all_tabs[0])


