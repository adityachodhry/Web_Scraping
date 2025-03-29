import requests
import json


rating_data = []
hotelId = "5e02d11c159c942764441694"

api_url = f"https://hotel.happyeasygo.com/api/web/room_type/reviews/{hotelId}"

response = requests.get(api_url)

if response.status_code == 200:

    response_content = response.json()

    # with open('Row_Data.json', 'w') as json_file:
    #     json.dump(response_content, json_file, indent=2)
    
    data = response_content.get('data', {})
    
    review_count = data.get("reviewCount")
    hotel_rating = data.get("reviewRating")

    r_data = {
            "review": review_count,
            'rating': hotel_rating
        }
    rating_data.append(r_data)

# Save the extracted data to a new JSON file
with open('ratings_and review.json', 'w') as json_file:
    json.dump(rating_data, json_file, indent=2)