import requests
import json
from datetime import datetime, timedelta

results = []

accounts = [
    {"email": "dir@zorisboutiquehotel.com", "password": "Zoris@6262"}
]

for account in accounts:
    email = account['email']
    password = account['password']

    def login(email, password):
        body = {
            "email": email,
            "password": password,
            "browser": "Chrome",
            "creation_mode": "WEBSITE"
        }

        login_url = "https://kernel.bookingjini.com/extranetv4/admin/auth"
        
        login_request = requests.post(login_url, body)

        login_response = login_request.json()
        message = login_response['message']
        hotelId = login_response['hotel_id']
        userId = login_response['admin_id']

        if message == "User authentication successful":
            print(message)
        elif message == "Authentication failed":
            print(message)

        return userId, hotelId

    hotelId, propertyId = login(email, password)

    def get_hotel_id(userid, hotelId):

        endpoint = f"https://kernel.bookingjini.com/extranetv4/get-user-details/{userid}/{hotelId}"
        
        request = requests.get(endpoint)

        response = request.json()

        hotel_id = response['user_details']['organization_id']

        return hotel_id

    hotelId = get_hotel_id(hotelId, propertyId)

    headers = {
        'Content-Type': 'application/json',
    }

    today = datetime.now()
    from_date = (today - timedelta(days=60)).strftime("%Y-%m-%d")
    to_date = today.strftime("%Y-%m-%d")

    body = {
        "from_date": from_date,
        "to_date": to_date,
        "date_type": "1",
        "source": [
            5449,
            5450,
            5484,
            5519,
            5585,
            5728,
            7885,
            -1,
            -4,
            -6
        ],
        "booking_status": "all",
        "hotel_id": hotelId,
        "booking_id": ""
    }

    post_endpoint = "https://be.bookingjini.com/extranetv4/booking-lists"
    post_response = requests.post(post_endpoint, headers=headers, json=body)

    response_data = post_response.json()
    with open('booking_Data.json', 'w') as json_file:
        json.dump(response_data, json_file, indent=2)

    booking_details = []

    booking_data = response_data.get('data', [0])

    for data in booking_data:
        bId = data.get('unique_id')
        no_nights = data.get('nights')
        no_room = data.get('no_of_rooms')
        booking_status = data.get('booking_status')
        checkin_at = data.get('checkin_at')
        checkout_at = data.get('checkout_at')
        booking_date = (data.get('booking_date')).split(' ')[0]
        confirm = data.get('confirm_status')
        ota_id = data.get('ota_id')
        customer_name = data.get('customer_details')
        room_type_details = data.get('room_type_details', [])
        payment_status = data.get('payment_status')
        pay_status = "Fully Paid" if payment_status == "Paid" else "Not Paid" 
        channel_name = data.get('channel_name')
            
        bookingDate = datetime.strptime(booking_date, '%Y-%m-%d')
        arrivalDate = datetime.strptime(checkin_at, '%Y-%m-%d')
        departureDate = datetime.strptime(checkout_at, '%Y-%m-%d')


        btn_status = data.get('btn_status')
        if btn_status == "Confirmed":
            if arrivalDate <= today <= departureDate:
                current_status = "CI"
            elif today < departureDate:
                current_status = "CFB"
            elif today > departureDate:
                current_status = "CO"
            else:
                current_status = "CN"
        else:
            if today < arrivalDate and confirm == 0:
                current_status = "NS"
            else:
                current_status = "CN"


        rooms = data.get('room_type_details')
        for room in rooms :
            room_type_id = room.get('room_type_id') if room_type_details else None
            room_type = room.get('room_type').strip() if room_type_details else None
            qtyOfRoom = int(room.get('qty'))
            noOfRoom = True if qtyOfRoom > 1 else False

        bookingDate = datetime.strptime(booking_date, '%Y-%m-%d')
        arrivalDate = datetime.strptime(checkin_at, '%Y-%m-%d')
        lead = (arrivalDate - bookingDate).days

        id_endpoint = "https://be.bookingjini.com/extranetv4/crs/crs-booking-details"

        body = {
            "booking_id": bId,
            "booking_source": ""
        }
        id_response = requests.post(id_endpoint, headers=headers, json=body)

        if id_response.status_code == 200:
            try :
                id_response_json = id_response.json()
            except :
                print(id_response.text)

        with open('booking_info.json', 'w') as json_file:
            json.dump(id_response_json, json_file, indent=2)

        guest_data = id_response_json.get('data')
        # print(guest_data)

        for key, values in guest_data.items():
            if key == 'guest_name':
                guest_name = values
            elif key == 'price':
                price = values
            elif key == 'booking_source':
                booking_source = values
            elif key == 'email_id':
                email = values
            elif key == 'currency_name':
                currency = values
            elif key == 'mobile':
                mobile = values
            elif key == 'bookingid':
                bookingid = values
            elif key == 'state_id':
                state_id = values
            elif key == 'tax_amount':
                tax_amount = values
            elif key == 'net_price':
                room_cost = values
            
        if qtyOfRoom > 1:
            roomCostPerRoom = float(room_cost) / qtyOfRoom
            taxAmountPerRoom = float(tax_amount) / qtyOfRoom
            totalAmountPerRoom = float(price) / qtyOfRoom
        else:
            roomCostPerRoom = room_cost
            taxAmountPerRoom = tax_amount
            totalAmountPerRoom = price
        
        guest_info = id_response_json.get('data', {}).get('other_information')
        print(guest_info)
        guest_company = None
        Company_Address = None
        for g_info in guest_info:
            if g_info.get("key") == "CustomerGstInfo":
                    company_data = g_info.get('value')
                    guest_company = company_data.split(',')[1].split(':')[1].strip() if company_data else None
                    Company_Address = company_data.split(',')[2].split(':')[1].strip() if company_data else None
                
        plan = id_response_json.get('data', {}).get('room_data')
        print(plan)
        for meal in plan:
            if meal:
                plan_type = meal.get('plan_type')
                plan_name = meal.get('plan_name')
                adult = meal.get('adult')
                child = meal.get('child')
            else:
                plan_type = None
                plan_name = None
                adult = None
                child = None

            # status = True if confirm == 0 else False
        
        for room_index in range(qtyOfRoom):
            if qtyOfRoom > 1:
                reservationNumber = f"{bId}-{room_index + 1}"
            else:
                reservationNumber = bId

            booking_info = {
                "hotelCode": str(hotelId),
                "reservationNumber": str(reservationNumber),
                "isGroup": noOfRoom,
                "source": channel_name,
                "guestDetails": {
                    "guestInfo": {
                        "name": guest_name,
                        "contactInfo": {    
                            "email": email if email else None,
                            "phones": [
                                {
                                    "number": mobile if mobile else None
                                }
                            ]
                        },
                        "guestCompanyName": guest_company,
                        "guestCompanyAddress": Company_Address,
                    }
                },
                "bookingDetails": {
                    "arrivalDate": checkin_at,
                    "departureDate": checkout_at,
                    "totalNights": int(no_nights) * int(no_room),
                    "currentStatus": current_status,
                    "roomDetails": {
                        "roomTypeId": str(room_type_id),
                        "roomTypeName": room_type,
                        "roomPlan": plan_type,
                        "pax": {
                            "totalAdults": int(adult),
                            "totalChildren": int(child)
                        }
                    },
                    "createdOn": booking_date,
                    "lastModifiedOn": booking_date
                },
                "paymentDetails": {
                    "status": pay_status,
                    "amount": float(totalAmountPerRoom),
                    "receiptNumber": str(bookingid)
                },
                "priceSummary": {
                    "roomCost": float(roomCostPerRoom) if roomCostPerRoom else 0.0,
                    "totalCost": float(totalAmountPerRoom),
                    "taxAmount": float(taxAmountPerRoom),
                },
            }

            booking_details.append(booking_info)

            with open(f'{hotelId} Reservation.json', 'w') as json_file:
                json.dump(booking_details, json_file, indent=2)

                print(f"Booking data extracted.")
