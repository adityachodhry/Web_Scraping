import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json

hotelName = 'swissotel-buyuk'
hotelId = 101142
num_days = 90

today = datetime.now()
room_data = {
    "hotelname": hotelName,
    "otpaid" : hotelId,
    "timestamp": today.strftime("%Y-%m-%d %H:%M:%S"),
    "rates": []
}

for day in range(num_days):
    check_in_date = (today + timedelta(days=day)).strftime("%Y.%m.%d")
    check_out_date = (today + timedelta(days=day + 1)).strftime("%Y.%m.%d")

    url = f"https://www.odamax.com/en/101142?check_in={check_in_date}&check_out={check_out_date}&room=1&adult_1=2"

    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        # with open("rates_raw.html", "w", encoding="utf-8")as html_file:
        #     html_file.write(html_content)

        # Find all room buttons
        room_buttons = soup.find_all("button", class_="select-room-one btn odamax-primary")

        for button in room_buttons:
            room_type = button.get("data-name")
            room_id = button.get("data-code")
            price = button.get("data-price")
            meal_plan = button.get("data-board-type")
            currency = button.get('data-currency')

            if 'Room Only' in meal_plan:
                    room_plan = 'EP'
            elif 'Half Board' in meal_plan:
                room_plan = 'MAP'
            elif 'Full Board' in meal_plan:
                room_plan = 'AP'
            elif 'Breakfast Included' in meal_plan:
                room_plan = 'CP'
            else:
                room_plan = 'Unknown'

            # Append room data to the room_data dictionary
            room_data["rates"].append({
                "roomId": room_id,
                "roomType": room_type,
                "check_in" : check_in_date,
                "check_out" : check_out_date,
                "room_plan": room_plan,
                "price": f"{price} {currency}"              
            })
    print(f'Hotel : {hotelName} | Checkin : {check_in_date}')

with open('rates_data.json', 'w') as json_file:
    json.dump(room_data, json_file, indent=4)
