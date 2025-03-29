import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import time

start_time = time.time()
num_days = 1
today = datetime.now()

room_data = {
    "timestamp": today.strftime("%Y-%m-%d %H:%M:%S"),
    'otaId': 18,
    'city': 'Turkey',
    "ota : odamax": []
}
ranking = 1

page = 1
limit = 20  

while ranking <= 100:  
    
    check_in_date = (today + timedelta(days=num_days - 1)).strftime("%Y.%m.%d")
    check_out_date = (today + timedelta(days=num_days)).strftime("%Y.%m.%d")

    url = f"https://www.odamax.com/hotel-search-load-more?hotelUrl=aegean-region-turkey-otelleri-743&check_in={check_in_date}&check_out={check_out_date}&room=1&adult_1=2&minPrice=0&maxPrice=0&loadMore=true&sortType=popular&sortDirection=desc&limit={limit}&page={page}&searchId="

    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # with open("ranking_raw.html", "w", encoding="utf-8")as html_file:
        #     html_file.write(html_content)

        hotels = soup.find_all("div", class_="col-md-12 hotel-offer")

        display_price = soup.find_all('div', class_="col-md-12 new-price")

        for hotel, price in zip(hotels, display_price):
            if ranking > 100:
                break 

            hotelName = hotel.get("data-name")
            HId = hotel.get('data-hotel-id')
            starRating = hotel.get('data-star')

            # price = price.get('data-price')
            # currency = price.get('data-currency')

            room_data['ota : odamax'].append({
                # "hotelName": hotelName,
                "hId": HId,
                "ranking": ranking,
                "starRating": starRating,
                # "price": f"{price} {currency}"
            })

            ranking += 1

        page += 1
    else:
        print(f"Request failed with status code: {response.status_code}")
        break


# Save room_data to a JSON file
with open('ranking_data.json', 'w') as json_file:
    json.dump(room_data, json_file, indent=4)

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")
