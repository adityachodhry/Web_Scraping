import requests
import json
from datetime import datetime, timedelta

hotel_name = 'Shahpura House'

url = "https://us.trip.com/restapi/soa2/14975/homepageSuggest"

payload = json.dumps({
  "keyword": hotel_name,
  "head": {}
})
headers = {
  'Cookie': 'UBT_VID=1704951651378.9b9dGqLrRvub',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

if response.status_code == 200:
    results = response.json()

    # with open('Row_Data.json', 'w') as json_file:
    #     json.dump(results, json_file)

    hotel_info = []

    data_slot = results.get('result')

    current_date = datetime.now().strftime("%Y-%m-%d")
    check_out_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    
    item = data_slot[0]
    hId = item.get('id')
    hotelName = item.get('name')
    cityName = item.get('districtName')
    url = f"https://www.trip.com/hotels/detail/?hotelId={hId}&checkIn={current_date}&checkOut={check_out_date}&adult=2&children=0"

    search_info = {
        'hId': hId,
        'hotelName': hotelName,
        'cityName': cityName,
        'url': url
    }
    hotel_info.append(search_info)
    print(hotel_info)
    
    # with open('trip_dot_com_hotelSearch.json', 'w') as json_file:
    #     json.dump(hotel_info, json_file)