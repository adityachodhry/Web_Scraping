import requests
import time
import json, re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

username = "Sales@shivacontinental.in"
password = "shiva@1234"
propertyCode = 670
accountId = 3920
seasonCode = 70211
channelId = 101
rateTypeId = 2892
roomId = 1912
roomName = "Deluxe with balcony (Non view | limited parking)"

driver = webdriver.Chrome()

url = 'https://apps.djubo.com/sign-in/'

driver.get(url)

driver.find_element(By.NAME, 'email_address').send_keys(username)
driver.find_element(By.NAME, 'password').send_keys(password)
driver.find_element(By.CLASS_NAME, 'submitBtn').click()

time.sleep(4)

if driver.current_url != url:
    print("Login Successful. The Provided Credentials are Correct.")

    try:
        manage_property_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "li[title='Manage this Property'] a.manage-property"))
        )
        WebDriverWait(driver, 10).until(EC.visibility_of(manage_property_link))
        
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li[title='Manage this Property'] a.manage-property")))

        manage_property_link.click()
        print("Manage this Property page opened!")

        time.sleep(5)  
        driver.refresh()  

        cookies = driver.get_cookies()

        auth_token_7 = next(
            (cookie['value'] for cookie in cookies if cookie['name'] == 'auth_token_7'), None)

        csrftoken = next(
            (cookie['value'] for cookie in cookies if cookie['name'] == 'csrftoken'), None)

        if auth_token_7:
            print(f'auth_token_7: {auth_token_7}')
        else:
            print("auth_token_7 cookie not found.")

        if csrftoken:
            print(f'csrftoken: {csrftoken}')
        else:
            print("csrftoken cookie not found.")
        
        # authorization = (f'auth_token_7={auth_token_7}; csrftoken={csrftoken}')
        # print(authorization)

        url = f"https://apps.djubo.com/rates-admin/accounts/{accountId}/properties/{propertyCode}/rates/rate-plans/{seasonCode}/"

        payload = json.dumps({
        "rates_meta_data": [
            {
            "category": {
                "id": roomId,
                "name": roomName,
                "display_order": 1
            },
            "id": 42286350,
            "occupancy": 1,
            "meal_plan": 1,
            "weekday_sun_rate": 2900,
            "weekday_mon_rate": 2800,
            "weekday_tue_rate": 2800,
            "weekday_wed_rate": 2800,
            "weekday_thu_rate": 2800,
            "weekday_fri_rate": 2800,
            "weekday_sat_rate": 2800,
            "last_updated_utc_timestamp": "2023-10-14T06:08:48.395323+00:00",
            "changedRates": [
                "weekday_sun_rate",
                "weekday_mon_rate",
                "weekday_tue_rate",
                "weekday_wed_rate",
                "weekday_thu_rate",
                "weekday_fri_rate",
                "weekday_sat_rate"
            ],
            "changeOccupancy": True
            }
        ],
        "rate_type_id": rateTypeId,
        "channel_id": channelId,
        "copy_to_all_channel": True,
        "allRateTypeChannelsIds": [
            100,
            101,
            102,
            105,
            102,
            106
        ],
        "check_zero_rates": True
        })

        headers = {
            'cookie': f'auth_token_7={auth_token_7}; csrftoken={csrftoken}',
            'x-requested-with': 'XMLHttpRequest',
            'djng-remote-method': 'update_rate_plan_rates',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code == 200:

            response_content = response.json()
            print(response_content)
            print("Rates Updated Successfully!")
        else:
            print("Failed to update rates.")
    
    except Exception as e:
        print(f"Could not find or click the Manage this Property link: {e}")

else:
    print("Login failed. Please Check Your Username and Password.")

time.sleep(2)

