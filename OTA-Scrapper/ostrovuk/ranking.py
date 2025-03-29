import requests
import json
from datetime import datetime, timedelta

num_days = 1
today = datetime.now()
check_in_date = (today + timedelta(days=num_days)).strftime("%Y-%m-%d")
check_out_date = (today + timedelta(days=num_days + 1)).strftime("%Y-%m-%d")

room_data = {
    "timestamp": today.strftime("%Y-%m-%d %H:%M:%S"),
    "rates": []
}

url = "https://ostrovok.ru/hotel/search/v2/site/serp?session=1a588ef6-c9c0-4699-b119-84b7ad200501"

body = {
    "session_params": {
        "currency": "INR",
        "language": "en",
        "search_uuid": "2a50c9aa-0c71-4747-8d3f-0a38497a0e3b",
        "arrival_date": check_in_date,
        "departure_date": check_out_date,
        "region_id": 2734,
        "paxes": [{"adults": 2}]
    },
    "page": 1,
    "map_hotels": True,
    "session_id": "1a588ef6-c9c0-4699-b119-84b7ad200501"
}

response = requests.post(url, json=body)

if response.status_code == 200:
    response_content = response.json()
    hotels = response_content.get('hotels', [])

    ranking = 1
    for hotel in hotels:
        static = hotel.get('static_vm', {})
        hotelName = static.get('name_en', 'Unknown Hotel')
        id = static.get('master_id', 'No ID')
        rating = static.get('rating', {})
        ratingTotal = rating.get('total', 'No Rating')

        room_data['rates'].append({
            "hId": id,
            'hotelName': hotelName,
            'rating': ratingTotal,
            'ranking': ranking
        })
        
        ranking += 1

    with open('ranking_data.json', 'w') as json_file:
        json.dump(room_data, json_file, indent=4)
else:
    print(f"Failed to fetch data: HTTP {response.status_code} - {response.reason}")
