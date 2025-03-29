import requests
import json
import datetime

hotel_id = 307143
ota_list = []  

today = datetime.datetime.now()

for day in range(30):
    check_in_date = (today + datetime.timedelta(days=day)).strftime("%Y-%m-%d")
    check_out_date = (today + datetime.timedelta(days=day + 1)).strftime("%Y-%m-%d")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://www.tripadvisor.com",
        "Referer": "https://www.tripadvisor.com/Hotel_Review-g297672-d307143-Reviews-Taj_Fateh_Prakash_Palace-Udaipur_Udaipur_District_Rajasthan.html"
    }

    body = {
        "variables": {
            "request": {
                "hotelId": hotel_id,
                "trackingEnabled": True,
                "requestCaller": "Hotel_Review",
                "currencyCode": "INR",
                "travelInfo": {
                    "adults": 2,
                    "rooms": 1,
                    "checkInDate": check_in_date,
                    "checkOutDate": check_out_date,
                    "childAgesPerRoom": [],
                    "usedDefaultDates": False
                },
            },
            "locationId": hotel_id
        },
        "extensions": {
            "preRegisteredQueryId": "85323ead4be8e49f"
        }
    }

    endpoint = "https://www.tripadvisor.com/data/graphql/ids"

    response = requests.post(endpoint, json=body, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        with open("tripAdvisor.json", "w") as json_file:
            json.dump(response_data, json_file, indent=2)

        data = response_data['data']

        locations = data['locations']

        for location in locations:
            hotelName = location["name"]

        providerDetails = data['HPS_getWebHROffers']['chevronOffers']

        for provider in providerDetails:
            ota = provider['provider']
            price_text_fk = provider.get('priceTextFK')
            merchandise_messages = provider.get('merchandiseMessages', [])

            if merchandise_messages:
                meal = merchandise_messages[0]['message']

                if 'Breakfast' in meal and 'Lunch' in meal and 'Dinner' in meal and '/' in meal:
                    rplan = 'MAP'
                elif 'Breakfast' in meal and 'Lunch' in meal and 'Dinner' in meal:
                    rplan = 'AP'
                elif 'Breakfast' in meal:
                    rplan = 'CP'
                else:
                    rplan = 'EP'

            if price_text_fk is not None and price_text_fk != "null":
                price = price_text_fk['value']
                ota_dict = {"OTA": ota, "Price": price, "CheckInDate": check_in_date, "CheckOutDate": check_out_date,
                            "roomPlan": rplan}
                ota_list.append(ota_dict)

        hiddenOffers = data['HPS_getWebHROffers']['hiddenOffers']
        for provider in hiddenOffers:
            ota = provider['provider']
            price_text_fk = provider.get('priceTextFK')
            merchandise_messages = provider.get('merchandiseMessages', [])

            if merchandise_messages:
                meal = merchandise_messages[0]['message']

                if 'Breakfast' in meal and 'Lunch' in meal and 'Dinner' in meal and '/' in meal:
                    rplan = 'MAP'
                elif 'Breakfast' in meal and 'Lunch' in meal and 'Dinner' in meal:
                    rplan = 'AP'
                elif 'Breakfast' in meal:
                    rplan = 'CP'
                else:
                    rplan = 'EP'

            if price_text_fk is not None and price_text_fk != "null":
                price = price_text_fk['value']
                ota_dict = {"OTA": ota, "Price": price, "CheckInDate": check_in_date, "CheckOutDate": check_out_date,
                            "roomPlan": rplan}
                ota_list.append(ota_dict)

           
    else:
        print(response.status_code)
        print(response.text)

final_data = ({
                "hID":"",
                "metaID": 1,
                "propertyID":hotel_id,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d"),
                "rates": ota_list
                })

with open("tripAdvisorSearchDetails.json", "w") as json_file:
    json.dump(final_data, json_file, indent=2)
