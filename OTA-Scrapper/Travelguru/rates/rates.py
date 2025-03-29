import requests
from datetime import datetime, timedelta
import json

city = "New Delhi"
hotelId = "00078943"
num_days = 90

today = datetime.now()
rates_list = []

for day in range(num_days):
    check_in_date = (today + timedelta(days=day)).strftime("%Y-%m-%d")
    check_out_date = (today + timedelta(days=day + 1)).strftime("%Y-%m-%d")

    url = f"https://hotels.travelguru.com/tgapi/hotels/v1/hotels/{hotelId}?checkInDate={check_in_date}&checkOutDate={check_out_date}&city.name=New%20Delhi&city.code=New%20Delhi&propertySource=TGU&hotelId={hotelId}&tenant=TGB2C&rooms[0].id=1&rooms[0].noOfAdults=1&_rn=mrj"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "X-Api-Key": "RcKU4ktJuNBFV1BknPWT"
    }
    
    response = requests.get(url, headers=headers)
    response_content = response.json()
    # print(response_content)
    
    data_slots = response_content.get('data', {}).get('rates', [])

    for rate in data_slots:
        name = rate.get('name', '')
        roomId = rate.get('roomTypeId', '')
        pricing = rate.get('pricing', {})
        pernightprice = pricing.get('perNightPrice', {})
        discountedprice = pernightprice.get('discountedPrice')

        if "room only" in name.lower():
            meal_plan = "EP"  
        elif "with breakfast" in name.lower():
            meal_plan = "CP"  
        else:
            meal_plan = "Unknown"

        if roomId:
            room_id = roomId.lstrip('0')
        else:
            room_id = "N/A"

        rate_entry = {
            "roomId": room_id,
            "name": name,
            "checkIn": check_in_date,
            "checkOut": check_out_date,
            "mealPlan": meal_plan,
            "displayPrice": discountedprice
        }

        rates_list.append(rate_entry)

    data_dict = {
    "otaPId": hotelId,
    "timeStamp": today.strftime("%Y-%m-%d %H:%M:%S"),
    "rates": rates_list
    }

    print(f"Hotel : {hotelId} | CheckIn : {check_in_date}")

with open('rates_data.json', 'w') as json_file:
    json.dump(data_dict, json_file, indent=4)
