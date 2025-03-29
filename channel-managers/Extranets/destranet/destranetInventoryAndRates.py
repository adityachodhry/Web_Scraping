import requests
import json
from datetime import datetime, timedelta

def destranetInventoryAndRate(username, password, propertyCode):
    current_date = datetime.now()
    date_start = current_date.strftime('%Y-%m-%d')
    date_end = (current_date + timedelta(days=30)).strftime('%Y-%m-%d')
    
    url = "https://destranet.desiya.com/extranet-controller/login"
    payload = json.dumps({
        "username": username,
        "password": password,
        "usertype": "DES"
    })

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        response_content = response.json()
        tokenData = response_content.get('data', {})
        tokenId = tokenData.get('token')

        inventory_url = f"https://destranet.desiya.com/extranet-controller/rateinfo?propertyType=B2B~B2C~MOR~GUESTHOUSE&type=AVL&categoryCode=AVL&from={date_start}&hotelId={propertyCode}&to={date_end}&token={tokenId}&validDays=[\"Mon\",\"Tue\",\"Weds\",\"Thur\",\"Fri\",\"Sat\",\"Sun\"]"
        inventory_response = requests.get(inventory_url)
        
        inventory_data = {}
        if inventory_response.status_code == 200:
            result = inventory_response.json()
            inventory_data = result.get('data', {}).get('inventories', [])

        rates_url = f"https://destranet.desiya.com/extranet-controller/rateinfo?type=RAT&categoryCode=RAT&from={date_start}&hotelId={propertyCode}&isShared=true&propertyType=B2C&rateType=B2C&to={date_end}&token={tokenId}&validDays=[\"Mon\",\"Tue\",\"Weds\",\"Thur\",\"Fri\",\"Sat\",\"Sun\"]"
        rates_response = requests.get(rates_url)

        rates_data = {}
        if rates_response.status_code == 200:
            rates_result = rates_response.json()
            rates_data = rates_result.get('data', {}).get('rateInfo', [])

        combined_data = {
            "hotelCode": propertyCode,
            "timestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
            "inventory": []
        }

        inventory_dict = {}
        for slot in inventory_data:
            room_id = slot.get('roomTypeCode')
            room_name = slot.get('roomTypename')
            availability_data = slot.get('availabilities', [])
            
            if room_id:
                if room_id not in inventory_dict:
                    inventory_dict[room_id] = {
                        "roomId": room_id,
                        "roomName": room_name,
                        "inventory": []
                    }
                
                for availability in availability_data:
                    arrival_date = availability.get('startDate')
                    available_rooms = availability.get('availability')
                    total_rooms = availability.get('totalRooms', available_rooms) 

                    inventory_dict[room_id]["inventory"].append({
                        "arrivalDate": arrival_date,
                        "totalRooms": total_rooms,
                        "availableRooms": available_rooms,
                        "rate": None 
                    })

        for rateInfo in rates_data:
            room_id = rateInfo.get('roomTypeCode')
            rate_plans = rateInfo.get('ratePlans', [])
            
            if room_id in inventory_dict:
                for ratePlan in rate_plans:
                    rates = ratePlan.get('rates', [])
                    for rate in rates:
                        start_date = rate.get('startDate')
                        net_rate = rate.get('netRate')
                        
                        for inventory_item in inventory_dict[room_id]["inventory"]:
                            if inventory_item["arrivalDate"] == start_date:
                                inventory_item["rate"] = net_rate

        combined_data["inventory"] = list(inventory_dict.values())

        with open('CombinedInventoryAndRates.json', 'w') as json_file:
            json.dump(combined_data, json_file, indent=4)

        print("Data saved successfully.")

        return combined_data
    
    else:
        print("Login failed:", response.status_code)

destranetInventoryAndRate('reservations@paramparacoorg.com', 'parampara123', '00007238')
