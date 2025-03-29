import requests
import json
from datetime import datetime, timedelta

hotelName = 'The Tower, London'
hotelId = 'A0525998'
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

    url = f"https://cloud.tui.com/osp/ao/ml/rooms-panel/rooms?hotelId={hotelId}&locale=en-GB&market=uk&passengers=30%2C30&startDate={check_in_date}&endDate={check_out_date}&duration=1&productId=9df30436-5876-49aa-b827-e3b7f3754517&sourcing=DYNAMIC&currency=INR"

    response = requests.get(url)

    if response.status_code == 200:
        response_content = response.json()

        # with open('rates_raw.json','w') as json_file:
        #     json.dump(response_content, json_file, indent = 4)

        room_types = response_content.get('roomTypes', [])

        for room in room_types:
            roomId = room.get('roomTypeCode',{})
            roomName = room.get('roomTypeName', {})
            offers = room.get('offers', [])

            for offer in offers:
                meal_plan = offer.get('board', {}).get('boardName', {})
                price = offer.get('pricePerPerson',{}).get('amount')

                if 'Room Only' in meal_plan:
                    room_plan = 'EP'
                elif 'Breakfast' in meal_plan and 'Lunch' in meal_plan and 'Dinner' in meal_plan and '/' in meal_plan:
                    room_plan = 'MAP'
                elif 'Breakfast included' in meal_plan and 'Lunch' in meal_plan and 'Dinner' in meal_plan:
                    room_plan = 'AP'
                elif 'Breakfast' in meal_plan:
                    room_plan = 'CP'
                else:
                    room_plan = 'Unknown'

                display_price = f"£ {price:.2f}" if price is not None else "N/A"

                room_data['rates'].append({
                            "roomId": roomId,
                            "name": roomName,
                            "check_in": check_in_date,
                            "check_out": check_out_date,
                            "room_plan": room_plan,
                            "displayprice" : display_price
                        })
    print(f'Hotel : {hotelName} | Checkin : {check_in_date}')

with open('rates_data.json', 'w') as json_file:
    json.dump(room_data, json_file, indent=4)

