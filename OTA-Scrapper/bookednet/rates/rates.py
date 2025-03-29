import requests
import json
from datetime import datetime, timedelta

hotelId = 348079
num_days = 90

today = datetime.now()
room_data = {
    "otaPId": hotelId,
    "timestamp": today.strftime("%Y-%m-%d %H:%M:%S"),
    "rates": []
}

for day in range(num_days):
    check_in_date = (today + timedelta(days=day)).strftime("%Y-%m-%d")
    check_out_date = (today + timedelta(days=day + 1)).strftime("%Y-%m-%d")

    url = f"https://api.booked.net/api/site_hotel_avail.json?hotel_id={hotelId}&check_in={check_in_date}&check_out={check_out_date}&ShowCurrency=INR"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response_content = response.json()

        # with open('rates_raw.json','w') as json_file:
        #     json.dump(response_content, json_file, indent = 4)

        data_slot = response_content['result'][0]['data']
        
        for data in data_slot:
            rooms = data.get('rooms',{})
            for detail in rooms:
                room_name = detail.get('name')
         
                roomId = detail.get('roomhash').split('|')[0]
                for rate in detail.get('rates', []):
                    price = rate.get('price')
                    meal_plan = rate.get('meal_plan')
                     
                    if meal_plan:
                        if 'Breakfast not included' in meal_plan:
                            room_plan = 'EP'
                        elif 'Breakfast included' in meal_plan and 'Lunch' in meal_plan and 'Dinner' in meal_plan:
                            room_plan = 'AP'
                        elif 'Breakfast included' in meal_plan and '/' in meal_plan:
                            room_plan = 'MAP'
                        elif 'Breakfast included' in meal_plan:
                            room_plan = 'CP'
                        else:
                            room_plan = 'Unknown'
                    else:
                        room_plan = 'Unknown'
                      
                    room_data['rates'].append({
                        "roomId": roomId,
                        "name": room_name,
                        "checkIn": check_in_date,
                        "checkOut": check_out_date,
                        "roomPlan": room_plan,
                        "displayPrice": price
                    })

    print(f'hotelId : {hotelId} | checkIn : {check_in_date}')

with open('rates_data.json', 'w') as json_file:
    json.dump(room_data, json_file, indent=4)