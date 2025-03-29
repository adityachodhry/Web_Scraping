import requests
import json
from datetime import datetime, timedelta

city_code = "CTJAI"

hotel_rankings = []

# Get the current date
current_date = datetime.now().strftime('%Y-%m-%d')

# Calculate the check-out date (assuming one day stay)
check_out_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

body = {
    "deviceDetails": {
        "appVersion": "121",
        "deviceId": "121",
        "bookingDevice": "DESKTOP",
        "deviceType": "DESKTOP"
    },
    "searchCriteria": {
        "checkIn": current_date,
        "checkOut": check_out_date,
        "limit": 101,
        "roomStayCandidates": [
            {
                "rooms": 1,
                "adultCount": 2,
                "childAges": []
            }
        ],
        "countryCode": "IN",
        "cityCode": city_code,
        "locationId": city_code,
        "locationType": "city",
        "currency": "INR",
        "personalizedSearch": True,
        "nearBySearch": False
    },
    "requestDetails": {
        "visitorId": "121",
        "visitNumber": 1,
        "funnelSource": "HOTELS",
        "idContext": "B2C",
        "pageContext": "LISTING"
    },
    "imageDetails": {
        "types": [
            "professional"
        ],
        "categories": [
            {
                "type": "H",
                "count": 1,
                "height": 162,
                "width": 243,
                "imageFormat": "webp"
            }
        ]
    },
    "reviewDetails": {
        "otas": [
            "MMT"
        ],
        "tagTypes": [
            "BASE"
        ]
    },
    "expData": "{PDO:PN}"
}


headers  = {
            "Usr-Mcid":"121",
            "Tid":"avc",
            "Accept":"application/json",
            "Accept-Encoding":"gzip, deflate, br",
            "Content-Type":"application/json",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"    
            }

try:
    endpoint = f"https://mapi.makemytrip.com/clientbackend/cg/search-hotels/DESKTOP/2?cityCode={city_code}"

    response = requests.post(endpoint, headers=headers,json=body)

    if response.status_code == 200:
        response_data = response.json()

        # with open("mmtRanksData.json","w") as json_file:
        #     json.dump(response_data , json_file,indent=2)

        
        hotel_data = response_data['response']['personalizedSections']
        for data in hotel_data:
            if data['name'] == "RECOMMENDED_HOTELS":
                hotels = data['hotels']
                for hotel in hotels:
                    hotel_id = hotel['id']
                    hotel_name = hotel['name']
                    star_rating = hotel['starRating']

                    hotel_rankings.append({
                        "rank":len(hotel_rankings) + 1,
                        "id":hotel_id,
                        "name":hotel_name
                    })
    else :
        print(response.text)

except Exception as e:
    print(f"An error occurred: {e}")

final_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d"),
        "otaId": 1,
        "cityCode": "CTJAI",
        "ranking": hotel_rankings[:100]
}

with open('makeMyTripRanks.json', 'w') as json_file:
    json.dump(final_data, json_file, indent=2)