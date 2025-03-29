import requests
import json
from datetime import datetime, timedelta

def cleartripReservation(username, password, propertyCodes):

    session = requests.Session()

    loginUrl = "https://suite.cleartrip.com/aggregator/v1/platform/authenticate/login"

    payload = json.dumps({
        "loginIdentifier": username,
        "password": password,
        "authenticationType": "PASSWORD"
    })

    headers = {
        'cookie': 'x-device-id=yKmXAdW7QneZPDKbOhp8v-1729070470830; x-platform=desktop;', 
        'Content-Type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }

    response = session.post(loginUrl, data=payload, headers=headers)

    if response.status_code == 200:
        print('Successfully logged in!')
        cookies = session.cookies.get_dict()
        formatted_cookies = '; '.join([f"{key}={value}" for key, value in cookies.items()])
    else:
        print('Login failed!')
        return
    
    year = 5
    today = datetime.now().strftime('%Y-%m-%d')
    date_start = (datetime.now() - timedelta(days=year * 365)).strftime('%Y-%m-%d')
    date_end = datetime.now().strftime('%Y-%m-%d')

    # If no property codes are provided, fetch them from the property list
    if not propertyCodes:
        propertyList = "https://suite.cleartrip.com/aggregator/ho/v1/platform/007/properties?payloadSize=6&pageNo=1&searchType=NAME&filterBy=ALL&sortBy=MODIFIED_DATE&sortOrder=DESC"
        headers = {
            'cookie': f'x-device-id=yKmXAdW7QneZPDKbOhp8v-1729070470830; x-platform=desktop; {formatted_cookies}',
            'Content-Type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
        }

        propertyResponse = session.get(propertyList, headers=headers)
        propertyResult = propertyResponse.json()
        propertyListDataSlot = propertyResult.get('response', {}).get('propertiesList', [])

        propertyCodes = [property.get('entityId') for property in propertyListDataSlot]

    all_reservations = []

    # Iterate through each propertyCode
    for propertyCode in propertyCodes:
        reservationUrl = f"https://suite.cleartrip.com/aggregator/bookings/v1/hotel/{propertyCode}/get-bookings?startDate={date_start}&endDate={date_end}&dateType=BOOKING"
        
        headers = {
            'cookie': f'x-device-id=yKmXAdW7QneZPDKbOhp8v-1729070470830; x-platform=desktop; {formatted_cookies}',
            'Content-Type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
        }

        reservationResponse = session.get(reservationUrl, headers=headers)

        if reservationResponse.status_code == 200:
            reservationResult = reservationResponse.json()
            data_slot = reservationResult.get('response', {}).get('results', [])

            for booking in data_slot:
                bookingId = booking.get('bookingInfo', {}).get('id')
                noOfAdults = booking.get('guests', {}).get('adultCount')
                noOfChildren = booking.get('guests', {}).get('childrenCount')

                eachReservationUrl = f"https://suite.cleartrip.com/aggregator/bookings/v1/hotel/{propertyCode}/details?booking-id={bookingId}"
                eachResponse = session.get(eachReservationUrl, headers=headers)

                if eachResponse.status_code == 200:
                    eachReservationResult = eachResponse.json()
                    eachDataSlot = eachReservationResult.get('response', {}).get('bookingInfo', {}).get('leadGuestInfo', {})
                    bookingInfo = eachReservationResult.get('response', {}).get('bookingInfo', {})

                    booking_id = bookingInfo.get('id')
                    checkInDate = bookingInfo.get('checkInDate')
                    checkOutDate = bookingInfo.get('checkOutDate')
                    checkInDateObj = datetime.strptime(checkInDate, '%Y-%m-%d') 
                    checkOutDateObj = datetime.strptime(checkOutDate, '%Y-%m-%d')  
                    totalNights = (checkOutDateObj - checkInDateObj).days

                    booking_status = bookingInfo.get('status')

                    if booking_status == 'CONFIRMED' and checkInDate <= today <= checkOutDate:
                        current_status = 'CI'
                    elif booking_status == 'CONFIRMED' and today > checkOutDate:
                        current_status = 'CO'
                    elif booking_status == 'CONFIRMED':
                        current_status = 'CFB'
                    elif booking_status == 'CANCELLED':
                        current_status = 'CN'
                    else:
                        current_status = 'NA'
                    
                    guestName = eachDataSlot.get('name')
                    roomData = bookingInfo.get('rooms', [])

                    for plan in roomData:
                        room_name = plan.get('name')
                        roomMealPlan = plan.get('ratePlanDetails', {}).get('name')

                    paymentInfo = eachReservationResult.get('response', {}).get('paymentInfo', {}).get('forwardTransactions', [])

                    for transaction in paymentInfo:
                        room_amount = transaction.get('amount')
                        utrNumber = transaction.get('utrNumber')
                        paymentStatus = transaction.get('status')

                        if paymentStatus == "PROCESSED":
                            payment_status = "Paid"
                        elif paymentStatus == "PENDING":
                            payment_status = "Not Paid"

                    totalPaymentInfo = eachReservationResult.get('response', {}).get('rateBreakupInfo', {}).get('rateBreakup', [])
                    if totalPaymentInfo:
                        total_rate = totalPaymentInfo[0].get('rate')
                        tax_rate = totalPaymentInfo[0]['breakup'][1].get('rate') if len(totalPaymentInfo[0].get('breakup', [])) > 1 else None
                        commission_rate = totalPaymentInfo[1].get('rate') if totalPaymentInfo else None
                    else:
                        total_rate = tax_rate = commission_rate = None
                    
                    room_count = len(roomData)
                    isGroup = room_count > 1

                    if room_count > 1:
                        roomCostPerRoom = room_amount / room_count
                        taxAmountPerRoom = tax_rate / room_count if tax_rate else None
                        totalAmountPerRoom = total_rate / room_count if total_rate else None
                        commissionAmountPerRoom = commission_rate / room_count if commission_rate else None
                    else:
                        roomCostPerRoom = room_amount
                        taxAmountPerRoom = tax_rate
                        totalAmountPerRoom = total_rate
                        commissionAmountPerRoom = commission_rate

                    for index, plan in enumerate(roomData, start=1):
                        reservation_number = f"{bookingId}-{index}" if room_count > 1 else bookingId
                        reservation_data = {
                            "hotelCode": propertyCode,
                            "reservationNumber": reservation_number,
                            "isGroup": isGroup,
                            "source": "ClearTrip",
                            "guestDetails": {
                                "guestInfo": {"name": guestName}
                            },
                            "bookingDetails": {
                                "arrivalDate": checkInDate,
                                "departureDate": checkOutDate,
                                "totalNights": totalNights,
                                "currentStatus": current_status,
                                "roomDetails": {
                                    "roomTypeName": room_name,
                                    "roomPlan": roomMealPlan,
                                    "pax": {"totalAdults": noOfAdults, "totalChildren": noOfChildren}
                                },
                            },
                            "paymentDetails": {
                                "status": payment_status,
                                "amount": totalAmountPerRoom,
                                "receiptNumber": utrNumber
                            },
                            "priceSummary": {
                                "roomCost": roomCostPerRoom,
                                "totalCost": totalAmountPerRoom,
                                "commissionAmount": commissionAmountPerRoom,
                                "taxAmount": taxAmountPerRoom,
                            },
                        }

                        all_reservations.append(reservation_data)

    # with open('cleartrip_reservations.json', 'w') as json_file:
    #     json.dump(all_reservations, json_file, indent=4)

    return all_reservations

# cleartripReservation('reservations@hoteltheroyalvista.com', 'Mahadev@123456', ['4271423'])
