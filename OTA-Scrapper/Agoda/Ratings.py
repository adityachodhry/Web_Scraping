import requests
import json
from datetime import datetime

rating_data = []
hotelId = 247799

api_url = "https://www.agoda.com/api/cronos/property/review/HotelReviews"

body = {
    "hotelId": hotelId,
    "hotelProviderId": 3038,
    "demographicId": 0,
    "pageNo": 2,
    "pageSize": 100,
    "sorting": 1,
    "reviewProviderIds": [
        332,
        3038,
        27901,
        28999,
        29100,
        27999,
        27980,
        27989,
        29014
    ],
    "isReviewPage": False,
    "isCrawlablePage": False,
    "paginationSize": 1
}
response = requests.post(api_url, json = body)

if response.status_code == 200:

    response_content = response.json()

    with open('Row_Data.json', 'w') as json_file:
        json.dump(response_content, json_file, indent=2)
    
    data = response_content.get('combinedReview', {}).get('score',{})

    review_count = data["reviewCount"]
    hotel_rating = data["score"]

    r_data = {
            "review": review_count,
            'rating': hotel_rating
        }
    rating_data.append(r_data)

with open('Agoda_Hotels_Reviews_Data.json', 'w') as json_file:
    json.dump(rating_data, json_file, indent=2)