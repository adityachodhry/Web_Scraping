import requests , json 
from datetime import datetime

city = 300000036

body = {
    "variables": {
        "context": {
            "siteId": city,
            "locale": "en_IN",
            "eapid": 36,
            "currency": "INR",
            "device": {
                "type": "DESKTOP"
            },
            "identity": {
                "duaid": "a2997024-cc74-4b89-ab60-474d689bb3dd",
                "expUserId": None,
                "tuid": None,
                "authState": "ANONYMOUS"
            },
            "privacyTrackingState": "CAN_TRACK",
            "debugContext": {
                "abacusOverrides": []
            }
        },
        "criteria": {
            "primary": {
                "dateRange": {
                    "checkInDate": {
                        "day": 29,
                        "month": 1,
                        "year": 2024
                    },
                    "checkOutDate": {
                        "day": 2,
                        "month": 2,
                        "year": 2024
                    }
                },
                "destination": {
                    "regionName": "Bhopal, Madhya Pradesh, India",
                    "regionId": "6130939",
                    "coordinates": {
                        "latitude": 23.259929,
                        "longitude": 77.412613
                    },
                    "pinnedPropertyId": None,
                    "propertyIds": None,
                    "mapBounds": None
                },
                "rooms": [
                    {
                        "adults": 2,
                        "children": []
                    }
                ]
            },
            "secondary": {
                "counts": [
                    {
                        "id": "resultsStartingIndex",
                        "value": 3
                    },
                    {
                        "id": "resultsSize",
                        "value": 97
                    }
                ],
                "booleans": [],
                "selections": [
                    {
                        "id": "sort",
                        "value": "RECOMMENDED"
                    },
                    {
                        "id": "privacyTrackingState",
                        "value": "CAN_TRACK"
                    },
                    {
                        "id": "useRewards",
                        "value": "SHOP_WITHOUT_POINTS"
                    },
                    {
                        "id": "searchId",
                        "value": "46ccb426-c2c4-4293-9408-a72c4b6fb521"
                    }
                ],
                "ranges": []
            }
        },
        "destination": {
            "regionName": None,
            "regionId": None,
            "coordinates": None,
            "pinnedPropertyId": None,
            "propertyIds": None,
            "mapBounds": None
        },
        "shoppingContext": {
            "multiItem": None
        },
        "returnPropertyType": False,
        "includeDynamicMap": False
    },
    "operationName": "LodgingPwaPropertySearch",
    "extensions": {
        "persistedQuery": {
            "sha256Hash": "e4ffcd90dd44f01455f9ddd89228915a177f9ec674f0df0db442ea1b20f551c3",
            "version": 1
        }
    }
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept-Language':'en-US,en;q=0.9',
    'Client-Info':'shopping-pwa,unknown,unknown'
}
endpoint = 'https://in.hotels.com/graphql'

response = requests.post(endpoint , headers=headers,data=body)
print(response.status_code)

try:
    if response.status_code == 200 :
     
        response_data = response.json()
        
        with open("hotelDotCom.json", "w") as json_file:
            json.dump(response_data, json_file, indent=2)

    else : 
        print(response.text)
except requests.RequestException as e:
        print(f"Request failed: {e}")
        print(response.text)
        pass

