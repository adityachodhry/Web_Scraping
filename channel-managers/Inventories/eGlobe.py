import time
import re
import requests
import json
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime

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
    else:
        print("Login Successful")

        html_content = driver.page_source

        ajax_url_match = re.search(r'"https://www\.eglobe-solutions\.com/cmapi/bookings/([A-Za-z0-9]+)/"', html_content)
        if ajax_url_match:
            specific_part = ajax_url_match.group(1)

            current_datetime = datetime.now()
            formatted_date = current_datetime.strftime("%d-%b-%Y")

            endpoint = f"https://www.eglobe-solutions.com/webapichannelmanager/inventory/{specific_part}/channels/1006?year={current_datetime.year}&month={current_datetime.month:02d}&dateToday={formatted_date}"

            response = requests.get(endpoint)

            if response.status_code == 200:
                response_content = response.json()

                with open('Inventory_Data.json', 'w') as json_file:
                    json.dump(response_content, json_file, indent=2)

                inventory_info = {
                    "hotelCode": str(property_code),
                    "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "inventory": []
                }

                data = response_content.get('RoomWiseInventory', [])

                for info in data:
                    room_id = info.get('RoomId')
                    room_name = info.get('RoomName')
                    day_wise_inventory = info.get('DayWiseInventory', [])

                    room_inventory = {
                        "roomId": room_id,
                        "roomName": room_name,
                        "inventory": []
                    }

                    for day_info in day_wise_inventory:
                        date_str = day_info.get('AsOnDate').split('T')[0]
                        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                        formatted_date = date_obj.strftime("%Y-%m-%d")

                        availability = day_info.get('DayAvailability')

                        day_info_entry = {
                            "arrivalDate": formatted_date,
                            "totalRooms": None,  
                            "availableRooms": availability
                        }

                        room_inventory["inventory"].append(day_info_entry)

                    inventory_info["inventory"].append(room_inventory)

                with open(f'{property_code} Inventory.json', 'w') as json_file:
                    json.dump(inventory_info, json_file, indent=2)

                print(f'{property_code} Inventory Data Extracted Successfully!')
            else:
                print("Failed to fetch data from the endpoint.")

    driver.quit()

