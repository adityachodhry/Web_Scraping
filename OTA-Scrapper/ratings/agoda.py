import requests
import json
from datetime import datetime

def save_agoda_data(hId, agodahId):

    url = "https://www.agoda.com/api/cronos/property/review/HotelReviews"

    headers = {
        "Content-Type": "application/json"
    }

    body = {
        "hotelId": agodahId,
        "hotelProviderId": 332,
        "demographicId": 0,
        "pageNo": 1,
        "pageSize": 10,
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

    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        response_data = response.json()

        try:
            rating_score = response_data["combinedReview"]["score"]["score"]
            total_rating_count = response_data["combinedReview"]["score"]["reviewCount"]
            total_reviews = response_data["combinedReview"]["score"]["reviewCommentsCount"]

            formatted_data = {
                "hId": hId,
                "otaId": 4,
                "otaPId": agodahId,
                "timestamp": current_date,
                "reputation": [
                    {
                        "ratingCount": float(rating_score),
                        "totalRatingCount": 10,
                        "totalRatings": int(total_rating_count),
                        "totalReviews": int(total_reviews)
                    }
                ]
            }
            return formatted_data

        except Exception as e:
            print("Exception occurred:", str(e))
            rating_score = response_data["score"]["demographics"][0]["score"]
            total_reviews = response_data["score"]["demographics"][0]["count"]

            formatted_data = {
                "hId": hId,
                "otaId": 4,
                "timestamp": current_date,
                "reputation": [
                    {
                        "ratingCount": float(rating_score),
                        "totalRatingCount": 10,
                        "totalReviews": int(total_reviews)
                    }
                ]
            }
            return formatted_data

    # else:
    #     print("Failed to fetch Agoda ranking data.")
    #     return None

# Example usage:
# hId = 20211
# agodahId = 343493
# save_agoda_data(hId, agodahId)
