import time
import requests
import json
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# username = 'info@aravalimahal.com'
# password = 'Password@123'
# propertyCode = 180045
# startDate = "2024-09-10"
# roomId = 302043
# roomPlanId = 240781
# occupancyId = 1
# rate = 6500

def axisRoom_ratesUpdate(username, password, propertyCode, seasonCode, channelCode, roomId, roomName, rateTypeId, roomPlanId, mealPlanId, availability, rate, perExtraPerson, extraChildren, extraChildrenRate, extraPerson, extraPersonRate, occupancy, occupancyRate, occupancyId, displayOrderId, selectWeekdays, selectWeekdaysRate, startDate, endDate):
   
    login_url = 'https://app.axisrooms.com/'

    session = requests.Session()
    
    try:
        driver = webdriver.Chrome()
        driver.get(login_url)
        time.sleep(4)

        driver.find_element(By.CSS_SELECTOR, 'input#emailId[name="emailId"]').send_keys(username)
        driver.find_element(By.CSS_SELECTOR, 'input#password[name="password"]').send_keys(password)
        driver.find_element(By.CSS_SELECTOR, 'button.g-recaptcha.theme-button-one.dark').click()

        time.sleep(5)

        for cookie in driver.get_cookies():
            session.cookies.set(cookie['name'], cookie['value'])
        
        api_url = "https://app.axisrooms.com/api/v1/updateInventoryAndPrice"

        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        payload = {
            "productId": propertyCode,
            "roomValue": [
                {
                    "roomId": roomId,
                    "dates": [
                        {
                            "date": [startDate],
                            "allocation": "-1",  
                            "ratePlans": [
                                {
                                    "ratePlanId": roomPlanId,
                                    "occupancyPrice": [
                                        {
                                            "occupancyId": occupancyId,
                                            "price": rate
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ],
            "allOtas": True,
            "otaIds": [] 
        }

        # print(payload)

        response = session.post(api_url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            # result = response.json()
            print(response.text)
        else:
            print(f"Error: {response.status_code}")

    except TimeoutException:
        print("Error: Timeout while trying to log in or retrieve data.")
    
    finally:
        driver.quit()

# axisRoom_ratesUpdate(username, password, propertyCode, roomId, roomPlanId, occupancyId, rate, startDate) 

        
