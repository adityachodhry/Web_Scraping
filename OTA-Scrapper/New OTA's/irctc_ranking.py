import requests
import json
from datetime import datetime, timedelta


url = "https://www.hotels.irctc.co.in/tourismUser/tourism/hotel/searchhotel"

current_date = datetime.now().strftime("%Y-%m-%d")

check_in_date = current_date
check_out_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

body = {
    "id": "-2",
    "checkInDate": check_in_date,
    "checkOutDate": check_out_date, 
    "noOfRoom": "1",
    "noOfAdt": "2",
    "noOfPax": "2",
    "noOfChd": "0",
    "type": "City",
    "affilId": "",
    "name": "Pune",
    # "fullName": "Maharashtra"
}

response = requests.post(url, json=body)

ranking = []

if response.status_code == 200:
    response_content = response.json()

    with open('Row_Data.json', 'w') as json_file:
        json.dump(response_content, json_file, indent=2)
    
    data = response_content.get('data', {}).get('hotelDetailsSummary', [])
    count = 1

    for rank in data:
        hotelcode = rank.get('hotelCode')
        hotelName = rank.get('hotelName')
        rate = rank.get('hotelPrice', {}).get('basePrice')
        startRating = rank.get('starRating')
        reviewCounts = rank.get('overallRating')

        # Check if startRating and reviewCounts are available
        rating = startRating if startRating is not None else "_"
        reviews = reviewCounts if reviewCounts is not None else "_"

        # Construct details dictionary
        details = {
            'Rank': count,
            'hotelCode': hotelcode,
            # 'hotelName': hotelName,
            # 'rate': int(rate),
            # 'startRating': rating if rating != "null" else "_",
            # 'reviewCounts': reviews if reviews != "null" else "_"
        }
        ranking.append(details)
        count += 1

else:
    print("Failed to retrieve data from the API.")

# Write the processed hotel information into a JSON file
with open('Hotel_Info.json', 'w') as json_file:
    json.dump(ranking, json_file, indent=2)
