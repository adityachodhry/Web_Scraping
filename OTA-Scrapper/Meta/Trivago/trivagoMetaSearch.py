import requests
import json
import datetime

hotel_id = 1357012
hotelName = "Amar_Kothi"
rates = []
today = datetime.datetime.now()
missing_dates = []
num_days = 60
try:
    for day in range(num_days):
        check_in_date = (today + datetime.timedelta(days=day)).strftime("%Y-%m-%d")
        check_out_date = (today + datetime.timedelta(days=day + 1)).strftime("%Y-%m-%d")

        body = {
    "operationName": "accommodationDealsQuery",
    "variables": {
        "pollData": None,
        "getAccommodationDealsParams": {
            "accommodationNsid": {
                "id": hotel_id,
                "ns": 100
            },
            "stayPeriod": {
                "arrival": check_in_date,
                "departure": check_out_date
            },
            "rooms": [
                {
                    "adults": 2,
                    "children": []
                }
            ],
            "tid": "abcd",
            "currency": "INR",
            "priceTypeRestrictions": [
                1
            ],
            "channel": {
                "branded": {
                    "isStandardDate": False,
                    "stayPeriodSource": {
                        "value": 40
                    }
                }
            },
            "deviceType": "DESKTOP_CHROME",
            "uiv": [
                {
                    "nsid": {
                        "ns": 100,
                        "id": 1357012
                    }
                }
            ],
            "applicationGroup": "UNDILUTED",
            "parentRequestId": "",
            "clientSideDecorated": 1,
            "clientApplicationType": 1
        },
        "advertiserLogoParams": {
            "locale": "in"
        },
        "shouldIncludeBedType": True,
        "shouldIncludeFreeWiFiStatus": False,
        "isBomCTestActive": False,
        "shouldIncludeFreeCancellationDeadline": True,
        "includeAllInPrices": False,
        "includeStrikeThroughPrice": True,
        "bookOnMetaDealCheckInput": {
            "rooms": {
                "adults": 2,
                "children": []
            }
        }
    },
    "extensions": {
        "persistedQuery": {
            "version": 1,
            "sha256Hash": "6c16ae963ea7a110ec6377de6dfe82dc1600c0752be600d8e7d4e51dba0e5d59"
        }
    }
}

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "X-Trv-App-Id": "HS_WEB_APP_WARP",  
            "X-Trv-Language": "en-IN",
            "Apollographql-Client-Name": "hs-web-app",
            "Apollographql-Client-Version": "b6595947",
            "Origin": "https://www.trivago.in",
        }

        endpoint = "https://www.trivago.in/graphql?accommodationDealsQuery"

        response = requests.post(endpoint, headers=headers, json=body)

        if response.status_code == 200:
            response_data = response.json()

            with open("trivago.json", "w") as json_file:
                json.dump(response_data, json_file, indent=2)

            accommodationDeals = response_data['data']['getAccommodationDeals']['deals']

            if not accommodationDeals:  # Check if there are no deals for the current date range
                missing_dates.append(check_in_date)
                continue

            for deal in accommodationDeals:
                trivagoOtaID = deal['advertiser']['nsid']['id']
                roomName = deal['description']
                roomID = deal['id']
                price = deal['pricePerNight']['amount']
                meal_plans = deal['enrichedPriceAttributesTranslated']

                for plan in meal_plans:
                    translated_name = plan.get('translatedName', {})

                    if translated_name is None:
                        continue
                    else:
                        value = translated_name['value']
                        if 'Breakfast' in value and 'Lunch' in value and 'Dinner' in value and '/' in translated_name:
                            roomPlan = 'MAP'
                        elif 'Breakfast' in value and 'Lunch' in value and 'Dinner' in value:
                            roomPlan = 'AP'
                        elif 'Breakfast' in value:
                            roomPlan = 'CP'
                        else:
                            roomPlan = 'EP'

                    roomPrices = {
                        "trivagoOtaID": trivagoOtaID,
                        "roomID": roomID,
                        "checkin": check_in_date,
                        "checkout": check_out_date,
                        "roomName": roomName,
                        "roomPlan": roomPlan,
                        "price": price
                    }

                    rates.append(roomPrices)

        else:
            print(response.status_code)
            print(response.text)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    final_data = {
        "hID": "",
        "metaID": 2,
        "propertyID": hotel_id,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d"),
        "rates": rates
    }

    with open(f'{hotelName}_trivago_rates_{datetime.datetime.now().strftime("%Y%m%d")}.json', 'w') as json_file:
        json.dump(final_data, json_file, indent=4)
    
    if missing_dates:
        print(f"missing for {len(missing_dates)} out of {num_days} days")
