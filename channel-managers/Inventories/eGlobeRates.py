import time
import re
import requests
import json
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime

driver = webdriver.Chrome()

username = 'akshay01'
password = 'akshay0120'

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

        current_datetime = datetime.now()
        formatted_date = current_datetime.strftime("%d-%b-%Y")
        
        rateEndPoint = f"https://www.eglobe-solutions.com/webapichannelmanager/rates/{specific_part}/channels/1006?year={current_datetime.year}&month={current_datetime.month:02d}&dateToday={formatted_date}"

        rateResponse = requests.get(rateEndPoint)

        if rateResponse.status_code == 200:
            rateResponseContent = rateResponse.json()

            # with open('Inventory_Data.json', 'w') as json_file:
            #     json.dump(rateResponseContent, json_file, indent=2)

            hotelCode = rateResponseContent.get('HotelId', '')

            inventory_info = {
                "hotelCode": str(hotelCode),
                "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "inventory": []
            }

            rateData = rateResponseContent.get('RoomWiseRates', [])
            
            for rateInfo in rateData:
                roomMealPlan = rateInfo.get('RatePlanName')

                if roomMealPlan in ['EP(SG)', 'CP(SG)', 'MAP(SG)', 'AP(SG)']:
                    room_inventory = {
                        "roomMealPlan": roomMealPlan,
                        "inventory": []
                    }

                    for day_info in rateInfo.get('DayWiseRates', []):
                        date_str = day_info.get('AsOnDate').split('T')[0]
                        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                        formatted_date = date_obj.strftime("%Y-%m-%d")

                        roomPrice = day_info.get('Rate')

                        day_info_entry = {
                            "arrivalDate": formatted_date, 
                            "roomPrice": roomPrice
                        }

                        room_inventory["inventory"].append(day_info_entry)

                    inventory_info["inventory"].append(room_inventory)

            with open('eGlobeInventory.json', 'w') as json_file:
                json.dump(inventory_info, json_file, indent=2)

            print('Inventory Data Extracted Successfully!')
        else:
            print("Failed to fetch data from the endpoint.")

driver.quit()
