import requests
from datetime import datetime, timedelta
import json

today = datetime.now()
hId = 41087
unique_room_names = set()
room_details_dict = {}  
results = []  

for day in range(10):
   
    check_in_date = (today + timedelta(days=day)).strftime("%d/%m/%Y")
    check_out_date = (today + timedelta(days=day + 1)).strftime("%d/%m/%Y")

    url = "https://www.cleartrip.com/hotel/orchestrator/v2/hotel/details"

    body = {
        "hotelId": hId,
        "useCaseContext": "DESKTOP_DETAILS",
        "checkInDate": check_in_date,
        "checkOutDate": check_out_date,
        "roomAllocations": [
            {
                "adults": {
                    "count": 2,
                    "metadata": []
                },
                "children": {
                    "count": 0,
                    "metadata": []
                }
            }
        ],
        "filters": {
            "includeOnlyFreeCancellation": False,
            "includeOnlyFreeBreakfast": True
        }
    }

    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    response = requests.post(url, json=body, headers=headers)

    if response.status_code == 200:
        response_data = response.json()

        slots_data = response_data.get('response', {}).get('slotsData', [])
        for slot in slots_data:
            slot_details = slot.get('slotData', {}).get('data', {}).get('roomTypes', {}).get('data', {}).get('dropDownContent', {}).get('data', {}).get('main', {}).get('data', {}).get('items', [])
            for details in slot_details:
                id = details.get('action', {}).get('payload', {}).get('id', {})
                name = details.get('data', {}).get('heading', {})
                price = details.get('data', {}).get('subHeading', {}).split('/')[0].split('₹')[1].replace(',', '')
                room_details_dict[id] = {'name': name, 'price': price}

            slot_details2 = slot.get('slotData', {}).get('data', {}).get('slots', [])
            for details2 in slot_details2:
                id = details2.get('slotData', {}).get('data', {}).get('id', None)
                if id is not None and any(c.isalpha() for c in id):
                    # print(id)
                    # Access corresponding details from room_details_dict using id
                    corresponding_details = room_details_dict.get(id, {})
                    # print(corresponding_details)

                meals = details2.get('slotData', {}).get('data', {}).get('roomVariants', [])
                
                for headingg in meals:
                    mealplan = headingg.get('data', {}).get('heading', None)
                    if mealplan is not None:
                        if 'Room with Breakfast & Dinner' in mealplan or 'Room with Breakfast & Lunch' in mealplan:
                            rplan = 'MAP'
                        elif 'Room with Breakfast, Lunch & Dinner' in mealplan:
                            rplan = 'AP'
                        elif 'Room with Breakfast' in mealplan:
                            rplan = "CP"
                        
                        elif 'Room Only' in mealplan:
                            rplan = 'EP'
                        # print(mealplan)
                        # print(rplan)
                        # print()

                        results.append({
                            "roomID": str(id),
                            "roomName": corresponding_details.get('name', ''),
                            "checkIn": (today + timedelta(days=day)).strftime("%Y-%m-%d"),
                            "checkOut": (today + timedelta(days=day + 1)).strftime("%Y-%m-%d"),
                            "roomPlan": rplan,
                            "price": float(corresponding_details.get('price', 0))
                        })

    print(f'OTA : 7 | Hotel : {hId} | Checkin : {(today + timedelta(days=day)).strftime("%Y-%m-%d")}')  

final_data = {
    "otaId": 6,
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "rates": results
}

with open('Rates.json', 'w', encoding='utf-8') as json_file:
    json.dump(final_data, json_file, indent=2)