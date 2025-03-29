import requests
import json, time

url = "https://www.expedia.co.in/graphql"

payload =  {
        "operationName": "PropertyOffersQuery",
        "variables": {
            "propertyId": "69693650",
            "searchCriteria": {
                "primary": {
                    "dateRange": {
                        "checkInDate": {
                            "day": 7,
                            "month": 3,
                            "year": 2024
                        },
                        "checkOutDate": {
                            "day": 8,
                            "month": 3,
                            "year": 2024
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
                    "rooms": [
                        {
                            "adults": 2,
                            "children": []
                        }
                    ]
                },
                "secondary": {
                    "counts": [],
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
                            "id": "searchId",
                            "value": "132a2866-acf3-4e9e-8fca-405109cf475e"
                        }
                    ],
                    "ranges": []
                }
            },
            "context": {
                "siteId": 27,
                "locale": "en_GB",
                "device": {
                    "type": "DESKTOP"
                }
            }
        },
        "extensions": {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": "573d0f3c7296be18f4a615906061714b05ebedc2e0b22f3e5d1b2919224d8d1d"
            }
        }
    }

headers = {
    "Content-Type":"application/json",
    "Accept-Language":"en-US,en;q=0.9",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Client-Info":"shopping-pwa,unknown,unknown",
    "Accept":"*/*",
    "Accept-Encoding" : "gzip, deflate, br",
}

response = requests.post(url,headers=headers,data={"query":payload})

print(response.status_code)
print(response.text)
