import time
import requests
import json
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# username = 'info@aravalimahal.com'
# password = 'Password@123'
# propertyCode = 180045
# startDate = "2024/09/10"
# endDate = "2024/09/10"
# roomId = ["302043", "302044"]
# availability = "9"
# selectWeekDays = ["Tuesday"]

login_url = 'https://app.axisrooms.com/'

session = requests.Session()

def get_days_selection(input_days):
    """Helper function to map the selected days into a boolean array for the API."""
    day_map = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    days_boolean = [True if day in input_days else False for day in day_map]
    
    return days_boolean

def axisRoom_inventoryBulkUpdate(username, password, propertyCode, seasonCode, channelCode, roomId, roomName, rateTypeId, roomPlanId, mealPlanId, availability, rate, perExtraPerson, extraChildren, extraChildrenRate, extraPerson, extraPersonRate, occupancy, occupancyRate, occupancyId, displayOrderId, selectWeekdays, selectWeekdaysRate, startDate, endDate):

    try:
        driver = webdriver.Chrome()

        driver.get(login_url)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#emailId[name="emailId"]'))).send_keys(username)

        driver.find_element(By.CSS_SELECTOR, 'input#password[name="password"]').send_keys(password)

        driver.find_element(By.CSS_SELECTOR, 'button.g-recaptcha.theme-button-one.dark').click()

        time.sleep(5)

        for cookie in driver.get_cookies():
            session.cookies.set(cookie['name'], cookie['value'])

        driver.quit()

        selected_days = get_days_selection(selectWeekdays)

        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
         
        payload = {
            "selectedRooms": roomId,
            "productId": propertyCode,
            "action": "ALLOCATION",
            "allocation": availability,  
            "startDate": startDate,
            "endDate": endDate,
            "days": selected_days
        }

        # print(json.dumps(payload, indent=4)) 

        api_url = "https://app.axisrooms.com/api/v1/updateInventory"

        response = session.post(api_url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            print("Inventory updated")
        else:
            print(f"Failed to update inventory. Status code: {response.status_code}")
            print(f"Details: {response.text}")

    except Exception as e:
        print({"error": str(e)})

# Call the function to update the inventory
# axisRoom_inventoryBulkUpdate(username, password, propertyCode, roomId, startDate, endDate, availability, selectWeekDays)

# Print the response
# print(json.dumps(response, indent=4))