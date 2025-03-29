import requests
import json

hotel_name = 'bloom Boutique Udaipur'

url = f"https://services.hrs-api.com/locations?query={hotel_name}&language=en"

response = requests.request("GET", url)

if response.status_code == 200:
    results = response.json()
    # print(results)

    # with open('Row_Data.json', 'w') as json_file:
    #     json.dump(results, json_file)

    hotel_info = []

    item = results[0]
    hId = item.get('hotelId')
    hotelName = item.get('name')
    cityName = item.get('additionalName').split(',')[0]
    url = f"https://www.hrs.com/detail?hn={hId}"

    search_info = {
        'hId': hId,
        'hotelName': hotelName,
        'cityName': cityName,
        'url': url
    }
    hotel_info.append(search_info)
    
    with open('hrshotelSearch.json', 'w') as json_file:
        json.dump(hotel_info, json_file)