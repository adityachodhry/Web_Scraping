import requests
import json
from datetime import datetime, timedelta
import time

def destranetReservations(username, password, propertyCodes):
   
    today = datetime.now()
    currentDate = today.strftime('%Y-%m-%d')

    # Calculate the starting date for 5 years ago
    five_years_ago = today - timedelta(days=5 * 365)

    url = "https://destranet.desiya.com/extranet-controller/login"
    payload = json.dumps({
        "username": username,
        "password": password,
        "usertype": "DES"
    })

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        response_content = response.json()
        tokenData = response_content.get('data', {})
        tokenId = tokenData.get('token')

        # Fetch all property codes if no specific ones are provided
        if not propertyCodes:
            allPropertyList = f"https://destranet.desiya.com/extranet-controller/vendors?token={tokenId}"
            property_response = requests.get(allPropertyList)

            if property_response.status_code == 200:
                property_data = property_response.json()
                propertyDataSlot = property_data.get('data', [])

                propertyCodes = [property.get('vendorId') for property in propertyDataSlot]

        reservations_list = []

        # Iterate over each property code first
        for propertyCode in propertyCodes:
            start_date = five_years_ago

            # Within each property, iterate over 4-month periods up to today
            while start_date < today:
                end_date = start_date + timedelta(days=120)
                if end_date > today:
                    end_date = today

                # Fetch reservation data within the 4-month period for the current property
                reservationsUrl = f"https://destranet.desiya.com/extranet-controller/vendors/{propertyCode}/Bookings?endDate={end_date}&filterBy=booking&startDate={start_date.strftime('%Y-%m-%d')}&token={tokenId}"
                
                time.sleep(3)
                ratesResponse = requests.get(reservationsUrl)

                if ratesResponse.status_code == 200:
                    response_data = ratesResponse.json()
                    data_slot = response_data.get('data', [])

                    for reservation in data_slot:
                        noOfRooms = int(reservation.get('noOfRooms'))
                        bookingId = reservation.get('bookingId')
                        arrivalDate = reservation.get('checkInDate').split('T')[0]
                        departureDate = reservation.get('checkOutDate').split('T')[0]
                        paymentStatus = reservation.get('paymentStatus')

                        if paymentStatus == "Payment Done":
                            payment_status = "Paid"
                        elif paymentStatus == "Payment Pending":
                            payment_status = "Not Paid"

                        currentStatus = reservation.get('bookingStatus')

                        if currentStatus == 'cnf' and arrivalDate <= currentDate <= departureDate:
                            current_status = 'CI'
                        elif currentStatus == 'cnf' and currentDate > departureDate:
                            current_status = 'CO'
                        elif currentStatus == 'cnf':
                            current_status = 'CFB'
                        elif currentStatus == 'cn':
                            current_status = 'CN'
                        else:
                            current_status = 'NA'

                        room_amount = reservation.get('totalNetRate')
                        total_rate = reservation.get('totalNetRate')
                        tax_rate = reservation.get('totalTax')

                        if noOfRooms > 1:
                            roomCostPerRoom = room_amount / noOfRooms
                            taxAmountPerRoom = tax_rate / noOfRooms
                            totalAmountPerRoom = total_rate / noOfRooms
                        else:
                            roomCostPerRoom = room_amount
                            taxAmountPerRoom = tax_rate
                            totalAmountPerRoom = total_rate

                        if noOfRooms == 1:
                            reservation_id_list = [bookingId]
                        else:
                            reservation_id_list = [f"{bookingId}-{i+1}" for i in range(noOfRooms)]

                        for res_id in reservation_id_list:
                            reservation_data = {
                                "hotelCode": reservation.get('vendorId'),
                                "reservationNumber": res_id,
                                "isGroup": noOfRooms > 1,
                                "source": reservation.get('sourceCode'),
                                "guestDetails": {
                                    "guestInfo": {
                                        "name": reservation.get('customerName').strip(),
                                        "contactInfo": {
                                            "email": reservation.get('guestEmail'),
                                            "phones": [
                                                {
                                                    "number": reservation.get('guestMobile')
                                                }
                                            ]
                                        },
                                        "address": {
                                            "streetAddress": reservation.get('guestStreet'),
                                            "guestCity": reservation.get('guestCity'),
                                            "guestState": reservation.get('guestState'),
                                            "guestCountry": reservation.get('guestCountry'),
                                            "guestZipCode": reservation.get('guestPostalCode'),
                                        }
                                    }
                                },
                                "bookingDetails": {
                                    "arrivalDate": arrivalDate,
                                    "departureDate": departureDate,
                                    "checkInTime": reservation.get('checkInDate').split('T')[1],
                                    "checkOutTime": reservation.get('checkOutDate').split('T')[1],
                                    "totalNights": int(reservation.get('noOfNights')),
                                    "currentStatus": current_status,
                                    "roomDetails": {
                                        "roomTypeName": reservation.get('roomName'),
                                        "pax": {
                                            "totalAdults": int(reservation.get('noOfAdults')),
                                            "totalChildren": int(reservation.get('noOfChilds'))
                                        }
                                    },
                                    "createdOn": reservation.get('bookingTime').split('T')[0],
                                },
                                "paymentDetails": {
                                    "status": payment_status,
                                    "amount": totalAmountPerRoom,
                                    "date": reservation.get('paymentIssuedOn'),
                                },
                                "priceSummary": {
                                    "roomCost": roomCostPerRoom,
                                    "totalCost": totalAmountPerRoom,
                                    "taxAmount": taxAmountPerRoom
                                }
                            }

                            reservations_list.append(reservation_data)

                    print(f"Data extracted successfully for propertyCode: {propertyCode} from {start_date.strftime('%Y-%m-%d')} to {end_date}")

                else:
                    print(f"Failed to retrieve reservations for propertyCode {propertyCode}: {ratesResponse.status_code} - {ratesResponse.text}")

                # Move to the next 4-month period for this property code
                start_date = end_date

        with open('reservations.json', 'w') as json_file:
            json.dump(reservations_list, json_file, indent=4)

        return reservations_list

    else:
        print(f"Login failed: {response.status_code} - {response.text}")


destranetReservations('reservations@paramparacoorg.com', 'parampara123', [])
