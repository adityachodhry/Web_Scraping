import requests
import json
from datetime import datetime, timedelta

hotel_name = "Shahpura House"

url = f"https://www.happyeasygo.com/hotel_api/web/city?name={hotel_name}"

headers = {
    'Content-Type': 'application/json',
    'X-Device': 'pc',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

response = requests.request("GET", url, headers=headers)
if response.status_code == 200:
    results = response.json()
    
    # with open ('Row_Data.json', 'w') as json_file:
    #     json.dump(results, json_file)

    hotel_info = []

    data_slot = results.get('data', {}).get('cityHotelList', [])
    # print(data_slot)

    # Get current date
    current_date = datetime.now().strftime("%Y-%m-%d")
    check_out_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    

    item = data_slot[0]
    hId = item.get('code')
    hotelName = item.get('name')
    cityName = item.get('cityName')
    url = f"https://hotel.happyeasygo.com/hotels/{cityName}/hotel_{hId}/{current_date}_{check_out_date}/2-0?source_from=happyeasygo"

    search_info = {
        'hId': hId,
        'hotelName': hotelName,
        'cityName': cityName,
        'url': url
    }
    hotel_info.append(search_info)
    print(hotel_info)

    # with open('happyEasyGo_hotelSearch.json', 'w') as json_file:
    #     json.dump(hotel_info, json_file)