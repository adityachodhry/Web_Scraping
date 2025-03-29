import sys
import time
import random
import requests, json
from datetime import datetime
from seleniumwire import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def staahInventory(email, password, property_code):

    options = {
        'verify_ssl': False 
    }
    
    driver = webdriver.Chrome(seleniumwire_options=options)

    url = 'https://max.staah.net/hotels/index.php'

    driver.get(url)
    time.sleep(4)

    driver.find_element(By.NAME, 'propertyId').send_keys(property_code)
    driver.find_element(By.NAME, 'email').send_keys(email)
    driver.find_element(By.NAME, 'password').send_keys(password)
    
    time.sleep(random.randint(2, 3))

    driver.find_element(By.NAME, 'password').send_keys(Keys.ENTER)

    time.sleep(random.randint(6, 8))

    availability_calendar_selector = 'a.nav-link.collapsed.false[href="/hotel/dashboard"]'

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, availability_calendar_selector))
        )
        element.click()
    except Exception as e:
        print(f"Error clicking on availability calendar: {e}")

    time.sleep(random.randint(4, 6))

    for request in driver.requests:
        if request.response:
            if 'Propertyauthkey' in request.headers:
                auth_key = request.headers['Propertyauthkey']
                print(f"Propertyauthkey: {auth_key}")
                break

    driver.quit()

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
        sys.exit()

    if response.text:
        try:
            response_data = json.loads(response.text)
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")
            print("Response text:", response.text)
            sys.exit()
    else:
        print("Empty response received")
        sys.exit()

    # with open("inventory_Row.json", "w") as outfile:
    #     json.dump(response_data, outfile, indent=4)

    row_data = response_data.get('data', {}).get('deals_data', {}).get('row', {})
    # print(row_data)

    inventory_info = {
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "inventory": []
    }

    for roomId, roomName in row_data.items():
        room_id = roomId.split('_')[1]
        room_name = roomName.split("::")[0]

        room_inventory_list = []

        availability_data = response_data.get('data', {}).get('deals_data', {}).get(roomId, {})

        for date, availability_info in availability_data.items():
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

    with open(f"{property_code} staahInventory.json", "w") as outfile:
        json.dump(inventory_info, outfile, indent=4)

    print(f"{property_code} Data saved to Staah_inventory.json")

# staahInventory('ankur.nograhiya@retvensservices.com', 'Retvens@123456', 5566)

