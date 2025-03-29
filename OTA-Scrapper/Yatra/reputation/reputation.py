import requests
import json
from datetime import datetime, timedelta

hotelName = "Roseate House"

today = datetime.now()

url = "https://hotel.yatra.com/tgapi/hotels/v1/hotels/00078943"
params = {
    'checkInDate': '15/05/2024',
    'checkOutDate': '16/05/2024',
    'city.name': 'New Delhi',
    'city.code': 'New Delhi',
    'propertySource': 'TGU',
    'country.name': 'India',
    'country.code': 'IND',
    'hotelId': '00078943',
    'rooms[0].id': '1'
}

headers = {
    'X-Api-Key': 'JN9aWyj7hJ1ZrExC7Ozo',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

response = requests.get(url, params=params, headers=headers)

if response.status_code == 200:
    response_content = response.json()

    # print(response_content)
    with open('reviews.json', 'w') as json_file:
        json.dump(response_content, json_file, indent=4)

    hotels_data = []

    data_slot = response_content.get('data', {}).get('content', {}).get('googleReviewInfo', {})

    if data_slot:
        reviews = data_slot.get('noOfReviews')
        rating = data_slot.get('averageRating')

        hotel_data = {
                'reviewsRating': rating,
                'reviewsCount': reviews
            }
        hotels_data.append(hotel_data)

    with open('reputation.json', 'w') as json_file:
        json.dump(hotels_data, json_file, indent=4)
        
