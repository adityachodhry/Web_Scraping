import requests
import json
from datetime import datetime, timedelta

num_days = 1
today = datetime.now()

room_data = {
    "timestamp": today.strftime("%Y-%m-%d %H:%M:%S"),
    'otaId' : 16,
    'city' : 'London',
    "ota : TUI": []
}
ranking = 1
page = 0

for day in range(num_days):
    check_in_date = (today + timedelta(days=day)).strftime("%Y-%m-%d")
    check_out_date = (today + timedelta(days=day + 1)).strftime("%Y-%m-%d")

    url = f"https://cloud.tui.com/osp/ao/ml/search/search/real/?market=uk&locale=en-GB&startDate={check_in_date}&endDate={check_out_date}&numberOfNights=1&passengers=30%2C30&filters=&geopolygon=51.67234324898703%2C51.38494012429096%2C0.1482710335611201%2C-0.3514683384218145&page=1&googleLocationId=ChIJdd4hrwug2EcRmSrV3Vo6llI&recommendedSortingVariant="

    response = requests.get(url)

    if response.status_code == 200:
        response_content = response.json()
        data_slots = response_content['results']

        for data_slot in data_slots:
            hotel_id = data_slot.get('hotelId')
            rating = data_slot.get('hotel', {}).get("rating")

            room_data['ota : TUI'].append({
                "hId": hotel_id,
                "rating": rating,
                "ranking" : ranking

            
        })

            ranking += 1 
            
        page += 1 

with open('ranking_data.json', 'w') as json_file:
    json.dump(room_data, json_file, indent=4)    

# with open('ranking_data.json', 'w') as json_file:
#     json.dump(room_data, json_file, indent=4)
