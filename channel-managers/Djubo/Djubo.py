import time
import requests
import random
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
# from mongo import push_to_mongodb

accounts = [
    {'username': 'Sales@shivacontinental.in', 'password': 'shiva@1234'},
]

results = []

driver = webdriver.Chrome()

try:
    for account in accounts:
        username = account['username']
        password = account['password']

        try:
            url = 'https://apps.djubo.com/sign-in/'

            driver.get(url)

            driver.find_element(By.NAME, 'email_address').send_keys(username)
            driver.find_element(By.NAME, 'password').send_keys(password)

            time.sleep(random.randint(6, 8))

            driver.find_elements(By.CLASS_NAME, 'submitBtn')[0].click()

            time.sleep(4)

            cookies = driver.get_cookies()

            authorization = next(
                (cookie['value'] for cookie in cookies if cookie['name'] == 'auth_token_7'), None)

            if not authorization:
                print(f"SSID cookie not found for account {username}. Skipping.")
            else:
                print(f'SSID for account {username}  {authorization}')

                headers = {
                    'Cookie': f'auth_token_7={authorization}',
                    'Content-Type': 'application/json'
                }
                property_endpoint = "https://apps.djubo.com/core-data/properties"
                property_response = requests.get(property_endpoint, headers=headers)
                property_response_content = property_response.json()
                for property in property_response_content :
                    hotel_id = property.get("id")

                page_number = 1 
                while True:

                    endpoint = f"https://apps.djubo.com/analytics-api-data/accounts/0/properties/{hotel_id}/folios-list?page={page_number}&search=&type=2&via=folioSearch"

                    response = requests.get(endpoint, headers=headers)

                    print(f"Status Code for account {username} (Page {page_number}): {response.status_code}")

                    response_content = response.json()

                    if not response_content:
                        print(f"No more data for account {username}. Exiting loop.")
                        break
                    
                    data_slot = response_content.get('general_details')
                    

                    for data in response_content:
                        bkgDetails = {}

                        bkgDetails['hotelName'] = data['general_details']['property_name']
                        bkgDetails['res'] = str(data['general_details']['guest_id'])

                        booking_date = datetime.strptime(data['general_details']['created_on'], '%m/%d/%Y')
                        bkgDetails['bookingDate'] = booking_date.strftime("%Y-%m-%d")

                        bkgDetails['guestName'] = data['general_details']['guest_name']

                        arrival_date = datetime.strptime(data['general_details']['arrival_date'], '%m/%d/%Y')
                        departure_date = datetime.strptime(data['general_details']['departure_date'], '%m/%d/%Y')

                        bkgDetails['arrivalDate'] = arrival_date.strftime("%Y-%m-%d")
                        bkgDetails['deptDate'] = departure_date.strftime("%Y-%m-%d")

                        room_type_full = data['general_details']['room_categories']
                        room_type_parts = room_type_full.split(' X ')
                        room_type = room_type_parts[0] if room_type_parts else room_type_full

                        bkgDetails['room'] = room_type

                        if data['general_details']['agency_class'] == "OTA":
                            bkgDetails['source'] = data['general_details']['agency_name']
                        else : 
                            continue

                        adults = data['general_details']['total_adults']
                        children = data['general_details']['total_children']
                        lead_time = arrival_date - booking_date

                        bkgDetails['pax'] = f"{adults}\{children}"

                        bkgDetails['noOfNights'] = data['room_details']['total_room_nights']
                        bkgDetails['totalCharges'] = round(data['payment_summary_details']['total_amount'], 2)
                        bkgDetails['ADR'] = bkgDetails['totalCharges'] / bkgDetails['noOfNights']


                        bkgDetails['lead'] = lead_time.days
                        bkgDetails['hotelCode'] = str(hotel_id)

                        if data['general_details']['status'] == 'Confirmed':
                            bkgDetails['isActive'] = "true"
                        else:
                            continue

                        results.append(bkgDetails)
                        
                    page_number += 1 

                with open('results_djubonewtemp.json', 'w') as json_file:
                    json.dump(results, json_file, indent=2)

        except Exception as e:
            print(f"An error occurred for account {username}  {str(e)}")
            # print(data)
            # with open('results_djubonew.json', 'w') as json_file:
            #     json.dump(results, json_file, indent=2)

    # push_to_mongodb(results)
finally:

    if 'driver' in locals():
        driver.quit()