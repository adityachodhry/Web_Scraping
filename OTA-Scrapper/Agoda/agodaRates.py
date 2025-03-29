import requests
import json
import sys
import datetime

# if len(sys.argv) != 4:
#     print("Usage: python script.py <hotel_id> <hotelName> <rHotelId>")
#     sys.exit(1)

# # Extract hotel ID and VCID from command-line arguments
# hotelId = int(sys.argv[1])
# hotelName = sys.argv[2]
# rhotelId = sys.argv[3]

hotelId = '411363'
hotelName = 'Hotel Shiva Continental'

rates = []
num_days = 90

today = datetime.datetime.now()
for day in range(num_days):

    check_in_date = (today + datetime.timedelta(days=day)).strftime("%Y-%m-%d")
    check_out_date = (today + datetime.timedelta(days=day + 1)).strftime("%Y-%m-%d")
    body = {
        "SearchType": 4,
        "ObjectID": hotelId,
        "CheckIn": f"{check_in_date}",
        "Origin": "IN",
        "LengthOfStay": 1,
        "Adults": 2,
        "Children": 0,
        "Rooms": 1,
        "IsEnableAPS": True,
        "RateplanIDs": [],
        "PlatformID": 0,
        "CurrencyCode": "INR",
        "ChildAgesStr": None,
        "ConnectedTrip": False,
        "HashId": "",
        "FlightSearchCriteria": {
            "CabinType": 4,
            "IsIncreaseMaximumFlightsPassenger": True
        },
        "PackageToken": None,
        "SessionId": "abc",
        "multiHotelNextCriteria": None,
        "IsDayUseFunnel": False,
        "PriceView": 1,
        "IsWysiwyp": True,
        "PollTimes": 1
    }

    headers = {
        'Cr-Currency-Code': 'INR',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }

    endpoint = "https://www.agoda.com/api/cronos/property/BelowFoldParams/RoomGridData"

    response = requests.post(endpoint, headers=headers, json=body)

    if response.status_code == 200:
        response_data = response.json()

        masterRooms = response_data['masterRooms']
        for masterroom in masterRooms:
            roomID = masterroom['id']
            checkIn = check_in_date
            checkOut = check_out_date
            roomName = masterroom['name']

            has_breakfast = False
            has_dinner = False
            has_lunch = False

            rooms = masterroom['rooms']
            for room in rooms:
                benefits = room['benefits']
                price = room['pricing']['displayPrice']

                for benefit in benefits:
                    meal = benefit['title']
                    if 'Breakfast' in meal:
                        has_breakfast = True
                    if 'Lunch' in meal:
                        has_lunch = True
                    if 'Dinner' in meal:
                        has_dinner = True

                try :
                    capacity_text = room['roomChildAndExtraBedPolicyViewModel']['capacityText']
                    
                    if 'Max 2 adults' in capacity_text:
                        if has_breakfast and (has_dinner and has_lunch):
                            room_plan = "AP"
                        elif has_breakfast and not has_dinner and has_lunch:
                            room_plan = "MAP"
                        elif has_breakfast and has_dinner and not has_lunch:
                            room_plan = "MAP"
                        elif has_breakfast and not has_dinner and not has_lunch:
                            room_plan = "CP"
                        else:
                            room_plan = "EP"

                            # Output the result
                        # print("roomPlan:", room_plan)

                        bkgDetails = {
                            "roomID": roomID,
                            "checkIn": check_in_date,
                            "checkOut": check_out_date,
                            "roomName": roomName,
                            "roomPlan": room_plan,
                            "price": price,
                        }
                        rates.append(bkgDetails)
                except :
                    print("Occupancy Not Matched")
                    pass
                else:
                    pass
                               
    print(f"OTA : 4 | Hotel : {hotelName} | Checkin: {check_in_date}")

final_data = {
    'hId': int(float(hotelId)),
    'otaId': 4,
    'otaPId': str(hotelId),
    'timestamp': datetime.datetime.now().strftime("%Y-%m-%d"),
    "rates": rates
}

with open(f'{hotelName}_agoda_rates_{datetime.datetime.now().strftime("%Y%m%d")}.json', 'w') as json_file:
    json.dump(final_data, json_file, indent=4)