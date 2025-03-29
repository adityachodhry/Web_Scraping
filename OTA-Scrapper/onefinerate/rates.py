import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import re

num_days = 90
today = datetime.now()
Id = 'ODE1NjQ'

room_data = {
    "otpaId": None,  
    "timestamp": today.strftime("%Y-%m-%d %H:%M:%S"),
    "rates": []
}

for day in range(num_days):
    check_in_date = (today + timedelta(days=day)).strftime("%d-%m-%Y")
    check_out_date = (today + timedelta(days=day + 1)).strftime("%d-%m-%Y")

    url = f"https://onefinerate.com/Search/HotelDetails?Id={Id}=&sCheckIn={check_in_date}&sCheckOut={check_out_date}&sRoomData=[{{%22room%22:1,%22adult%22:2,%22child%22:0,%22ChildAge%22:[]}}]"

    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        # with open("rates.html", "w", encoding="utf-8")as html_file:
        #     html_file.write(html_content)

        rooms_div = soup.find('div', id='rooms')

        if rooms_div:
            room_listings = rooms_div.find_all('div', class_='hotel-list')

            for room in room_listings:
                room_name_tag = room.find('a', class_='hoteltitles')
                room_name = room_name_tag.get_text(strip=True) if room_name_tag else "Room name not found"

                price_inputs = room.find_all('input', class_='txtRooms', attrs={'data-price': True})

                if not room_data['otpaId']:
                    first_room_url = room.find('input', class_='txtRooms')['data-spricecheckurl']
                    match_hotel = re.search(r'/properties/(\d+)/', first_room_url)
                    if match_hotel:
                        room_data['otpaId'] = match_hotel.group(1)

                meal_plan_div = room.find_all('ul', class_='incl-point')

                for input_elem, meal_elem in zip(price_inputs, meal_plan_div):
                    price = input_elem['data-price']
                    room_url = input_elem['data-spricecheckurl']
                    match_room = re.search(r'/rooms/(\d+)/', room_url)
                    if match_room:
                        room_id = match_room.group(1)
                    else:
                        room_id = "Room ID not found"

                    meals = meal_elem.get_text().strip()

                    room_plan = 'EP'  

                    if 'Half board' in meals:
                        room_plan = 'MAP'  
                    elif 'Free breakfast' in meals or 'Full Breakfast'in meals:
                        room_plan = 'CP'  

                    room_data['rates'].append({
                        "roomId": room_id,
                        "name": room_name,
                        "check_in": check_in_date,
                        "check_out": check_out_date,
                        "room_plan": room_plan,
                        "displayprice": price
                    })

    print(f'Checkin : {check_in_date}')

with open('rates_data.json', 'w') as json_file:
    json.dump(room_data, json_file, indent=4)

print(f'Data collected and saved to rates_data.json')