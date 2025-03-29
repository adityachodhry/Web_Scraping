import requests
import json

hotelName = "Hilton Garden Inn Dikmen"

url = f"https://www.odamax.com/ajax/autocomplete?pagetype=SEARCH&q={hotelName}"

response = requests.get(url)

if response.status_code == 200:
    response_content = response.json()

    # print(response_content)
    # with open('hoteldetail.json', 'w') as json_file:
    #     json.dump(response_content, json_file, indent=4)

    hotels_data = []

    data_slot = response_content.get('suggestions', [])[0]

    url = data_slot.get('url')

    # Extracting hotel code from the URL
    hotel_code_index = url.rfind('-') + 1
    hotel_code = url[hotel_code_index:].split('/')[0]

    full_hotel_name = data_slot.get('name')
    hotel_name = full_hotel_name.split(',')[0].strip()

    hUrl = url.split('/')
    url_split = "/".join(hUrl[:-1])

    hotel_url = f"https://www.odamax.com{url_split}"

    # # Extract the location (city) from the full name
    # location = ', '.join(full_hotel_name.split(',')[1:]).strip()
    # print(location)

    hotel_data = {
        'hId': hotel_code,
        'hotelName': hotel_name,
        'hotelUrl': hotel_url
    }
    hotels_data.append(hotel_data)

with open('hotelSearch.json', 'w') as json_file:
    json.dump(hotels_data, json_file, indent=4)
