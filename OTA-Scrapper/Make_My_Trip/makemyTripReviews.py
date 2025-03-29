import requests , json 
from datetime import datetime , timedelta 

hotel_id = "312254274337401"

hotel_reviews = []

body = {
    "filter": {
        "ota": "MMT"
    },
    "sortCriteria": {
        "sortBy": "Latest first"
    },
    "start": 0,
    "limit": 2999
}
headers  = {
            "Usr-Mcid":"121",
            "Tid":"avc",
            "Vid": "121",
            "Accept":"application/json",
            "Accept-Encoding":"gzip, deflate, br",
            "Content-Type":"application/json",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"    
            }

endpoint = f"https://mapi.makemytrip.com/clientbackend/entity/api/hotel/{hotel_id}/flyfishReviews?srcClient=DESKTOP"

response = requests.post(endpoint, headers=headers,json=body)
print(response.status_code)
if response.status_code == 200:

    response_data = response.json()
    print(response_data)

    with open("mmtReviewsData.json","w") as json_file:
        json.dump(response_data , json_file , indent=2)
    
    reviews_data = response_data['payload']['response']['MMT']

    for review in reviews_data:
        publishDate = review['publishDate']
        guestName = review['travellerName']
        rating = review['rating']
        reviewText = review['reviewText']
        roomType = review['roomType']

        if "travelType" in review:
            guestType = review['travelType']
            # print(guestType)
        else:
            guestType = "NA"
        
             
        response_details = []

        if 'responseToReview' in review:
            responses = review['responseToReview']
            for response in responses:

                responseDate = response['responseDate']
                responseText = response['responseText']

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
            "guestType":guestType,
            "responses":response_details
    
        })



with open("mmtReviews.json","w") as json_file:
        json.dump(hotel_reviews , json_file , indent=2 ,default=str)
