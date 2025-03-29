import requests
import json
from datetime import datetime, timedelta

today = datetime.now()

hId = 47374272

results = []

for day in range(1):
    check_in_date = (today + timedelta(days=day)).strftime("%Y%m%d")
    check_out_date = (today + timedelta(days=day + 1)).strftime("%Y%m%d")

    url = "https://www.trip.com/restapi/soa2/28820/getHotelRoomList"

    body = {
        "search": {
            "hotelId": hId,
            "roomId": 0,
            "checkIn": check_in_date,
            "checkOut": check_out_date,
            "roomQuantity": 1,
            "adult": 2
        },
        "head": {
            "platform": "PC",
            "cver": "0",
            "group": "trip",
            "locale": "en-XX",
            "timezone": "5.5",
            "currency": "INR",
            'aid' : '15214',
            "pageId": "123"
        }
    }
    
    response = requests.post(url, json=body)

    if response.status_code == 200:
        response_data = response.json()

        # with open('Trip.com.json', 'w', encoding='utf-8') as json_file:
        #     json.dump(response_data, json_file, indent=2)

        data_slot1 = response_data.get('data', {}).get('physicRoomMap', {})
        data_slot2 = response_data.get('data', {}).get('saleRoomMap', {})

        # Store physical room information
        physical_room_info = {}
        for key, value in data_slot1.items():
            physical_room_info[key] = {"id": value["id"], "name": value["name"]}

        for key, value in data_slot2.items():
            physical_room_id = value['physicalRoomId']
            meal_plan = value.get('mealInfo',{}).get('title',{})

            rplan = 'EP'

            if meal_plan:
                if 'Includes 1 breakfast' in meal_plan or 'Includes 2 breakfasts' in meal_plan or 'Includes 3 breakfasts' in meal_plan:
                    rplan = 'CP'
                elif 'Half board for 2' in meal_plan or 'Half board for 1' in meal_plan:
                    rplan = 'MAP'
                elif 'Full board for 1' in meal_plan or 'Full board for 2' in meal_plan:
                    rplan = 'AP'
                
            display_price = value.get('priceInfo', {}).get('displayPrice').split()[-1]
            display_price = display_price.replace(",", "")  # Remove commas

            room_id = physical_room_info.get(str(physical_room_id), {}).get("id", "")
            room_name = physical_room_info.get(str(physical_room_id), {}).get("name", "")

            results.append({
                "roomID": str(room_id),
                "roomName": room_name,
                "checkIn": (today + timedelta(days=day)).strftime("%Y-%m-%d"),
                "checkOut": (today + timedelta(days=day + 1)).strftime("%Y-%m-%d"),
                "roomPlan": rplan,
                "price": float(display_price)
            })

    print(f'OTA : 7 | Hotel : {hId} | Checkin : {(today + timedelta(days=day)).strftime("%Y-%m-%d")}')  

final_data = {
    "otaId": 9,
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "rates": results
}

with open('TripRates.json', 'w', encoding='utf-8') as json_file:
    json.dump(final_data, json_file, indent=2)