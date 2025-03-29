import time
import json
import requests
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def exelyRatePush(propertyCode, cmCreds, ratesConfig):

    username = cmCreds.get('username')
    password = cmCreds.get('password')

    driver = webdriver.Chrome()
    login_url = 'https://secure.exely.com/secure/Enter.aspx'
    driver.get(login_url)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="username"]')))
    driver.find_element(By.CSS_SELECTOR, 'input[name="username"]').send_keys(username)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
    driver.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys(password)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn.btn-md.btn-primary')))
    driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-md.btn-primary').click()

    time.sleep(5)
    if "Invalid username or password" in driver.page_source:
        print("Login Unsuccessful")
        driver.quit()
        return
    else:
        print("Login Successful")

    try:
        room_management_menu = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[text()='Room management']"))
        )
        room_management_menu.click()  
        print("Navigated to Room Management")

        rate_plans_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@ng-href, '/secure/Extranet/#/SpecialOffers')]"))
        )
        rate_plans_link.click()
        print("Navigated to Rate Plans")

        cookies = driver.get_cookies() 
        cookie_string = '; '.join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])

        for config in ratesConfig.get('info', []):
            channelCode = config.get('channelCode')

            for room in config.get('roomInfo', []):
                roomId = room.get('roomId')
                
                # Dictionary to keep track of rates by occupancyId and date
                rates_by_occupancy = {}

                for roomPlan in room.get('roomPlanInfo', []):
                    roomPlanDetails = roomPlan.get('roomPlan', {})
                    occupancyId = roomPlanDetails.get('occupancyId')
                    rate = roomPlanDetails.get('rate')
                    date = roomPlanDetails.get('date').replace('-', '')

                    # Generate a unique key for each occupancyId + date pair
                    key = f"{occupancyId}-{date}"
                    
                    # Store rates separately for the same occupancyId on different dates
                    if key not in rates_by_occupancy:
                        rates_by_occupancy[key] = {
                            "data": [str(rate)],
                            "datePeriods": [
                                {
                                    "daysCount": 1,
                                    "startDate": date
                                }
                            ],
                            "dimensionPoints": [
                                {
                                    "channel": str(channelCode),
                                    "roomType": str(roomId),
                                    "placement": f"{channelCode}-{occupancyId}-{roomId}",
                                    "pricesAndRestrictions": "Prices"
                                }
                            ]
                        }

                # Create payloads for each key
                for key, payload_data in rates_by_occupancy.items():
                    payload = json.dumps([payload_data])
                    print(payload)

                    headers = {
                        'cookie': cookie_string,
                        'x-http-method-override': 'PUT',
                        'Content-Type': 'application/json',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
                    }

                    ratePushAPI = "https://secure.exely.com/secure/Extranet/api/tlui/calendar/v2/price-calendar/10027691"
                    response = requests.request("POST", ratePushAPI, headers=headers, data=payload)

                    print(response.text)
                    print(response.status_code)
                    return response   # return response

    except Exception as e:
        print(f"Failed to navigate: {str(e)}")
        return

    driver.quit()

# cmCreds = {
#     "username": "TL-503098-REV",
#     "password": "NEST@786*1263"
# }

# ratesConfig = {
#     "info": [
#         {
#             "channelCode": 0,
#             "roomInfo": [
#                 {
#                     "roomId": 5016143,
#                     "roomPlanInfo": [
#                         {
#                             "roomPlan": {
#                                 "occupancyId": 10038311,
#                                 "rate": 3350,
#                                 "date": "2024-10-23"
#                             }
#                         },
#                         {
#                             "roomPlan": {
#                                 "occupancyId": 10038311,
#                                 "rate": 3350,
#                                 "date": "2024-10-24"    
#                             }
#                         }
#                     ]
#                 }
#             ]
#         },
#         {
#             "channelCode": 0,
#             "roomInfo": [
#                 {
#                     "roomId": 5016193,
#                     "roomPlanInfo": [
#                         {
#                             "roomPlan": {
#                                 "occupancyId": 10038446,
#                                 "rate": 4900,
#                                 "date": "2024-10-23"
#                             }
#                         },
#                         {
#                             "roomPlan": {
#                                 "occupancyId": 10038446,
#                                 "rate": 4900,
#                                 "date": "2024-10-24"
#                             }
#                         }
#                     ]
#                 }
#             ]
#         }
#     ]
# }

# exelyRatePush('4271423', cmCreds, ratesConfig)
