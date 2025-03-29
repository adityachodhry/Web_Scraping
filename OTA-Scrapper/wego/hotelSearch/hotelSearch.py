import requests
import json

hotelName = "Shahpura House"

url = "https://srv.wego.com/places/search?locale=en&site_code=IN&query=shahpura%20house&types[]=city&types[]=district&types[]=hotel&types[]=region&min_hotels=1"

response = requests.get(url)

if response.status_code == 200:
    response_content = response.json()

    # print(response_content)
    # with open('hoteldetail.json', 'w') as json_file:
    #     json.dump(response_content, json_file, indent=4)

    hotels_data = []

    data_slot = response_content
    for data in data_slot:
        Hid = data.get('id')
        hotelName = data.get('name')
        cityCode = data.get('cityCode')
        cityName = data.get('cityName')

        hotel_data = {
                    'hId': Hid,
                    'hotelName': hotelName,
                    'location' : cityName,
                    'cityCode' : cityCode
                }
        hotels_data.append(hotel_data)

    with open('hotelSearch.json', 'w') as json_file:
        json.dump(hotels_data, json_file, indent=4)
