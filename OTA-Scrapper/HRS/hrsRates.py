import requests
import json
import datetime

def fetch_hotel_rates(hotelID):
    rates = []
    days=12

    today = datetime.datetime.now()

    for day in range(days):
        check_in_date = (today + datetime.timedelta(days=day)).strftime("%Y-%m-%d")
        check_out_date = (today + datetime.timedelta(days=day + 1)).strftime("%Y-%m-%d")

        body = {
            "hotelId": hotelID,
            "requestParameter": {
                "requestType": "ROOM",
                "dateRange": {
                    "fromDate": check_in_date,
                    "toDate": check_out_date
                },
                "offerType": "NORMAL",
                "roomRequests": [
                    {
                        "roomNumber": 1,
                        "roomType": "SINGLEROOM",
                        "occupancy": {
                            "adults": [{"extraBed": False}],
                            "children": []
                        }
                    }
                ]
            }
        }

        headers = {
            "X-Client-Id": "9c4af7c1-d620-48af-b7b4-df19480319de",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        }

        endpoint = "https://svl-sales-offer.hrs.com/pec/v2/offers/offer-basket"

        response = requests.post(endpoint, headers=headers, json=body)

        response_data = response.json()
        if response.status_code == 200:

            room_types = response_data['offers']
            for room in room_types:
                bkgDetails = {}
                bkgDetails['roomID'] = room["id"]
                bkgDetails['checkIn'] = check_in_date
                bkgDetails['checkOut'] = check_out_date
                bkgDetails['roomName'] = room['roomConfigurationTo']['roomConfiguration']['roomCategory']
                meal = room['meal']['meal']['type']

                if 'BREAKFAST' in meal and 'LUNCH' in meal and 'DINNER' in meal and '/' in meal:
                    bkgDetails['roomPlan'] = 'MAP'
                elif 'BREAKFAST' in meal and 'LUNCH' in meal and 'DINNER' in meal:
                    bkgDetails['roomPlan'] = 'AP'
                elif 'BREAKFAST' in meal:
                    bkgDetails['roomPlan'] = 'CP'
                else:
                    bkgDetails['roomPlan'] = 'EP'

                rates.append(bkgDetails)
            
            print(f'OTA : 8 | Hotel : {hotelID} | Checkin : {check_in_date} with status : {response.status_code}')

    return rates