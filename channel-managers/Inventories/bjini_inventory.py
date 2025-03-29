import requests
import json
from datetime import datetime, timedelta

def getBookingJiniInventory(email, password, property_code):
    def authenticate_user(email, password):
        auth_url = "https://kernel.bookingjini.com/extranetv4/admin/auth"
        auth_body = {
            "email": email,
            "password": password,
            "browser": "Chrome",
            "creation_mode": "WEBSITE"
        }
        auth_headers = {'Content-Type': 'application/json'}
        
        auth_response = requests.post(auth_url, headers=auth_headers, json=auth_body)
        if auth_response.status_code == 200:
            auth_data = auth_response.json()
            auth_token = auth_data.get('auth_token')
            message = auth_data.get('message')
            if message == "User authentication successful":
                print(message)
                return auth_token
            else:
                print(message)
                exit()
        else:
            print(f"Authentication failed with status code: {auth_response.status_code}")
            exit()

    def fetch_inventory_data(auth_token, property_code, start_date, end_date, room_id):
        date_url = f"https://cm.bookingjini.com/extranetv4/inventory/get-inventory/{property_code}/{start_date}/{end_date}/{room_id}"
        date_headers = {'Authorization': f'Bearer {auth_token}'}
        
        date_response = requests.get(date_url, headers=date_headers)
        if date_response.status_code == 200:
            return date_response.json().get('data', [])
        else:
            print(f"Failed to fetch data with status code: {date_response.status_code}")
            return []

    def fetch_room_types(auth_token, property_code):
        inventory_url = f"https://kernel.bookingjini.com/extranetv4/hotel_master_room_type/all/{property_code}"
        headers = {'Authorization': auth_token}
        
        response = requests.request("GET", inventory_url, headers=headers)
        if response.status_code == 200:
            return response.json().get('data', [])
            
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return []
    
    auth_token = authenticate_user(email, password)
    
    start_date = datetime.now().strftime('%Y-%m-%d')
    end_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    
    room_types = fetch_room_types(auth_token, property_code)
    
    formatted_data = {
        "hotelCode": str(property_code),
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "inventory": []
    }
    
    for room in room_types:
        room_id = room.get('room_type_id')
        room_name = room.get('room_type').strip()
        total_rooms = room.get('total_rooms')
        
        inventory_data = fetch_inventory_data(auth_token, property_code, start_date, end_date, room_id)
        
        room_info = {
            "roomId": str(room_id),
            "roomName": room_name,
            "inventory": []
        }
        
        max_inventory = {}
        
        for data_item in inventory_data:
            for inv_item in data_item.get('inv', []):
                arrival_date = inv_item.get('date')
                no_of_rooms = inv_item.get('no_of_rooms')
                
                if arrival_date not in max_inventory:
                    max_inventory[arrival_date] = no_of_rooms
                else:
                    max_inventory[arrival_date] = max(max_inventory[arrival_date], no_of_rooms)
        
        for arrival_date, max_rooms in max_inventory.items():
            room_info["inventory"].append({
                "arrivalDate": arrival_date,
                "totalRooms": total_rooms,
                "availableRooms": max_rooms
            })
        
        formatted_data["inventory"].append(room_info)
    
    with open(f"{property_code} inventory.json", "w") as json_file:
        json.dump(formatted_data, json_file, indent=4)
    
    print(f"{property_code} Data extracted and stored successfully!")

# email = "dir@zorisboutiquehotel.com"
# password = "Zoris@6262"
# property_code = "2308"

# getBookingJiniInventory(email, password, property_code)
