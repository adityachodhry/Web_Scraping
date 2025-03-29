import time
import json
import requests
import random
from datetime import datetime, timedelta
from seleniumwire import webdriver
from selenium.webdriver.common.by import By

accounts = [{'username': 'akshay01', 'password': 'akshay0120'}]

results = []

months_per_request = 3

current_date = datetime.now()
start_date = current_date - timedelta(days=365 * 3)

driver = webdriver.Chrome()

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

    post_endpoint = "https://www.eglobe-solutions.com/cmapi/bookings/search"
    
    while start_date < current_date:
        end_date = start_date + timedelta(days=30 * months_per_request)

        FromDate = start_date.strftime("%d %b %Y")
        TillDate = end_date.strftime("%d %b %Y")

        body = {
            "SearchBy": "BookingDate",
            "FromDate": FromDate,
            "TillDate": TillDate
        }
        post_response = requests.post(post_endpoint, headers=headers, json=body)

        post_response_content = post_response.json()

        hotelcodes = post_response_content.get('BookingList', [])
        hotelcode = hotelcodes[0].get('EgsPropertyId', None) if hotelcodes else None

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

        # with open('Row.json', 'w') as json_file:
        #     json.dump(response_content, json_file, indent=2)

        bookingList = response_content['Result']['Data']
        for booking in bookingList:

            noOfRoom = booking.get('NumRooms')
            print(noOfRoom)
            BookingId = booking.get('BookingCode')
            print(BookingId)
            ChannelName = booking.get('ChannelName')
            GuestName = booking.get('GuestName')
            GuestEmail = booking.get('GuestEmail')
            NumNights = booking.get('NumNights')
            NumAdults = booking.get('NumAdults')
            NumChildren = booking.get('NumChildren')
            totalAmount = booking.get('Amount_BookingTotal')
            totalTax = booking.get('Amount_TotalTaxes')
            InvoiceCode = booking.get('InvoiceCode')
            roomCostInfo = totalAmount - totalTax

            PaymentTypeName = booking.get('PaymentTypeName')
            if PaymentTypeName == 'PrePaid':
                paymentStatus = 'Fully Paid'
            elif PaymentTypeName == 'PayAtHotel':
                paymentStatus = 'Not Paid'
            else:
                paymentStatus = 'NA'

            roomName = booking.get('BookedRoomsInfo').split('(')[0].strip()
            booked_rooms = booking.get('BookedRooms', [])
            if booked_rooms:
                first_room = booked_rooms[0]
                roomId = first_room.split('(')[1].split(')')[0]
                roomPlan = first_room.split('-')[-1].split('(')[0].strip()
            
            GuestMobile = booking.get('GuestPhone')
            if GuestMobile:
                guestMobile = booking.get('GuestPhone').split(',')[0].strip()
            else:
                guestMobile = GuestMobile

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

            BookingStatus = booking.get('BookingStatus')
            checkIn_dt = datetime.strptime(arrival_date, "%Y-%m-%d")
            checkOut_dt = datetime.strptime(departure_date, "%Y-%m-%d")

            if BookingStatus == 'BOOKED' and checkIn_dt <= current_date <= checkOut_dt:
                current_status = 'CI'
            elif BookingStatus == 'BOOKED' and current_date > checkOut_dt:
                current_status = 'CO'
            elif BookingStatus == 'BOOKED':
                current_status = 'CFB'
            elif BookingStatus == 'CANCELLED':
                current_status = 'CN'
            else:
                current_status = 'NA'

            noOfRoomCount = True if noOfRoom > 1 else False

            if noOfRoom > 1:
                totalAmountPerRoom = float(totalAmount) / noOfRoom
                roomCost = float(roomCostInfo) / noOfRoom
            else:
                totalAmountPerRoom = totalAmount
                roomCost = roomCostInfo

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
                                        "number": guestMobile if guestMobile else ""
                                    }
                                ]
                            },
                        }
                    },
                    "sourceSegment": 'OTA',
                    "bookingDetails": {
                        "arrivalDate": arrival_date,
                        "departureDate": departure_date,
                        "totalNights": NumNights,
                        "currentStatus": current_status,
                        "roomDetails": {
                            "roomTypeId": roomId if roomId else "",
                            "roomTypeName": roomName,
                            "roomPlan": roomPlan if roomPlan else "",
                            "pax": {
                                "totalAdults": NumAdults,
                                "totalChildren": NumChildren
                            }
                        },
                        "invoiceNumber": InvoiceCode,
                        "createdOn": booking_date
                    },
                    "paymentDetails": {
                        "status": paymentStatus,
                        "amount": totalAmountPerRoom,
                    },
                    "priceSummary": {
                        "roomCost": roomCost,
                        "totalCost": totalAmountPerRoom,
                        "taxAmount": totalTax
                    },
                }

                results.append(bkglist)

                with open('eglobeBooking.json', 'w') as json_file:
                    json.dump(results, json_file, indent=2)

        start_date = end_date

    driver.quit()
