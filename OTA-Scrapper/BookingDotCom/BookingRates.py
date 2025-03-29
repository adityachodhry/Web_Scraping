import argparse
import json
import datetime
import requests
from bs4 import BeautifulSoup

result = []
otapid = None

def upload_rate(rates_data):
    response = requests.post(url="https://rsserver.retvenstechnologies.com/api/json/uploadRateJson", json=rates_data)
    if response.status_code == 200:
        print("Successfully Uploaded")
    else:
        print(f"Failed to upload. Status code: {response.status_code}")

def fetch_booking_data(url, checkin, checkout):
    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        
        parse(response, checkin, checkout)
    else:
        print(f"Failed to fetch data from {url}. Status code: {response.status_code}")

def parse(response, checkin, checkout):
    
    soup = BeautifulSoup(response.text, 'html.parser')
    with open('booking.html', 'w', encoding='utf-8') as html_file:
        html_file.write(str(soup))

    # Find the script tag containing "b_hotel_id"
    script_hotel_id = soup.find('script', text=lambda text: 'b_hotel_id' in text)

    if script_hotel_id:
        initial_state = script_hotel_id.text
        start_index = initial_state.find("b_hotel_id:")
        end_index = initial_state.find("b_hotel_name")

        if start_index != -1 and end_index != -1:
            start_index += len("b_hotel_id:")
            b_hotel_id = initial_state[start_index:end_index].strip().rstrip(",")

            # Extract otapid from b_hotel_id
            otapid = int(b_hotel_id.strip("'"))

    # Find the script tag containing "b_rooms_available_and_soldout:"
    script_rooms = soup.find('script', text=lambda text: 'b_rooms_available_and_soldout:' in text)

    if script_rooms:
        initial_state = script_rooms.text
        start_index = initial_state.find('b_rooms_available_and_soldout:')
        end_index = initial_state.find('b_photo_pid')

        if start_index != -1 and end_index != -1:
            start_index += len('b_rooms_available_and_soldout:')
            data = initial_state[start_index:end_index].strip().rstrip(',')

            # Parse the JSON data
            parsed_data = json.loads(data)

            for element in parsed_data:
                for room_option in element['b_blocks']:
                    if room_option['b_max_persons'] == 2:
                        for stay_price in room_option['b_stay_prices']:
                            if stay_price['b_stays'] == 1:
                                room_plan = room_option['b_mealplan_included_name']
                                if room_plan == "full_board":
                                    r_plan = 'AP'
                                elif room_plan == "half_board":
                                    r_plan = 'MAP'
                                elif room_plan == "breakfast":
                                    r_plan = 'CP'
                                else:
                                    r_plan = 'EP'

                                rates = {
                                    'roomID': str(element['b_id']),
                                    'checkIn': checkin,
                                    'checkOut': checkout,
                                    'roomName': element['b_name'],
                                    'roomPlan': r_plan,
                                    'price': int(stay_price['b_price'].replace("\xa0", " ").split(' ')[1].replace(",", "")),
                                }
                                result.append(rates)

    print(f"OTA : 3 | Hotel : {hotel_name} | Checkin : {checkin}")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape booking data and upload rates.")
    parser.add_argument("--url", required=True, help="Booking URL")
    parser.add_argument("--hotel_name", required=True, help="Hotel Name")
    parser.add_argument("--rhotel_id", required=True, help="RHOTEL ID")
    parser.add_argument("--currency_code",required=True, help="Currency Code")

    args = parser.parse_args()

    url = args.url
    hotel_name = args.hotel_name
    rhotel_id = args.rhotel_id
    currency_code = args.currency_code
    
    start_date = datetime.datetime.now(datetime.timezone.utc)
    num_days = 2

    for k in range(num_days):
        checkin = (start_date + datetime.timedelta(days=k)).strftime("%Y-%m-%d")
        checkout = (start_date + datetime.timedelta(days=k + 1)).strftime("%Y-%m-%d")
        request_url = f"{url}?&checkin={checkin}&checkout={checkout}&group_adults=2&group_children=0&selected_currency={currency_code}"
        
        fetch_booking_data(request_url, checkin, checkout)

    final_data = {
        "hId": int(rhotel_id),
        "otaId": 3,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d"),
        'otaPId': None,  
        "rates": result
    }

    with open(f'{hotel_name}_booking_rates_{datetime.datetime.now().strftime("%Y%m%d")}.json', 'w') as json_file:
        json.dump(final_data, json_file, indent=4)

    # upload_rate(final_data)
