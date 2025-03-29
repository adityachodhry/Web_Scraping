import requests
import json
from datetime import datetime, timedelta

today = datetime.now()

room_data = {
    "timestamp": today.strftime("%Y-%m-%d %H:%M:%S"),
    'otaId' : 15,
    'cityCode' : 'UDR',
    "ota : wego": []
}
ranking = 1

searchId = 'f67e0cc2d75666ef'

url = f"https://srv.wego.com/v3/metasearch/hotels/searches/{searchId}/results?locale=en&currencyCode=INR&amountType=NIGHTLY&clientId=858bf707-716c-471c-9378-1c599b4e7c8c&offset=0&isLastPolling=false&moreRates=true&"

response = requests.get(url)

if response.status_code == 200:
    response_content = response.json()
    # print(response_content)
    
    with open('wego_raw.json','w') as json_file:
        json.dump(response_content, json_file, indent = 4)

    hotels = response_content.get('hotels', [])

    for index, data in enumerate(hotels):
        hotel_id = data.get('id')
        hotel_name = data.get('name')
        star_rating = data.get('star')

        room_data['ota : wego'].append({
            "ranking": ranking,
            "hId": hotel_id
            # "name": hotel_name,
            # "check_in": check_in_date,
            # "check_out": check_out_date,
            # "starRating": star_rating,  
            
        })

        ranking += 1 

        with open('ranking_data.json', 'w') as json_file:
            json.dump(room_data, json_file, indent=4)

else:
    print(response.status_code)