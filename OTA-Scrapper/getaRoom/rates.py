import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta

hotelSlug = 'the-whitehall-hotel'
num_days = 90

today = datetime.now()
room_data = {
    "otaPId": 23,
    "timestamp": today.strftime("%Y-%m-%d %H:%M:%S"),
    "rates": []
}

for day in range(num_days):
    check_in_date = (today + timedelta(days=day)).strftime("%Y-%m-%d")
    check_out_date = (today + timedelta(days=day + 1)).strftime("%Y-%m-%d")

    url = f"https://m.getaroom.com/hotels/{hotelSlug}.mobile?check_in={check_in_date}&check_out={check_out_date}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers= headers)

    if response.status_code == 200:
        html_content = response.text
        # print(html_content)

        # with open("getaRoom.html", "w", encoding="utf-8")as html_file:
        #     html_file.write(html_content)

        soup = BeautifulSoup(html_content, 'html.parser')

        room_anchors = soup.find_all('a', class_='photo')
        price_spans = soup.find_all('span', class_='amount')

        for room_anchor, price_span in zip(room_anchors, price_spans):
            room_id = room_anchor.get('data-unit-uuid')
            room_name = room_anchor.get('title')
            price_text = price_span.get_text(strip=True)

            room_data['rates'].append({
                            "roomId": room_id,
                            "name": room_name,
                            "checkIn": check_in_date,
                            "checkOut": check_out_date,
                            "roomPlan" : "EP",
                            "displayPrice": price_text
                        })

    print(f'HotelId : {hotelSlug} | Checkin : {check_in_date}')

with open('rates_data.json', 'w') as json_file:
    json.dump(room_data, json_file, indent=4)