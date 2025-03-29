import requests
import json
from datetime import datetime, timedelta

today = datetime.now()
city = 'Mumbai'

room_data = {
    "timestamp": today.strftime("%Y-%m-%d %H:%M:%S"),
    'otaId' : 17,
    'cityCode' : 'Mumbai',
    "ota : Yatra": []
}
ranking = 1
page = 1
offset = 30

while ranking <= 100:

    url = f"https://hotel.yatra.com/tgapi/hotels/v1/pageSearch?source=BOOKING_ENGINE&rooms[0].id=1&city={city}&page={page}&offset={offset}"

    headers= {'X-Api-Key': 'JN9aWyj7hJ1ZrExC7Ozo',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}

    response = requests.get(url, headers= headers)

    response.status_code == 200
    response_content = response.json()
    print(response_content)

        # with open('ranking.json','w') as json_file:
        #     json.dump(response_content, json_file, indent = 4)

    data_slot = response_content.get('data',{})
    content = data_slot.get('content',{}).get('hotels',[])

    for data in content:
        hotel_id = data.get('id')
        rating = data.get('gr',{}).get('rating')
        room_data['ota : Yatra'].append({
                "hId": hotel_id,
                "ranking": ranking

        })

        ranking += 1 
    
    page += 1

with open('ranking_data.json', 'w') as json_file:
    json.dump(room_data, json_file, indent=4)




