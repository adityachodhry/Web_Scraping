import requests
import json
from datetime import datetime, timedelta

def maximojoInventories(username, password, property_code):
    # Create a session
    session = requests.Session()

    login_url = f"https://api.platform.maximojo.com/mantrasv5.svc/login?u={username}&p={password}"
    login_response = session.get(login_url)
    if login_response.status_code == 200:
        print("Login successfully!")
        
        try:
            login_data = json.loads(login_response.content.decode('utf-8-sig'))
            session_id = login_data.get('session-id')
        except json.JSONDecodeError as e:
            print("Error decoding JSON response:", e)
            return
    else:
        print("Invalid Credential!")
        return

    current_date = datetime.now() + timedelta(days=-1)
    total_days = 1
    end_date = current_date + timedelta(days=total_days)

    output = {
        "hotelCode": property_code,
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "inventory": []
    }

    endpoint = "https://api.platform.maximojo.com/mantrasv5.svc/getRateCalendarSnapshot"
    body = {
        "hotelId": property_code,
        "startDate": current_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "endDate": end_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    }

    response_content = session.post(endpoint, json=body)
    if response_content.status_code == 200:
        data = response_content.content.decode('utf-8-sig')
        result_data1 = json.loads(data)

        with open('inventory_Row.json', 'w') as json_file:
            json.dump(result_data1, json_file, indent=2)
        
        if result_data1:
            DomainId = result_data1[0].get('DomainId')
            print(f"DomainId fetched dynamically: {DomainId}")
    else:
        print(f"Failed to retrieve DomainId: {response_content.status_code} - {response_content.text}")
        return
    
    roomURL = f"https://api.platform.maximojo.com/mantrasv5.svc/SwitchSessionContext?d={DomainId}&h={property_code}"
    response1 = session.get(roomURL)
    if response1.status_code == 200:
        print("Successfully fetched room data!")
        json_text = response1.text.lstrip('\ufeff')
        roomTypeResult = json.loads(json_text)

        roomDataSlot = roomTypeResult.get('HotelContext', {}).get('RoomTypes', [])
    else:
        print(f"Failed to fetch room data: {response1.status_code} - {response1.text}")
        return
    
    processed_rooms = {}

    while current_date <= end_date:
        month_start = current_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        month_end = (current_date + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        
        payload = json.dumps({
            "DomainId": DomainId,
            "HotelId": property_code,
            "ChannelCodes": ["MAX"],
            "StayDates": {
                "Start": month_start,
                "End": month_end
            },
            "IsRemote": False
        })

        headers = {
            'session-id': session_id, 
            'Content-Type': 'application/json'
        }

        inventoryUrl = "https://api.platform.maximojo.com/mantrasv5.svc/FindRateCalendars"
        response = session.post(inventoryUrl, headers=headers, data=payload)

        if response.status_code == 200:
            data = response.content.decode('utf-8-sig')
            result_data = json.loads(data)

            for inventory_info in result_data:
                room_summaries = inventory_info.get('RoomRatePlans', [])
                if not room_summaries:
                    print("Skipping entry due to missing 'RoomRatePlans'")
                    continue

                arrivalDate = inventory_info.get('StayDate').split('T')[0]

                # Dictionary to store minimum rates for each room for the current date
                room_min_rates = {}

                for room_summary in room_summaries:
                    roomID = room_summary.get('RoomTypeId')
                    roomPrice = room_summary.get('RoomRate', {}).get('PerDay', 0)

                    if roomID not in room_min_rates:
                        room_min_rates[roomID] = {
                            "rate": roomPrice,
                            "totalAvailability": room_summary.get('TotalAvailability', 0),
                            "availableRooms": room_summary.get('Availability', 0)
                        }
                    else:
                        # Update the rate and availability if a lower rate is found
                        if roomPrice < room_min_rates[roomID]["rate"]:
                            room_min_rates[roomID] = {
                                "rate": roomPrice,
                                "totalAvailability": room_summary.get('TotalAvailability', 0),
                                "availableRooms": room_summary.get('Availability', 0)
                            }

                for roomID, rate_info in room_min_rates.items():
                    if roomID not in processed_rooms:
                        roomTypeSecondName = None
                        for roomTypeName in roomDataSlot:
                            if roomTypeName.get('Id') == roomID:
                                roomTypeSecondName = roomTypeName.get('Name')

                        room_inventory = {
                            "roomId": roomID,
                            "roomName": roomTypeSecondName,
                            "inventory": []
                        }
                        output["inventory"].append(room_inventory)
                        processed_rooms[roomID] = room_inventory  

                    processed_rooms[roomID]["inventory"].append({
                        "arrivalDate": arrivalDate,
                        "totalRooms": rate_info["totalAvailability"],
                        "availableRooms": rate_info["availableRooms"],
                        "rate": rate_info["rate"]
                    })

            print(f"Fetched data for {month_start} to {month_end}")
        else:
            print(f"Failed to retrieve data for {month_start} to {month_end}: {response.status_code} - {response.text}")

        # Move to the next month
        current_date += timedelta(days=1)

    # Store formatted response data in a JSON file
    with open('maximojoInventory.json', 'w') as json_file:
        json.dump(output, json_file, indent=4)

    print("Response data saved to formatted_maximojo_response.json")

maximojoInventories('vrrastoria', 'VRR@1234', "IN-08b8203d-78ca-434f-a6fc-b8791dca6ccb")
