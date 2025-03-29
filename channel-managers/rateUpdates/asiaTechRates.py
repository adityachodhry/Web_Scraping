import time
import requests
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By

session = requests.Session()
    
def AsiaTech_rates_update(userType, username, password, propertyCode, roomId, roomPlanId, channelCode, rate, startDate, endDate, selectWeekDays):
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
        
        # Submit the login form
        driver.find_elements(By.CLASS_NAME, 'btn-block')[0].click()
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
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        # Prepare and send the POST request to update inventory
        payload = {
            'ck_channel_id[]': channelCode,
            'regid': propertyCode,
            'bs_id': '',
            'roomid': roomId,  
            'mealplan': roomPlanId,  
            "0": rate,  
            '1': '',
            'extrabed': '',
            'extrachild': '',
            'extrainfnt': '',
            'from': startDate,
            'to': endDate,
            'days[]': selectWeekDays
        }
        
        api_url = 'https://www.asiatech.in/booking_engine/admin/update_inventory'
        # Send the POST request
        response = session.post(api_url, headers=headers, data=payload)
        return response.text

    except Exception as e:
        print(f"Error during processing account: {e}")
    finally:
        driver.quit()

if __name__ == '__main__':
    # Example usage
    userType = 'admin'
    username = 'Briars'
    password = 'Hotel@123'
    propertyCode = '5639' 
    channelCode = '3'
    roomId = '17951'
    roomPlanId = 'EP'
    rate = 5664
    selectWeekDays = 'Mon'  # Ensure this matches the expected format in the API

    startDate = "2024-09-09"
    endDate = "2024-09-10"

    # response = AsiaTech_rates_update(userType, username, password, propertyCode, roomId, roomPlanId, channelCode, rate, startDate, endDate, selectWeekDays)
    # print(f"Response: {response}, True")
