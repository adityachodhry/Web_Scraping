import sys
import time
import random
import requests, json
from seleniumwire import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def staahRatePush(propertyCode, cmCreds, ratesConfig):

    email = cmCreds.get('email')
    password = cmCreds.get('password')

    options = {
        'verify_ssl': False 
    }
    
    driver = webdriver.Chrome(seleniumwire_options=options)

    url = 'https://max.staah.net/hotels/index.php'

    driver.get(url)
    time.sleep(4)

    driver.find_element(By.NAME, 'propertyId').send_keys(propertyCode)
    driver.find_element(By.NAME, 'email').send_keys(email)
    driver.find_element(By.NAME, 'password').send_keys(password)
    
    time.sleep(random.randint(2, 3))

    driver.find_element(By.NAME, 'password').send_keys(Keys.ENTER)

    time.sleep(random.randint(6, 8))

    try:
        close_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[onclick=\"checkGoogleBulletin('N');\"]"))
        )
        driver.execute_script("arguments[0].click();", close_button)
        print("Popup Closed")
    except Exception as e:
        print(f"Popup did not appear or could not be closed: {e}")

    time.sleep(2)

    try:
        max_v2_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.redirectmaxeco.maxv2-btn[title='Redirect to V2']"))
        )
        max_v2_link.click()
        print("Max V2 Page Open!")
    except Exception as e:
        print(f"Could not find or click the Max V2 link: {e}")
    
    time.sleep(2)

    availability_calendar_selector = 'a.nav-link.collapsed.false[href="/hotel/dashboard"]'

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, availability_calendar_selector))
        )
        element.click()
        print('The Availability Calendar Opened Successfully')
    except Exception as e:
        print(f"Error clicking on availability calendar: {e}")

    time.sleep(random.randint(4, 6))

    auth_key = None
    for request in driver.requests:
        if request.response:
            if 'Propertyauthkey' in request.headers:
                auth_key = request.headers['Propertyauthkey']
                print(f"Propertyauthkey: {auth_key}")
                break

    driver.quit()

    if not auth_key:
        print("Authorization key not found.")
        return
    
    for info in ratesConfig.get('info', []):  
        for room in info.get('roomInfo', []):
            roomId = room.get('roomId')
            
            # Check if roomPlanInfo exists
            if 'roomPlanInfo' not in room:
                print(f"Skipping room {roomId}, roomPlanInfo not found")
                continue
            
            for roomPlan in room['roomPlanInfo']:
                # Extract rate and date from roomPlan
                rate = roomPlan.get('roomPlan', {}).get('rate')
                date = roomPlan.get('roomPlan', {}).get('date')

                # Skip if required information is missing
                if not roomId or not rate or not date:
                    print(f"Skipping entry, missing data for room {roomId}")
                    continue

                # Construct the dynamic data payload
                data_dict = {roomId: {date: {"ratevalue": str(rate)}}}
                data_str = json.dumps(data_dict)

                ratePushurl = "https://max2.staah.net/webservice/maxApi.php"

                payload = json.dumps({
                    "module": "availabilityandrates",
                    "mode": "save",
                    "isbulkupdate": "Y",
                    "data": data_str
                })
                
                headers = {
                    'propertyauthkey': auth_key,
                    'origin': 'https://v2.staah.net',
                    'Content-Type': 'application/json'
                }

                response = requests.request("POST", ratePushurl, headers=headers, data=payload)

                print(f"Response for room {roomId}, date {date}: {response.text}")


# # Credentials and rate configuration data
# cmCreds = {
#     "email": "ankur.nograhiya@retvensservices.com",
#     "password": "Retvens@1234567"
# }

# ratesConfig = {
#     "info": [
#         {
#             "roomInfo": [
#                 {
#                     "roomId": "136100",
#                     "roomPlanInfo": [
#                         {
#                             "roomPlan": {
#                                 "rate": 4000,
#                                 "date": "2024-09-13"
#                             }
#                         },
#                         {
#                             "roomPlan": {
#                                 "rate": 4500,
#                                 "date": "2024-09-14"
#                             }
#                         }
#                     ]
#                 }
#             ]
#         },
#         {
#             "roomInfo": [
#                 {
#                     "roomId": "136101",
#                     "roomPlanInfo": [
#                         {
#                             "roomPlan": {
#                                 "rate": 5280,
#                                 "date": "2024-09-13"
#                             }
#                         },
#                         {
#                             "roomPlan": {
#                                 "rate": 5500,
#                                 "date": "2024-09-14"
#                             }
#                         }
#                     ]
#                 }
#             ]
#         }
#     ]
# }

# staahRatePush('5566', cmCreds, ratesConfig)
