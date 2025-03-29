import requests
import json
from datetime import datetime, timedelta

num_days = 1
today = datetime.now()
room_data = {
    "timestamp": today.strftime("%Y-%m-%d %H:%M:%S"),
    "rates": []
}

ranking = 1
page = 1
offset = 20

while ranking <=20:
    check_in_date = (today + timedelta(days=num_days)).strftime("%Y/%m/%d")
    check_out_date = (today + timedelta(days=num_days + 1)).strftime("%Y/%m/%d")

    url = f"https://hotels.travelguru.com/tgapi/hotels/v1/pageSearch?checkInDate=07/05/2024&checkOutDate=08/05/2024&page=1&offset=20"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'X-Api-Key': 'RcKU4ktJuNBFV1BknPWT'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response_content = response.json()
 
        data_slot = response_content.get('data', {})
        rates = data_slot.get('rates', {}).get('hotels', [])  
        content = data_slot.get('content', {}).get('hotels', []) 

        for rate, hotel in zip(rates, content):

            if ranking > 20:
                break 

            id = hotel.get('id')
            name = hotel.get('orgName')
            price = rate.get('totalAmount')
            rating = hotel.get('gr', {}).get('rating')
            stars = hotel.get('st', {})

            if id:
                room_id = id.lstrip('0')
            else:
                room_id = "N/A"

            room_data['rates'].append({
                "roomId": room_id,
                'starRating' : stars,
                'ranking' : ranking
                # "name": name,
                # "check_in": check_in_date,
                # "check_out": check_out_date,
                # "displayprice": price
            })

            ranking += 1 

        # page += 1

with open('ranking_data.json', 'w') as json_file:
    json.dump(room_data, json_file, indent=4)
