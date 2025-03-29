import requests
import json
from datetime import datetime, timedelta

hotelName = "Hotel Amar Kothi Udaipur"

# Get current date
current_date = datetime.now().strftime("%Y-%m-%d")
check_out_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

url = f"https://www.booked.net/?page=search_json&langID=1&kw={hotelName}&bcomid=1"

response = requests.get(url)

if response.status_code == 200:
    response_content = response.json()

    with open('hoteldetail.json', 'w') as json_file:
        json.dump(response_content, json_file, indent=4)

    hotels_data = []
    
    data_slot = response_content['results']
    for data in data_slot:
        id = data.get('id')
        name = data.get('n')
        location = data.get('l')
        cityId = data.get('cid')
        hUrl = data.get('u')

        # hUrlName = hUrl.split('/')[2]
        # hHotelUrlName = hUrlName.split('-')[:-1]
        # print(hHotelUrlName)

        hotel_url = f"https://www.booked.net{hUrl}"

        # # Prepend "https://" to the hotel_url
        # if hotel_url:
        #     hotel_url = "https://" + hotel_url

        hotel_data = {
            'hId': id,
            'hotelName': name,
            'cityName' : location,
            # 'cityId' : cityId,
            'hotelUrl': hotel_url
        }
        hotels_data.append(hotel_data)
    data_slot = response_content['results'][0]
    id = data_slot.get('id')
    name = data_slot.get('n')
    location = data_slot.get('l')
    cityId = data_slot.get('cid')
    url = data_slot.get('u')
        
    hotel_data = {
                'hId': id,
                'hotelName': name,
                'Location' : location,
                'cityId' : cityId,
                'url' : url
            }
    hotels_data.append(hotel_data)

    with open('hotelSearch.json', 'w') as json_file:
        json.dump(hotels_data, json_file, indent=4)
