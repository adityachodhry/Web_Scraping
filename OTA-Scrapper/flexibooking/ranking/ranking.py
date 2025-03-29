import requests
from datetime import datetime, timedelta
import json

latitude = 51.5072178
longitude =-0.1275862
num_days = 1
today = datetime.now()
room_data = {
    "timestamp": today.strftime("%Y-%m-%d %H:%M:%S"),
    "rates": []
}

ranking = 1
page = 1

check_in_date = (today + timedelta(days=num_days)).strftime("%Y/%m/%d")
check_out_date = (today + timedelta(days=num_days + 1)).strftime("%Y/%m/%d")

url = f"https://flexibookingsapi.azurewebsites.net/api/Search/SearchHotels?siteId=2&checkInDate={check_in_date}&checkInTime=14&checkOutDate={check_out_date}&checkOutTime=11&latitude={latitude}&longitude={longitude}&distance=20000&pagesize=20&pagenumber={page}"


response = requests.get(url)
if response.status_code == 200:

    response_content = response.json()
    # with open('ranking_raw.json','w') as json_file:
    #     json.dump(response_content, json_file, indent = 4)
    
    data_slot = response_content['SearchResults']
    for data in data_slot:
        id = data.get('Hotel').get('Id')
        name = data.get('Hotel').get("Name")
        starRating = data.get('Hotel').get('DescriptionStars')
        
        room_data['rates'].append({
                "hId": id,
                'starRating' : starRating,
                'ranking' : ranking
                # "name": name,   
            })
        
        ranking += 1 
    
    page += 1

    with open('ranking_data.json', 'w') as json_file:
        json.dump(room_data, json_file, indent=4)

else:
    print(response.status_code)