import requests
import json
from datetime import datetime, timedelta

def maximojoInventories(username, password, property_code):

    session = requests.Session()

    login_url = f"https://api.platform.maximojo.com/mantrasv5.svc/login?u={username}&p={password}"

    login_response = session.get(login_url)
    if login_response.status_code == 200:
        print("Login successfully!")
    else:
        print("Invalid Credential!")
        return

    roomURL = "https://api.platform.maximojo.com/mantrasv5.svc/SwitchSessionContext?d=fab40c6a-5b74-b7cb-0b51-a153498791b3&h=IN-08b8203d-78ca-434f-a6fc-b8791dca6ccb"
    
    # headers = {
    #     'Session-Id': '3e926135-9354-4d17-b91d-dd39b4e9d107',
    #     'Cookie': 'ASP.NET_SessionId=5viw5ri0hswgkkng4ua3b40g; session-id=46c82702-a6fb-424d-9ae7-8e536630a9a5'
    # }

    response1 = session.get(roomURL)
    if response1.status_code == 200:
        print("Successfully fetched room data!")

        json_text = response1.text.lstrip('\ufeff')
        roomTypeResult = json.loads(json_text)

        with open("RowRoom.json", "w") as json_file:
            json.dump(roomTypeResult, json_file, indent=4)

        roomDataSlot = roomTypeResult.get('HotelContext', {}).get('RoomTypes', [])

    endpoint = "https://api.platform.maximojo.com/mantrasv5.svc/getRateCalendarSnapshot"

    current_date = datetime.now() + timedelta(days=-1)
    end_date = current_date + timedelta(days=371)

    start_date_str = current_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    end_date_str = end_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    
    body = {
        "hotelId": property_code,
        "startDate": start_date_str,
        "endDate": end_date_str
    }

    response_content = session.post(endpoint, json=body)

    if response_content.status_code == 200:
        data = response_content.content.decode('utf-8-sig')
        result_data = json.loads(data)

        with open('inventory_Row.json', 'w') as json_file:
            json.dump(result_data, json_file, indent=2)

        formatted_data = {
            "hotelCode": property_code,
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "inventory": []
        }

        for inventory_info in result_data:

            arrival_Date = inventory_info.get('StayDate')
            if not arrival_Date:
                print("Skipping entry due to missing 'StayDate'")
                continue

            arrival_date_formatted = datetime.strptime(arrival_Date.split('T')[0], "%Y-%m-%d").strftime("%Y-%m-%d")
            TotalInventory = inventory_info.get('TotalInventory', 0)

            room_summaries = inventory_info.get('RooomSummaries', [])
            if not room_summaries:
                print("Skipping entry due to missing 'RoomSummaries'")
                continue

            for room_summary in room_summaries:
                RoomID = room_summary.get('RoomID')
                if not RoomID:
                    print("Skipping room summary due to missing 'RoomID'")
                    continue

                Inventory_count = room_summary.get('Inventory', None)
                TotalAvailability = room_summary.get('TotalAvailability', None)
                roomPrice = room_summary.get('MinRate', None)

                room_data = next((item for item in formatted_data["inventory"] if item["roomId"] == RoomID), None)

                roomTypeSecondName = None
                for roomTypeName in roomDataSlot:
                    if roomTypeName.get('Id') == RoomID:
                        roomTypeSecondName = roomTypeName.get('Name')

                inventory_entry = {
                    "arrivalDate": arrival_date_formatted,
                    "totalRooms": TotalInventory,
                    "availableRooms": Inventory_count,
                    "rate": roomPrice
                }

                if not room_data:
                    room_data = {
                        "roomId": RoomID,
                        "roomName": roomTypeSecondName,
                        "inventory": [inventory_entry]
                    }
                    
                    formatted_data["inventory"].append(room_data)
                else:
                    room_data["inventory"].append(inventory_entry)

        with open('Inventory_Maximojo_Data.json', 'w') as json_file:
            json.dump(formatted_data, json_file, indent=2)

        print("Data Extracted Successfully")

    else:
        print(f"Failed to fetch data. Status code: {response_content.status_code}")

maximojoInventories('vrrastoria','VRR@1234',"IN-08b8203d-78ca-434f-a6fc-b8791dca6ccb")
