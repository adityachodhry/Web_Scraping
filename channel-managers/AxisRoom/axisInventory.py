import time
import requests
import json
from datetime import datetime, timedelta
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the driver
driver = webdriver.Chrome()

username = 'dargelislodge@gmail.com'
password = 'Lodge@123'

login_url = 'https://app.axisrooms.com/'

# Go to the login page
driver.get(login_url)
time.sleep(4)

# Input credentials and submit the form
driver.find_element(By.CSS_SELECTOR, 'input#emailId[name="emailId"]').send_keys(username)
driver.find_element(By.CSS_SELECTOR, 'input#password[name="password"]').send_keys(password)

# Click on the login button
driver.find_element(By.CSS_SELECTOR, 'button.g-recaptcha.theme-button-one.dark').click()

time.sleep(4)
# Get the cookies
cookies = driver.get_cookies()

access_token = next((cookie['value'] for cookie in cookies if cookie['name'] == 'access_token'), None)
# print(access_token)

# Extract inventory data
current_date = datetime.now().strftime("%Y%m%d")
end_date = (datetime.now() + timedelta(days=1)).strftime("%Y%m%d")


pId = 188592

endpoint = f"https://app.axisrooms.com/api/v1/getInventory?productId={pId}&start={current_date}&end={end_date}"
price_url = f"https://app.axisrooms.com/api/v1/getPriceDetails?productId={pId}&start={current_date}&end={end_date}"

headers = {
    'Cookie': f"access_token={access_token}"
}

# body = {
# 'productId': pId,
# 'start': current_date,
# 'end': end_date
# }

inventory_response = requests.request("GET", endpoint, headers=headers)

if inventory_response.status_code == 200:
    inventory_content = inventory_response.json()

    data = inventory_content.get('invObj', [])

    room_data = []

    for room_id, room_info in data.items():
        room_name = room_info.get('roomName')
        room_inventory = room_info.get('inventory', {})
        room_inventory_data = []

        for date, details in room_inventory.items():
            booking = details.get('booked', 0)
            available = details.get('available', 0)
            room_inventory_data.append({
                'date': date,
                'booking': booking,
                'available': available
            })

        room_data.append({
            'room_id': room_id,
            'room_name': room_name,
            'inventory': room_inventory_data
        })

    if room_data:
        with open('Room_Inventory.json', 'w') as room_file:
            json.dump(room_data, room_file, indent=2)
        print('Inventory Data Extracted Successfully!')
    else:
        print('No Inventory Data Available!')

else:
    print('Failed to Retrieve Inventory Data!')
