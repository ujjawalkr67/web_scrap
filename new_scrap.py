import time
import json
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Configure logging
logging.basicConfig(level=logging.INFO)

# Credentials and URL
LOGIN_URL = "https://hypeauditor.com/login/"
#DISCOVERY_URL = "https://app.hypeauditor.com/recruiting/influencer-discovery"
DISCOVERY_URL = "https://app.hypeauditor.com/recruiting/influencer-discovery?hash=8434571c5e40fe14f252973662c77a7d&search_hash=b115de6d22a3e00fb666f68642114499"
EMAIL = "20ics067@gbu.ac.in"
PASSWORD = "maddy@1234"

# Setting up Selenium WebDriver
driver = webdriver.Chrome()

# Step 1: Log in to the website
def login_to_hypeauditor(driver):
    logging.info("Navigating to login page...")
    driver.get(LOGIN_URL)
    
    # Debugging: Capture a screenshot of the login page
    #driver.save_screenshot('login_page_before_wait.png')
    
    try:
        # Wait for the email input to be visible
        logging.info("Waiting for email input field to be visible...")
        email_input = WebDriverWait(driver, 50).until(
            EC.visibility_of_element_located((By.NAME, 'email'))
        )
        
        # Enter email
        logging.info("Entering email...")
        email_input.send_keys(EMAIL)
        
        # Wait for the password input to be visible
        logging.info("Waiting for password input field to be visible...")
        password_input = WebDriverWait(driver, 50).until(
            EC.visibility_of_element_located((By.NAME, 'password'))
        )
        
        # Enter password
        logging.info("Entering password...")
        password_input.send_keys(PASSWORD)
        
        # Submit the login form
        logging.info("Submitting the login form...")
        password_input.send_keys(Keys.RETURN)
        
        # Debugging: Capture another screenshot after submitting the form
        #driver.save_screenshot('login_page_after_submission.png')
        
        # Wait for the discovery page to load after login
        logging.info("Waiting for discovery page to load...")
        # WebDriverWait(driver, 50).until(
        #     EC.url_to_be(DISCOVERY_URL)
        # )
        driver.get(DISCOVERY_URL)
        
        logging.info("Successfully logged in and navigated to discovery page.")
        
    except Exception as e:
        logging.error(f"An error occurred during login: {e}")
        driver.save_screenshot('login_error.png')
        # Capture page source for debugging
        with open("login_error_page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        raise e
    

def scrape_user_data(driver):
    try:
        
        logging.info("Locating the user row in the table...")
        user_row = driver.find_element(By.CLASS_NAME, 'table__td user')

        name_element = user_row.find_element(By.CSS_SELECTOR, 'span.text.--theme-default.--size-md.--weight-semibold')
        user_name = name_element.text

        id_element = user_row.find_element(By.CSS_SELECTOR, 'span.text.--theme-gray-300.--size-md.--weight-regular')
        user_id = id_element.text
        
   
        user_data = {
            "name": user_name,
            "id": user_id
        }
        
        with open('user_data.json', 'w') as json_file:
            json.dump(user_data, json_file, indent=4)
        
        logging.info(f"Scraped data: {user_data}")
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        driver.save_screenshot('scraping_error.png')
        raise e     


try:
    login_to_hypeauditor(driver)
  
    time.sleep(5)  

    # Call the scraping function
    scrape_user_data(driver)
finally:
    driver.quit()
