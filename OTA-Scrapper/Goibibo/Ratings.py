import requests
import json
from datetime import datetime, timedelta

rating_data = []
goId = 6292178372692755934
api_url = "https://mapi.goibibo.com/clientbackend-gi/cg/static-detail/desktop/2?language=eng&region=in&currency=INR&idContext=B2C&countryCode=IN&ck=ab8443b5-2d6e-4d93-97b8-1f9be192b7b9"

headers = {
    "Tid": "avc"
}

# Get current date
current_date = datetime.now()

# Calculate check-in and check-out dates
check_in_date = current_date.strftime("%Y-%m-%d")
check_out_date = (current_date + timedelta(days=1)).strftime("%Y-%m-%d")

body = {
    "deviceDetails": {
        "appVersion": "108.0",
        "deviceId": "94e676d0-d9e9-400d-9a97-3f2e6adf84ba",
        "deviceType": "Desktop",
        "bookingDevice": "DESKTOP"
    },
    "featureFlags": {
        "staticData": True
    },
    "requestDetails": {
        "visitorId": "94e676d0-d9e9-400d-9a97-3f2e6adf84ba",
        "visitNumber": 1,
        "funnelSource": "HOTELS",
        "idContext": "B2C",
        "pageContext": "DETAIL",
        "brand": "GI"
    },
    "requiredApis": {
        "reviewSummaryRequired": True
    },
    "reviewDetails": {
        "otas": [
            "MMT",
            "TA",
            "MANUAL",
            "OTHER",
            "EXT"
        ],
        "tagTypes": [
            "BASE",
            "WHAT_GUESTS_SAY"
        ]
    },
    "searchCriteria": {
        "vcId": "2820046943342890302",
        "giHotelId": goId,
        "checkIn": check_in_date,
        "checkOut": check_out_date,
        "roomStayCandidates": [
            {
                "adultCount": 2,
                "childAges": []
            }
        ]
    }
}

response = requests.post(api_url, json=body, headers=headers)

if response.status_code == 200:

    response_content = response.json()

    # with open('Row_Data.json', 'w') as json_file:
    #     json.dump(response_content, json_file, indent=2)

    data = response_content.get('response', {}).get('reviewSummaryGI', {}).get('giData', {})

    review_count = data.get("reviewCount")
    hotel_rating = data.get("hotelRating")

    r_data = {
        "review": review_count,
        'rating': hotel_rating
    }
    rating_data.append(r_data)

with open('ratings_and_review.json', 'w') as json_file:
    json.dump(rating_data, json_file, indent=2)
