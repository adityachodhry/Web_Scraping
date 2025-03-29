import sys
import time
import random
import requests
import json
from datetime import datetime
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def staahReservation(email, password, property_code):

    options = {
        'verify_ssl': False 
    }
    
    driver = webdriver.Chrome(seleniumwire_options=options)

    url = 'https://max.staah.net/hotels/index.php'

    driver.get(url)
    time.sleep(4)

    driver.find_element(By.NAME, 'propertyId').send_keys(property_code)
    driver.find_element(By.NAME, 'email').send_keys(email)
    driver.find_element(By.NAME, 'password').send_keys(password)
    
    time.sleep(random.randint(2, 3))

    driver.find_element(By.NAME, 'password').send_keys(Keys.ENTER)

    time.sleep(random.randint(6, 8))

    availability_calendar_selector = 'a.nav-link.collapsed.false[href="/hotel/dashboard"]'

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, availability_calendar_selector))
        )
        element.click()
    except Exception as e:
        print(f"Error clicking on availability calendar: {e}")

    time.sleep(random.randint(4, 6))

    auth_key = None
    for request in driver.requests:
        if request.response:
            if 'Propertyauthkey' in request.headers:
                auth_key = request.headers['Propertyauthkey']
                print(f"Propertyauthkey: {auth_key}")
                break

    driver.quit()

    if not auth_key:
        print("Authorization key not found.")
        return

    first_endpoint = "https://max2.staah.net/webservice/maxApi.php"

    payload = json.dumps({
        "module": "bookings",
        "Action": "createSessionForBookings",
        "searchchoice": "bookingdate",
        "datefrom1": "05-May-2024",
        "dateto1": "05-Jun-2024",
        "source": "All",
        "channel_flag": "Y",
        "pid": "",
        "PageNo": 1
    })

    headers = {
        'Propertyauthkey': auth_key,
        'Origin': 'https://v2.staah.net',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Content-Type': 'application/json'
    }

    response = requests.post(first_endpoint, headers=headers, data=payload)
    response_data = response.json()

    first_data = response_data.get('data', {})
    accessformid = first_data.get('accessformid')
    print(f"Accessformid: {accessformid}")

    if not isinstance(first_data, dict):
        print("Unexpected data structure:", type(first_data))
        return

    bookings = []
    get_bookings = first_data.get('GetBookings', {})
    if isinstance(get_bookings, dict):
        for booking_id, booking_details in get_bookings.items():
            if isinstance(booking_details, dict):
                bookingsId = booking_details.get('bm_bookingsId', None)
                if bookingsId:
                    bookings.append(bookingsId)
                    print(f"Booking ID for {booking_id}: {bookingsId}")
    else:
        print("GetBookings is not a dict.")

    if not accessformid or not bookings:
        print("Required formid or bookingsId not found.")
        return

    all_booking_data = []
    extracted_booking_data = []

    for bookingsId in bookings:
        second_endpoint = "https://max2.staah.net/webservice/maxApi.php"

        payload = json.dumps({
            "module": "booking_details_new",
            "formid": accessformid,
            "bookingsId": bookingsId
        })

        second_response = requests.post(second_endpoint, headers=headers, data=payload)
        second_data = second_response.json()
        all_booking_data.append(second_data)
        
        # Extract required fields
        booking_info = second_data.get('data', {})
        if booking_info:
            booking_details = {
                'bookdate': booking_info.get('bookdate'),
                'firstName': booking_info.get('getDecodedData', {}).get('firstName'),
                'lastName': booking_info.get('getDecodedData', {}).get('lastName'),
                'roomId': booking_info.get('roomType_package', {}).get('roomIdsArray', {}),
                'propertyId': booking_info.get('roomidandpackageidrows', {}).get('propertyId'),
                'bookingsId': booking_info.get('roomidandpackageidrows', {}).get('bookingsId'),
                'checkIn': booking_info.get('roomidandpackageidrows', {}).get('checkIn'),
                'checkOut': booking_info.get('roomidandpackageidrows', {}).get('checkOut'),
                'rooms': booking_info.get('roomidandpackageidrows', {}).get('rooms'),
                'amount': booking_info.get('roomidandpackageidrows', {}).get('amount'),
                'adults': booking_info.get('roomidandpackageidrows', {}).get('adults'),
                'children': booking_info.get('roomidandpackageidrows', {}).get('children'),
                'gdsrateplan': booking_info.get('roomidandpackageidrows', {}).get('gdsrateplan'),
                'baseRate': booking_info.get('roomidandpackageidrows', {}).get('baseRate'),
                'no_of_nights': booking_info.get('roomidandpackageidrows', {}).get('no_of_nights'),
                'Total_noofnights': booking_info.get('Total_noofnights'),
                'Total_noofguests': booking_info.get('Total_noofguests'),
                'RoomTotal': booking_info.get('RoomTotal'),
                'TotalTaxes': booking_info.get('TotalTaxes'),
                'AmountPaid': booking_info.get('AmountPaid'),
                'AmountDue': booking_info.get('AmountDue'),
                'bm_status': booking_info.get('bookingdetail', {}).get('bm_status'),
                'bm_channelName': booking_info.get('bookingdetail', {}).get('bm_channelName'),
                'bm_cancellationReason': booking_info.get('bookingdetail', {}).get('bm_cancellationReason'),
                'bm_currencyCode': booking_info.get('bookingdetail', {}).get('bm_currencyCode')

            }
            extracted_booking_data.append(booking_details)
            # [0].data.bookingdetail.bm_status
            
    # with open('staah_booking_Data.json', 'w') as json_file:
    #     json.dump(all_booking_data, json_file, indent=2)

    # Save extracted fields
    with open('extracted_booking_Data.json', 'w') as json_file:
        json.dump(extracted_booking_data, json_file, indent=2)

    print("All booking data saved to staah_booking_Data.json")
    print("Extracted booking data saved to extracted_booking_Data.json")

staahReservation('md@shantiram.in', 'Ayush$9797', 9295)
