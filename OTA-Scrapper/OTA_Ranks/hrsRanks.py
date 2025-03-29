import requests
import json
from datetime import datetime, timedelta

def get_HRS_rankings(cityName, locationID):
    ranks = []

    current_date = datetime.now().strftime('%Y-%m-%d')

    # Calculate the check-out date (assuming one day stay)
    check_out_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

    body = {
        "requestParameter": {
            "requestType": "ROOM",
            "dateRange": {
                "fromDate": current_date,
                "toDate": check_out_date
            },
            "offerType": "NORMAL",
            "roomRequests": [
                {
                    "roomNumber": 1,
                    "roomType": "SINGLEROOM",
                    "occupancy": {
                        "adults": [
                            {
                                "extraBed": False
                            }
                        ],
                        "children": []
                    }
                }
            ]
        },
        "findParameter": {
            "matchGroup": "CITY",
            "matchType": "LOCATION",
            "locationId": locationID
        },
        "recommendationParameter": {
            "distributionChannel": "PRIVATE_WEB",
            "btc": {}
        },
        "statusFilterType": "BOOKABLE",
        "skipHotelsIfNoValidOffer": True
    }

    headers = {
        "X-Client-Id": "9c4af7c1-d620-48af-b7b4-df19480319de",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }

    try:
        endpoint = "https://svl-sales-hotelsearch.hrs.com/pec/v2/hotel-search/hotels"
        response = requests.post(endpoint, headers=headers, json=body)

        if response.status_code == 200:
            response_data = response.json()

            # with open('HRS_Row.json', 'w') as file:
            #     json.dump(response_data, file)

            hotel_list = response_data['hotels']

            for hotel in hotel_list:
                hotels = {}
                hotels['rank'] = len(ranks) + 1
                hotels['otaPId'] = str(hotel['hotelData']['hotelId'])
                hotels['Name'] = hotel['hotelData']['hotelName']
                hotels['Rating'] = hotel['hotelData']['hotelCategory']['hrsStars']
                # hotels['location'] = hotel['hotelData']['districtName']
                hotels['Location'] = hotel['hotelData']['cityName']

                hotels['ReviewSummary'] = {
                            "RatingScore": hotel['hotelData']['averageRating']['ratings']['ALLHRS'],
                            "RatingCount": hotel['hotelData']['averageRating']['numberOfRatings']['ALLHRS'],  # Placeholder for rating count
                            # "ReviewCount": eventData['h_total_amount']  # Placeholder for review count
                        }

                ranks.append(hotels)

                print(f'OTA : 8 | Hotel : {cityName} | Checkin : {current_date} with status : {response.status_code}')

        else:
            print(response.status_code)
            print(response.text)

    except Exception as e:
        print(f"An error occurred: {e}")
    
    return ranks

    # final_data = {
    #     "timestamp": datetime.now().strftime("%Y-%m-%d"),
    #     "otaId": 8,
    #     "cityCode": "CTJAI",
    #     "ranking": ranks[:100]
    # }

#     with open(f'{cityName}_hrs_ranks_{datetime.now().strftime("%Y%m%d")}.json', 'w') as json_file:
#         json.dump(final_data, json_file, indent=4)

# # Example usage:
# cityName = "Berlin"
# locationID = 55133
# get_HRS_rankings(cityName, locationID)
