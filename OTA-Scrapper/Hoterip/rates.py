import requests
import json
from datetime import datetime, timedelta

hotel_id = "aston-denpasar-hotel-convention-center" 

num_days = 90

today = datetime.now()
room_data = {
    "timestamp": today.strftime("%Y-%m-%d %H:%M:%S"),
    "rates": []
}

for day in range(num_days):
    check_in_date = (today + timedelta(days=day)).strftime("%Y-%m-%d")
    check_out_date = (today + timedelta(days=day + 1)).strftime("%Y-%m-%d")

    url = f"https://api.hoterip.com/api/v2/hotels/{hotel_id}/rooms?check_in={check_in_date}&check_out={check_out_date}&number_of_rooms=1&capacities=[{{%22number_of_adults%22:1}}]"

    headers = {
        'Accept-Language': 'id'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_content = response.json()

        data_slot = response_content['data']
        for room in data_slot:
            room_info = room.get('room', {}).get('selected_text', {})
            room_id = room_info.get('room_id')
            room_name = room_info.get('name')
            
            campaign = room.get('campaign', {})
            items_data = campaign.get('items_data', [[]])[0]
            meal_plan = "EP"  

            if items_data:
                breakfast = items_data[0].get('breakfast', "false")
                lunch = items_data[0].get('lunch', "false")
                dinner = items_data[0].get('dinner', "false")

                if breakfast == "true":
                    if lunch == "true" or dinner == "true":
                        meal_plan = "AP"
                    else:
                        meal_plan = "CP"
                elif lunch == "true" or dinner == "true":
                    meal_plan = "MAP"

            price = campaign.get('raw_items', [{}])[0].get('price') if campaign else None
            
            room_data['rates'].append({
                "roomId": room_id,
                "name": room_name,
                "checkIn": check_in_date,
                "checkOut": check_out_date,
                "roomPlan": meal_plan,
                "displayPrice": f"IDR {price}"
            })

    print(f'HotelID : {hotel_id} rates for Checkin: {check_in_date}')

with open('rates_data.json', 'w') as json_file:
    json.dump(room_data, json_file, indent=4)
