import requests
import json
from datetime import datetime, timedelta

hotelId = 291843
searchId = "f67e0cc2d75666ef"
num_days = 90

today = datetime.now()
room_data = {
    "otapid": hotelId,
    "timestamp": today.strftime("%Y-%m-%d %H:%M:%S"),
    "rates": []
}

for day in range(num_days):
    check_in_date = (today + timedelta(days=day)).strftime("%Y-%m-%d")
    check_out_date = (today + timedelta(days=day + 1)).strftime("%Y-%m-%d")

    url = f"https://srv.wego.com/v3/metasearch/hotels/{hotelId}/rates?searchId={searchId}&currencyCode=INR&checkIn={check_in_date}&checkOut={check_out_date}"

    response = requests.get(url)

    if response.status_code == 200:
        response_content = response.json()
        # print(response_content)

        # with open('wego_raw.json','w') as json_file:
        #     json.dump(response_content, json_file, indent = 4)

        data_slot = response_content['rates']
        for data in data_slot:
            roomids = data.get('roomIds')  
            if roomids and isinstance(roomids, list) and len(roomids) > 0:
                roomid = roomids[0]  
            else:
                roomid = None
            roomName = data.get('description')
            ota = data.get('provider',{}).get('name')
            price = data.get('price',{}).get('amount')
            amenity = data.get('roomKeyWithAmenity')

            if amenity:
                if 'breakfast' in amenity.lower():
                    mealplan = 'breakfast included'
                else:
                    mealplan = 'No meals'
            else:
                mealplan = None

            if 'No meals' in mealplan:
                room_plan = 'EP'
            elif 'breakfast included' in mealplan and 'lunch' in mealplan and 'dinner' in mealplan and '/' in mealplan:
                room_plan = 'MAP'
            elif 'breakfast included' in mealplan and 'Lunch' in mealplan and 'Dinner' in mealplan:
                room_plan = 'AP'
            elif 'breakfast included' in mealplan:
                room_plan = 'CP'
            else:
                room_plan = 'Unknown'

            room_data['rates'].append({
                "roomId": roomid,
                "name": roomName,
                "ota" : ota,
                "check_in": check_in_date,
                "check_out": check_out_date,
                "room_plan": room_plan,
                "displayprice": price
            })
    print(f'Hotel : {hotelId} | Checkin : {check_in_date}')

with open('rates_data.json', 'w') as json_file:
        json.dump(room_data, json_file, indent=4)
