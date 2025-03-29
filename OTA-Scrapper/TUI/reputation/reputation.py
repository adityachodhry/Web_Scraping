import requests
import json

hotelName = "Rosen Inn International"
hotelId = 'A0508197'

url = f"https://cloud.tui.com/osp/ao/ml/love-at-first-sight/hotels/{hotelId}?market=uk&locale=en-GB&sourceSystem=TRIPS"

response = requests.get(url)

if response.status_code == 200:
    response_content = response.json()

    # with open('reviews.json', 'w') as json_file:
    #     json.dump(response_content, json_file, indent=4)

    hotels_data = []

    data_slot = response_content.get('tripAdvisor',{})
    reviews = data_slot.get('numberOfReviews')
    rating = data_slot.get('rating')

    hotel_data = {
                'reviewsRating': rating,
                'reviewsCount': reviews
            }
    hotels_data.append(hotel_data)

    with open('reputation.json', 'w') as json_file:
        json.dump(hotels_data, json_file, indent=4)


