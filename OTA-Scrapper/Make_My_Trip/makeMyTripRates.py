import requests
import json
import sys
import datetime

if len(sys.argv) != 5:
    print("Usage: python script.py <hotel_id> <citycode> <hotelname> <rhotelid>")
    sys.exit(1)

# Extract hotel ID and VCID from command-line arguments
hotelId = int(sys.argv[1])
cityCode = sys.argv[2]
hotelName = sys.argv[3]
rhotelId = sys.argv[4]

rates = []
num_days = 90

rates = []
today = datetime.datetime.now()
for day in range(num_days):
    check_in_date = (today + datetime.timedelta(days=day)).strftime("%Y-%m-%d")
    check_out_date = (today + datetime.timedelta(days=day + 1)).strftime("%Y-%m-%d")
    body = {
    "deviceDetails": {
        "appVersion": "121",
        "deviceId": "121",
        "deviceType": "Desktop",
        "bookingDevice": "DESKTOP"
    },
    "searchCriteria": {
        "hotelId": hotelId,
        "checkIn": check_in_date,
        "checkOut": check_out_date,
        "roomStayCandidates": [
            {
                "adultCount": 2
            }
        ],
        "countryCode": "in",
        "cityCode": "CTUDR",
        "currency": "INR"
    },
    "requestDetails": {
        "visitorId": "121",
        "visitNumber": 1,
        "trafficSource": {
            "type": "CMP",
            "source": "googlehoteldfinder",
            "hotelId": "121"
        },
        "loggedIn": True,
        "funnelSource": "HOTELS",
        "idContext": "B2C",
        "pageContext": "DETAIL",
        "channel": "B2Cweb"
    },
    "featureFlags": {
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

    endpoint = "https://mapi.makemytrip.com/clientbackend/cg/search-rooms/DESKTOP/2?language=eng&region=in&currency=INR&idContext=B2C&countryCode=IN"
    try:
        response = requests.post(endpoint, headers=headers, json=body)
        response_data = response.json()

        if response.status_code == 200:

            # with open("mmt.json", "w") as json_file:
            #     json.dump(response_data, json_file, indent=2)
            try:
                room_details = response_data['response']['exactRooms']
            except :
                try :
                    room_details = response_data['response']['occupancyRooms']
                except :
                    pass
            try:
                for room_detail in room_details:
                    
                    ratePlans = room_detail['ratePlans']
                    for plan in ratePlans:
                        priceDetails = plan["tariffs"]
                        for detail in priceDetails:
                            pricemaps = detail['priceMap']['DEFAULT']['details']
                            for price in pricemaps:
                                bkgDetails = {}
                                key = price['key']
                                if key == "PRICE_AFTER_DISCOUNT":
                                    bkgDetails['roomID'] = str(room_detail['roomCode'])
                                    bkgDetails['checkIn'] = check_in_date
                                    bkgDetails['checkOut'] = check_out_date
                                    bkgDetails['roomName'] = room_detail['roomName']
                                    
                                    meal = plan['name']
                                    if 'Breakfast' in meal and 'Lunch' in meal and 'Dinner' in meal and '/' in meal :
                                        rplan = 'MAP'
                                    elif 'Breakfast' in meal and 'Lunch' in meal and 'Dinner' in meal :
                                        rplan = 'AP'
                                    elif 'Breakfast' in meal :
                                        rplan = 'CP'
                                    else :
                                        rplan = 'EP'
                                    bkgDetails['roomPlan'] = rplan
                                    bkgDetails['price'] = price['amount']
                                    break
                                    
                                elif key == "BASE_FARE":
                                    bkgDetails['roomID'] = str(room_detail['roomCode'])
                                    bkgDetails['checkIn'] = check_in_date
                                    bkgDetails['checkOut'] = check_out_date
                                    bkgDetails['roomName'] = room_detail['roomName']
                                    
                                    meal = plan['name']
                                    if 'Breakfast' in meal and 'Lunch' in meal and 'Dinner' in meal and '/' in meal:
                                        rplan = 'MAP'
                                    elif 'Breakfast' in meal and 'Lunch' in meal and 'Dinner' in meal:
                                        rplan = 'AP'
                                    elif 'Breakfast' in meal:
                                        rplan = 'CP'
                                    else:
                                        rplan = 'EP'
                                    bkgDetails['roomPlan'] = rplan
                                    bkgDetails['price'] = price['amount'] 
                            rates.append(bkgDetails)
            except:
                pass
        else:
            print(response.text)
        print(f'OTA : 1 | Hotel : {hotelName} | Checkin : {check_in_date}')
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        print(response.text)
        pass
final_data = ({
                "hId":int(rhotelId),
                "otaId": 1,
                "otaPId":str(hotelId),
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d"),
                "rates": rates
                })

with open(f'{hotelName}_mmt_rates_{datetime.datetime.now().strftime("%Y%m%d")}.json', 'w') as json_file:
                    json.dump(final_data, json_file, indent=4)