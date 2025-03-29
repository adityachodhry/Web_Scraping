import time
import json
import requests
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup

def exelyInventory(username, password):
    session = requests.Session()

    driver = webdriver.Chrome()
    login_url = 'https://secure.exely.com/secure/Enter.aspx'
    driver.get(login_url)

    # Login sequence
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

    selenium_cookies = driver.get_cookies()
    for cookie in selenium_cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    current_date = datetime.now()
    date_str = current_date.strftime('%Y-%m-%d')
    end_date = (current_date + timedelta(days=371)).strftime('%Y-%m-%d')

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

    inventoryUrl = "https://secure.exely.com/secure/ManagementOld/View/RoomTypeAvailabilityInRows.aspx"
    payload = {
        'start-date': date_str,
        'end-date': end_date,
        'room-type-quota-id': room_type_quota_id,
        'fixed-quota-mode': 'false'
    }

    response = session.post(inventoryUrl, data=payload)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        room_rows = soup.find_all('tr', class_='room-type-quantity-control-row')

        output_data = {
            "hotelCode": hotel_code,
            "timestamp": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
            "inventory": []
        }

        roomPlanIdUrl = "https://secure.exely.com/secure/Extranet/service/specialoffers"
        response2 = session.get(roomPlanIdUrl)
        roomPlanData = response2.json() if response2.status_code == 200 else {}
        roomplanInfo = roomPlanData.get('specialOffers', [])

        for room_row in room_rows:
            room_name = room_row.find('span', class_='room-type-name-label').text.strip()
            room_id = room_row.find('input', class_='room-type-id-input')['value']
            room_inventory = []

            for i in range(371):
                date_check = (current_date + timedelta(days=i)).strftime('%Y-%m-%d')

                room_control = soup.find('td', id=f'room-type-control-{room_id}-date-{date_check}')

                if room_control:
                    available_rooms = room_control.find_all('td', class_='colSlave')
                    available_room_count = int(available_rooms[0].text.strip()) if len(available_rooms) > 0 and available_rooms[0].text.strip().isdigit() else 0
                    quota_count = int(available_rooms[1].text.strip()) if len(available_rooms) > 1 and available_rooms[1].text.strip().isdigit() else 0
                    booking_count = room_control.find('td', class_='colBooking')
                    booking_count_value = int(booking_count.find('span').text.strip()) if booking_count and booking_count.find('span').text.strip().isdigit() else 0
                    total_rooms = quota_count + booking_count_value

                    roomPlanName = None
                    roomPlanId = None
                    rate = None

                    for roomplan in roomplanInfo:
                        if roomplan.get('name') == "EP (ROOM ALONE)":
                            roomPlanId = roomplan.get('id')
                            rateDate = (current_date + timedelta(days=i)).strftime('%Y-%m-%dT00:00:00.000Z')
                            ratesUrl = f"https://secure.exely.com/secure/Extranet/service/prices-and-restrictions/popup-preview?channelId=0&date={rateDate}&roomTypeId={room_id}&specialOfferId={roomPlanId}"

                            response3 = session.get(ratesUrl)
                            if response3.status_code == 200:
                                ratesData = response3.json()
                                roomCostData = ratesData.get('placementPrices', [])
                                for rataInfo in roomCostData:
                                    placementName = rataInfo.get('placementName')
                                    price = rataInfo.get('price') if placementName == "1 guest(s)" else None
                                    if price:
                                        rate = price
                                        print(f"Extracting data from {date_str} to {end_date}")
                                        break

                    room_inventory.append({
                        'arrivalDate': date_check,
                        'totalRooms': total_rooms,
                        'availableRooms': quota_count,
                        'rate': rate,
                    })

            output_data['inventory'].append({
                'roomId': room_id,
                'roomName': room_name,
                'inventory': room_inventory
            })

        with open('room_inventory.json', 'w', encoding='utf-8') as json_file:
            json.dump(output_data, json_file, ensure_ascii=False, indent=4)

        print("Inventory Data Extracted Successfully!")
    else:
        print(f"Failed to retrieve data: {response.status_code}")

    driver.quit()

exelyInventory('TL-503098-REV', 'NEST@786*1263')
