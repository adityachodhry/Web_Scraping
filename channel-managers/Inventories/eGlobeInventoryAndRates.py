import time
import re
import requests
import json
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
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
    else:
        print("Login Successful")

        html_content = driver.page_source

        ajax_url_match = re.search(r'"https://www\.eglobe-solutions\.com/cmapi/bookings/([A-Za-z0-9]+)/"', html_content)
        if ajax_url_match:
            specific_part = ajax_url_match.group(1)
            print(specific_part)

            current_datetime = datetime.now().date()  
            end_date = current_datetime + timedelta(days=200)  

            inventory_info = {
                "hotelCode": str(property_code),
                "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "inventory": []
            }

                    data = response_content.get('RoomWiseInventory', [])
                    rateData = rateResponseContent.get('RoomWiseRates', [])

                    for info in data:
                        room_id = info.get('RoomId')
                        room_name = info.get('RoomName')
                        day_wise_inventory = info.get('DayWiseInventory', [])

                        selected_room_inventory = None 

                        for rateInfo in rateData:
                            if rateInfo.get('RoomId') == room_id:
                                roomMealPlan = rateInfo.get('RatePlanName')
                                roomPrice = rateInfo.get('DayWiseRates', [])[0].get('Rate')

                                if roomMealPlan == 'EP(SG)' and selected_room_inventory is None:
                                    selected_room_inventory = {
                                        "roomId": room_id,
                                        "roomName": room_name,
                                        # "roomMealPlan": roomMealPlan,
                                        "inventory": []
                                    }
                                elif roomMealPlan == 'CP(SG)' and selected_room_inventory is None:
                                    selected_room_inventory = {
                                        "roomId": room_id,
                                        "roomName": room_name,
                                        # "roomMealPlan": roomMealPlan,
                                        "inventory": []
                                    }
                                elif roomMealPlan == 'MAP(SG)' and selected_room_inventory is None:
                                    selected_room_inventory = {
                                        "roomId": room_id,
                                        "roomName": room_name,
                                        # "roomMealPlan": roomMealPlan,
                                        "inventory": []
                                    }
                                elif roomMealPlan == 'AP(SG)' and selected_room_inventory is None:
                                    selected_room_inventory = {
                                        "roomId": room_id,
                                        "roomName": room_name,
                                        # "roomMealPlan": roomMealPlan,
                                        "inventory": []
                                    }

                            room_price = None
                            for rate_info in room_rates:
                                if rate_info.get('RoomId') == room_id:
                                    room_meal_plan = rate_info.get('RatePlanName')
                                    room_price = rate_info.get('DayWiseRates', [])[0].get('Rate')

                                    if room_meal_plan in ['EP(SG)', 'CP(SG)', 'MAP(SG)', 'AP(SG)']:
                                        break

                            for day_info in day_wise_inventory:
                                as_on_date_str = day_info.get('AsOnDate').split('T')[0]
                                as_on_date = datetime.strptime(as_on_date_str, "%Y-%m-%d").date()

                                if current_datetime <= as_on_date <= end_date:
                                    day_info_entry = {
                                        "arrivalDate": as_on_date.strftime("%Y-%m-%d"),
                                        "availableRooms": day_info.get('DayAvailability'),
                                        "rate": room_price,
                                    }
                                    room_inventory_map[room_id]["inventory"].append(day_info_entry)

                    else:
                        print(f"Failed to fetch rate data for {for_month}/{for_year}. Status code: {rate_response.status_code}")
                else:
                    print(f"Failed to fetch inventory data for {for_month}/{for_year}. Status code: {inventory_response.status_code}")

            # Fetch data for both current month and the following month if necessary
            fetch_data(current_datetime.month, current_datetime.year)

            if current_datetime.month != end_date.month:
                fetch_data(end_date.month, end_date.year)

            # Convert room_inventory_map to the required list format
            inventory_info["inventory"] = list(room_inventory_map.values())

            with open(f'{property_code}_Inventory.json', 'w') as json_file:
                json.dump(inventory_info, json_file, indent=2)

            print(f'{property_code} Inventory Data Extracted Successfully!')

        else:
            print("Failed to fetch data from the endpoint.")

    driver.quit()

username = 'akshay01'
password = 'akshay0120'
property_code = '1234'

eGlobeInventory(username, password, property_code)
