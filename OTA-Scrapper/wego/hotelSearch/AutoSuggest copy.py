import requests
import json
from datetime import datetime, timedelta

hotelName = "Shahpura House"

# Get current date
current_date = datetime.now().strftime("%Y-%m-%d")
check_out_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

url = f"https://srv.wego.com/places/search?locale=en&site_code=IN&query={hotelName}&types[]=city&types[]=district&types[]=hotel&types[]=region&min_hotels=1"

response = requests.get(url)

if response.status_code == 200:
    response_content = response.json()

    hotels_data = []
    data = response_content[0]

    Hid = data.get('id')
    hotelName = data.get('name')
    cityCode = data.get('cityCode')
    cityName = data.get('cityName')

    # Construct hotel URL
    hotel_url = fhotel_url = f"https://www.wego.co.in/hotels/searches/{cityCode}/{current_date}/{check_out_date}/{Hid}?ab=true&guests=2"

    hotel_data = {
        'hId': Hid,
        'hotelName': hotelName,
        'cityName': cityName,
        'cityCode': cityCode,
        'hotelUrl': hotel_url
    }
    hotels_data.append(hotel_data)

with open('hotelSearch.json', 'w') as json_file:
    json.dump(hotels_data, json_file, indent=4)
