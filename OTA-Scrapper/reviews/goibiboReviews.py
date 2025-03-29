import requests
import json
from datetime import datetime

def get_goibibo_reviews(hotel_id, limit=50):
    goibibo_hotel_reviews = []
    hotelId = 3482996341396368975
    offset = 0

    while True:
        url = f"https://ugcx.goibibo.com/api/HotelReviews/forMobileV4/{hotel_id}?offset={offset}&limit={limit}"

        headers = {
            "User-Agent": "Your User Agent Here"
        }
        response = requests.get(url, headers=headers)
        response_content = response.json()

        data_slot = response_content.get('reviews', [])

        if not data_slot:
            break

        for data in data_slot:
            reviewId = data.get('id')
            publishDate = data.get('submittedAt')
            guestName = f"{data.get('firstName')} {data.get('lastName')}"
            rating = data.get('totalRating')
            reviewTitle = None
            reviewText = data.get('reviewContent')
            roomType = data.get('roomInfo', {}).get('name')
            guestType = None
            response = data.get('hotelReply')
            responseText = response.get('response') if response else None
            responseDate = response.get('createdAt') if response else None

            review_data = {
                "hId": 20671,
                'otaPId' : str(hotelId),
                "reviewId": str(reviewId),
                "publishDate": {
                    "$date": publishDate
                },
                "guestName": guestName,
                "rating": rating,
                "reviewTitle": reviewTitle,
                "reviewText": reviewText,
                "roomType": roomType,
                "guestType": guestType,
                "responses": {
                    "responseDate": {
                        "$date": responseDate
                    },
                    "responseText": responseText
                } if response else None
            }

            goibibo_hotel_reviews.append(review_data)

        offset += limit

    return goibibo_hotel_reviews

