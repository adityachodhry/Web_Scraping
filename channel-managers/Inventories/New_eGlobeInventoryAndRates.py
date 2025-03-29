import time
import re
import requests
import json
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta

def eGlobeInventory(username, password, property_code):
    driver = webdriver.Chrome()

    login_url = 'https://www.eglobe-solutions.com/hms/dashboard'

    driver.get(login_url)
    time.sleep(4)

    driver.find_element(By.NAME, 'Username').send_keys(username)
    driver.find_element(By.NAME, 'Password').send_keys(password)
    driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-success.btn-block[name="button"][value="login"]').click()

    time.sleep(2)

    if "Invalid username or password" in driver.page_source:
        print("Login Unsuccessful")
        driver.quit()
    else:
        print("Login Successful")

        try:
            pms_menu = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//a[@class="has-arrow" and contains(., "PMS")]'))
            )
            pms_menu.click()
            print("PMS menu clicked")

            front_desk_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, 'Front Desk'))
            )

            front_desk_link.click()
            print("Navigating to Front Desk...")

            time.sleep(5)

            # Capture the API request to the specific endpoint and extract the Authorization header
            for request in driver.requests:
                if request.url.startswith('https://www.eglobe-solutions.com/frontdeskapi/frontdesk/fdeskV4a'):
                    auth_header = request.headers.get('Authorization')
                    if auth_header:
                        print(f"Authorization Header: {auth_header}")
                        break
            else:
                print("No matching API request found or Authorization header missing")

        except Exception as e:
            print(f"Error during navigation: {e}")

        inventory_info = {
            "hotelCode": str(property_code),
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "inventory": []
        }

        current_date = datetime.now().date()

        for day_offset in range(30):
            date_to_fetch = current_date + timedelta(days=day_offset)
            formatted_date = date_to_fetch.strftime("%d-%b-%Y")
            arrival_date = date_to_fetch.strftime("%Y-%m-%d")

            url = f"https://www.eglobe-solutions.com/frontdeskapi/frontdesk/fdeskV4a?fromDate={formatted_date}"

            headers = {
                'authorization': auth_header
            }

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                response_data = response.json()
                print(f"Inventory data fetched successfully for {formatted_date}.")

                mainData = response_data.get('RoomCategories', [])
                for data in mainData:
                    roomId = data.get('CatId')
                    roomname = data.get('CatName')

                    rooms = data.get('Rooms', [])
                    room_count = len(rooms)
                    available_rooms = data.get('Avl', [0])[0] 

                    room_inventory = next((item for item in inventory_info['inventory'] if item['roomId'] == roomId), None)
                    if room_inventory is None:
                        room_inventory = {
                            'roomId': roomId,
                            'roomName': roomname,
                            'inventory': []
                        }
                        inventory_info['inventory'].append(room_inventory)

                    room_inventory['inventory'].append({
                        'arrivalDate': arrival_date,
                        'totalRooms': room_count,
                        'availableRooms': available_rooms,
                    })

            else:
                print(f"Failed to fetch data for {formatted_date}. Status code: {response.status_code}")

        with open('eGlobe_Processed_Inventory.json', 'w') as json_file:
            json.dump(inventory_info, json_file, indent=4)

        print("Successfully Fetched Inventory Information")

        return inventory_info

    driver.quit()

username = 'akshay01'
password = 'akshay0120'
property_code = '1234'

eGlobeInventory(username, password, property_code)
