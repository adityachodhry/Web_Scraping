import requests
import json


rating_data = []
hotelId = 73238

api_url = f"https://svl-sales-rating.hrs.com/pec/v1/ratings/web/extended?hotelIds={hotelId}&options.personGroup=ALLHRS&options.sortCriterion.language=en&options.sortCriterion.descending=true"

headers = {
    "X-Client-Id":"9c4af7c1-d620-48af-b7b4-df19480319de",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
response = requests.get(api_url, headers=headers)

if response.status_code == 200:
  
    response_content = response.json()

    with open('Row_Data.json', 'w') as json_file:
        json.dump(response_content, json_file, indent=2)
    
    data = response_content[0].get('extAvgRatings', {}).get('averageRating', {})

    review_count = data.get("totalNumberOfRatings")
    hotel_rating = data.get("totalAverage")

    r_data = {
            "review": review_count,
            'rating': hotel_rating
        }
    rating_data.append(r_data)

# Save the extracted data to a new JSON file
with open('ratings_and review.json', 'w') as json_file:
    json.dump(rating_data, json_file, indent=2)






# params = {
#     "hotelIds":"393",
#     "options.personGroup":"ALLHRS",
#     "options.sortCriterion.language":"en",
#     "options.sortCriterion.descending":"true"
# }