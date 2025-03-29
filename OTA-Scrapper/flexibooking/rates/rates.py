import requests
import json
from datetime import datetime, timedelta

hotelName = "Mercury London Paddington"
hotelId = 45
num_days = 9

today = datetime.now()
room_data = {
    "otaPId": hotelId,
    "timestamp": today.strftime("%Y-%m-%d %H:%M:%S"),
    "rates": []
}

for day in range(num_days):
    check_in_date = (today + timedelta(days=day)).strftime("%Y-%m-%d")
    check_out_date = (today + timedelta(days=day + 1)).strftime("%Y-%m-%d")

    url = f"https://flexibookingsapi.azurewebsites.net/api/Search/HotelRates?Id={hotelId}&checkInDate={check_in_date}&checkOutDate={check_out_date}&checkInTime=14&checkOutTime=11"

    response = requests.get(url)
    if response.status_code == 200:
        response_content = response.json()
       
        # with open('flexibooking_rates.json','w') as json_file:
        #     json.dump(response_content, json_file, indent = 4)

        data_slot = response_content
        for data in data_slot:
            roomId = data.get('RoomId')
            name = data.get('RoomName')
            rrates = data['Rates']
            for rates in rrates:
                price = rates.get('Price')
                meal_plan = rates.get('Meals')
                     
                if meal_plan:
                    if 'Breakfast' in meal_plan:
                        room_plan = 'CP'                    
                    elif 'Breakfast' in meal_plan and 'Lunch' in meal_plan and 'Dinner' in meal_plan:
                        room_plan = 'AP'
                    elif 'Breakfast included' in meal_plan and '/' in meal_plan:
                        room_plan = 'MAP'
                else:
                    room_plan = 'EP'
                    
                room_data['rates'].append({
                        "roomId": roomId,
                        "name": name,
                        "checkIn": check_in_date,
                        "checkOut": check_out_date,
                        "roomPlan": room_plan,
                        "displayPrice": price
                    })

    print(f'hotel : {hotelName} | Checkin : {check_in_date}')

with open('rates_data.json', 'w') as json_file:
    json.dump(room_data, json_file, indent=4)
