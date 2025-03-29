import requests
import json
from datetime import datetime

def get_agoda_booking_reviews(hotel_id, page_no=1):
    agoda_reviews_data = []
    hotelId = 36202051

    body = {
        "hotelId": hotel_id,
        "hotelProviderId": 332,
        "demographicId": 0,
        "pageNo": page_no,
        "pageSize": 50,
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
        "isCrawlablePage": True,
        "paginationSize": 1
    }

    endpoint = "https://www.agoda.com/api/cronos/property/review/HotelReviews"

    try:
        response = requests.post(endpoint, json=body)
        response.raise_for_status()  

        response_data = response.json()
        # with open('agodaRaw.json','w') as json_file:
        #     json.dump(response_data, json_file, indent = 4)

        comments = response_data.get("commentList", {}).get("comments", [])

        for data in comments:
            hId = 20671
            reviewId = data.get("hotelReviewId")
            review_provider_id = data.get('providerId', None)
            review_text = data.get('reviewComments', None) or data.get('reviewPositives', None) or data.get('reviewNegatives', None)
            room_type = data.get('roomTypeName', None)
            review_title = data.get('ratingText', None)

            response_details = None
            if "responseText" in data:
                response_date = data.get('responseDateText')
                response_text = data.get('responseText')

                response_date_cleaned = response_date.replace("Responded ", "")

                # print("Response Date:", response_date) 
                # print("Response Text:", response_text)  
                if response_date_cleaned:
                    try:
                        response_date_obj = datetime.strptime(response_date_cleaned, "%B %d, %Y")
                        response_date_formatted = response_date_obj.strftime("%Y-%m-%d")
                    except ValueError:
                        response_date_formatted = None

                    if response_date_formatted:
                        response_details = {
                            "responseDate": { 
                                "$date":response_date_formatted
                                },
                            "responseText": response_text
                        }

            publish_date_str = data.get('formattedReviewDate')
            if publish_date_str:
                try:
                    hId = hId
                    publish_date = datetime.strptime(publish_date_str, "%B %d, %Y")
                    formatted_publish_date = publish_date.strftime("%Y-%m-%d")
                except ValueError:
                    formatted_publish_date = None

                if formatted_publish_date:
                    e_data = {
                        'hId' : hId,
                        'otaPId' : str(hotelId),
                        'reviewId': str(reviewId),
                        "publishDate": {
                            "$date": formatted_publish_date
                        },
                        'guestName': data.get('reviewerInfo', {}).get('displayMemberName', None),
                        'rating': data.get('rating'),
                        'reviewTitle': review_title,
                        'reviewText': review_text,
                        'roomType': room_type,
                        'guestType': data.get('reviewerInfo', {}).get('reviewGroupName', None),
                        'responses': response_details
                    }
                    if review_provider_id == 332:
                        agoda_reviews_data.append(e_data)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Agoda reviews: {e}")

    return agoda_reviews_data
