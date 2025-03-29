import requests
from datetime import datetime

def get_hotel_reviews(hotel_id):
    hotel_reviews = []

    body = {
        "filter": {
            "ota": "MMT"
        },
        "sortCriteria": {
            "sortBy": "Latest first"
        },
        "start": 0,
        "limit": 20
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
    if response.status_code == 200:

        response_data = response.json()

        try :
            reviews_data = response_data['payload']['response']['MMT']
        except :
            try :
                reviews_data = response_data['payload']['response']["EXT"]
            except :
                return []

        for review in reviews_data:
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

            response_details = []

            if 'responseToReview' in review:
                responses = review['responseToReview']
                for response in responses:
                    responseDate = datetime.strptime(response['responseDate'], "%b %d, %Y").strftime("%Y-%m-%d")
                    responseText = response['responseText']

                    response_details.append({
                        "responseDate": responseDate,
                        "responseText": responseText
                    })
            else:
                response_details = None

            hotel_reviews.append({
                "publishDate": publishDate,
                "guestName": guestName,
                "rating": rating,
                "reviewTitle" : title,
                "reviewText": reviewText,
                "roomType": roomType,
                "guestType": guestType,
                "responses": response_details
            })

    return hotel_reviews