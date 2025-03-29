import time, json
import requests
import random
from datetime import datetime, timedelta
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
# from mongo import push_to_mongodb

accounts = [{'username': 'htlkana1', 'password': 'htlkana111'}]

results = []

months_per_request = 3

current_date = datetime.now()

start_date = current_date - timedelta(days=365 * 3)

driver = webdriver.Chrome()

try:
    for account in accounts:
        username = account['username']
        password = account['password']

        url = 'https://www.eglobe-solutions.com/hms/dashboard'

        driver.get(url)
        time.sleep(4)

        driver.find_element(By.NAME, 'Username').send_keys(username)
        driver.find_element(By.NAME, 'Password').send_keys(password)

        time.sleep(random.randint(6, 8))

        driver.find_elements(By.NAME, 'button')[0].click()

        time.sleep(2)

        authorization_value = next(
            (request.headers['authorization'] for request in driver.requests if 'authorization' in request.headers), None)
        print(f"Auth = {authorization_value}")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': authorization_value
        }

        body = {
            "SearchBy": "BookingDate",
            "FromDate": "1-Jan-2023",
            "TillDate": "22-Nov-2023"
        }
        post_endpoint = "https://www.eglobe-solutions.com/cmapi/bookings/search"
        post_response = requests.post(
            post_endpoint, headers=headers, json=body)

        post_response_content = post_response.json()

        hotelcodes = post_response_content.get('BookingList', [])
        hotelcode = hotelcodes[0].get(
            'EgsPropertyId', None) if hotelcodes else None

        while start_date < current_date:
            end_date = start_date + timedelta(days=30 * months_per_request)

            date_from = start_date.strftime("%d %b %Y")
            date_till = end_date.strftime("%d %b %Y")

            api_url = "https://www.eglobe-solutions.com/hmsapi/reports/ArcReport"

            main_body = {
                "SearchBy": "BookingDate",
                "DateFrom": date_from,
                "DateTill": date_till
            }

            response = requests.post(api_url, headers=headers,json=main_body)

            response_content = response.json()

            bookingList = response_content['Result']['Data']
            # bookingList = response_result.get('Data', [])
            for booking in bookingList:
                try:
                    booking_date = datetime.strptime(
                        booking['BookingTime'], "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d")
                except ValueError:
                    booking_date = datetime.strptime(
                        booking['BookingTime'], "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d")

                try:
                    arrival_date = datetime.strptime(
                        booking['CheckInDate'], "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d")
                except ValueError:
                    arrival_date = datetime.strptime(
                        booking['CheckInDate'], "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d")

                lead_time = (datetime.strptime(arrival_date, "%Y-%m-%d") -
                             datetime.strptime(booking_date, "%Y-%m-%d")).days

                bkglist = {
                    'hotelName': booking['PropertyName'],
                    'res': str(booking['BookingId']),
                    'bookingDate': booking_date,
                    'guestName': booking['GuestName'],
                    'arrivalDate': datetime.strptime(booking['CheckInDate'], "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d"),
                    'deptDate': datetime.strptime(booking['CheckOutDate'], "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d"),
                    'room': booking['BookedRoomsInfo'].split('(')[0].strip(),
                    'pax': f"{booking['NumAdults']}\{booking['NumChildren']}",
                    'source': booking['ChannelName'],
                    'totalCharges': booking['Amount_BookingTotal'],
                    'noOfNights': booking['NumNights'] * booking['NumRooms'],
                    'lead': int(lead_time),
                    'hotelCode': str(hotelcode),
                    'isActive': "true" if booking['BookingStatus'] == 'BOOKED' else "false",
                    'ADR' : booking['Amount_BookingTotal'] / (booking['NumNights'] * booking['NumRooms'])
                }
                results.append(bkglist)

                with open('neweglobeBooking.json', 'w') as json_file:
                    json.dump(results, json_file, indent=2)

            start_date = end_date

finally:
    if 'driver' in locals():
        driver.quit()

print(results)
# push_to_mongodb(results)