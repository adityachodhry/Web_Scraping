import time
import requests
import random
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from mongo import push_to_mongodb
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Run the script with CLI options')
    parser.add_argument('--propertyCode', required=True)
    parser.add_argument('--username', required=True)
    parser.add_argument('--password', required=True)
    return parser.parse_args()

# Get command-line arguments
args = parse_args()

accounts = [
    {'property_code': args.propertyCode, 'username': args.username, 'password': args.password}]

# Create an empty list to store results
results = []
today = datetime.date.today().strftime("%d/%m/%Y")
driver = webdriver.Chrome()

try:
    for account in accounts:
        property_code = account['property_code']
        username = account['username']
        password = account['password']

        try:
            url = 'https://live.ipms247.com/login/'

            # Go to the login page
            driver.get(url)
            time.sleep(4)

            # Input credentials and submit the form
            driver.find_element(By.NAME, 'username').send_keys(username)
            driver.find_element(By.NAME, 'password').send_keys(password)
            driver.find_element(By.NAME, 'hotelcode').send_keys(property_code)
            driver.find_element(By.ID, 'universal_login').submit()

            # Wait for the login process to complete
            time.sleep(random.randint(6, 8))

            try :
                driver.find_elements(By.ID, 'close_btn')[0].click()
                time.sleep(random.randint(3,5))
            except :
                 pass
            
            try :
                driver.find_elements(By.CLASS_NAME, 'btnER')[0].click()
            except :
                 pass

            # Wait for the button click to take effect
            time.sleep(4)

            # Get the cookies
            cookies = driver.get_cookies()

            # Find the SSID cookie
            ssid_cookie = next(
                (cookie['value'] for cookie in cookies if cookie['name'] == 'SSID'), None)

            # Check if SSID cookie is found before proceeding
            if not ssid_cookie:
                print(
                    f"SSID cookie not found for account {username} ({property_code}). Skipping.")
            else:
                print(
                    f'SSID for account {username} ({property_code}): {ssid_cookie}')

                # Set up the endpoint and headers for the POST request
                endpoint = "https://live.ipms247.com/rcm/services/servicecontroller.php"
                headers = {
                    'Cookie': f'SSID={ssid_cookie}',
                    'Content-Type': 'application/json'
                }

                # Set up the body for the POST request
                body = {
                    "action": "getbookinglist",
                    "limit": 20000,
                    "offset": 0,
                    "guestname": "",
                    "roomtype": "",
                    "source": "",
                    "arrivalfrom": "",
                    "arrivalto": "",
                    "resfrom": "27/11/2021",
                    "resto": today,
                    "status": "",
                    "restype": "",
                    "arrivalflag": "false",
                    "resfromflag": "true",
                    "onlyunconfimpayment": "false",
                    "web": "true",
                    "channel": "true",
                    "pmcstatus": "",
                    "deptflag": "false",
                    "deptFrom": "",
                    "deptTo": "",
                    "search": "",
                    "rmsstatus": "",
                    "number": "",
                    "chkPMS": "false",
                    "is_property": property_code,
                    "exportlimit": 0,
                    "ratetype": "",
                    "pgtype": "",
                    "datetype": 1,
                    "stayoverfrom": "",
                    "stayoverto": "",
                    "service": "bookinglist_rcm"
                }

                # Make the POST request
                response = requests.post(endpoint, headers=headers, json=body)

                # Print the response status code and content
                print(f"Status Code for account {username} ({property_code}): {response.status_code}")

                response_content = response.json()

                entries = response_content['0']['data']

                for entry in entries:
                    bkg_details = {}

                    booking_date = datetime.datetime.strptime(entry.get('transaction_date'), "%d/%m/%Y")
                    checkin_date = datetime.datetime.strptime(entry.get('arrival_date'), "%Y-%m-%d")
                    lead_time = (checkin_date - booking_date).days

                    bkg_details['hotelName'] =  entry.get('hotel_name')
                    bkg_details['res'] = entry.get('ResNo')
                    bkg_details['bookingDate'] = booking_date.strftime("%Y-%m-%d")
                    bkg_details['guestName'] = entry.get('GuestName')
                    bkg_details['arrivalDate'] = entry.get('arrival_date')
                    bkg_details['deptDate'] = entry.get('departure_date') 
                    bkg_details['room'] = entry.get('roomtype')
                    bkg_details['pax'] = f"{entry.get('adult')}\{entry.get('child') }"
                    bkg_details['ADR'] = float(entry.get('ADR'))
                    bkg_details['source'] = entry.get('Source')
                    bkg_details['noOfnights'] = int(entry.get('noofnights'))
                    bkg_details['lead'] = int(lead_time)
                    bkg_details['totalCharges'] = bkg_details['ADR'] * bkg_details['noOfnights']
                    bkg_details['hotelCode'] =  property_code
                    bkg_details['isActive'] = "true"

                # Append the result to the list
                    results.append(bkg_details)
                

        except Exception as e:
            print(
                f"An error occurred for account {username} ({property_code}): {str(e)}")

finally:
    # Close the browser in the finally block to ensure it happens even if there's an exception
    if 'driver' in locals():
        driver.quit()

push_to_mongodb(results)