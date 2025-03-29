import requests
import json
from datetime import datetime, timedelta

hotelName = "Hotel King City Muzaffarnagar"
# Get current date
current_date = datetime.now().strftime("%d/%m/%Y")
check_out_date = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")

url = f"https://cdn.travelguru.com/api/v4/autosuggest?key={hotelName}&filter=all&count=10&propertyType=all"

response = requests.get(url)

hotels_data = []
print(response.status_code)
if response.status_code == 200:
    print(response.text)
    response_content = response.json()

    data_slot = response_content['hotels'][0]
    print(data_slot)

    hotelName = data_slot.get('displayName')
    Hid = data_slot.get('sourceID')
    cityName = data_slot.get('cityName')

    hotel_url = f"https://hotel.yatra.com/hotel-search/dom/details?checkoutDate={check_out_date}&checkinDate={current_date}&roomRequests[0].id=1&roomRequests[0].noOfAdults=2&roomRequests[0].noOfChildren=0&hotelId={Hid}"

    hotel_data = {
        'Hid': Hid,
        'hotelName': hotelName,
        'cityName': cityName,
        'hotelUrl': hotel_url
    }
    hotels_data.append(hotel_data)

with open('hotelSearch.json', 'w') as json_file:
    json.dump(hotels_data, json_file, indent=4)
