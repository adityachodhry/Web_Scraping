import time
import json
import requests
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def eGlobeRoomConfig(username, password):
    driver = webdriver.Chrome()
    login_url = 'https://www.eglobe-solutions.com/hms/dashboard'
    driver.get(login_url)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'Username')))
    driver.find_element(By.NAME, 'Username').send_keys(username)
    driver.find_element(By.NAME, 'Password').send_keys(password)
    driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-success.btn-block[name="button"][value="login"]').click()

    time.sleep(5)  
    if "Invalid username or password" in driver.page_source:
        print("Login Unsuccessful")
        driver.quit()
        return

    token = None
    for request in driver.requests:
        if request.response and 'authorization' in request.headers:
            token = request.headers['authorization']
            break
    
    if not token:
        print("Failed to retrieve authorization token")
        driver.quit()
        return

    url = "https://www.eglobe-solutions.com/cmapi/derivedpricing/setupinfo"
    headers = {
        'authorization': token
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response_data = response.json()

        processed_rooms = {}
        
        data_slot = response_data.get('RatePlans', [])
        for roomConfig in data_slot:
            room_id = roomConfig.get('RoomId')
            room_name = roomConfig.get('RoomName')

            rate_plan = {
                "ratePlanName": roomConfig.get('RatePlanName'),
                "ratePlanCode": roomConfig.get('RatePlanId'),
                "maxOccupancy": roomConfig.get('Occupancy'),
                "derived": roomConfig.get('DerivedPrice'),
                "rateTypeCode": roomConfig.get('RateTypeId'),
                "priceDiffPlusMinus": roomConfig.get('PriceDiffPlusMinus'),
                "PriceDiff": roomConfig.get('PriceDiff'),
                "isSelected": roomConfig.get('IsSelected')
            }

            if room_id not in processed_rooms:
                processed_rooms[room_id] = {
                    "roomCode": room_id,
                    "roomName": room_name,
                    "ratePlans": []
                }
            
            processed_rooms[room_id]["ratePlans"].append(rate_plan)

        processed_rooms_list = list(processed_rooms.values())

        with open('processed_response.json', 'w') as json_file:
            json.dump(processed_rooms_list, json_file, indent=4)
        
        print("Data successfully saved to 'processed_response.json'.")
        
        return processed_rooms_list

    driver.quit()

eGlobeRoomConfig('akshay01', 'akshay0120')
