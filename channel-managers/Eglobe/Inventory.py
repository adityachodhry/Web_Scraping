import time
import re
import requests
import json
from bs4 import BeautifulSoup
from seleniumwire import webdriver
from selenium.webdriver.common.by import By

# Initialize the driver
driver = webdriver.Chrome()

username = 'amantras'
password = 'shilpi@2014'

login_url = 'https://www.eglobe-solutions.com/hms/dashboard'

# Go to the login page
driver.get(login_url)
time.sleep(4)

# Input credentials and submit the form
driver.find_element(By.NAME, 'Username').send_keys(username)
driver.find_element(By.NAME, 'Password').send_keys(password)

# Click on the login button
driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-success.btn-block[name="button"][value="login"]').click()

time.sleep(2)

if "Invalid username or password" in driver.page_source:
    print("Login Unsuccessful")
else:
    print("Login Successful")
    
    # Extract HTML content
    html_content = driver.page_source

    # Use regular expression to extract the specific part from the AJAX URL
    ajax_url_match = re.search(r'"https://www\.eglobe-solutions\.com/cmapi/bookings/([A-Za-z0-9]+)/"', html_content)
    if ajax_url_match:
        specific_part = ajax_url_match.group(1)
    
        endpoint = f"https://www.eglobe-solutions.com/webapichannelmanager/inventory/{specific_part}/channels/1006?year=2024&month=05&dateToday=11-May-2024"

        response = requests.get(endpoint)

        if response.status_code == 200:
            response_content = response.json()

            inventory_info = []

            data = response_content.get('RoomWiseInventory', [])

            for info in data:
                room_id = info.get('RoomId')
                room_name = info.get('RoomName')
                day_wise_inventory = info.get('DayWiseInventory', [])

                for day_info in day_wise_inventory:
                    date = day_info.get('AsOnDate')
                    availability = day_info.get('DayAvailability')

                    room_info = {
                        'roomId': room_id,
                        'roomName': room_name,
                        'date': date,
                        'available': availability
                    }

                    inventory_info.append(room_info)

            with open('Inventory_Info.json', 'w') as json_file:
                json.dump(inventory_info, json_file, indent=2)

            print('Inventory Data Extracted Successfully!')
        else:
            print("Failed to fetch data from the endpoint.")

# Close the driver
driver.quit()
