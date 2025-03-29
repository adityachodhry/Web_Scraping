import requests
import json

hotelName = "Roseate House"

url = "https://hotels.travelguru.com/tgapi/hotels/v1/hotels/00187138?city.name=Udaipur&city.code=Udaipur&propertySource=TGU&hotelId=00187138&tenant=TGB2C&rooms[0].id=1&rooms[0].noOfAdults=1&_rn=e62"

headers = { 'X-Api-Key':'RcKU4ktJuNBFV1BknPWT',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36' }

response = requests.get(url,headers=headers)

if response.status_code == 200:
    response_content = response.json()

    # print(response_content)
    # with open('reviews.json', 'w') as json_file:
    #     json.dump(response_content, json_file, indent=4)

    hotels_data = []

    data_slot = response_content.get('data',{}).get('content',{}).get('googleReviewInfo',{})
    reviews = data_slot.get('noOfReviews')
    rating = data_slot.get('averageRating')
    
    hotel_data = {
                'reviewsRating': rating,
                'reviewsCount': reviews
            }
    hotels_data.append(hotel_data)

    with open('reputation.json', 'w') as json_file:
        json.dump(hotels_data, json_file, indent=4)
        
