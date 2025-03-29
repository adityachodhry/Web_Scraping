import requests
import json
from datetime import datetime, timedelta

username = 'vrrastoria'
password = 'VRR@1234'
# property_code = "IN-08b8203d-78ca-434f-a6fc-b8791dca6ccb"

def maximojoDataExtraction(username, password, roomId, roomName, channelId, rateTypeId, channelName, domainId):

    session = requests.Session()

    login_url = f"https://api.platform.maximojo.com/mantrasv5.svc/login?u={username}&p={password}"

    login_response = session.get(login_url)

    if login_response.status_code == 200:
        print("Login successfully!")
        
        cookies = session.cookies.get_dict()
        asp_session_id = cookies.get('ASP.NET_SessionId')
        session_id = cookies.get('session-id')

        print("Extracted Cookies:")
        print(f"ASP.NET_SessionId: {asp_session_id}")
        print(f"session-id: {session_id}")

    else:
        print("Invalid Credential!")
        exit()

    # Date setup
    current_date = datetime.now()
    end_date = current_date + timedelta(days=30)

    start_date_str = current_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    end_date_str = end_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    # Fetching room data
    roomURL = "https://api.platform.maximojo.com/mantrasv5.svc/SwitchSessionContext?d=fab40c6a-5b74-b7cb-0b51-a153498791b3&h=IN-08b8203d-78ca-434f-a6fc-b8791dca6ccb"
        
    headers = {
    'session-id': session_id,
    'Content-Type': 'application/json',
    'Cookie': f'ASP.NET_SessionId={asp_session_id}; session-id={session_id}'
    }

    response1 = session.get(roomURL, headers=headers)
    if response1.status_code == 200:
        print("Successfully fetched room data!")

        json_text = response1.text.lstrip('\ufeff')
        roomTypeResult = json.loads(json_text)

        # with open("RowRoom.json", "w") as json_file:
        #     json.dump(roomTypeResult, json_file, indent=4)

        propertyCode = roomTypeResult.get('HotelContext').get('HotelId')
        propertyName = roomTypeResult.get('HotelContext').get('HotelName')
        domainId = roomTypeResult.get('User').get('DomainId')
        # channelCodes = roomTypeResult.get('HotelContext').get('ChannelCodes', [])
        roomDataSlot = roomTypeResult.get('HotelContext', {}).get('RoomTypes', [])
        mealDataSlot = roomTypeResult.get('HotelContext', {}).get('RatePlans', [])

        
        endpoint = "https://api.platform.maximojo.com/mantrasv5.svc/FindRateCalendars"

        body = {
            "DomainId": domainId,
            "HotelId": propertyCode,
            "ChannelCodes": [
            "MAX"
            ],
            "StayDates": {
                "Start": start_date_str,
                "End": end_date_str
            },
            "IsRemote": False
        }

        response_content = requests.post(endpoint, json=body, headers=headers)

        if response_content.status_code == 200:
            data = response_content.content.decode('utf-8-sig')
            result_data = json.loads(data)

            # with open('Row.json', 'w') as json_file:
            #     json.dump(result_data, json_file, indent=2)

            formatted_data = []
            property_data = {
                "propertyCode": propertyCode,
                "propertyName": propertyName,
                "info": []
            }

            if isinstance(result_data, list) and len(result_data) > 0:
                first_item = result_data[0]
                data_slot = first_item.get('RoomRatePlans', [])

                for ratePlan in data_slot:
                    rateTypeId = ratePlan.get('RatePlanId', '')
                    # print(rateTypeId)
                    channelId = ratePlan.get('Id', '')
                    channelName = ratePlan.get('ChannelCode', '')

                    room_info_list = []
                    for room in roomDataSlot:
                        roomId = room.get('Id', '')
                        roomName = room.get('Name', '')

                        room_plan_info_list = []
                        for mealPlan in mealDataSlot:
                            room_plan_info_list.append({
                                "roomPlanId": mealPlan.get('Id', ''),
                                "roomPlanName": mealPlan.get('Name', '')
                            })

                        room_info_list.append({
                            "roomId": roomId,
                            "roomName": roomName,
                            "roomPlanInfo": room_plan_info_list
                        })

                    property_data["info"].append({
                        "rateTypeId": rateTypeId,
                        "channelId": channelId,
                        "channelName": channelName,
                        "roomInfo": room_info_list
                    })

                formatted_data.append(property_data)

                with open('hotel_data.json', 'w') as json_file:
                    json.dump(formatted_data, json_file, indent=2)

                print("Data formatted and saved successfully!")

            else:
                print("Unexpected data structure or empty list.")

        else:
            print(f"Failed to fetch data. Status code: {response_content.status_code}")
    else:
        print(f"Failed to fetch room data. Status code: {response1.status_code}")
    
    # return maximojoDataExtraction
