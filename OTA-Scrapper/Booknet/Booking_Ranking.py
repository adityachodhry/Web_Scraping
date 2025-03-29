import requests
from bs4 import BeautifulSoup
import json

city_name = 'Udaipur'

url = f"https://www.booked.net/hotels/india/{city_name}-4?"

response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    ld_json_scripts = soup.find_all('script', type='application/ld+json')
    
    extracted_data = []
    rank = 1  

    for script in ld_json_scripts:
        json_content = json.loads(script.string)  

        name = json_content.get('name', None)
        starRating = json_content.get('starRating', None)
        ratingValue = json_content.get('aggregateRating', {}).get('ratingValue', None)
        ratingCount = json_content.get('aggregateRating', {}).get('ratingCount', None)

        hName = name if name is not None else "_"
        Star = starRating if starRating is not None else "_"
        rating = ratingValue if ratingValue is not None else "_"
        reviews = ratingCount if ratingCount is not None else "_"
        
        hid = None

        data = {
            'Rank': rank,
            'hid': hid if hid is not None else "_",
            # 'name': hName,
            # 'starRating': Star,
            # 'ratingValue': rating,
            # 'ratingCount': reviews
        }

        extracted_data.append(data)
        rank += 1  

    # Find all div elements with class "h-list__hotel-card"
    hotel_cards = soup.find_all('div', class_='h-list__hotel-card')

    # Extract the 'hid' attribute from each hotel card and update the corresponding data dictionary
    for i, card in enumerate(hotel_cards):
        hid = card.get('data-hid')
        extracted_data[i]['hid'] = hid if hid is not None else "_"

    # Save the extracted data to a JSON file
    with open('Hotel_Info.json', 'w') as json_file:
        json.dump(extracted_data, json_file, indent=2)
