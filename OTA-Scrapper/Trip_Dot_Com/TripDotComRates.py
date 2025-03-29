import requests
import json
import datetime
from datetime import timedelta, timezone

def extract_hotel_data(hotel_id, city_id):
    num_days = 5  # Fixed number of days

    extracted_data = []
    start_date = datetime.datetime.now(timezone.utc)

    for k in range(num_days):
        checkin = (start_date + timedelta(days=k)).strftime("%Y%m%d")
        checkout = (start_date + timedelta(days=k+1)).strftime("%Y%m%d")

        endpoint = "https://www.trip.com/restapi/soa2/28820/getHotelRoomList"

        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br'
        }

        body = {
            "search": {
                "hotelId": hotel_id,
                "roomId": 0,
                "checkIn": checkin,
                "checkOut": checkout,
                "roomQuantity": 1,
                "adult": 2,
                "childInfoItems": [],
                "priceType": 0,
                "hotelUniqueKey": "",
                "mustShowRoomList": [],
                "location": {
                    "geo": {
                        "cityID": city_id
                    }
                },
                "filters": [],
                "meta": {
                    "fgt": -1,
                    "roomkey": "",
                    "minCurr": "",
                    "minPrice": ""
                },
                "hasAidInUrl": False,
                "cancelPolicyType": 0,
                "fixSubhotel": 0,
                "isFirstEnterDetailPage": "F",
                "listTraceId": ""
            },
            "head": {
                "platform": "PC",
                "cver": "0",
                "cid": "1704",
                "bu": "IBU",
                "group": "trip",
                "aid": "",
                "sid": "",
                "ouid": "",
                "locale": "en-US",
                "timezone": "5.5",
                "currency": "INR",
                "pageId": "123",
                "vid": "",
                "guid": "",
                "isSSR": False,
                "frontVersion": "1.1.0"
            },
            "hotelExtension": {
                "fingerprint": "",
                "token": ""
            }
        }

        try:
            response = requests.post(endpoint, headers=headers, json=body)
            response.raise_for_status()  # Raise an exception for 4XX and 5XX status codes

            response_content = response.json()

            if 'data' in response_content:
                room_names = response_content['data'].get('physicRoomMap', {})
                hotel_info = response_content['data'].get('saleRoomMap', {})

                for room_id, room in room_names.items():
                    id = room.get("id")
                    name = room.get("name")
                    meal_category = "_"

                    for sale_room_id, sale_room_info in hotel_info.items():
                        physical_room_id = sale_room_info.get('physicalRoomId')

                        if physical_room_id == id:
                            meal_info = sale_room_info.get('mealInfo', {})
                            hover_info = meal_info.get('hover')
                            meal_description = hover_info[0] if hover_info else None

                            if meal_description and "2 guests" in meal_description:
                                if "Full board for 2 guest" in meal_description:
                                    meal_category = "AP"
                                elif "Includes breakfast and dinner for 2 guest" in meal_description:
                                    meal_category = "MAP"
                                elif "Half board for 2 guests" in meal_description:
                                    meal_category = "MAP"
                                elif "Includes breakfast for 2 guests" in meal_description:
                                    meal_category = "CP"
                                else:
                                    meal_category = "EP"

                                if isinstance(meal_description, list):
                                    meal_description = meal_description[0] if meal_description else None
                                
                                price_info = sale_room_info.get('priceInfo', {})
                                rate = price_info.get("price")

                                room_data = {
                                    'roomID': str(id),
                                    "checkIn": (start_date + timedelta(days=k)).strftime("%Y-%m-%d"),
                                    "checkOut": (start_date + timedelta(days=k+1)).strftime("%Y-%m-%d"),
                                    'roomName': name,
                                    'roomPlan': meal_category,
                                    'price': rate
                                }
                                extracted_data.append(room_data)

            print(f'OTA : 9 | Hotel : {hotel_id} | Checkin : {(start_date + timedelta(days=k)).strftime("%Y-%m-%d")} with status : {response.status_code}')
            
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {checkin}: {e}")

    return extracted_data
