import requests
import json
from datetime import datetime, timedelta

username = "vrrastoria"
password = "VRR@1234"

today = datetime.now()
# current = today.strftime("%Y-%m-%dT%H:%M:%S.000Z")
# end = (today + timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%S.000Z")

start_date = (today - timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%S.000Z")

end_date = today.strftime("%Y-%m-%dT%H:%M:%S.000Z")

def days_between(d1, d2):
    return abs((d2 - d1).days)

def format_date(date_str):
    if date_str == "0001-01-01T00:00:00Z":
        return None
    date_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    return date_obj.strftime("%Y-%m-%d")

login_url = f"https://api.platform.maximojo.com/mantrasv5.svc/login?u={username}&p={password}"
login_response = requests.get(login_url)

if login_response.status_code == 200:
    login_response_content = json.loads(login_response.content.decode('utf-8-sig'))
    session_id = login_response_content.get('Id')
    print(session_id)

    hotel_details = login_response_content.get('DomainContext', {}).get('Domains', [])
    for detail in hotel_details:
        domainHotels = detail.get('DomainHotels', {})
        for data in domainHotels:
            hotelId = data.get('Id')
            name = data.get('Name')

    hId = hotelId

    url = "https://api.platform.maximojo.com/mantrasv5.svc/FindBookings"
    body = {
        "HotelIds": [hId],
        "DomainIds": [],
        "BookingDates": {
            "End": end_date,
            "Start": start_date
        },
        "StayDates": None,
        "CheckInDates": None,
        "BookingIds": None
    }

    headers = {'session-id': session_id}

    response = requests.post(url, json=body, headers=headers)

    if response.status_code == 200:
        response_content = json.loads(response.content.decode('utf-8-sig'))

        with open('Row.json', 'w', encoding='utf-8') as json_file:
            json.dump(response_content, json_file, indent=2)

        reservation_data = []

        for booking in response_content:
            res_id = booking.get('Id')
            HotelId = booking.get('HotelId')
            guest_name = booking.get('ContactInfo', {}).get('FirstName')
            email = booking.get('ContactInfo', {}).get('Email')

            MailingAddress = booking.get('ContactInfo', {}).get('MailingAddress')
            if MailingAddress:
                streetAddress = MailingAddress.get('Street')
                city = MailingAddress.get('City')
                state = MailingAddress.get('State')
                zipcode = MailingAddress.get('ZipCode')
                Country = MailingAddress.get('Country')
            else:
                continue

            phone = booking.get('ContactInfo', {}).get('Phones', [{}])[0]
            if phone:
                phone_type = phone.get('Type')
                phone_Number = phone.get('Number')
            else:
                continue

            CreditCard = booking.get('CreditCard')
            if CreditCard:
                cardType = CreditCard.get('Type')
                cardNumber = CreditCard.get('Number')
                cardholderName = CreditCard.get('Name')
                expirationDate = CreditCard.get('Expiration')
                cvv = CreditCard.get('ValidationCode')
            else:
                continue

            created_date = datetime.fromisoformat(booking.get("CreatedOn").replace("Z", "+00:00"))
            arrival_date = datetime.fromisoformat(booking['StayInfo'].get('InDate'))
            departure_date = datetime.fromisoformat(booking['StayInfo'].get('OutDate'))

            lead_time = days_between(created_date, arrival_date)
            base_nights = days_between(arrival_date, departure_date)

            room_count = len(booking.get("Rooms", []))
            total_nights = base_nights * room_count

            CreatedOn = booking.get('CreatedOn')
            ModifiedOn = booking.get('ModifiedOn')
            PaymentType = booking.get('PaymentType')

            adults_in_first_room = booking.get('Rooms', [{}])[0].get('Occupants', {})
            Adults = adults_in_first_room.get('Adults')
            Children = adults_in_first_room.get('Children')
            RatePlanName = booking.get('Rooms', [{}])[0].get('RatePlanName')

            price = booking.get('Rooms', [{}])[0].get('Rates', [{}])[0].get('AmountItem', {})
            NetAmount = price.get('NetAmount')
            TaxAmount = price.get('TaxAmount')
            TotalAmount = price.get('TotalAmount')
            SellAmount = price.get('SellAmount')
            Commision = price.get('Commision')
            NetTaxAmount = price.get('NetTaxAmount')

            Room_info = booking.get('Rooms', [{}])[0]
            roomId = Room_info.get('RoomId')
            RoomName = Room_info.get('RoomName')

            booking_vendor_name = booking.get('Tags', {})
            source = booking_vendor_name.get('BookingVendorName')
            VendorBookingId = booking_vendor_name.get('VendorBookingId')

            Status = booking.get('Status')
            if Status == 0 or 5:
                current_status = 'UCB'
            elif Status == 1:
                current_status = 'Vo'
            elif Status == 2 or 4:
                current_status = 'CFB'
            elif Status == 3:
                current_status = 'CN'
            elif Status == 6:
                current_status = 'NS'
            else:
                current_status = 'ND'

            booking_info = {
                "hotelCode": HotelId,
                "reservationNumber": res_id,
                "source": source,
                "guestDetails": {
                "guestInfo": {
                "name": guest_name,
                "contactInfo": {
                    "email": email,
                    "phones": [
                    {
                        "type": phone_type,
                        "number": phone_Number
                    }
                    ]
                },
                "address": {
                    "streetAddress": streetAddress,
                    "guestCity": city,
                    "guestState": state,
                    "guestCountry": Country,
                    "guestZipCode": zipcode,
                    "guestNationality": Country
                },
                }
            },
                "bookingDetails": {
                    "checkInTime": format_date(booking['StayInfo'].get('InDate')),
                    "checkOutTime": format_date(booking['StayInfo'].get('OutDate')),
                    "currentStatus": current_status,
                    "totalNights": total_nights,
                    "roomDetails": {
                        "roomTypeId": roomId,
                        "roomTypeName": RoomName,
                        "roomPlan": RatePlanName,
                        "pax": {
                            "totalAdults": Adults,
                            "totalChildren": Children
                        }
                    },
                    "createdOn": format_date(booking.get('CreatedOn')),
                    "lastModifiedOn": format_date(booking.get('ModifiedOn')),
                },
                "paymentDetails": {
                    "amount": TotalAmount,
                },
                "priceSummary": {
                    "roomCost": NetAmount,
                    "totalCost": TotalAmount,
                    "commissionAmount": Commision,
                    "TaxAmount": TaxAmount,
                },
                "ccDetails": {
                "cardholderName": cardholderName,
                "cardNumber": cardNumber,
                "expirationMonth": expirationDate.split('T')[0].split('-')[1],
                "expirationYear": expirationDate.split('T')[0].split('-')[0],
                "billingAddress": {
                    "streetAddress": streetAddress,
                    "city": city,
                    "state": state,
                    "country": Country
                },
                "cvv": cvv
            },
        }
            reservation_data.append(booking_info)

        with open('output.json', 'w', encoding='utf-8') as json_file:
            json.dump(reservation_data, json_file, indent=2)
            print("Reservation Data Extracted.")
