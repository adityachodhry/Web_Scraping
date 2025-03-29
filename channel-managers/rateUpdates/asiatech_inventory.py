import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

def AsiaTech_rates_update(userType, username, password, propertyCode, roomId, channelCode, availability, rate, startDate, endDate):
    session = requests.Session()
    driver = webdriver.Chrome()

    try:
        url = 'https://www.asiatech.in/booking_engine/admin/login'

        driver.get(url)
        time.sleep(4)

        driver.find_element(By.ID, 'sel_master_login').send_keys(propertyCode)
        driver.find_element(By.ID, 'email').send_keys(username)
        driver.find_element(By.ID, 'password').send_keys(password)
        
        driver.find_elements(By.CLASS_NAME, 'btn-block')[0].click()
        time.sleep(4)

        for cookie in driver.get_cookies():
            session.cookies.set(cookie['name'], cookie['value'])

        hotel_name_element = driver.find_element(By.CLASS_NAME, 'username')
        hotel_name = hotel_name_element.text
        print(f"Logged in as: {hotel_name}")

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        payload = {
            "regid": propertyCode,
            "bs1id": "",
            "roomArray": [
                {
                    "roomid": roomId,
                    "updatevalues": [
                        {
                            "date": startDate,
                            "inventory": availability,
                            "rate": rate,
                            "prev": ''
                        }
                    ]
                }
            ],
            "startDate": startDate,
            "endDate": endDate
        }

        api_url = 'https://www.asiatech.in/booking_engine/admin/cm-ajax/cm-inventory/single-inventory.php'
       
        response = session.post(api_url, headers=headers, data=payload)

        return response.text

    except Exception as e:
        print(f"Error during processing account: {e}")
    finally:
        driver.quit()

if __name__ == '__main__':

    userType = 'admin'
    username = 'Briars'
    password = 'Hotel@123'
    propertyCode = '5639' 
    availability = "0"
    roomId = '17951'
    startDate = "2024-09-09"
    endDate = "2024-09-10"  

AsiaTech_rates_update(userType, username, password, propertyCode, roomId,availability, startDate, endDate)

    # print(f"Response: {response}")
