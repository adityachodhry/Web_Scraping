import requests
import json

hotelId = 624008

url = f"https://srv.wego.com/hotels/hotels/{hotelId}?locale=en&app_type=WEB_APP"

response = requests.get(url)

if response.status_code == 200:
    response_content = response.json()

    # with open('reviews.json', 'w') as json_file:
    #     json.dump(response_content, json_file, indent=4)

    hotels_data = []

    reviews = response_content['reviews']
    
    if reviews:
        first_review = reviews[0]  
        reviews = first_review.get('count')
        score = first_review.get('score')
        
        if reviews is not None and score is not None:
            rating = score / 10.0
        
    hotel_data = {
                'reviewsRating': rating,
                'reviewsCount': reviews
            }
    hotels_data.append(hotel_data)

    with open('reputation.json', 'w') as json_file:
        json.dump(hotels_data, json_file, indent=4)
        