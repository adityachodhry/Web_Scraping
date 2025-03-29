import requests
import time
import json, re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime


def djuboRatePush(username, password, propertyCode):

    driver = webdriver.Chrome()

    url = 'https://apps.djubo.com/sign-in/'

    driver.get(url)

    driver.find_element(By.NAME, 'email_address').send_keys(username)
    driver.find_element(By.NAME, 'password').send_keys(password)
    driver.find_element(By.CLASS_NAME, 'submitBtn').click()

    time.sleep(4)

    if driver.current_url != url:
        print("Login Successful.")

    try:
        manage_property_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "li[title='Manage this Property'] a.manage-property"))
        )
        manage_property_link.click()
        print("Clicked 'Manage this Property' link.")
    except Exception as e:
        print("Error while clicking 'Manage this Property':", e)
    
    time.sleep(5)
    driver.refresh()

    cookies = driver.get_cookies()
    auth_token_7 = next((cookie['value'] for cookie in cookies if cookie['name'] == 'auth_token_7'), None)
    print("Auth token", auth_token_7)
    csrftoken = next((cookie['value'] for cookie in cookies if cookie['name'] == 'csrftoken'), None)
    
    accountIdEndpoint = "https://apps.djubo.com/core-data/properties"

    headers = {
        'cookie': f'auth_token_7={auth_token_7}',
        'x-requested-with': 'XMLHttpRequest',
        'djng-remote-method': 'update_rate_plan_rates'
    }

    response = requests.get(accountIdEndpoint, headers=headers)

    if response.status_code == 200:
        result_data = response.json()

        if isinstance(result_data, list) and len(result_data) > 0:
            first_item = result_data[0]
            accountId = first_item['account_id']
            print("AccountID:", accountId)
        
            roomIdEndpoint = "https://apps.djubo.com/core-data/properties"
            headers = {
                'cookie': f'auth_token_7={auth_token_7}',
                'x-requested-with': 'XMLHttpRequest',
                'djng-remote-method': 'update_rate_plan_rates'
            }
            response = requests.get(roomIdEndpoint, headers=headers)

            if response.status_code == 200:
                result_data = response.json()

                if isinstance(result_data, list) and len(result_data) > 0:
                    first_item = result_data[0]
                    accountId = first_item['account_id']
                    propertyCode = first_item['id']
                    propertyName = first_item['name']
                    print(propertyName)
                    data_slot = first_item.get('room_categories', [])


djuboRatePush('Sales@shivacontinental.in', 'shiva@1234', 670)