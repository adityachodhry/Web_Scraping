import requests
import json
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime

def staahInventory(email, password, property_code):

    driver = webdriver.Chrome()

    url = 'https://max.staah.net/hotels/index.php'

    driver.get(url)
    time.sleep(4)

    driver.find_element(By.NAME, 'propertyId').send_keys(property_code)
    driver.find_element(By.NAME, 'email').send_keys(email)
    driver.find_element(By.NAME, 'password').send_keys(password)
    time.sleep(random.randint(2, 3))

    driver.find_element(By.NAME, 'password').send_keys(Keys.ENTER)

    time.sleep(random.randint(6, 8))

    cookies = driver.get_cookies()

    AWSLABCORS_Cookie = next((cookie['value'] for cookie in cookies if cookie['name'] == 'AWSALBCORS'), None)
    PHPSESSID_Cookie = next((cookie['value'] for cookie in cookies if cookie['name'] == 'PHPSESSID'), None)

    driver.quit()

    endpoint = f"https://max2.staah.net/hotels/lib/availabilityandrates?gb_propertyId={property_code}&gb_returntype=json"
    
    headers = {
        "X-Requested-With": "XMLHttpRequest",
        "Cookie": f"PHPSESSID={PHPSESSID_Cookie}; AWSALBCORS={AWSLABCORS_Cookie}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    payload = {
        'mode': 'getavailablity',
        'startdate': '',
        'tagarray': '',
        'fromdeals': 'yes'
    }

    response = requests.post(endpoint, headers=headers, data=payload)

    if response.status_code == 403:
        print("Access denied. Check your credentials, headers, and ensure your IP is not blocked.")
        return

    if response.text:
        try:
            response_data = json.loads(response.text)
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")
            return
    else:
        print("Empty response received")
        return

    row_data = response_data.get('row', {})

    inventory_info = {
        "hotelCode": str(property_code),
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "inventory": []
    }

    for roomId, roomName in row_data.items():
        room_id = roomId.split('_')[1]
        room_name = roomName.split("::")[0]

        availability_data = response_data.get(roomId, {})

        room_inventory_list = []

        for date, availability_info in availability_data.items():
            # rate = availability_info.get('rate')
            avail = availability_info.get('avail')
            total = availability_info.get('totalRooms')

            room_inventory_list.append({
                "arrivalDate": datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d'),
                "totalRooms": int(total),
                "availableRooms": int(avail)
            })

        inventory_info["inventory"].append({
            "roomId": str(room_id),
            "roomName": room_name,
            "inventory": room_inventory_list
        })

    with open(f"{property_code} inventory.json", "w") as outfile:
        json.dump(inventory_info, outfile, indent=4)

    print(f"{property_code} Data saved to inventory_staah_data.json")

# staahInventory('ankur.nograhiya@retvensservices.com', 'Retvens@123456', 5566)
