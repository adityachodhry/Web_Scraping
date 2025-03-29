import requests
import json
from datetime import datetime

hotel_id = 1069880228104738794
offset = 0
hotel_reviews = []

endpoint = "https://ugcx.goibibo.com/api/HotelReviews/forMobileV4/1979804176894827166?offset=0&limit=50"

response = requests.get(endpoint)

if response.status_code == 200:
    response_data = response.json()
    

    reviews = response_data['reviews']

    for review in reviews:
        reviewerId = review['reviewerId']
        reviewText = review['reviewContent']
        roomType = review['roomInfo']['name']
        rating = review['totalRating']
        guestName = review['firstName']
        publishDate = datetime.strptime(review['submittedAt'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")

        response_details = []
        if 'hotelReply' in review:
            responseDate = datetime.strptime(review['hotelReply']['createdAt'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")
            responseText = review['hotelReply']['response']

            response_details.append({
                    "responseDate":responseDate,
                    "responseText":responseText
            })
        else:
            response_details = "null"
        
        hotel_reviews.append({
            "publishDate" : publishDate,
            "guestName" : guestName,
            "rating" : rating,
            "reviewText" : reviewText,
            "roomType":roomType,
            "responses":response_details
        })
             
             
else:
    print(f"Error: {response.status_code}")
    
with open("goibiboReviews.json","w") as json_file:
        json.dump(hotel_reviews , json_file , indent=2 ,default=str)
