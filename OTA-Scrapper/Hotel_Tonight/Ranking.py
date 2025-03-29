import requests, json
from datetime import datetime, timedelta

result_size = 30
city_name = 'london-gb'

start_date = datetime.now().strftime("%Y-%m-%d")

url = f"https://api.hoteltonight.com/v6/inventory?place_source=MarketCity&start_date={start_date}&num_nights=1&place_id={city_name}&latitude=21.290&longitude=81.690&room_count=1&result_size={result_size}"


response = requests.get(url)
if response.status_code == 200:
    response_content = response.json()

    hotel_list = []  

    data = response_content.get('rooms')

    rank_count = 1

    for room in data:
        hotel_info = room.get('hotel', {})  

        hotelId = hotel_info.get('id')
        hotelName = hotel_info.get('name')
        hotelPrice = room.get('customer_price_per_night')  
        review_count = hotel_info.get('review_count')

        details = {
            'rank': rank_count,
            'hId': hotelId,
            'hName': hotelName,
            'price': hotelPrice,
            'reviewCount': review_count
        }

        hotel_list.append(details) 
        rank_count += 1

    with open('Hotel_Ranking.json', 'w') as json_file:
        json.dump(hotel_list, json_file, indent=2)

    print("Ranking Data Extracted successfully!")
else:
    print("Failed to Extract Data from the API!")
