import requests
from datetime import datetime
import json

def get_mmt_hotel_reviews(hotel_id):
    mmt_hotel_reviews = []
    hotelId = 201909021327101502

    body = {
        "filter": {
            "ota": "MMT"
        },
        "sortCriteria": {
            "sortBy": "Latest first"
        },
        "start": 0,
        "limit": 200
    }

    headers = {
        "Usr-Mcid": "121",
        "Tid": "avc",
        "Vid": "121",
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    endpoint = f"https://mapi.makemytrip.com/clientbackend/entity/api/hotel/{hotel_id}/flyfishReviews?srcClient=DESKTOP"

    response = requests.post(endpoint, headers=headers, json=body)
    # print(response.text)
    if response.status_code == 200:

        response_data = response.json()
        

        try :
            reviews_data = response_data['payload']['response']['MMT']
        except :
            try :
                reviews_data = response_data['payload']['response']["EXT"]
            except :
                return mmt_hotel_reviews

        for review in reviews_data:
            reviewId = review['id']
            publishDate = datetime.strptime(review['publishDate'], "%b %d, %Y").strftime("%Y-%m-%d")
            guestName = review['travellerName']
            rating = review['rating']
            title = review['title']
            reviewText = review['reviewText']
            roomType = review['roomType']

            if "travelType" in review:
                guestType = review['travelType']
            else:
                guestType = None

            response_details = None  

            if 'responseToReview' in review:
                responses = review['responseToReview']
                for response in responses:
                    responseDate = datetime.strptime(response['responseDate'], "%b %d, %Y").strftime("%Y-%m-%d")
                    responseText = response['responseText']

                    response_details = {
                        "responseDate": {
                            "$date":responseDate
                        },
                        "responseText": responseText
                    }

            mmt_hotel_reviews.append({
                'hId' : 20671,
                'otaPId' : str(hotelId),
                "reviewId" : str(reviewId),
                "publishDate": {
                    "$date": publishDate
                },
                "guestName": guestName,
                "rating": rating,
                "reviewTitle" : title,
                "reviewText": reviewText,
                "roomType": roomType,
                "guestType": guestType,
                "responses": response_details  
            })
    return mmt_hotel_reviews