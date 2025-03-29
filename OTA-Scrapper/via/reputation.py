import requests
import json

hotelName = "Hotel Sahara Star"
hotelId = 22468

url = f"https://in.via.com/apiv2/hotels/search?regionId=9H{hotelId}"

response = requests.get(url)

if response.status_code == 200:
    response_content = response.json()

    # with open('reviews.json','w') as json_file:
    #     json.dump(response_content, json_file, indent = 4)

    data_slot = response_content.get('HotelList', [])

    # Create a list to store hotel data
    hotels_data = []

    for hotel in data_slot:
        trip_data = hotel.get('TripAdvisorData', {})
        if trip_data:
            rating = trip_data.get('RATING_SCORE')
            reviews = trip_data.get('NUM_REVIEWS')

            hotel_data = {
                'reviewsRating': rating,
                'reviewsCount': reviews
            }

            hotels_data.append(hotel_data)

with open('reputation.json', 'w') as json_file:
    json.dump(hotels_data, json_file, indent=4)

