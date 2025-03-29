import requests
import json
from datetime import datetime, timedelta

hotelName = "Shahpura House"

# Get current date
current_date = datetime.now().strftime("%d/%m/%Y")
check_out_date = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")

url = f"https://cdn.travelguru.com/api/v4/autosuggest?key={hotelName}&filter=domestic&count=1"

headers = {'X-Api-Key': 'RcKU4ktJuNBFV1BknPWT'}
response = requests.get(url, headers = headers)

if response.status_code == 200:
    response_content = response.json()
    
    # with open('hoteldetail.json', 'w') as json_file:
    #     json.dump(response_content, json_file, indent=4)

    hotels_data = []

    data_slot = response_content['hotels'][0]

    hotelName = data_slot.get('displayName')
    Hid = data_slot.get('sourceID')
    cityName = data_slot.get('cityName')

    hotel_url = f"https://hotels.travelguru.com/hotel-search/tgdom/details?&checkinDate={current_date}&checkoutDate={check_out_date}&roomRequests[0].id=1&roomRequests[0].noOfAdults=1&hotelId={Hid}"

    hotel_data = {
                'hId': Hid,
                'hotelName': hotelName,
                'cityName' : cityName,
                'hotelUrl': hotel_url
            }
    
    hotels_data.append(hotel_data)
    print(hotel_data)

# with open('hotelSearch.json', 'w') as json_file:
#     json.dump(hotels_data, json_file, indent=4)
        