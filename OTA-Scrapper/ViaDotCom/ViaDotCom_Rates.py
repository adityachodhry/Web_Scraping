import requests
import json
from datetime import datetime, timedelta
from urllib.parse import quote

Hotel_Id = '9H25463'
num_days = 10

hotel_info = []

for day in range(num_days):
    today = datetime.now() + timedelta(days=day)
    check_in_date1 = quote(today.strftime("%d/%m/%Y"))
    check_out_date1 = quote((today + timedelta(days=1)).strftime("%d/%m/%Y"))

    url = f"https://in.via.com/apiv2/hotels/search?Room1Adults=2&Room1Children=0&regionId={Hotel_Id}&checkInDate={check_in_date1}&checkOutDate={check_out_date1}&rooms=1"
    # print(url)
    response = requests.get(url)
    if response.status_code == 200:
        response_content = response.json()

        data = response_content.get('HotelList', [])

        for hotel in data:
            results = hotel.get('Results', [])
        
            for room_data in results:
                roomId = room_data.get('RoomId')
                roomName = room_data.get('RoomName')
                totalPrice = room_data.get('TotalPrice')
                # print(totalPrice)

                meal_plan = room_data.get('MealPlan')
                plan_type = None

                # Determine the plan type based on the meal plan
                if meal_plan == "Room Only":
                    plan_type = "EP"
                elif "Breakfast" in meal_plan:
                    if "Dinner" in meal_plan or "Lunch" in meal_plan:
                        plan_type = "MAP"
                    else:
                        plan_type = "CP"
                else:
                    if "Dinner" in meal_plan and "Lunch" in meal_plan:
                        plan_type = "AP"

                details = {
                    'roomId': roomId,
                    'roomName': roomName,
                    'checkInDate': check_in_date1,
                    'checkOutDate': check_out_date1,
                    'mealPlan': plan_type,
                    'rate': totalPrice
                }

                # print(details)

                hotel_info.append(details)

            print(f"{day+1} Days Data Extracted!")

final_data_Via = {
        "hId": Hotel_Id,
        "otaId": 11,
        "timestamp": datetime.now().strftime("%Y-%m-%d"),
        "rates": hotel_info
    }

with open('Hotel_Info.json', 'w') as json_file:
    json.dump(final_data_Via, json_file, indent=2)
