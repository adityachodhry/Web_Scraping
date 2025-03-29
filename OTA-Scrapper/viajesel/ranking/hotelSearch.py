import requests
import json
from datetime import datetime, timedelta

hotel_name = "Shahpura House Jaipur"

# Get current date
current_in = datetime.now().strftime("%d/%m/%Y")
check_out = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
    

url = f"https://autocomplete.toolfactory.tech/query?q={hotel_name}&f=json&l=es&t=ISL%2CZON%2CCIU%2CHOT"

response = requests.request("GET", url)

if response.status_code == 200:
    results = response.json()

    # with open('Row_Data.json', 'w') as json_file:
    #     json.dump(results, json_file, indent=4 )

    hotel_search = []

    data = results.get('d')
    item = data[0]
    
    hId = item.get('value')
    hName = item.get('text').split(',')[0]
    url = f"https://bookings.viajeselcorteingles.es/hotels/hotel/?check_in={current_in}&check_out={check_out}&hotel={hId}"

    hotel_url = {
        "hId": hId,
        "hName": hName,
        "url": url
    }
    hotel_search.append(hotel_url)

    with open('hotelSearch.json', 'w') as json_file:
        json.dump(hotel_search, json_file, indent=4)
    print("hotel search information stored..")