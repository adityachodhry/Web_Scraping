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
from pymongo import MongoClient

def staahRoomConfig():
    
    client = MongoClient("mongodb+srv://Retvens:JMdZt2hEPsqHuVQl@r-rate-shopper-cluster.nlstcxk.mongodb.net/")
    db = client["ratex"]
    collection = db['channelmanagers']

    properties = collection.find({'cmId': 108})

    for property in properties:
        userCredential = property.get("userCredential")
        email = userCredential.get('email')
        password = userCredential.get('password')
        propertyId = property.get('channelManagerHotelId')

        if not (email and password and propertyId):
            print(f"Incomplete data for propertyId: {propertyId}")
            continue

        print(f"Processing propertyId: {propertyId}")

        options = {
            'verify_ssl': False
        }
        driver = webdriver.Chrome(seleniumwire_options=options)

        url = 'https://max.staah.net/hotels/index.php'
        driver.get(url)
        time.sleep(4)

        driver.find_element(By.NAME, 'propertyId').send_keys(propertyId)
        driver.find_element(By.NAME, 'email').send_keys(email)
        driver.find_element(By.NAME, 'password').send_keys(password)
        
        time.sleep(random.randint(2, 3))
        driver.find_element(By.NAME, 'password').send_keys(Keys.ENTER)
        time.sleep(random.randint(2, 4))

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

        time.sleep(random.randint(2, 4))

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
            continue  

        today = datetime.now()
        current_date = today.strftime("%Y-%m-%d")

        endpoint = "https://max2.staah.net/webservice/maxApi.php"
        payload = json.dumps({
            "module": "availabilityandrates",
            "mode": "getavailablity",
            "startdate": current_date,
            "fromdeals": "yes",
            "rmdata": "",
            "tagarray": "",
            "readOnly": "Y"
        })

        headers = {
            'Propertyauthkey': auth_key,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'Origin': 'https://v2.staah.net',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", endpoint, headers=headers, data=payload)

        if response.status_code == 403:
            print("Access denied. Check your credentials, headers, and ensure your IP is not blocked.")
            continue

        if response.text:
            try:
                response_data = json.loads(response.text)
            except json.JSONDecodeError as e:
                print(f"JSONDecodeError: {e}")
                print("Response text:", response.text)
                continue
        else:
            print("Empty response received")
            continue

        row_data = response_data.get('data', {}).get('deals_data', {}).get('row', {})

        final_data = {
            "hotelCode": propertyId,
            "info": []
        }

        room_info_data = {
            "rateTypeId": None,
            "channelCode": None,
            "channelName": None,
            "roomInfo": []
        }

        for roomId, roomName in row_data.items():
            room_id = roomId.split('_')[1]
            room_name = roomName.split("::")[0]

            room_data = {
                "roomId": room_id,
                "roomName": room_name,
                "roomPlanInfo": []
            }

            availability_data = response_data.get('data', {}).get('deals_data', {}).get(roomId, {})

            for availability_date, availability_info in availability_data.items():
                if availability_date == current_date:
                    avail = availability_info.get('avail')
                    total = availability_info.get('totalRooms')
                    roomPrice = availability_info.get('rate')

                    room_plan_data = {
                        "roomPlanId": None,
                        "roomPlanName": None
                    }
                    room_data["roomPlanInfo"].append(room_plan_data)

            if room_data["roomPlanInfo"]:
                room_info_data["roomInfo"].append(room_data)

        final_data["info"].append(room_info_data)

        # Insert into MongoDB
        dataCollection = db["CMRoomDetail"]
        dataCollection.insert_one(final_data)
        print(f"{propertyId} Data inserted into MongoDB")

staahRoomConfig()
