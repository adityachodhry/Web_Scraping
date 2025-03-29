import sys
import time
import random
import requests, json
from seleniumwire import webdriver
from datetime import datetime, timedelta
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

    try:
        close_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[onclick=\"checkGoogleBulletin('N');\"]"))
        )

        WebDriverWait(driver, 10).until(EC.visibility_of(close_button))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[onclick=\"checkGoogleBulletin('N');\"]")))

        driver.execute_script("arguments[0].click();", close_button)
        print("Popup Closed")
    except Exception as e:
        print(f"Popup did not appear or could not be closed: {e}")

    time.sleep(2)

    try:
        max_v2_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.redirectmaxeco.maxv2-btn[title='Redirect to V2']"))
        )

        WebDriverWait(driver, 10).until(EC.visibility_of(max_v2_link))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.redirectmaxeco.maxv2-btn[title='Redirect to V2']")))

        max_v2_link.click()
        print("Max V2 Page Open!")
    except Exception as e:
        print(f"Could not find or click the Max V2 link: {e}")
    
    time.sleep(2)

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
    
    today = datetime.now()
    from_date = (today - timedelta(days=60)).strftime("%Y-%m-%d")
    to_date = today.strftime("%Y-%m-%d")

    first_endpoint = "https://max2.staah.net/webservice/maxApi.php"

    page = 1
    all_booking_data = []
    extracted_booking_data = []

    while True:
        payload = json.dumps({
            "module": "bookings",
            "Action": "createSessionForBookings",
            "searchchoice": "bookingdate",
            "datefrom1": from_date,
            "dateto1": to_date,
            "source": "All",
            "channel_flag": "Y",
            "pid": "",
            "PageNo": page
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
            break

        get_bookings = first_data.get('GetBookings', {})
        if not get_bookings:
            break  

        bookings = []
        if isinstance(get_bookings, dict):
            for booking_id, booking_details in get_bookings.items():
                if isinstance(booking_details, dict):
                    bookingsId = booking_details.get('bm_bookingsId', None)
                    if bookingsId:
                        bookings.append(bookingsId)
                        print(f"Booking ID {booking_id}")
        else:
            print("GetBookings is not a dict.")
            break

        if not accessformid or not bookings:
            print("Required formid or bookingsId not found.")
            break

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

            with open('Row.json', 'w') as json_file:
                json.dump(second_data, json_file, indent=4)

            booking_info = second_data.get('data', {})
            totalTax = booking_info.get('TotalTaxes').split(' ')[1].replace(',', '')
            RoomTotal = booking_info.get('RoomTotal').split(' ')[1].replace(',', '')
            AmountDue = float(booking_info.get('AmountDue').split(' ')[1].replace(',', ''))


            if booking_info:
                hInfo = booking_info.get('roomidandpackageidrows', [])
                if hInfo:
                    propertyId = hInfo[0].get('propertyId')
                    bookings_Id = hInfo[0].get('bookingsId').split(' ')[0]
                    checkIn = hInfo[0].get('checkIn')
                    checkOut = hInfo[0].get('checkOut')
                    rooms = int(hInfo[0].get('rooms'))
                    amount = float(hInfo[0].get('amount'))
                    adults = hInfo[0].get('adults').split(':')[0]
                    children = hInfo[0].get('children').split(':')[0]
                    baseRate = hInfo[0].get('baseRate')
                    no_of_nights = hInfo[0].get('no_of_nights')

                    if AmountDue == amount or AmountDue > 0.0:
                        status = "Not Paid"
                    elif AmountDue == 0.0:
                        status = "Fully Paid"
                    else:
                        status = "N/A"

                    gdsrateplan_full = hInfo[0].get('gdsrateplan')
                    if gdsrateplan_full:
                        parts = gdsrateplan_full.split('+')
                        last_code = parts[-1].strip()
                        
                        if 'Breakfast+Included' in gdsrateplan_full:
                            roomPlan = 'CP'
                        elif 'Room+Only' in gdsrateplan_full:
                            roomPlan = 'EP'
                        elif last_code in ['MAP', 'CP', 'EP']:
                            roomPlan = last_code
                        else:
                            roomPlan = 'NA'
                    else:
                        roomPlan = 'NA'

                    bookingdetail = booking_info.get('bookingdetail', {})
                    if bookingdetail:
                        bm_channelName = bookingdetail.get('bm_channelName')
                        if bm_channelName in ['Goibibo', 'Booking.com', 'Agodaycs', 'MakeMyTrip', 'go-mmt']:
                            channelSegment = 'OTA'
                        elif bm_channelName:
                            channelSegment = 'PMS'
                        else:
                            channelSegment = "NA"

                        bm_lastupdated = bookingdetail.get('bm_lastupdated').split(' ')[0]
                        booking_date = bookingdetail.get('bm_createDate').split(' ')[0]
                        bm_currencyCode = bookingdetail.get('bm_currencyCode')

                        bm_status = bookingdetail.get('bm_status')
                        checkIn_dt = datetime.strptime(checkIn, "%Y-%m-%d")
                        checkOut_dt = datetime.strptime(checkOut, "%Y-%m-%d")
                        
                        if bm_status == 'C' and checkIn_dt <= today <= checkOut_dt:
                            current_status = 'CI'
                        elif bm_status == 'C' and today > checkOut_dt:
                            current_status = 'CO'
                        elif bm_status == 'M' or 'P':
                            current_status = 'UCB'
                        elif bm_status == 'C':
                            current_status = 'CFB'
                        elif bm_status == 'D':
                            current_status = 'CN'
                        else:
                            current_status = 'NA'
                    
                    if len(hInfo) > 1:
                        rooms += 1

                    isActive = rooms > 1

                    if rooms > 1:
                        roomCostPerRoom = float(RoomTotal) / rooms
                        taxAmountPerRoom = float(totalTax) / rooms
                        totalAmountPerRoom = amount / rooms

                    else:
                        roomCostPerRoom = RoomTotal
                        taxAmountPerRoom = totalTax
                        totalAmountPerRoom = amount
            

                    for room_index, room_info in enumerate(hInfo):
                        roomId = room_info.get('roomId', '')
                        roomName = room_info.get('roomTypeName', '').replace('+', ' ')

                        if rooms > 1:
                            reservationNumber = f"{bookings_Id}-{room_index + 1}"
                        else:
                            reservationNumber = bookings_Id

                        for guest_detail in room_info.get('guestDetails', []):
                            guest_name = f"{guest_detail.get('roomfirstName', '')} {guest_detail.get('roomlastName', '')}"
                            try:
                                adultNew = int(guest_detail.get('adults', 0))
                            except ValueError:
                                adultNew = 0
                            try:
                                childrenNew = int(guest_detail.get('children', 0))
                            except ValueError:
                                childrenNew = 0

                            booking_details = {
                                "hotelCode": propertyId,
                                "reservationNumber": reservationNumber,
                                "isGroup": isActive,
                                "source": bm_channelName,
                                "guestDetails": {
                                    "name": guest_name,
                                },
                                "bookingDetails": {
                                    "arrivalDate": checkIn,
                                    "departureDate": checkOut,
                                    "totalNights": int(no_of_nights),
                                    "currentStatus": current_status,
                                    "roomDetails": {
                                        "roomTypeId": roomId,
                                        "roomTypeName": roomName,
                                        "roomPlan": roomPlan,
                                        "pax": {
                                            "totalAdults": adultNew,
                                            "totalChildren": childrenNew
                                        }
                                    },
                                    "createdOn": booking_date,
                                    "lastModifiedOn": bm_lastupdated,
                                },
                                # "sourceSegment": channelSegment,
                                "paymentDetails": {
                                    "status": status,
                                    "amount": float(totalAmountPerRoom),
                                    "outstanding": AmountDue
                                },
                                "priceSummary": {
                                    "roomCost": float(roomCostPerRoom),
                                    "totalCost": float(totalAmountPerRoom),
                                    "taxAmount": float(taxAmountPerRoom),
                                }
                            }

                            extracted_booking_data.append(booking_details)
        page += 1

    with open('extracted_booking_Data.json', 'w') as json_file:
        json.dump(extracted_booking_data, json_file, indent=2)

        print(f"{propertyId} Reservation Data Extracted!")

    return extracted_booking_data

# staahReservation('ankur.nograhiya@retvensservices.com', 'Retvens@1234567', 5566)
