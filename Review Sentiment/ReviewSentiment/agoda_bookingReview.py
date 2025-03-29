import requests
import json
from datetime import datetime

def get_agoda_booking_reviews(hotel_id, page_no=1):
    agoda_reviews_data = []
    booking_reviews_data = []

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

    response = requests.post(endpoint, json=body)

    if response.status_code == 200:
        response_data = response.json()
        with open('temp.json','w') as json_file :
            json.dump(response_data,json_file)

        reviews_data = response_data["commentList"]["comments"]

        for data in reviews_data:
            review_provider_id = data.get('providerId', 'NA')

            review_comments = data.get('reviewComments','NA')
            review_positive = data.get('reviewPositives', 'NA')
            review_negative = data.get('reviewNegatives', 'NA')

            if len(review_positive) > len(review_negative) and len(review_positive) > len(review_comments):
                review_text = review_positive
            elif len(review_negative) > len(review_positive) and len(review_positive) > len(review_comments):
                review_text = review_negative
            else :
                review_text = review_comments


            room_type = data.get('roomTypeName', 'NA')
            review_title = data.get('ratingText','NA')

            if review_provider_id == 3038:
                response_details = get_response_details(data)
                save_review_data(booking_reviews_data, data, room_type, review_text,review_title, response_details)
            elif review_provider_id == 332:
                response_details = get_response_details(data)
                save_review_data(agoda_reviews_data, data, room_type, review_text,review_title, response_details)

    else:
        print(f"Error: {response.status_code}")

    return agoda_reviews_data

def get_response_details(data):
    response_details = []

    if "responseText" in data:
        response_date = data.get('responseDateText')
        response_text = data.get('responseText')

        date_parts = response_date.split(" ")[1:]
        date_parts[1] = date_parts[1].replace(',', '')
        date_string = ' '.join(date_parts)

        response_date_obj = datetime.strptime(date_string, "%B %d %Y")
        response_date_formatted = response_date_obj.strftime("%Y-%m-%d")

        response_details.append({
            "responseDate": response_date_formatted,
            "responseText": response_text
        })

    return response_details if response_details else None

def save_review_data(reviews_data, data, room_type, review_text,review_title, response_details):
    publish_date_str = data.get('formattedReviewDate')
    publish_date = datetime.strptime(publish_date_str, "%B %d, %Y")
    formatted_publish_date = publish_date.strftime("%Y-%m-%d")

    e_data = {
        'publishDate': formatted_publish_date,
        'guestName' : data.get('reviewerInfo', {}).get('displayMemberName'),
        'rating': data.get('rating'),
        'reviewTitle' : review_title,
        'reviewText': review_text,
        'roomType': room_type,
        'guestType': data.get('reviewerInfo', {}).get('reviewGroupName'),
        'response': response_details
    }
    reviews_data.append(e_data)