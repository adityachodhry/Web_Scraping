import requests
import json
from datetime import datetime
import pandas as pd

current_date = datetime.now()

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

    body = {
        "from_date": "2024-05-01",
        "to_date": "2024-05-17",
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
        hId = data.get('hotel_id')
        no_nights = data.get('nights')
        no_room = data.get('no_of_rooms')
        channel_name = data.get('channel_name')
        booking_status = data.get('booking_status')
        checkin_at = data.get('checkin_at')
        checkout_at = data.get('checkout_at')
        booking_date = (data.get('booking_date')).split(' ')[0]
        display_booking_date = data.get('display_booking_date')
        confirm = data.get('confirm_status')
        cancel_status = data.get('cancel_status')
        btn_status = data.get('btn_status')
        ota_id = data.get('ota_id')
        customer_name = data.get('customer_details')
        room_type_details = data.get('room_type_details', [])
        payment_status = data.get('payment_status')

        room_type = room_type_details[0].get('room_type') if room_type_details else None
        room_type_id = room_type_details[0].get('room_type_id') if room_type_details else None
        
        business_booking = data.get('business_booking')

        bookingDate = datetime.strptime(booking_date, '%Y-%m-%d')
        arrivalDate = datetime.strptime(checkin_at, '%Y-%m-%d')
        lead = (arrivalDate - bookingDate).days

        # data[0].room_type_details[0].room_type_id
        # data[0].is_card_chargeable

        id_endpoint = "https://be.bookingjini.com/extranetv4/crs/crs-booking-details"

        body = {
            "booking_id": bId,
            "booking_source": ""
        }
        id_response = requests.post(id_endpoint, headers=headers, json=body)

        try :
            if id_response.status_code == 200:
                id_response_json = id_response.json()

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
            
            guest_info = id_response_json.get('data', {}).get('other_information')
            for g_info in guest_info:
                if g_info.get("key") == "CustomerGstInfo":
                    company_data = g_info.get('value')
                    guest_company = company_data.split(',')[1].split(':')[1] if company_data else None
                    Company_Address = company_data.split(',')[2].split(':')[1] if company_data else None
                else :
                    guest_company = None
                    Company_Address = None
            plan = id_response_json.get('data', {}).get('room_data')
            for meal in plan:
                plan_type = meal.get('plan_type')
                plan_name = meal.get('plan_name')
                adult = meal.get('adult')
                child = meal.get('child')

            status = "true" if confirm == 1 else "false"

            booking_info = {
                "hotelName" : "Zoris Boutique Hotel",
                "res" : str(bId),
                "bookingDate": booking_date,
                "guestName": guest_name,
                "arrivalDate":checkin_at,
                "deptDate": checkout_at,
                "roomId": room_type_id,
                "room": room_type,
                "pax" : "",
                "ADR" : float(price)/int(no_nights),
                "totalCharges" : float(price),
                "lead" : lead,
                "source": booking_source,
                "noOfNights": int(no_nights)*int(no_room),
                "hotelCode": str(hId),
                "isActive": status,
                "guestCompanyEmail": email,
                "guestCompanyName": guest_company,
                "CompanyAddress": Company_Address,
                "currency": currency,
                "bookingId": bookingid,
                "stateId": state_id,
                "mobile": mobile,
                "planType": plan_type,
                "planName": plan_name,
                "noOfAdults": int(adult),
                "noOfChild": child
                
            }

            booking_details.append(booking_info)

            with open('booking_main.json', 'w') as json_file:
                json.dump(booking_details, json_file, indent=2)

            # df = pd.DataFrame(booking_details)
            # df.to_excel('jiniBooking.xlsx', index=False)

            print(f"{booking_date} booking data extracted.")
        except Exception as e :
            print(e)
            print(id_response.text)