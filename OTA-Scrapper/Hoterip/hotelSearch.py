import requests
import json

hotelName = "ayodya resort bali"

url = f"https://api.hoterip.com/api/v1/hotels/locations/search?q={hotelName}"

response = requests.get(url)

if response.status_code == 200:
    response_content = response.json()
    with open('hotelDetails.json','w') as json_file:
        json.dump(response_content, json_file, indent = 4)
    
    hotels_data = []
    hotels = response_content.get('data_groups', {}).get('hotels', [])
    
    if hotels: 
        first_hotel = hotels[0]  
        
        hId = first_hotel.get('url_segment')
        hotelName = first_hotel.get('label')
        cityName = first_hotel.get('city_name')
        cityCode = first_hotel.get('city_id')
        countryCode = first_hotel.get('country_id')
        
        hotel_data = {
            'hId': hId,
            # 'hotelName': hotelName,
            'location': cityName,
            'cityCode': cityCode,
            'countryCode': countryCode
        }
        hotels_data.append(hotel_data)

        with open('hotelSearch.json', 'w') as json_file:
            json.dump(hotels_data, json_file, indent=4)
