import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime, timedelta

# Create a session to manage cookies across requests
session = requests.Session()

def asiaTech_RatesBulk(userType, username, password, propertyCode, roomId, roomPlanId, channelCode, rate, startDate, endDate, selectWeekDays):
    # Initialize Selenium WebDriver
    driver = webdriver.Chrome()

    try:
        url = 'https://www.asiatech.in/booking_engine/admin/login'

        # Go to the login page
        driver.get(url)
        time.sleep(4)

        # Input credentials and submit the form
        driver.find_element(By.ID, 'sel_master_login').send_keys(propertyCode)
        driver.find_element(By.ID, 'email').send_keys(username)
        driver.find_element(By.ID, 'password').send_keys(password)
        driver.find_element(By.CLASS_NAME, 'btn-block').click()
        time.sleep(4)

        # Set cookies for the requests session
        for cookie in driver.get_cookies():
            session.cookies.set(cookie['name'], cookie['value'])

        # Extract the hotel name for verification (optional)
        hotel_name_element = driver.find_element(By.CLASS_NAME, 'username')
        hotel_name = hotel_name_element.text
        print(f"Logged in as: {hotel_name}")

        # Prepare the headers
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }

        # Convert start and end dates from string to datetime objects
        startDate = datetime.strptime(startDate, "%Y-%m-%d")
        endDate = datetime.strptime(endDate, "%Y-%m-%d")

        # Convert start and end dates to the proper format for the payload
        startDate = startDate.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        endDate = endDate.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        # Prepare the payload
        payload = {
            "ck_channel_id[]": channelCode,
            "regid": propertyCode,
            "roomid": roomId,
            "mealplan": roomPlanId,
            "rate": rate,
            "from": startDate,
            "to": endDate,
            "days[]": selectWeekDays  # List of selected weekdays
        }

        # Post request setup
        post_url = "https://www.asiatech.in/booking_engine/admin/cm-ajax/cm-rate/ratecal_modal_update_data.php"

        # Send the POST request
        response = session.post(post_url, headers=headers, data=payload)

        # Print the response
        print(f"Response for {propertyCode}: {response.text}")
    
    except Exception as e:
        print(f"Error during processing account: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    # Define the hotel details and rate information
    roomId = '17951'
    ratePlanId = 'EP'
    channelCode = ["BookingEngine",'3']
    rate = 4800

    # Set the date range
    startDate = "2024-09-09"
    endDate = "2024-09-10"  
    selectWeekDays = ['Mon', 'Tue']

    # Define account credentials
    account = {
        'userType': 'admin',
        'username': 'Briars',
        'password': 'Hotel@123',
        'propertyCode': '5639'
    }

    # Call the function directly
    response = asiaTech_RatesBulk(account['userType'], account['username'], account['password'], account['propertyCode'], roomId, ratePlanId, channelCode, rate, startDate, endDate, selectWeekDays)
