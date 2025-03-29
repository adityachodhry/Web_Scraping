import time
import json
import requests
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup

def exelyRoomConfig(username, password):
    session = requests.Session()

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

        selenium_cookies = driver.get_cookies()
        for cookie in selenium_cookies:
            session.cookies.set(cookie['name'], cookie['value'])
        
        # current_date = datetime.now()
        # date_start = current_date.strftime('%d.%m.%Y')
        # date_end = (current_date + timedelta(days=1)).strftime('%d.%m.%Y')

        roomIdUrl = "https://secure.exely.com/secure/Extranet/service/roomtypes"
        response1 = session.get(roomIdUrl)
        if response1.status_code == 200:
            results1 = response1.json()
            room_types = results1.get('roomTypes', [])
        
        roomPlanIdUrl = "https://secure.exely.com/secure/Extranet/service/specialoffers"
        response2 = session.get(roomPlanIdUrl)
        roomPlanData = response2.json() if response2.status_code == 200 else {}
        room_plan_info = roomPlanData.get('specialOffers', [])
        
        room_type_quota_id = "https://secure.exely.com/secure/ManagementOld/RoomTypeAvailability.aspx?"
        response1 = session.get(room_type_quota_id)

        if response1.status_code == 200:
            soup = BeautifulSoup(response1.text, 'html.parser')
            quota_link = soup.find('a', href=lambda href: href and "RoomTypeQuotaDefaults.aspx?id=" in href)
            
            if quota_link:
                room_type_quota_id = quota_link['href'].split('=')[-1]
            else:
                print("Room Type Quota ID not found.")
                driver.quit()
                return
            
            hotel_code_div = soup.find('div', class_='rightFloated hotelName')
            hotel_code = hotel_code_div.contents[0].strip().split('#')[1].strip() if hotel_code_div else "Unknown"

            hotel_name_tag = hotel_code_div.find('strong') if hotel_code_div else None
            hotel_name = hotel_name_tag.text.strip() if hotel_name_tag else "Unknown"

        final_data = {
            "hotelCode": hotel_code,
            "propertyName": hotel_name,
            "info": [
                {
                    "channelId": 0,
                    "channelName": None,
                    "roomInfo": []
                }
            ]
        }

        for room in room_types:
            room_id = room.get('id')
            room_name = room.get('name')

            room_plan_list = []
            for roomplan in room_plan_info:
                roomPlanId = roomplan.get('id')
                roomPlanName = roomplan.get('name')
                room_plan_list.append({
                    "roomPlanId": roomPlanId,
                    "roomPlanName": roomPlanName
                })
            
            room_info = {
                "roomId": room_id,
                "roomName": room_name,
                "roomPlanInfo": room_plan_list
            }
            final_data["info"][0]["roomInfo"].append(room_info)
        
        with open('ExelyRateData.json', 'w') as json_file:
            json.dump(final_data, json_file, indent=2)

        print("Data saved successfully to ExelyRateData.json")

        return final_data

    except Exception as e:
        print(f"Failed to navigate: {str(e)}")
    finally:
        driver.quit()

exelyRoomConfig('TL-503098-REV', 'NEST@786*1263')
