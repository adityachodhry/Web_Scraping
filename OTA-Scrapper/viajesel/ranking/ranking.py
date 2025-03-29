import requests
from datetime import datetime, timedelta
import json

today = datetime.now()
num_days = 1

check_in_date = (today + timedelta(days=num_days)).strftime("%Y/%m/%d")
check_out_date = (today + timedelta(days=num_days + 1)).strftime("%Y/%m/%d")

url_top = "https://bookings.viajeselcorteingles.es/hotels/api/hotel/top/"
params_top = {
    'code': '8543072',
    'type': 'CIU',
    'check_in': check_in_date,
    'check_out': check_out_date,
    'language': 'es'
}

headers = {
    'Referer': f'https://bookings.viajeselcorteingles.es/hotels/results/?check_in={check_in_date}&check_out={check_out_date}&rooms=30%2C30&type=CIU&code=8543072',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

response_top = requests.get(url_top, params=params_top, headers=headers)

if response_top.status_code == 200:
    response_content_top = response_top.json()
    
    # with open('Raw.json','w') as json_file:
    #     json.dump(response_content_top, json_file, indent = 4)
    
    hotel_ids = response_content_top.get('hotel_list', [])[:500]

room_data = {
    "timestamp": today.strftime("%Y-%m-%d %H:%M:%S"),
    'otaId': 19,
    'city': 'paris',
    "ota": "viajesel",
    "hotels": []
}

ranking = 1

hotel_id_list = ','.join(hotel_ids) 

url = f"https://bookings.viajeselcorteingles.es/hotels/api/hotel/search/?hotels={hotel_id_list}&language=es&is_list=true"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    response_content = response.json()

    # with open('ranking_raw.json','w') as json_file:
    #     json.dump(response_content, json_file, indent = 4)

    hotels_data = response_content.get('hotels', {})

    for hotel_id, hotel_info in hotels_data.items():
        hotel_code = hotel_info['hotel_info']['hotel_code']
        hotel_name = hotel_info['hotel_info']['name']
        hotel_rating_symbol = hotel_info['hotel_info'].get('hotel_category', 'Unknown')

        star_count = hotel_rating_symbol.count('*')

        room_data['hotels'].append({
            "hId": hotel_code,
            "name": hotel_name,
            "ranking": ranking,
            "rating": star_count
        })

        ranking += 1 

with open('ranking_data.json', 'w') as json_file:
    json.dump(room_data, json_file, indent=4)
