import requests
import json
import time
from datetime import datetime, timedelta
from seleniumwire import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

email = 'dargelislodge@gmail.com'
password = 'Lodge@123'

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
    exit()

print("Login Successful")

current_date = datetime.now().strftime("%Y%m%d")
end_date = (datetime.now() + timedelta(days=1)).strftime("%Y%m%d")

url = f"https://app.axisrooms.com/api/v1/getPriceDetails?productId=188592&start={current_date}&end={end_date}&otaId="

headers = {
    'Cookie': f"access_token={access_token}"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    rooms = data.get('rooms', {})
    
    inventory_list = []

    for room_id, room_data in rooms.items():
        bar_data = room_data.get('bar', {})
        
        for date, price in bar_data.items():
            inventory_list.append({
                "arrivalDate": date,
                "roomPrice": price,
            })

        structured_inventory = {
            "roomId": room_id,
            "inventory": inventory_list
        }

    structured_data = {
        "timestamp": datetime.now().isoformat() + "Z",
        "inventory": [structured_inventory]
    }

    with open('bar_data.json', 'w') as json_file:
        json.dump(structured_data, json_file, indent=4)

    print("Bar data has been written to bar_data.json")
else:
    print(f"Request failed with status code: {response.status_code}")

driver.quit()
