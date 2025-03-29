import requests
import json
from datetime import datetime, timedelta

hotelId = 208071
num_days = 90

today = datetime.now()
room_data = {
    "otapid": hotelId,
    "timestamp": today.strftime("%Y-%m-%d %H:%M:%S"),
    "rates": []
}

for day in range(num_days):
    check_in_date = (today + timedelta(days=day)).strftime("%d/%m/%Y")
    check_out_date = (today + timedelta(days=day + 1)).strftime("%d/%m/%Y")

    url = f"https://hotel.yatra.com/tgapi/hotels/v1/hotels/00{hotelId}?checkInDate={check_in_date}&checkOutDate={check_out_date}&rooms[0].id=1"
    

    headers = {
        "X-Api-Key": "JN9aWyj7hJ1ZrExC7Ozo",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response_content = response.json()

        with open('rates_raw.json','w') as json_file:
            json.dump(response_content, json_file, indent = 4)
        if 'data' in response_content:
            data_slot = response_content['data']

            if 'rates' in data_slot:
                rates = data_slot['rates']

                for rate in rates:
                    roomid = rate.get('roomTypeId')
                    roomname = rate.get('roomName')
                    ratetype = rate.get('name')
                    mealplan = rate.get('inclusions', [])
                    pricing = rate.get('pricing', {}).get('perNightPrice', {})
                    price = pricing.get('price')

                    room_plan = 'Unknown'
                    if 'Room Only' in mealplan:
                        room_plan = 'EP'
                    elif 'Half Board' in mealplan:
                        room_plan = 'MAP'
                    elif 'Bed and Breakfast' in mealplan:
                        room_plan = 'CP'

                    formatted_check_in_date = (today + timedelta(days=day)).strftime("%d-%m-%Y")
                    formatted_check_out_date = (today + timedelta(days=day + 1)).strftime("%d-%m-%Y")

                    room_data['rates'].append({
                        'roomid': roomid,
                        'Name': roomname,
                        'check_in': formatted_check_in_date,
                        'check_out': formatted_check_out_date,
                        'room_plan': room_plan,
                        'displayprice': price
                    })

        print(f'Hotel : {hotelId} | Checkin : {check_in_date}')

with open('rates_data.json', 'w') as json_file:
    json.dump(room_data, json_file, indent=4)
