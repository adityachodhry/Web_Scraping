import requests
import json
import sys
from datetime import datetime, timedelta
# from uploadRates import uploadRate

# if len(sys.argv) != 5:
#     print("Usage: python script.py <hotel_id> <vcid>")
#     sys.exit(1)

# # Extract hotel ID and VCID from command-line arguments
# hotelId = int(sys.argv[1])
# vcID = int(sys.argv[2])
# hotelName = sys.argv[3]
# rhotelId = sys.argv[4]

vcID = '7802292548766851295'
hotelId = '2332122723124821447'
hotelName = 'Hotel Sheetal international'
rhotelId = '2332122723124821447'

num_days = 45
room_info_list = []

start_date = datetime.today()
checkin_date = start_date
checkout_date = checkin_date + timedelta(days=1)
checkin_str = checkin_date.strftime("%Y%m%d")
checkout_str = checkout_date.strftime("%Y%m%d")

url_first_request = f"https://hermes.goibibo.com/hotels/v13/daterange/price/v3/{vcID}/{checkin_str}/{checkout_str}/1-2-0/{hotelId}"

 # Define default headers
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-IN,en;q=0.9,mr-IN;q=0.8,mr;q=0.7,hi-IN;q=0.6,hi;q=0.5,en-GB;q=0.4,en-US;q=0.3',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'hermes.goibibo.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

response_first_request = requests.get(url_first_request, headers=headers)

if response_first_request.status_code == 200:

    cookies = response_first_request.cookies
    
    for k in range(num_days):
        start_date = datetime.today()
        checkin_date = start_date + timedelta(days=k)
        checkout_date = checkin_date + timedelta(days=1)
        checkin_str = checkin_date.strftime("%Y%m%d")
        checkout_str = checkout_date.strftime("%Y%m%d")

        url_second_request = f"https://hermes.goibibo.com/hotels/v13/detail/price/v3/{vcID}/{checkin_str}/{checkout_str}/1-2-0/{hotelId}"

        checkin = checkin_date.strftime("%Y-%m-%d")
        checkout = checkout_date.strftime("%Y-%m-%d")

        response_second_request = requests.get(
            url_second_request, headers=headers, cookies=cookies)

        if response_second_request.status_code == 200:
            response_data = response_second_request.json()

            if response_data['data']['error_message'] == 'All requested Hotel soldout from GDS' :
                continue

            with open('goibiboNew.json', 'w') as json_file:
                json.dump(response_data, json_file, indent=4)
            try :
                registrations = response_data['data']['reg']
            except :
                registrations = response_data['data']['mprl']

            for registration in registrations:
                room_ID = registration['rtc']
                room_name = registration['rtn']

                room_plan_list = registration['rpl']

                for roomplan in room_plan_list:
                    try :
                        room_plan = roomplan['rpt']
                        try :
                            price = roomplan['pd']['spr']
                        except :
                            price = roomplan['pwi'][0]['pd']['spr']

                        if "Rooms only" in room_plan or "Beds only" in room_plan:
                            rPlan = "EP"
                        elif "Breakfast" in room_plan:
                            if "Lunch/Dinner" in room_plan:
                                rPlan = "MAP"
                            else:
                                rPlan = "CP"
                        else:
                            rPlan = "Unknown"
                    except :
                        rPlan = "Unknown"
                        try :
                            price = roomplan['pd']['spr']
                        except :
                            price = roomplan['pwi'][0]['pd']['spr']
                
                    room_info = {
                        'roomID': str(room_ID),
                        'checkIn': checkin,
                        'checkOut': checkout,
                        'roomName': room_name,
                        'roomPlan': rPlan,
                        'price': int(price),
                    }

                    # print(room_info)
                    room_info_list.append(room_info)
        else:
            
            print(f"Error in second request: {response_second_request.status_code}")
            print(response_second_request.text)
            
        print(f"OTA : 2 | Hotel : {hotelName} | Checkin : {checkin}")

else:

    print(f"Error in first request: {response_first_request.status_code}")
    print(response_first_request.text)

final_data = {
    'hId': int(float(rhotelId)),
    'otaId': 2,
    'otaPId': str(hotelId),
    'timestamp': datetime.now().strftime("%Y-%m-%d"),
    'rates': room_info_list
}

with open(f'{hotelName}_goibibo_rates_{datetime.now().strftime("%Y%m%d")}.json', 'w') as json_file:
    json.dump(final_data, json_file, indent=4)