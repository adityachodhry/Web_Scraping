import requests
import json
from datetime import datetime

# hId = 20211
# gohId = 7760221340435780885

current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def save_goibibo_data(hId, gohId):
    
    # Make the API request
    url = f"https://voyagerx.goibibo.com/api/v2/hotels/get_hotels_static_data_v3/?id={gohId}"

    response = requests.get(url)
    if response.status_code == 200:
        response_data = response.json()

        # with open('goibibo.json', 'w') as json_file:
        #     json.dump(response_data, json_file, indent=2)

    # Extract relevant information
    rating_score = response_data[0]["gir_data"]["hotel_rating"]
    total_rating_count = response_data[0]["gir_data"]["rating_count"]
    total_reviews = response_data[0]["gir_data"]["review_count"]

    # Create a new dictionary with the extracted information
    formatted_data = {
        "hId": hId,
        "otaId": 2,
        "otaPId": gohId,
        "timestamp": current_date,
        "reputation": [
            {
                "ratingCount": float(rating_score),
                "totalRatingCount": 5,
                "totalRatings" : int(total_rating_count),
                "totalReviews": int(total_reviews)
            }
        ]
    }

    return formatted_data

#     # Save the formatted data in a JSON file
#     with open("Goibibo_Ratings", 'w') as json_file:
#         json.dump(formatted_data, json_file, indent=2)

#     print("Rating Data Extracted!")

# save_goibibo_data(hId, hotel_id)