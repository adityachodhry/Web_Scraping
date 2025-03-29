import requests
import json
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

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
            return None, None
    else:
        print(f"HTTP Error: {response.status_code}")
        return None, None

    cookies = response.cookies
    formatted_cookies = "; ".join([f"{cookie.name}={cookie.value}" for cookie in cookies])
    # print("Formatted Cookies:", formatted_cookies)

    today = datetime.now()
    from_date = today.strftime("%d %b, %Y")
    to_date = (today + timedelta(days=370)).strftime("%d %b, %Y")

    endpoint_url = f"https://cm.resavenue.com/channelcontroller/roomAssign.do?command=getRoomAvailability&iPropertyId={property_code}&vFromDate={from_date}&vToDate={to_date}"
    
    headers = {
        'Cookie': formatted_cookies,
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest'
    }

    response = requests.post(endpoint_url, headers=headers)

    if response.status_code == 200:
        response_text = response.text
        
        with open('response1.html', 'w') as response_html:
            response_html.write(response_text)
        
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

        total_no_of_rooms = []
        for item in totals.split('<div class="tbl_content">'):
            try:
                total_no_of_rooms.append(int(item.split('>')[1].split('<')[0]))
            except (IndexError, ValueError):
                pass

        hotel_inventory = {
            "hotelCode": str(property_code),
            "timestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
            "inventory": list(room_info.values())
        }

        return formatted_cookies, hotel_inventory
    else:
        print(f"HTTP Error: {response.status_code}")
        return None, None

def getRateID(cookies, property_code, room_id):
    url = f"https://cm.resavenue.com/channelcontroller/rateManagment1.do?command=getMappedRates&iPropId={property_code}&iRoomId={room_id}&flag=rate"
    payload = f'command=getMappedRates&iPropId={property_code}&iRoomId={room_id}&flag=rate'
    headers = {
        'Cookie': cookies,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        response_text = response.text

        with open('response2.html', 'w') as response_html:
            response_html.write(response_text)

    response_parts = response.text.split('$$$$')
    for part in response_parts:
        if 'EP Plan' in part:
            desired_value = part.split('$$')[0]
            return desired_value
    return None

def getRates(cookies, property_code, room_id, rate_id):
    url = "https://cm.resavenue.com/channelcontroller/rate.do?sCommand=searchMultipleRatePlans"
    today = datetime.now().strftime("%d/%m/%Y")
    next_month = (datetime.now() + timedelta(days=370)).strftime("%d/%m/%Y")
    payload = f'iPropId={property_code}&iRoomId={room_id}&sRateIds={rate_id}&sFromDate={today}&sToDate={next_month}'

    headers = {
        'Cookie': cookies,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(url, headers=headers, data=payload)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    tr_elements = soup.find_all('tr', rel=True)

    data = []
    for tr in tr_elements:
        if tr.get('rel') == '1' and tr.get('rel2') == '03_Double':
            tds = tr.find_all('td', class_='list-content list-content-data border')
            for td in tds:
                rate_input = td.find('input', class_='directive vRateVal')
                if rate_input:
                    rate = rate_input['value']
                    rel = td.get('rel', '')
                    rel_parts = rel.split('|')
                    if len(rel_parts) > 1:
                        date = rel_parts[1]
                        try:
                            rate_value = float(rate)
                            data.append({
                                "roomId": room_id,
                                "date": date,
                                "rate": rate_value
                            })
                        except ValueError:
                            print(f"Skipping invalid rate value: {rate}")
                    else:
                        print(f"Skipping td element with invalid rel attribute: {rel}")

    return data

def resAvenueRatesInventory(email,password,property_code) :
    cookies, inventory_data = resAvenueInventory(email,password,property_code)
    if cookies and inventory_data:
        combined_data = []
        room_info = {room['roomId']: room for room in inventory_data['inventory']}
        for room_id in room_info.keys():
            rate_id = getRateID(cookies, property_code, room_id)
            if rate_id:
                rates = getRates(cookies, property_code, room_id, rate_id)
                combined_data.extend(rates)

        # Update the inventory data with rates
        for room in inventory_data['inventory']:
            room_id = room['roomId']
            for inventory_item in room['inventory']:
                arrival_date = inventory_item['arrivalDate']
                # Find the matching rate
                for rate in combined_data:
                    if rate['roomId'] == room_id and rate['date'] == arrival_date:
                        inventory_item['rate'] = rate['rate']
                        break

        # Save data to JSON file
        with open(f'resavenueInventory.json', 'w') as json_file:
            json.dump(inventory_data, json_file, indent=4)
        
        return inventory_data

resAvenueRatesInventory('cmknmh@gmail.com', 'Abcd@12345', 3397)