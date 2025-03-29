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

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'Username')))
    driver.find_element(By.NAME, 'Username').send_keys(username)
    driver.find_element(By.NAME, 'Password').send_keys(password)
    driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-success.btn-block[name="button"][value="login"]').click()

    time.sleep(2)
    if "Invalid username or password" in driver.page_source:
        print("Login Unsuccessful")
        driver.quit()
        return
    
    roomCount = {}
    print("Login Successful")
    
    html_content = driver.page_source
    ajax_url_match = re.search(r'"https://www\.eglobe-solutions\.com/cmapi/bookings/([A-Za-z0-9]+)/"', html_content)
    if ajax_url_match:
        specific_part = ajax_url_match.group(1)
        print(specific_part)

        current_datetime = datetime.now().date()
        end_date = current_datetime + timedelta(days=370)  # 371 days total (including today)
        inventory_info = {
            "hotelCode": str(property_code),
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "inventory": []
        }
        print(inventory_info)
        
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

            for request in driver.requests:
                if request.url.startswith('https://www.eglobe-solutions.com/frontdeskapi/frontdesk/fdeskV4a'):
                    auth_header = request.headers.get('Authorization')
                    if auth_header:
                        break
            else:
                print("No matching API request found or Authorization header missing")
                driver.quit()
                return

            room_inventory_map = {}

            def fetch_data(for_date):
                formatted_date = for_date.strftime("%d-%b-%Y")
                inventory_endpoint = f"https://www.eglobe-solutions.com/webapichannelmanager/inventory/{specific_part}/channels/1006?year={for_date.year}&month={for_date.month:02d}&dateToday={formatted_date}"
                inventory_response = requests.get(inventory_endpoint)

                if inventory_response.status_code == 200:
                    inventory_data = inventory_response.json()
                else:
                    print(f"Failed to fetch inventory data for {formatted_date}. Status code: {inventory_response.status_code}")
                    return

                rate_endpoint = f"https://www.eglobe-solutions.com/webapichannelmanager/rates/{specific_part}/channels/1006?year={for_date.year}&month={for_date.month:02d}&dateToday={formatted_date}"
                rate_response = requests.get(rate_endpoint)

                totalRoomEndPoint = f"https://www.eglobe-solutions.com/frontdeskapi/frontdesk/fdeskV4a?fromDate={formatted_date}"
                headers = {'authorization': auth_header}
                response = requests.get(totalRoomEndPoint, headers=headers)

                if response.status_code == 200:
                    response_data = response.json()
                    print(f"Inventory data fetched successfully for {formatted_date}.")

                    mainData = response_data.get('RoomCategories', [])
                    for data in mainData:
                        roomId = data.get('CatId')
                        rooms = data.get('Rooms', [])
                        room_count = len(rooms)
                        roomCount[roomId] = room_count

                    if rate_response.status_code == 200:
                        rate_data = rate_response.json()
                        room_inventory = inventory_data.get('RoomWiseInventory', [])
                        room_rates = rate_data.get('RoomWiseRates', [])

                        for room in room_inventory:
                            room_id = room.get('RoomId')
                            room_name = room.get('RoomName')
                            day_wise_inventory = room.get('DayWiseInventory', [])

                            if room_id not in room_inventory_map:
                                room_inventory_map[room_id] = {
                                    "roomId": room_id,
                                    "roomName": room_name,
                                    "inventory": []
                                }

                                room_price = None
                                for rate_info in room_rates:
                                    if rate_info.get('RoomId') == room_id:
                                        room_price = rate_info.get('DayWiseRates', [])[0].get('Rate')
                                        break

                                for day_info in day_wise_inventory:
                                    as_on_date_str = day_info.get('AsOnDate').split('T')[0]
                                    as_on_date = datetime.strptime(as_on_date_str, "%Y-%m-%d").date()

                                    if current_datetime <= as_on_date <= end_date:
                                        day_info_entry = {
                                            "arrivalDate": as_on_date.strftime("%Y-%m-%d"),
                                            "totalRooms": roomCount.get(int(room_id)),
                                            "availableRooms": day_info.get('DayAvailability'),
                                            "rate": room_price,
                                        }
                                        room_inventory_map[room_id]["inventory"].append(day_info_entry)

                else:
                    print(f"Failed to fetch rate data for {formatted_date}. Status code: {rate_response.status_code}")

            # Loop through the next 371 days (including today)
            for i in range(371):
                fetch_data(current_datetime + timedelta(days=i))

            # Convert room_inventory_map to the required list format
            inventory_info["inventory"] = list(room_inventory_map.values())

            with open(f'{property_code}_Inventory.json', 'w') as json_file:
                json.dump(inventory_info, json_file, indent=2)

            print(f'{property_code} Inventory Data Extracted Successfully!')

        except Exception as e:
            print(f"Error during navigation or data fetching: {e}")

    driver.quit()

username = 'akshay01'
password = 'akshay0120'
property_code = '1234'

eGlobeInventory(username, password, property_code)
