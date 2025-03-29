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
headers = {'Authorization': f'Bearer {auth_token}'}

response = requests.get(inventory_url, headers=headers)

if response.status_code == 200:
    data = response.json()
    
    with open("RowRoom.json", "w") as json_file:
        json.dump(data, json_file, indent=4)
    
    data_slots = data.get('data', [])
    all_rooms_info = []

    start_date = datetime.now().strftime('%Y-%m-%d')
    end_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')

    for slot in data_slots:
        room_id = slot.get('room_type_id')
        room_name = slot.get('room_type')
        print(f"Fetching rates for: {room_name} (Room Type ID: {room_id})")

        date_url = f"https://cm.bookingjini.com/extranetv4/rates/get-rates-channel-wise/{property_code}/-1/{start_date}/{end_date}"
        date_headers = {'Authorization': f'Bearer {auth_token}'}

        date_response = requests.get(date_url, headers=date_headers)

        if date_response.status_code == 200:
            result = date_response.json()

            with open("RowRoom.json", "w") as json_file:
                json.dump(result, json_file, indent=4)
            
            minimum_prices = result.get('channel_rates', {}).get('minimum_price_by_room_type', {})
            room_prices = minimum_prices.get(str(room_id), {})

            all_rooms_info.append({
                "roomId": room_id,
                "roomName": room_name,
                "roomPriceInfo": room_prices
            })

        else:
            print(f"Failed to fetch rates with status code: {date_response.status_code}")

    with open("bookingJiniRate.json", "w") as json_file:
        json.dump(all_rooms_info, json_file, indent=4)

    print("Room price information has been saved to RoomPriceInfo.json")

else:
    print(f"Failed to fetch room types with status code: {response.status_code}")
