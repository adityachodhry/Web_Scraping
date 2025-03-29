import requests
import json
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

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
    to_date = (today + timedelta(days=6)).strftime("%d %b, %Y")

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
        availability_details = [item.split('@@@') for item in availability_data.split('||') if item]

        room_info = {}
        for room in room_details:
            room_id, room_name = room
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

        hotel_inventory = {
            "hotelCode": property_code,
            "timestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
            "inventory": list(room_info.values())
        }

        with open(f'{property_code} Inventory.json', 'w') as json_file:
            json.dump(hotel_inventory, json_file, indent=4)

        print(f"{property_code} Data saved to room_inventory.json")

        date_range = pd.date_range(start=today, periods=7).strftime("%Y-%m-%d").tolist()
        room_names = [room['roomName'] for room in hotel_inventory['inventory']]
        data = {date: [0] * len(room_names) for date in date_range}

        for room in hotel_inventory['inventory']:
            for inventory in room['inventory']:
                if inventory['arrivalDate'] in date_range:
                    data[inventory['arrivalDate']][room_names.index(room['roomName'])] = inventory['availableRooms']

        df = pd.DataFrame(data, index=room_names).reset_index()
        df.rename(columns={'index': 'Room Name'}, inplace=True)

        fig, ax = plt.subplots(figsize=(12, 5))

        table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center', colColours=['#D3D3D3'] * len(df.columns))

        plt.subplots_adjust(top=0.7)

        logo_path = "D:\Downloads\Retvens_Logo.jpg" 
        img = mpimg.imread(logo_path)
        ax_logo = fig.add_axes([0.1, 0.5, 0.2, 0.3], anchor='C', zorder=1)
        ax_logo.imshow(img)
        ax_logo.axis('off')

        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
        ax.set_frame_on(False)

        plt.show()

    else:
        print(f"HTTP Error: {response.status_code}")

resAvenueInventory('aditi.ntrpriss@gmail.com', 'Velvet!23', 1090)
