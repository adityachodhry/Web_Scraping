import time
import requests
import json
from datetime import datetime
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



# username = 'info@aravalimahal.com'
# password = 'Password@123'
# propertyCode = "180045"
# startDate = "2024-09-10"
# roomId = "302043"
# availability = "9"

def axisRoom_inventoryUpdate(username, password, propertyCode, seasonCode, channelCode, roomId, roomName, rateTypeId, roomPlanId, mealPlanId, availability, rate, perExtraPerson, extraChildren, extraChildrenRate, extraPerson, extraPersonRate, occupancy, occupancyRate, occupancyId, displayOrderId, selectWeekdays, selectWeekdaysRate, startDate, endDate):

    # Initialize the driver
    driver = webdriver.Chrome()

    login_url = 'https://app.axisrooms.com/'

    # Initialize a session
    session = requests.Session()

    try:
        # Go to the login page
        driver.get(login_url)

        # Wait for email input field to be present, then enter username
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#emailId[name="emailId"]'))).send_keys(username)

        # Enter password
        driver.find_element(By.CSS_SELECTOR, 'input#password[name="password"]').send_keys(password)

        # Click on the login button (captcha might need to be handled manually if present)
        driver.find_element(By.CSS_SELECTOR, 'button.g-recaptcha.theme-button-one.dark').click()

        # Wait for login to complete (you can adjust time as needed)
        time.sleep(5)

        # Transfer cookies from Selenium to the requests session
        for cookie in driver.get_cookies():
            session.cookies.set(cookie['name'], cookie['value'])

        # Close the browser after getting the necessary cookies
        driver.quit()

        # Prepare headers for the API request
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        # Prepare the payload for the inventory update
        payload = {
            "productId": propertyCode,
            "roomValue": [
                {
                    "roomId": roomId,
                    "dates": [
                        {
                            "date": startDate,
                            "allocation": availability,
                            "ratePlans": []
                        }
                    ]
                }
            ],
            "allOtas": True,
            "otaIds": []
        }

        # print(json.dumps(payload, indent=4))
        
        api_url = "https://app.axisrooms.com/api/v1/updateInventoryAndPrice"

        # Make the API request
        response = session.post(api_url, headers=headers, data=json.dumps(payload))

        # Check for response status and return JSON or error message
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to update inventory. Status code: {response.status_code}", "details": response.text}

    except Exception as e:
        return {"error": str(e)}

# Call the function and get the response
# response = axisRoom_inventoryUpdate(username, password, propertyCode, roomId, availability, startDate)

# # Print the response
# print(json.dumps(response, indent=4))
