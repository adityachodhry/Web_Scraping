import requests
import json
from datetime import datetime, timedelta

current_date = datetime.now().strftime("%Y-%m-%d")

check_in_date = current_date
check_out_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

url = f"https://in.via.com/apiv2/hotels/search?Room1Adults=2&Room1Children=0&residence=null&nationality=137&flowType=NODE&ajax=true&jsonData=false&action1=HOTELSEARCHRESULT&regionId=5C278&checkInDate={check_in_date}&checkOutDate={check_out_date}&id=5C278&checkIn={check_in_date}&checkOut={check_out_date}&rooms=1&guest%5B%5D=2-0&guest%5B%5D=null&guest%5B%5D=137"

response = requests.get(url)
if response.status_code == 200:
    response_content = response.json()

    with open('Row_Data.json', 'w') as json_file:
        json.dump(response_content, json_file, indent=2)

hotel_info = []

data = response_content.get('HotelList', {})

# Sort hotels based on star rating
sorted_hotels = sorted(data, key=lambda x: x.get('StarRating', 0), reverse=True)

# Assign ranks
rank = 1

for hotel in sorted_hotels:
    hId = hotel.get('HotelId')
    hName = hotel.get('HotelName')
    starRating = hotel.get('StarRating')
    ratingScore = hotel.get('TripAdvisorData', {}).get('RATING_SCORE')
    reviewsScore = hotel.get('TripAdvisorData', {}).get('NUM_REVIEWS')

    # Check if starRating is less than or equal to 5
    if starRating <= 5:
        # Check if the values are available
        if ratingScore is not None:
            rating = ratingScore
        else:
            rating = "_"

        if reviewsScore is not None:
            reviews = reviewsScore
        else:
            reviews = "_"

        details = {
            'Rank': rank,
            'hId': hId,
            'hName': hName,
            'starRating': starRating,
            'ratingScore': rating if rating != "null" else "_",
            'reviewsScore': reviews if reviews != "null" else "_"
        }

        hotel_info.append(details)
        rank += 1

with open('Hotel_Info.json', 'w') as json_file:
    json.dump(hotel_info, json_file, indent=2)
