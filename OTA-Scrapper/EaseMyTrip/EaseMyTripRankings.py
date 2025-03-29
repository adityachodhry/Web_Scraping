import requests
import json
import datetime

def get_EMT_rankings(city_name):
    ranks = []
    today = datetime.datetime.now()
    check_in_date = (today + datetime.timedelta(days=0)).strftime("%Y-%m-%d")
    check_out_date = (today + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    
    endpoint = "https://hotelservice.easemytrip.com/api/HotelService/GetStatic"

    for page_number in range(1, 5):
       
        body = {
            "PageNo": page_number,
            "CheckInDate": check_in_date,
            "CheckOut": check_out_date,
            "CityName": city_name
        }

        response = requests.post(endpoint, json=body)

        if response.status_code == 200:
            
            response_content = response.json()

            if "htllist" in response_content and isinstance(response_content["htllist"], list):
                
                for hotel in response_content["htllist"]:
                    ranks.append({
                        "rank": len(ranks) + 1,  
                        "hotelCode": hotel.get("ecid"),
                        "hotelName": hotel.get("nm"),
                        "starCategory": hotel.get("rat"),
                        "catgry": hotel.get("catgry"),
                        "rating": hotel.get("tr"),
                    })
                    
                    print(f'OTA : 6 | Hotel : {city_name} | Checkin : {check_in_date} with status : {response.status_code}')
            else:
                print(f"Error: 'htllist' key not found in the response for page {page_number}")

        else:
            print(f"Error: {response.status_code}")

    
    return ranks

city_name = "Indore"
hotel_rankings = get_EMT_rankings(city_name)

with open('EaseMyTripRankings.json', 'w') as json_file:
    json.dump(hotel_rankings, json_file, indent=2)
