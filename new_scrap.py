import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import csv

LOGIN_URL = "https://hypeauditor.com/login/"
DISCOVERY_URL = "https://app.hypeauditor.com/recruiting/influencer-discovery?hash=4f965fa12eca686b41eaeccfcaabca8f&search_hash=c688bc170db0804e9e809cc89ab2de31"
EMAIL = "ayush@dollarpe.com"
PASSWORD = "Aa@9300064885"

driver = webdriver.Chrome()

def login_to_hypeauditor(driver):
    driver.get(LOGIN_URL) # Open hyperauditor.com
    try:
        email_input = WebDriverWait(driver, 50).until(
            EC.visibility_of_element_located((By.NAME, 'email'))
        ) # Wait for email feild to be visible
        
        email_input.send_keys(EMAIL) # Populate input field

        password_input = WebDriverWait(driver, 50).until(
            EC.visibility_of_element_located((By.NAME, 'password'))
        ) # Wait for password field to be visible

        password_input.send_keys(PASSWORD) # Populate input field
        
        password_input.send_keys(Keys.RETURN) # Press enter
        time.sleep(5) # Wait for browser to login
        driver.get(DISCOVERY_URL) # Navigate to target url

        csv_headers = [["name", "handle", "followers", "quality_audience", "engagement_rate", "united_states_%", "audience_age", "indian_%"]]
        with open('data.csv', 'a+', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerows(csv_headers) # Creates CSV with headers

        scrape_user_data(driver) # Starts scraping the first page
    except Exception as e:
        raise e
    

def scrape_user_data(driver):
    time.sleep(10)
    data_list = []
    try:
        total_rows = 3
        for row in range(total_rows):
            data_row_list = []        
            name = driver.find_element(By.XPATH, f'//*[@id="app"]/main/div[3]/div/div/div[2]/div[4]/div/div[2]/div/div[3]/table/tbody/tr[{row+1}]/td[2]/div/div/div[1]/div/div/div/div[2]/div/div[1]/a/span')
            data_row_list.append(name.text)

            handle = driver.find_element(By.XPATH, f'//*[@id="app"]/main/div[3]/div/div/div[2]/div[4]/div/div[2]/div/div[3]/table/tbody/tr[{row+1}]/td[2]/div/div/div[1]/div/div/div/div[2]/div/div[2]/span')
            data_row_list.append(handle.text)

            followers = driver.find_element(By.XPATH, f'//*[@id="app"]/main/div[3]/div/div/div[2]/div[4]/div/div[2]/div/div[3]/table/tbody/tr[{row+1}]/td[3]/div/text()')
            data_row_list.append(followers)

            quality_audience = driver.find_element(By.XPATH, f'//*[@id="app"]/main/div[3]/div/div/div[2]/div[4]/div/div[2]/div/div[3]/table/tbody/tr[{row+1}]/td[4]/div/text()')
            data_row_list.append(quality_audience)

            engagement_rate = driver.find_element(By.XPATH, f'//*[@id="app"]/main/div[3]/div/div/div[2]/div[4]/div/div[2]/div/div[3]/table/tbody/tr[{row+1}]/td[5]/div/text()')
            data_row_list.append(engagement_rate)

            united_states_perc = driver.find_element(By.XPATH, f'//*[@id="app"]/main/div[3]/div/div/div[2]/div[4]/div/div[2]/div/div[3]/table/tbody/tr[{row+1}]/td[9]/div/text()')
            data_row_list.append(united_states_perc)

            audience_age = driver.find_element(By.XPATH, f'//*[@id="app"]/main/div[3]/div/div/div[2]/div[4]/div/div[2]/div/div[3]/table/tbody/tr[{row+1}]/td[10]/div/text()')
            data_row_list.append(audience_age)

            indian_perc = driver.find_element(By.XPATH, f'//*[@id="app"]/main/div[3]/div/div/div[2]/div[4]/div/div[2]/div/div[3]/table/tbody/tr[{row+1}]/td[11]/div/text()')
            data_row_list.append(indian_perc)

            data_list.append(data_row_list)

            with open('data.csv', 'a+', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerows(data_list) # Creates CSV with headers
    except Exception as e:
        raise e


try:
    login_to_hypeauditor(driver)
finally:
    driver.quit()
