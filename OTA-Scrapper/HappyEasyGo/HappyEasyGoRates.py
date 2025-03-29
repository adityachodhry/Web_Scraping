import requests
import csv
import datetime
from datetime import timedelta, timezone

def get_hotel_rates(hotel_id, pName):
    num_days = 100  
    extracted_data = []
    start_date = datetime.datetime.now(timezone.utc)

    for k in range(num_days):
        checkin = (start_date + timedelta(days=k)).strftime("%Y-%m-%d")
        checkout = (start_date + timedelta(days=k + 1)).strftime("%Y-%m-%d")

        endpoint = f"https://hotel.happyeasygo.com/api/web/room_type/{hotel_id}/searchRoom"

        body = {
            "cityName": "",
            "guests": [
                {
                    "id": 1,
                    "adult": 2,
                    "child": 0,
                    "age": []
                }
            ],
            "hotelCode": hotel_id,
            "checkIn": checkin,
            "checkOut": checkout
        }

        response = requests.post(endpoint, json=body)

        if response.status_code == 200:
            response_content = response.json()
            hotel_info = response_content.get('data', {}).get('roomInfo', [])

            for hotel in hotel_info:
                hotel_cards = hotel.get('ratePlansInfo', [])

                for card in hotel_cards:
                    room_plan = card.get('ratePlanName')
                    if 'Breakfast & Lunch And Dinner' in room_plan:
                        meal_plan = 'AP'
                    elif 'Breakfast & Lunch Or Dinner' in room_plan:
                        meal_plan = 'MAP'
                    elif 'Breakfast' in room_plan:
                        meal_plan = 'CP'
                    else:
                        meal_plan = 'EP'

                    info = {
                        'room_id': card.get('roomTypeId'),
                        'check_in': checkin,
                        'check_out': checkout,
                        'room_name': hotel.get('roomTypeName'),
                        'room_plan': meal_plan,
                        'price': card.get('currentPrice'),
                    }
                    extracted_data.append(info)
                print(f"OTA : 7 | Hotel : {pName} | Checkin: {checkin}")
        else:
            print(f"Error: {response.status_code}, {response.text}")

    with open('HappyEasyGoRates.csv', 'w', newline='') as csvfile:
        fieldnames = ['room_id', 'check_in', 'check_out', 'room_name', 'room_plan', 'price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for data in extracted_data:
            writer.writerow(data)

    print("Data has been written to HappyEasyGoRates.csv")

# 5e45600b2b0a5f10a4dede2a
hotel_id = '5e02d11e159c942764441756'
pName = 'Hotel Shiva'
get_hotel_rates(hotel_id, pName)
