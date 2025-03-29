import requests
import json
import datetime

def fetch_cleartrip_hotel_rankings(city_name, state_name, country_code, cityId):
    today = datetime.datetime.now()
    check_in_date = datetime.datetime.now().strftime("%d/%m/%Y")
    check_out_date = (today + datetime.timedelta(days=1)).strftime("%d/%m/%Y")

    # API endpoint
    endpoint = "https://www.cleartrip.com/hotel/orchestrator/v2/search"

    # Request headers
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br'
    }

    hotel_rankings = []

    # Request body
    body = {
        "useCaseContext": "DESKTOP_SRP_PAGE",
        "city": city_name,
        "state": state_name,
        "country": country_code,
        "checkInDate": check_in_date,
        "checkOutDate": check_out_date,
        "pageNo": 0,
        "pageSize": 120,
        "roomAllocations": [
            {
                "adults": {
                    "count": 2,
                    "metadata": []
                },
                "children": {
                    "count": 0,
                    "metadata": []
                }
            }
        ],
        "cityId": cityId,
        "localityId": None,
        "locality": None,
        "sortAndFilters": {
            "sortBy": {
                "key": "recommended",
                "metadata": None,
                "order": "asc"
            }
        },
        "version": "V1"
    }

    try:
        # Make the POST request
        response = requests.post(endpoint, headers=headers, json=body)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            response_content = response.json()

            slots_data = response_content['response']['slotsData']

            hotel_count = None

            for slot in slots_data:
                if 'hotelCount' in slot['slotData']['data']:
                    hotel_count = slot['slotData']['data']['hotelCount']
                    break

            for slot in slots_data:
                if slot['slotData']['type'] == 'HOTEL_CARD_LIST':
                    hotelCards = slot['slotData']['data']['hotelCardList']
                    for card in hotelCards:
                        ranks = {}
                        eventData = card['ravenTracking']['eventData']
                        ranks['rank'] = eventData['h_hotel_rank']
                        ranks['otaPId'] = eventData['h_hotel_id']
                        ranks['hotelName'] = eventData['h_hotel_name']
                        ranks['starCategory'] = eventData['h_star_category']
                        ranks['userRating'] = eventData['h_user_rating']
                        ranks['totalAmount'] = eventData['h_total_amount']

                        hotel_rankings.append(ranks)

            return hotel_count, hotel_rankings[:100]

        else:
            print("Error: Request failed with status code", response.status_code)
            return None, []

    except Exception as e:
        print("Error occurred:", str(e))
        return None, []

# Example usage:
# hotel_count, cleartrip_ranking = fetch_cleartrip_hotel_rankings("Indore", "Madhya Pradesh", "IN", "33923")
