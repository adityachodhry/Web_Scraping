import time
import json
import requests
import random
from datetime import datetime, timedelta
from seleniumwire import webdriver
from selenium.webdriver.common.by import By

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
        
        authorization_value = next((request.headers['authorization'] for request in driver.requests if 'authorization' in request.headers), None)
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
        post_response = requests.post(post_endpoint, headers=headers, json=body)

        post_response_content = post_response.json()

        hotelcodes = post_response_content.get('BookingList', [])
        hotelcode = hotelcodes[0].get('EgsPropertyId', None) if hotelcodes else None

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

            response = requests.post(api_url, headers=headers, json=main_body)

            response_content = response.json()

            bookingList = response_content['Result']['Data']
            for booking in bookingList:

                noOfRoom = booking.get('NumRooms')
                print(noOfRoom)
                BookingId = booking.get('BookingId')
                print(BookingId)
                ChannelName = booking.get('ChannelName')
                GuestName = booking.get('GuestName')
                GuestEmail = booking.get('GuestEmail')
                GuestMobile = booking.get('GuestMobile')
                NumNights = booking.get('NumNights')
                BookingStatus = booking.get('BookingStatus')
                roomName = booking.get('BookedRoomsInfo').split('(')[0].strip()
                NumAdults = booking.get('NumAdults')
                NumChildren = booking.get('NumChildren')
                totalAmount = booking.get('Amount_BookingTotal')

                try:
                    booking_date = datetime.strptime(booking['BookingTime'], "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d")
                except ValueError:
                    booking_date = datetime.strptime(booking['BookingTime'], "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d")

                try:
                    arrival_date = datetime.strptime(booking['CheckInDate'], "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d")
                except ValueError:
                    arrival_date = datetime.strptime(booking['CheckInDate'], "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d")

                try:
                    departure_date = datetime.strptime(booking['CheckOutDate'], "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d")
                except ValueError:
                    departure_date = datetime.strptime(booking['CheckOutDate'], "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d")

                lead_time = (datetime.strptime(arrival_date, "%Y-%m-%d") - datetime.strptime(booking_date, "%Y-%m-%d")).days

                noOfRoomCount = True if noOfRoom > 1 else False

                for room_index in range(noOfRoom):
                    if noOfRoom > 1:
                        reservationNumber = f"{BookingId}-{room_index + 1}"
                    else:
                        reservationNumber = BookingId

                bkglist = {
                    "hotelCode": str(hotelcode),
                    "reservationNumber": str(reservationNumber),
                    "isGroup": noOfRoomCount,
                    "source": ChannelName,
                    "guestDetails": {
                        "guestInfo": {
                            "name": GuestName,
                            "contactInfo": {
                                "email": GuestEmail if GuestEmail else "",
                                "phones": [
                                    {
                                        "number": GuestMobile if GuestMobile else ""
                                    }
                                ]
                            },
                        }
                    },
                    "sourceSegment": "",
                    "bookingDetails": {
                        "arrivalDate": arrival_date,
                        "departureDate": departure_date,
                        "totalNights": NumNights,
                        "checkInTime": "",
                        "checkOutTime": "",
                        "currentStatus": BookingStatus,
                        "roomDetails": {
                            "roomTypeId": 0,
                            "roomTypeName": roomName,
                            "roomPlan": "",
                            "pax": {
                                "totalAdults": NumAdults,
                                "totalChildren": NumChildren
                            }
                        },
                        "createdOn": booking_date,
                    },
                    "paymentDetails": {
                        "status": "",
                        "amount": totalAmount,
                    },
                    "priceSummary": {
                        "roomCost": 0,
                        "totalCost": totalAmount,
                    },
                }

                results.append(bkglist)

                with open('eglobeBooking.json', 'w') as json_file:
                    json.dump(results, json_file, indent=2)

            start_date = end_date

finally:
    if 'driver' in locals():
        driver.quit()

# print(results)
# push_to_mongodb(results)
