import requests
import json

url = "https://cloud.tui.com/osp/ao/ml/rooms-panel/rooms?hotelId=A0525998&locale=en-GB&market=uk&passengers=30%2C30&startDate=2024-04-27&duration=2&productId=9df30436-5876-49aa-b827-e3b7f3754517&sourcing=DYNAMIC"

response = requests.get(url)
if response.status_code == 200:
    response_content = response.json()

    with open('Row_Data.json', 'w') as json_file:
        json.dump(response_content, json_file, indent=2)

    hotel_info = []

    data = response_content.get('roomTypes', [])

    for hotel in data:
        room_name = hotel.get('roomTypeName', '')
        offers = hotel.get('offers', [])
        for offer in offers:
            price_per_person = offer.get('pricePerPerson', {})
            formatted_price = price_per_person.get('formattedPrice', '')
            

            details = {
            'hName': room_name,
            'rate': formatted_price,
        }

        hotel_info.append(details)

else:
    print("Failed to retrieve data from the API.")

with open('Hotel_Info.json', 'w') as json_file:
    json.dump(hotel_info, json_file, indent=2)
