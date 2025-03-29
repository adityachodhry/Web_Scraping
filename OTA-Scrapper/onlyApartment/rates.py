import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta

hotelId = 1714542727246
num_days = 90

today = datetime.now()
room_data = {
    "timestamp": today.strftime("%Y-%m-%d %H:%M:%S"),
    "rates": []
}

for day in range(num_days):
    check_in_date = (today + timedelta(days=day)).strftime("%Y-%m-%d")
    check_out_date = (today + timedelta(days=day + 1)).strftime("%Y-%m-%d")

    url = f"https://only-apartments.com/_ajax/show_total_price?date={check_in_date}&checkOut={check_out_date}&length=1n&productId=lstY1DGZG&_={hotelId}"

    response = requests.get(url)

    if response.status_code == 200:
        data_content = json.loads(response.text)
        
        combinations = data_content.get('combinations')
        
        soup = BeautifulSoup(combinations, 'html.parser')

        for room_div in soup.find_all('div', class_='text-center'):
            room_name_element = room_div.find('span', class_='font-medium')
            if room_name_element:
                room_name = room_name_element.text.strip()
            else:
                room_name = "Room Name Not Available"

            room_id_element = room_div.find('button', class_='modal-unit')
            if room_id_element and 'data-id' in room_id_element.attrs:
                room_id = room_id_element['data-id']
            else:
                room_id = "Room ID Not Available"

            room_info_list = []
            for room_div in soup.find_all('div', class_='row modality-row'):
                room_info = {}
                room_info['board_type'] = room_div.find('li', class_='board').get_text(strip=True)
                total_price_element = room_div.find('div', class_='total-price')
                integer_part = total_price_element.get_text(strip=True).split('.')[0]
                decimal_part = total_price_element.find('span', class_='decimals-small').get_text(strip=True)
                room_info['price'] = f"{integer_part}{decimal_part}"
                room_info_list.append(room_info)

                if "accommodation only" in room_info['board_type'].lower():
                    roomPlan = "EP"
                elif "bed and breakfast" in room_info['board_type'].lower():
                    roomPlan = "CP"
                else:
                    roomPlan = "Unknown"    
                
                display_price = room_info['price'].replace("\u20a8", "")

                room_data['rates'].append({
                    "roomId": room_id,
                    "roomName": room_name,
                    "checkIn": check_in_date,
                    "checkOut": check_out_date,
                    "roomPlan": roomPlan,
                    "displayPrice": f"Rs.{display_price}"   
                })

        print(f'HotelID : {hotelId} rates for Checkin: {check_in_date}')

with open('rooms_data.json', 'w') as json_file:
    json.dump(room_data, json_file, indent=4)
