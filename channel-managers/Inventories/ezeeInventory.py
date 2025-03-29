import requests
import json
import time
import requests
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta

endpoint = "https://live.ipms247.com/rcm/services/servicecontroller.php"


def getEzeeInventories(username, password, property_code):
    today = datetime.now()
    end_date = today + timedelta(days=7)
    driver = webdriver.Chrome()

    try:
        url = 'https://live.ipms247.com/login/'

        driver.get(url)
        time.sleep(4)

        driver.find_element(By.NAME, 'username').send_keys(username)
        driver.find_element(By.NAME, 'password').send_keys(password)
        driver.find_element(By.NAME, 'hotelcode').send_keys(property_code)
        driver.find_element(By.ID, 'universal_login').submit()

        time.sleep(random.randint(6, 8))

        try:
            driver.find_elements(By.ID, 'close_btn')[0].click()
            time.sleep(random.randint(3, 5))
        except:
            pass

        try:
            driver.find_elements(By.CLASS_NAME, 'btnER')[0].click()
        except:
            pass

        # Wait for the button click to take effect
        time.sleep(10)

        try:
            txt_change_pwd = driver.find_element(By.ID, 'txtchnagepwd')
            if txt_change_pwd:
                txt_change_pwd.send_keys(password)
                # Find and click the Unlock button within the specified div
                unlock_button = driver.find_element(
                    By.CSS_SELECTOR, 'div.pwdfooter > button.btnprimary')
                unlock_button.click()
                print("Password entered and Unlock button clicked.")
                time.sleep(5)
        except Exception as e:
            print(
                f"Password change input field not found or could not be interacted with")

        cookies = driver.get_cookies()

        ssid_cookie = next(
            (cookie['value'] for cookie in cookies if cookie['name'] == 'SSID'), None)

        if not ssid_cookie:
            print(
                f"SSID cookie not found for account {username} ({property_code}). Skipping.")
        else:
            print(
                f'SSID for account {username} ({property_code}): {ssid_cookie}')

            start_date = today.strftime("%Y-%m-%d")
            end_date = end_date.strftime("%Y-%m-%d")

            body = {
                "action": "getInventoryData",
                "service": "inventoryrates",
                "startdate": start_date,
                "allocationmode": "ALLOCATED",
                "enddate": end_date
            }

            headers = {
                'Cookie': f'SSID={ssid_cookie}',
                'Content-Type': 'application/json'
            }

            response = requests.post(endpoint, headers=headers, json=body)
            print(
                f"Status Code for account {username} ({property_code}): {response.status_code}")

            response_json = response.json()

            inventory_data = response_json["inventorydata"]
            listing = response_json["listing"]

            room_data = []

            for room_type in listing:
                mapped_data = []
                room_id = room_type["roomtypeunkid"]
                room_name = room_type["roomtype"]
                for a, b in inventory_data.items():
                    inventory_counts = b.get(room_id, {})

                current_date = start_date
                while current_date <= end_date:
                    for availability in inventory_counts:
                        if isinstance(availability, str):
                            totalRooms = int(availability)
                            break
                    for availability in inventory_counts:
                        mapped_data.append({
                            "arrivalDate": current_date,
                            "totalRooms": totalRooms,
                            "availableRooms": int(availability)
                        })
                        current_date = (datetime.strptime(
                            current_date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")

                room_data.append({
                    "roomId": room_id,
                    "roomName": room_name,
                    "inventory": mapped_data
                })

            final_data = {
                "hotelCode": str(property_code),
                "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "inventory": room_data
            }

            # Save the mapped data to a separate JSON file
            with open(f"{property_code}_inventory_data.json", "w") as outfile:
                json.dump(final_data, outfile, indent=4)

            print("Mapped data saved to mapped_inventory_data.json")
    except:
        pass

    finally:
        # Close the browser in the finally block to ensure it happens even if there's an exception
        if 'driver' in locals():
            driver.quit()