import time
import requests
import json
from datetime import datetime, timedelta
from seleniumwire import webdriver
from selenium.webdriver.common.by import By

def axisRoomsInventory(email, password, property_code):

    driver = webdriver.Chrome()

    login_url = 'https://app.axisrooms.com/'

    driver.get(login_url)
    time.sleep(4)

    driver.find_element(By.CSS_SELECTOR, 'input#emailId[name="emailId"]').send_keys(email)
    driver.find_element(By.CSS_SELECTOR, 'input#password[name="password"]').send_keys(password)

    driver.find_element(By.CSS_SELECTOR, 'button.g-recaptcha.theme-button-one.dark').click()

    time.sleep(4)

    cookies = driver.get_cookies()
    access_token = next((cookie['value'] for cookie in cookies if cookie['name'] == 'access_token'), None)

    if not access_token:
        print("Login Unsuccessful")
        driver.quit()
        return

    print("Login Successful")

    headers = {
        'Cookie': f"access_token={access_token}"
    }

    current_date = datetime.now()
    days_to_fetch = 371
    inventory_info = {
        "hotelCode": str(property_code),
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "inventory": []
    }

    while days_to_fetch > 0:

        chunk_days = min(371, days_to_fetch)
        end_date = current_date + timedelta(days=chunk_days)

        current_date_str = current_date.strftime("%Y%m%d")
        end_date_str = end_date.strftime("%Y%m%d")

        inventory_endpoint = f"https://app.axisrooms.com/api/v1/getInventory?productId={property_code}&start={current_date_str}&end={end_date_str}"
        price_endpoint = f"https://app.axisrooms.com/api/v1/getPriceDetails?productId={property_code}&start={current_date_str}&end={end_date_str}&otaId="

        # Get Inventory Data
        inventory_response = requests.get(inventory_endpoint, headers=headers)
        
        # Get Price Data
        price_response = requests.get(price_endpoint, headers=headers)

        if inventory_response.status_code == 200 and price_response.status_code == 200:
            inventory_content = inventory_response.json()
            price_content = price_response.json()

            data = inventory_content.get('invObj', [])
            rooms = price_content.get('rooms', {})

            for room_id, room_info in data.items():
                room_name = room_info.get('roomName')
                room_inventory = room_info.get('inventory', {})

                # Sort the inventory data by date to ensure sequential order
                sorted_inventory = sorted(room_inventory.items(), key=lambda x: x[0])

                room_inventory_data = []

                for date, details in sorted_inventory:
                    available = details.get('available', 0) 
                    booked = details.get('booked', 0)  
                    totalRoom = available + booked

                    totalNoOfRoom = None if totalRoom == 0 or totalRoom == "" else totalRoom
                    totalAvailableRoom = None if available == 0 or available == "" else available

                    bar_data = rooms.get(room_id, {}).get('bar', {})
                    room_price = bar_data.get(date, None)
                    price = None if room_price == 0 or room_price == "" else room_price

                    arrival_Date = datetime.strptime(date, "%Y%m%d").strftime("%Y-%m-%d")

                    room_inventory_data.append({
                        "arrivalDate": arrival_Date,
                        "totalRooms": totalNoOfRoom,
                        "availableRooms": totalAvailableRoom,
                        "roomPrice": price  
                    })

                inventory_info["inventory"].append({
                    "roomId": room_id,
                    "roomName": room_name,
                    "inventory": room_inventory_data
                })

            print(f"Data retrieved from {current_date_str} to {end_date_str}")

        else:
            print(f"Failed to retrieve data for {current_date_str} to {end_date_str}")

        # Update current date for next iteration
        current_date = end_date + timedelta(days=1)
        days_to_fetch -= chunk_days

    # Save the accumulated data to the JSON file
    with open('Inventory_axisRoom_Data_371.json', 'w') as room_file:
        json.dump(inventory_info, room_file, indent=2)

    print('371 Days of Inventory and Price Data Extracted Successfully!')

    driver.quit()

axisRoomsInventory('reservations@presidencyhotel.com', 'Password@123', 102665)
