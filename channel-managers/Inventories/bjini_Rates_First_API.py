import requests
import json
from datetime import datetime, timedelta

email = "dir@zorisboutiquehotel.com"
password = "Zoris@6262"
property_code = "2308"

auth_url = "https://kernel.bookingjini.com/extranetv4/admin/auth"
auth_body = {
    "email": email,
    "password": password,
    "browser": "Chrome",
    "creation_mode": "WEBSITE"
}
auth_headers = {'Content-Type': 'application/json'}

auth_response = requests.post(auth_url, headers=auth_headers, json=auth_body)

if auth_response.status_code == 200:
    auth_data = auth_response.json()
    auth_token = auth_data.get('auth_token')
    message = auth_data.get('message')
    if message == "User authentication successful":
        print(message)
    else:
        print(message)
        exit()
else:
    print(f"Authentication failed with status code: {auth_response.status_code}")
    exit()

inventory_url = f"https://kernel.bookingjini.com/extranetv4/hotel_master_room_type/all/{property_code}"
headers = {'Authorization': auth_token}

response = requests.get(inventory_url, headers=headers)

if response.status_code == 200:
    data = response.json()
    
    with open("RowRoom.json", "w") as json_file:
        json.dump(data, json_file, indent=4)
    
    data_slots = data.get('data', [])
    all_rooms_info = []

    for slot in data_slots:
        room_id = slot.get('room_type_id')
        room_name = slot.get('room_type')
        print(room_name)
        print(f"Room Type ID: {room_id}")

        start_date = datetime.now().strftime('%Y-%m-%d')
        end_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')

        date_url = f"https://cm.bookingjini.com/extranetv4/rates/get-rates/{property_code}/{room_id}/{start_date}/{end_date}"
        date_headers = {'Authorization': f'Bearer {auth_token}'}

        date_response = requests.get(date_url, headers=date_headers)

        if date_response.status_code == 200:
            result = date_response.json()

            with open("RowRates.json", "w") as json_file:
                json.dump(result, json_file, indent=4)
            
            roomPriceInfoList = []

            rate_slot = result.get('channel_rates', [])
            for rate_info in rate_slot:
                if rate_info.get('name') == "Bookingjini":
                    minimum_prices = rate_info.get('minimum_price', [])
                    for price_info in minimum_prices:
                        roomRate = price_info.get('min_price')
                        print(f"Room Rate: {roomRate}")
                        
                        roomPriceInfo = {
                            "roomPrice": roomRate
                        }
                        roomPriceInfoList.append(roomPriceInfo)
                
            ratePlan = {
                "roomId": room_id,
                "roomName": room_name,
                "roomPriceInfo": roomPriceInfoList
            }

            all_rooms_info.append(ratePlan)

        else:
            print(f"Failed to fetch rates for room ID {room_id} with status code: {date_response.status_code}")

    with open("bookingJiniRate.json", "w") as json_file:
        json.dump(all_rooms_info, json_file, indent=4)
    
    print("Data extracted and stored successfully!")

else:
    print(f"Failed to fetch inventory with status code: {response.status_code}")
    exit()
