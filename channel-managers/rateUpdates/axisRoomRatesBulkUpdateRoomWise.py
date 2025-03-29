import time
import requests
import json
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from datetime import timedelta, datetime

# username = 'info@aravalimahal.com'
# password = 'Password@123'
# propertyCode = "180045"
# roomId = "302043"
# roomPlanId = "240781"
# occupancyId = [1, 2, 3]  
# startDate = "2024-09-10"
# endDate = "2024-09-10"
# rate = [9000, 9000, 10000]  
# selectWeekDays = ["Tuesday"] 

session = requests.Session()

def get_days_selection(input_days):
    day_map = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    days_boolean = [True if day in input_days else False for day in day_map]
    return days_boolean

def axisRoomRateBulkUpdate(username, password, propertyCode, seasonCode, channelCode, roomId, roomName, rateTypeId, roomPlanId, mealPlanId, availability, rate, perExtraPerson, extraChildren, extraChildrenRate, extraPerson, extraPersonRate, occupancy, occupancyRate, occupancyId, displayOrderId, selectWeekdays, selectWeekdaysRate, startDate, endDate):
    
    driver = webdriver.Chrome()
    login_url = 'https://app.axisrooms.com/'

    driver.get(login_url)
    time.sleep(4)

    driver.find_element(By.CSS_SELECTOR, 'input#emailId[name="emailId"]').send_keys(username)
    driver.find_element(By.CSS_SELECTOR, 'input#password[name="password"]').send_keys(password)
    driver.find_element(By.CSS_SELECTOR, 'button.g-recaptcha.theme-button-one.dark').click()

    time.sleep(4)

    for cookie in driver.get_cookies():
        session.cookies.set(cookie['name'], cookie['value'])

    driver.quit()

    formatted_startDate = datetime.strptime(startDate, "%Y-%m-%d").strftime("%Y/%m/%d")
    formatted_endDate = datetime.strptime(endDate, "%Y-%m-%d").strftime("%Y/%m/%d")

    days_selected = get_days_selection(selectWeekdays)

    rates = [{"occupancyId": occ_id, "final": r} for occ_id, r in zip(occupancyId, rate)]

    url = "https://app.axisrooms.com/api/v1/updatePeriodPrice"

    payload = {
        "productId": propertyCode,
        "roomId": roomId,
        "ratePlanId": roomPlanId,
        "allOtas": True,
        "otaIds": [],
        "periods": [
            {
                "startDate": formatted_startDate,
                "endDate": formatted_endDate,
                "days": days_selected 
            }
        ],
        "prices": rates  
    }

    print(json.dumps(payload, indent=4))

    headers = {
        'Content-Type': 'application/json'
    }

    response = session.post(url, headers=headers, data=json.dumps(payload))

    return response.json()

# response = axisRoomRateBulkUpdate(username, password, propertyCode, roomId, roomPlanId, occupancyId, rate, selectWeekDays,startDate,endDate)

# print(response)