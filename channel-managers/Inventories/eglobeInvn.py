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
    room_inventory_map = {}

    html_content = driver.page_source
    ajax_url_match = re.search(r'"https://www\.eglobe-solutions\.com/cmapi/bookings/([A-Za-z0-9]+)/"', html_content)
    if ajax_url_match:
        specific_part = ajax_url_match.group(1)

        inventory_info = {
            "hotelCode": str(property_code),
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "inventory": []
        }
    
    pms_menu = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[@class="has-arrow" and contains(., "PMS")]')))
    pms_menu.click()
    print("PMS menu clicked")

    front_desk_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Front Desk')))
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
    
    headers = {'authorization': auth_header}

    # Function to format date to a string as required by the API
    def format_date(date):
        return date.strftime('%d-%b-%Y')  # Format: '11-Oct-2024'
    
    # Set the start and end dates
    startDate = datetime.today()
    endDate = startDate + timedelta(days=371)

    # Loop through the date range in increments of 14 days
    date = startDate
    while date < endDate:
        # Calculate the end of the 14-day period
        next_date = date + timedelta(days=14)
        
        # Format the dates
        date_str = format_date(date)
        
        # Update the URLs with the current date
        rates_url = f"https://www.eglobe-solutions.com/webapichannelmanager/rates/{specific_part}/channels/1006?year={date.year}&month={date.month}&dateToday={format_date(startDate)}"
        inv_url = f"https://www.eglobe-solutions.com/frontdeskapi/frontdesk/fdeskV4a?fromDate={date_str}"
        inventory_endpoint = f"https://www.eglobe-solutions.com/webapichannelmanager/inventory/{specific_part}/channels/1006?year={date.year}&month={date.month}&dateToday={format_date(startDate)}"
        
        # Make the API requests
        rate_response = requests.get(rates_url)
        inv_response = requests.get(inv_url, headers=headers)
        inventory_response = requests.get(inventory_endpoint)
        
        if inv_response.status_code == 200 and inventory_response.status_code == 200:
            print(f"Inventory Data for {date_str}:")
            response_data = inv_response.json()
            mainData = response_data.get('RoomCategories', [])
            
            for data in mainData:
                roomId = data.get('CatId')
                rooms = data.get('Rooms', [])
                room_count = len(rooms)
                roomCount[roomId] = room_count
            
            # Check if the rate response is valid
            if rate_response.status_code == 200:
                rate_data = rate_response.json()
                inventory_data = inventory_response.json()
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
                    
                    # Get room rate
                    room_price = None
                    for rate_info in room_rates:
                        if rate_info.get('RoomId') == room_id:
                            room_price = rate_info.get('DayWiseRates', [])[0].get('Rate')
                            break

                    # Append inventory data
                    for day_info in day_wise_inventory:
                        as_on_date_str = day_info.get('AsOnDate').split('T')[0]
                        as_on_date = datetime.strptime(as_on_date_str, "%Y-%m-%d").date()

                        day_info_entry = {
                            "arrivalDate": as_on_date.strftime("%Y-%m-%d"),
                            "totalRooms": roomCount.get(int(room_id)),
                            "availableRooms": day_info.get('DayAvailability'),
                            "rate": room_price,
                        }
                        room_inventory_map[room_id]["inventory"].append(day_info_entry)
            else:
                print(f"Failed to fetch rates data for {date_str}")
        else:
            print(f"Failed to fetch inventory data for {date_str}")
        
        # Move to the next 14-day period
        date = next_date

    inventory_info['inventory'] = room_inventory_map 
    with open(f'Inventory.json', 'w') as json_file:
        json.dump(inventory_info, json_file, indent=2)


username = 'akshay01'
password = 'akshay0120'
property_code = '1234'

eGlobeInventory(username, password, property_code)