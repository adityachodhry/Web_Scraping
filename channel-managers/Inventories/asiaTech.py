import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import re

def asiaTechInventory(username, password, property_code):

    login_url = "https://www.asiatech.in/booking_engine/admin/ajaxrequest/loginphp.php"

    login_data = {
        "form_token": "", 
        "login_email": username,
        "login_password": password,
        "login_type": "0"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }

    session = requests.Session()
    response = session.post(login_url, headers=headers, data=login_data)

    if "2" in response.text:
        print("Login Successful")
        fetch_data(session,property_code)
    else:
        print("Login failed: Unknown error")

def fetch_data(session,property_code):
    data_url = "https://www.asiatech.in/booking_engine/admin/ajaxrequest/asia-roomavailability.php"
    current_date = datetime.now().strftime('%Y-%m-%d')
    data_body = {
        'regid': '16',
        'bs1_id': '13',
        'nextdate': current_date,
        'duration': '7'
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    # property_code = 6011
    data_response = session.post(data_url, headers=headers, data=data_body)
    inventory_info = {
        "hotelCode": str(property_code),
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "inventory": []
    }

    if data_response.status_code == 200:
        soup = BeautifulSoup(data_response.text, 'html.parser')
        
        room_dict = {}

        for tr in soup.find_all('tr', attrs={"data-roomid": True}):
            room_id = tr.get('data-roomid')
            for td in tr.find_all('td'):
                text_content = td.text.strip()
                match = re.search(r"^(.*)\s*\((\d+)\)$", text_content)
                if match:
                    room_name = match.group(1).strip()
                    total_inventory = int(match.group(2))
                    inputs = td.parent.find_all('input', type="text")
                    for input_tag in inputs:
                        date_str = input_tag.get('data-update')
                        available_rooms = input_tag.get('data-prev')
                        if date_str and available_rooms:
                            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                            formatted_date = date_obj.strftime("%Y-%m-%d")
                            if room_id not in room_dict:
                                room_dict[room_id] = {
                                    "roomId": room_id,
                                    "roomName": room_name,
                                    "inventory": []
                                }
                            room_dict[room_id]["inventory"].append({
                                "arrivalDate": formatted_date,
                                "totalRooms": total_inventory,
                                "availableRooms": int(available_rooms)
                            })

        for room_data in room_dict.values():
            inventory_info["inventory"].append(room_data)

        with open("inventory_asiaTech_Data.json", "w") as json_file:
            json.dump(inventory_info, json_file, indent=4)

        print("Data successfully stored in inventoryData.json")
    else:
        print("Failed to retrieve data:", data_response.status_code)

# asiaTechInventory('boutiquehotel1', 'TheMohua@G1', 6011)
