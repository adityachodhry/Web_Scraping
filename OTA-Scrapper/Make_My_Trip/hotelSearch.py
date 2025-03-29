import requests
import json
from datetime import datetime, timedelta

hotel_name = 'Shahpura House Jaipur'

url = f"https://mapi.makemytrip.com/autosuggest/v5/search?q={hotel_name}&language=eng&currency=INR"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

response = requests.request("GET", url, headers=headers)

if response.status_code == 200:
    results = response.json()
    
    # with open ('Row_Data.json', 'w') as json_file:
    #     json.dump(results, json_file)

    hotel_info = []

    current_date = datetime.now().strftime("%Y%m%d")
    check_out_date = (datetime.now() + timedelta(days=1)).strftime("%Y%m%d")

    item = results[0]
    hId = item.get('id')
    hotelName = item.get('name')
    cityName = item.get('cityName')
    cityCode = item.get('cityCode')
    url = f"https://www.makemytrip.com/hotels/hotel-details/?hotelId={hId}&_uCurrency=INR&checkin=05082024&checkout=05092024&city={cityCode}&3&roomStayQualifier=2e0e"

    search_info = {
        'hId': hId,
        'hotelName': hotelName,
        'cityCode': cityCode,
        'cityName': cityName,
        'url': url
    }
    hotel_info.append(search_info)
    
    with open ('MMT_hotelSearch.json', 'w') as json_file:
        json.dump(hotel_info, json_file)