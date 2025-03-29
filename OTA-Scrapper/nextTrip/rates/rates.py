import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

num_days = 90
cityName = 'New York City'
today = datetime.now()
hotelId = 3916875

room_data = {
    "otaPId": 25,
    "timestamp": today.strftime("%Y-%m-%d %H:%M:%S"),
    "rates": []
}

for day in range(num_days):
    check_in_date = (today + timedelta(days=day)).strftime("%Y-%m-%d")
    check_out_date = (today + timedelta(days=day + 1)).strftime("%Y-%m-%d")

    url = f"https://results.nexttrip.com/details.php?fd={check_in_date}&td={check_out_date}&ap1=2&hotelTo={cityName}%2C+US&hotelUniqueId={hotelId}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        # with open("rates.html", "w", encoding="utf-8")as html_file:
        #     html_file.write(html_content)

        property_page_wrap_div = soup.find('div', id='property-page-wrap')

        if property_page_wrap_div:
            hotelId = property_page_wrap_div.get('data-hotel-unique-id', '')
            room_data['otapid'] = hotelId

            room_divs = soup.find_all('div', class_='bottom-content data-box room mt10')

            for room_div in room_divs:
                h3_element = room_div.find('h3', class_='text-regular mt10')
                if h3_element:
                    roomName = h3_element.text.strip()

                    price_span = room_div.find('span', class_='at-details-day-sell')
                    if price_span:
                        price = price_span.text.strip()

                        room_details_div = room_div.find('div', class_='room-details')
                        if room_details_div:
                            roomId = room_details_div.get('data-room-id', '')

                            p_element = room_details_div.find('p')
                            if p_element:
                                meal_plan = p_element.text.strip()

                                if 'Breakfast included' in meal_plan:
                                    room_plan = 'CP'
                                else:
                                    room_plan = 'EP'

                                room_data['rates'].append({
                                    "roomId": roomId,
                                    "name": roomName,
                                    "checkIn": check_in_date,
                                    "checkOut": check_out_date,
                                    "roomPlan": room_plan,
                                    "displayPrice": price
                                })
    else:
        print(response.status_code)

    print(f'HotelID : {hotelId} rates for Checkin: {check_in_date}')

with open('rates_data.json', 'w') as json_file:
    json.dump(room_data, json_file, indent=4)
