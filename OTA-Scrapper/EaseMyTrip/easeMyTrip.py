import requests
import json
import datetime
import xml.etree.ElementTree as ET

def final(hotel_id):
    
    today = datetime.datetime.now()

    UserName = "EaseMyTrip"
    Password = "C2KYph9PJFy6XyF6GT7SAeTq2d5e9Psrq5vmH34S"

    results = []  

    for day in range(5):
     
        check_in_date = (today + datetime.timedelta(days=day)).strftime("%Y-%m-%d")
        check_out_date = (today + datetime.timedelta(days=day + 1)).strftime("%Y-%m-%d")

        def get_ip():
            endpoint_url = "https://gi.easemytrip.com/UserIP.svc/GetIP"
            response_get = requests.get(endpoint_url)

            if response_get.status_code == 200:
          
                xml_content = response_get.content.decode('utf-8')
                root = ET.fromstring(xml_content)

                ip_address = root.text
            else:
                print("Failed to retrieve data. Status Code:", response_get.status_code)

            return ip_address

        def get_token(UserName , Password):
            endpoint_url = "https://hotelservice.easemytrip.com/api/HotelService/UserLogin"

            body = {"UserName":UserName,"Password":Password}

            request = requests.post(endpoint_url , json=body)
            response = request.json()

            token = response['message']
            return token

        token = get_token(UserName , Password)

        IP_address = get_ip()

        body = {
            "SearchRQ": {
                "RoomDetails": [
                    {
                        "NoOfRooms": 1,
                        "NoOfAdult": 2
                    }
                ],
                "CheckInDate": check_in_date,
                "CheckOut": check_out_date,
                "CityCode": "Bangalore, India",
                "CityName": "Bangalore, India",
                "wlcode": "",
                "NoOfRooms": 1
            },
            "EMTId": f"EMTHOTEL-{hotel_id}",
            "auth": {
                "AgentCode": 1,
                "UserName": "EaseMyTrip",
                "Password": "C2KYph9PJFy6XyF6GT7SAeTq2d5e9Psrq5vmH34S",
                "loginInfo": ""
            },
            "token":f"{token}",
            "ipaddress": IP_address
        }
        endpoint = "https://hotelservice.easemytrip.com/api/HotelInfo/GetHotelDescriptionV1"
        request = requests.post(endpoint, json=body)

        response = request.json()

        # with open(f"EMT_{day}.json", "w") as json_file:
        #     json.dump(response, json_file, indent=2)

        result_data = response['result']

        i = 0
        if result_data == None :
            continue

        while i < len(result_data):
            result = result_data[f'{i}']

            for room_info in result:
                hotelDetails = {}

                hotelDetails['roomId'] = room_info['roomTypeCode']
                hotelDetails['checkin'] = check_in_date
                hotelDetails['checkout'] = check_out_date
                hotelDetails['roomName'] = room_info['roomType']
                meal = room_info['nm']

                if meal == "Room With Full Board":
                    hotelDetails['roomPlan'] = 'AP'
                elif meal == "Room With Breakfast & Dinner" or meal == "Room With Breakfast & Lunch":
                    hotelDetails['roomPlan'] = 'MAP'
                elif meal == "Room With Breakfast":
                    hotelDetails['roomPlan'] = 'CP'
                elif meal == "Room Only":
                    hotelDetails['roomPlan'] = 'EP'
                else:
                    hotelDetails['roomPlan'] = 'NA'

                hotelDetails['price'] = room_info['price'] - \
                    room_info['discountedPrice']

                results.append(hotelDetails)
            i += 1
        print(f'OTA : 6 | Hotel : {hotel_id} | Checkin : {check_in_date} with status : {request.status_code}')

    return results

all_results = final(5700251)

with open('EaseMyTripRates.json', 'w') as json_file:
    json.dump(all_results, json_file, indent=2)