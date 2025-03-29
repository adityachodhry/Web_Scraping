import requests
from datetime import datetime, timedelta
import json

hotelName = "ITC Maratha"
hotelId = 20131124133838404
num_days = 90

today = datetime.now()  

room_data_list = []

for day in range(num_days):
    check_in_date = (today + timedelta(days=day)).strftime("%d-%m-%Y")
    check_out_date = (today + timedelta(days=day + 1)).strftime("%d-%m-%Y")

    url = "https://www.hotels.irctc.co.in/tourismUser/tourism/hotel/hoteldetails"

    body = {
        "hotelCode": str(hotelId),
        "checkInDate": check_in_date,
        "checkOutDate": check_out_date,
        "noOfRoom": "1",
        "noOfAdt": "2",
        "type": "Hotel",
        "provider": "MMT",
        "searchKeys": {
            "fullName": "Mumbai,Maharashtra",
            "name": hotelName,
            "type": "Hotel"
        }
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    response = requests.post(url, json=body, headers=headers)

    if response.status_code == 200:
        response_content = response.json()

        # with open('rates_raw.json','w') as json_file:
        #     json.dump(response_content, json_file, indent = 4)


        if 'data' in response_content and response_content['data']:
            data_slot = response_content['data']
            if 'hotelRoomDetails' in data_slot and data_slot['hotelRoomDetails']:
                for room in data_slot['hotelRoomDetails']:
                    roomid = room.get('hotelRoomTypeID').split('#')[0]
                    roomName = room.get('roomType')
                    price = room.get('fare')

                    room_name = None
                    meal_plan = None

                    if "with" in roomName or "With" in roomName:
                        if "with" in roomName:
                            parts = roomName.split("with", 1)
                        else:  # "With" in roomName
                            parts = roomName.split("With", 1)
                        room_name = parts[0].strip().capitalize()
                        meal_plan = parts[1].strip()

                    if meal_plan:
                        meal_plan_lower = meal_plan.lower()
                        if 'breakfast not included' in meal_plan_lower:
                            room_plan = 'EP'
                        elif 'breakfast' in meal_plan_lower and '+' in meal_plan_lower and 'lunch' in meal_plan_lower and '/' in meal_plan_lower and 'dinner' in meal_plan_lower:
                            room_plan = 'MAP'
                        elif 'breakfast' in meal_plan_lower and '+' in meal_plan_lower and 'lunch' in meal_plan_lower and '+' in meal_plan_lower and 'dinner' in meal_plan_lower:
                            room_plan = 'AP'
                        elif 'breakfast' in meal_plan_lower:
                            room_plan = 'CP'
                        else:
                            room_plan = 'Unknown'
                    else:
                        room_plan = 'Unknown'

                    room_data = {
                        "check_in": check_in_date,
                        "check_out": check_out_date,
                        "room_id": roomid,
                        "room_type": room_name if room_name else "Not specified",
                        "room_plan": room_plan,
                        "displayprice": price
                    }

                    room_data_list.append(room_data)

    final_data = {
    "otapid": hotelId,
    "timestamp": today.strftime("%Y-%m-%d %H:%M:%S"),  
    "rates": room_data_list
}


    print(f'Hotel: {hotelName} | Check-in: {check_in_date}')

# Write JSON data to a file
with open('rates_data.json', 'w') as json_file:
    json.dump(final_data, json_file, indent=4)

print("Data stored successfully in hotel_room_data.json")
