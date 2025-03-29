import requests
import json
from datetime import datetime, timedelta

def resAvenueInventory(username, password, property_code):
    url = "https://cm.resavenue.com/channelcontroller/registeration.do"

    body = {
        "command": "checkUserExist",
        "sEmailAddress": username,
        "sPassword": password
    }

    response = requests.post(url, data=body)

    if response.status_code == 200:
        if "Invalid username and/or password." not in response.text:
            print("Login successful.")
        else:
            print("Invalid email or password.")
            return
    else:   
        print(f"HTTP Error: {response.status_code}")
        return

    cookies = response.cookies

    formatted_cookies = "; ".join([f"{cookie.name}={cookie.value}" for cookie in cookies])
    print(formatted_cookies)

    today = datetime.now()
    from_date = today.strftime("%d %b, %Y")
    to_date = (today + timedelta(days=30)).strftime("%d %b, %Y")

    endpoint_url = f"https://cm.resavenue.com/channelcontroller/roomAssign.do?command=getRoomAvailability&iPropertyId={property_code}&vFromDate={from_date}&vToDate={to_date}"
    
    headers = {
        'Cookie': formatted_cookies,
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest'
    }
    response = requests.post(endpoint_url, headers=headers)

    if response.status_code == 200:
        response_text = response.text

        room_data, availability_data, totals = response_text.split('$$')

        room_details = [item.split('@@@') for item in room_data.split('||') if item]
        print(room_details)
        availability_details = [item.split('@@@') for item in availability_data.split('||') if item]

        room_info = {}
        for room in room_details:
            room_id, room_name = room
            # print(room_id, room_name)
            room_info[room_id] = {
                'roomId': room_id,
                'roomName': room_name,
                'inventory': []
            }

        for availability in availability_details:
            room_id, date, available_rooms, _ = availability
            if room_id in room_info:
                room_info[room_id]['inventory'].append({
                    'arrivalDate': date,
                    'availableRooms': int(available_rooms)
                })

        total_no_of_rooms = []
        for item in totals.split('<div class="tbl_content">'):
            try:
                total_no_of_rooms.append(int(item.split('>')[1].split('<')[0]))
            except (IndexError, ValueError):
                pass

        # for i, room_id in enumerate(room_info):
        #     if i < len(total_no_of_rooms):
        #         total_rooms = total_no_of_rooms[i]
        #         for inventory in room_info[room_id]['inventory']:
        #             inventory['totalRooms'] = total_rooms
        #     else:
        #         for inventory in room_info[room_id]['inventory']:
        #             inventory['totalRooms'] = None 

        hotel_inventory = {
            "hotelCode": str(property_code),
            "timestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
            "inventory": list(room_info.values())
        }

        with open(f'{property_code} Inventory.json', 'w') as json_file:
            json.dump(hotel_inventory, json_file, indent=4)

        print(f"{property_code} Data saved to room_inventory.json")

resAvenueInventory('info@redwingscastle.com', 'Redwings@#12345', 8386)
