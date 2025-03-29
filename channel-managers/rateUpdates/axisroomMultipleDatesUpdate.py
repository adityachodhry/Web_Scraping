import time
import requests
import json
from seleniumwire import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

login_url = 'https://app.axisrooms.com/'

session = requests.Session()

def axisRoom_ratesUpdate(username, password, propertyCode, data):

    driver.get(login_url)
    time.sleep(4)

    driver.find_element(By.CSS_SELECTOR, 'input#emailId[name="emailId"]').send_keys(username)
    driver.find_element(By.CSS_SELECTOR, 'input#password[name="password"]').send_keys(password)
    driver.find_element(By.CSS_SELECTOR, 'button.g-recaptcha.theme-button-one.dark').click()

    time.sleep(5)

    for cookie in driver.get_cookies():
        session.cookies.set(cookie['name'], cookie['value'])

    driver.quit()

    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    room_entries = {}

    for entry in data:
        date = entry["date"]
        roomId = entry["roomId"]
        roomPlanId = entry["roomPlanId"]
        occupancyId = entry["occupancyId"]
        rate = entry["rate"]
        
        date_payload = {
            "date": date,
            "allocation": "-1",
            "ratePlans": []
        }

        for planId in roomPlanId:
            rate_plan = {
                "ratePlanId": planId,
                "occupancyPrice": []
            }
            for id in occupancyId:
                occupancy_price = {
                    "occupancyId": id,
                    "price": rate
                }
                rate_plan["occupancyPrice"].append(occupancy_price)
            date_payload["ratePlans"].append(rate_plan)

        if roomId in room_entries:
            room_entries[roomId]["dates"].append(date_payload)
        else:
            room_entries[roomId] = {"roomId": roomId, "dates": [date_payload]}

    payload = {
        "productId": propertyCode,
        "allOtas": True,
        "otaIds": [],
        "roomValue": list(room_entries.values())  
    }

    print(json.dumps(payload, indent=4))

    api_url = "https://app.axisrooms.com/api/v1/updateInventoryAndPrice"
    
    response = session.post(api_url, headers=headers, data=json.dumps(payload))

    return response.json()

username = 'info@aravalimahal.com'
password = 'Password@123'
propertyCode = "180045"
dates = ["2024-09-10", "2024-09-11"]
roomIds = ["302043", "302044"]
roomPlanId = ["240781"]  
occupancyId = ["1"]   
rates = [9000, 9000]

data = []
for i in range(len(dates)):
    entry = {
        "date": dates[i],
        "roomId": roomIds[i],
        "roomPlanId": roomPlanId,  
        "occupancyId": occupancyId,  
        "rate": rates[i]
    }
    data.append(entry)

response = axisRoom_ratesUpdate(username, password, propertyCode, data)

print(response)