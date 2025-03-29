import requests
import json
from datetime import datetime, timedelta

username = 'vrrastoria'
password = 'VRR@1234'

login_url = f"https://api.platform.maximojo.com/mantrasv5.svc/login?u={username}&p={password}"

headers = {
    'Cookie': 'ASP.NET_SessionId=2ebgd5k5nsbgq2ddip4kccyc; session-id=c353c0d2-9f57-481c-83af-da763569319e'
}
login_response = requests.get(login_url, headers=headers)
if login_response.status_code == 200:
    print("Login successfully!")
else:
    print("Invalid Credential!")
    exit()

current_date = datetime.now()
end_date = current_date + timedelta(days=30)

start_date_str = current_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
end_date_str = end_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

property_code = "IN-08b8203d-78ca-434f-a6fc-b8791dca6ccb"

endpoint = "https://api.platform.maximojo.com/mantrasv5.svc/getRateCalendarSnapshot"

body = {
    "hotelId": property_code,
    "startDate": start_date_str,
    "endDate": end_date_str
}

response_content = requests.post(endpoint, json=body, headers=headers)

if response_content.status_code == 200:
    try:
        data = response_content.content.decode('utf-8-sig')
        result_data = json.loads(data)

        formatted_data = {
            "hotelCode": property_code,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "inventory": []
        }

        for inventory_info in result_data:
            print("Inventory Info:", inventory_info)

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

                Inventory_count = room_summary.get('Inventory', 0)
                MinRate = room_summary.get('MinRate', 0)

                room_data = next((item for item in formatted_data["inventory"] if item["roomId"] == RoomID), None)

                inventory_entry = {
                    "arrivalDate": arrival_date_formatted,
                    "totalRooms": TotalInventory,
                    "availableRooms": Inventory_count,
                    # "minRate": MinRate
                }

                if not room_data:
                    room_data = {
                        "roomId": RoomID,
                        "inventory": [inventory_entry]
                    }
                    formatted_data["inventory"].append(room_data)
                else:
                    room_data["inventory"].append(inventory_entry)

        with open('RateCalendarSnapshot.json', 'w') as json_file:
            json.dump(formatted_data, json_file, indent=2)
        print("Data Extracted Successfully")

    except json.JSONDecodeError as e:
        print(f"Failed to parse response as JSON: {e}")
else:
    print(f"Failed to fetch data. Status code: {response_content.status_code}")
