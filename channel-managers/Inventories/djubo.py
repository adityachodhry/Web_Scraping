import requests
import json
from datetime import datetime

def djuboInventory(username, password, property_code):
    url = "https://apps.djubo.com/sign-in/"

    form_data = {
        "csrfmiddlewaretoken": "",
        "email_address": username,
        "password": password
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    response = requests.post(url, headers=headers, data=form_data)

    if "Loading" in response.text:
        print("Login Successful")

        properties_url = "https://apps.djubo.com/core-data/properties"
        headers = {
            'Cookie': 'auth_token_7=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxNTQzLCJ1c2VybmFtZSI6InNhbGVzQHNoaXZhY29udGluZW50YWwuaW4iLCJleHAiOjE3MjA0NjIzNTIsImVtYWlsIjoic2FsZXNAc2hpdmFjb250aW5lbnRhbC5pbiJ9.jeAw4LGVEpiGoAC4c-dw9CBDkXdeDFDftysnZs2Bx64'
        }
        response = requests.get(properties_url, headers=headers)

        if response.status_code == 200:
            properties_data = response.json()
            room_names = {}
            for property in properties_data:
                room_categories = property.get('room_categories', [])
                for category in room_categories:
                    room_id = category.get('id')
                    room_name = category.get('name')
                    rooms = category.get('rooms', [])
                    total_inventory = len(rooms)
                    room_names[room_id] = room_name
            
            current_datetime = datetime.now()
            start_date = current_datetime.strftime("%Y-%m-%d")

            # property_code = 670

            url = f"https://apps.djubo.com/inventory-data/accounts/3920/properties/{property_code}/channel-wise-inventories?nod=15&st_dt={start_date}"

            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                try:
                    response_data = response.json()

                    # with open('Inventory_Data.json', 'w') as json_file:
                    #     json.dump(response_data, json_file, indent=2)

                except json.JSONDecodeError as e:
                    print(f"Failed to parse response as JSON: {e}")
                    exit(1)

                inventory_info = {
                    "hotelCode": str(property_code),
                    "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "inventory": []
                }

                category_totals = {}
                for date, channel_data in response_data.items():
                    category_count = {}
                    for rooms in channel_data.values():
                        for room in rooms:
                            category_id = room.get("category_id")
                            if category_id and category_id in room_names:
                                room_name = room_names[category_id]

                                if category_id not in category_count:
                                    category_count[category_id] = {'count': 0, 'room_name': room_name}

                                category_count[category_id]['count'] += 1

                    for category_id, count_data in category_count.items():
                        if category_id not in category_totals:
                            category_totals[category_id] = total_inventory

                        room_inventory = {
                            "arrivalDate": datetime.strptime(date, '%Y-%m-%d').strftime("%Y-%m-%d"),
                            "totalRooms": category_totals[category_id],
                            "availableRooms": category_totals[category_id] - count_data['count']
                        }
                        
                        room_data = next((item for item in inventory_info["inventory"] if item["roomId"] == str(category_id)), None)
                        if not room_data:
                            inventory_info["inventory"].append({
                                "roomId": str(category_id),
                                "roomName": count_data['room_name'],
                                "inventory": [room_inventory]
                            })
                        else:
                            room_data["inventory"].append(room_inventory)

                with open(f"{property_code} inventory.json", "w") as json_file:
                    json.dump(inventory_info, json_file, indent=4)

                print(f"{property_code} Data saved to inventory_Djubo_Data.json")
            else:
                print("Failed to fetch data. Status code:", response.status_code)
        else:
            print("Failed to fetch properties data. Status code:", response.status_code)

    elif "Login Failed!!" in response.text:
        print("Login failed: Invalid username or password")

# djuboInventory('Sales@shivacontinental.in', 'shiva@1234', 670)
