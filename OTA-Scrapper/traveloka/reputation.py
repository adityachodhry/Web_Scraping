import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime, timedelta

searchId = 1798397778562408282
num_days = 1
today = datetime.now()
start_time = time.time()

for day in range(num_days):
    check_in_date = (today + timedelta(days=day)).strftime("%Y.%m.%d")
    check_out_date = (today + timedelta(days=day + 1)).strftime("%Y.%m.%d")

    url = f"https://www.traveloka.com/en-en/hotel/detail?spec=08-05-2024.09-05-2024.1.1.HOTEL.1000000242768.Shangri-La%20Eros%2C%20New%20Delhi.1&prevSearchId={searchId}"

    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        hotels_data = []

        script_tag = soup.find("script", type="application/ld+json")

        if script_tag:
            script_content = script_tag.string

            if script_content:
                json_data = json.loads(script_content)
                rating = json_data['aggregateRating']['ratingValue']
                reviews = json_data['aggregateRating']['reviewCount']

                hotel_data = {
                    'reviewsRating': rating,
                    'reviewsCount': reviews
                }
                hotels_data.append(hotel_data)
    else:
        print(f"Failed to retrieve content from {url}")

with open('reputation.json', 'w') as json_file:
    json.dump(hotels_data, json_file, indent=4)
