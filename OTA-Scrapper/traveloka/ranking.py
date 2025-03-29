import requests
import json
from datetime import datetime, timedelta

num_days = 1
today = datetime.now()
room_data = {
    "timestamp": today.strftime("%Y-%m-%d %H:%M:%S"),
    "rates": []
}

ranking = 1
page = 1
offset = 20  

url = "https://www.traveloka.com/api/v2/hotel/searchList"

headers = {"X-Domain":"accomSearch",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
"Origin":"https://www.traveloka.com",
"Cookie" : "_gcl_au=1.1.1682877213.1712574295; _cs_c=1; _fbp=fb.1.1712574316399.321402342; _tt_enable_cookie=1; _ttp=5GC1QEg243caLr2zwkDfvOI5H9h; countryCode=IN; _gid=GA1.2.1788192069.1713272740; cto_bundle=V83Aw19MUU5zVHBKRVJVY0ZFYUxoQWdVd0s4R1dsMnEyZzd3SyUyQkpuODFyUmxxVUdyc3RiZmY3JTJGWk5ZU1JBUXpmY0szSXNGaVJ0TFpsSENCeldRRXZkcmVIMHBxU1FwRUclMkZYWHN5QmdQOWc0cWE4TVR5VCUyRktsRlJmcDV4VSUyQmFpVWVTVnBKcldWb3VadUQ3VFF2YkVMeDlybDVXJTJGS3F6NkdRY0RuSGhQSWEwJTJGeHY2TUVNVGpISmdIOE1YcyUyRlc0dHI2aWk0eHVsN1JUdm9aeHcyNGZ6N095U2NlZyUzRCUzRA; tv-repeat-visit=true; aws-waf-token=de17caee-4f0b-479a-a546-edc81a7e6cd2:BQoAlkFc6icBAAAA:aP0FJuSGwzYaOyhWP+j5rZ5iBE2hI/6GmTSAtspE9mdZ0k0Cx1YehxEquesUhN0BgWb7rg8BBXq54HRNZFe3lCMtgwK8ToJvZ/WnZStWJif4D7VOzJ1oN3QZMZN51xlnwKApDvkbg/WudKPRV2L7bK3Vvuqg+SGxNQx/3iZGanKOHvQGQT46SmI+x3ciUKE1tkM=; _cs_id=755aa14b-5380-a4d7-bdab-5e5425521ee7.1712574295.6.1713359661.1713359615.1.1746738295902.1; _cs_s=4.5.0.1713361461039; _ga=GA1.2.452047242.1712574296; _ga_RSRSMMBH0X=GS1.1.1713359615.7.1.1713359674.1.0.0; amp_1a5adb=7IOyruSWsUxyYNdt87vghY...1hrm31qs1.1hrm33stf.3u.6.44; amp_f4354c=HFYhkE3fffvc1uGWVENcQq...1hrm31qs4.1hrm33sv6.0.6.6; tvs=iXNnVBXy0007XRdlydZvfMS4O0KLsXs7BRkgVLEe31NvjxyzTerJQTNAtr3jUFw8Dxw9Jv4R+ltIffT94pnGuKLa0YuqbPXvm9Yqf/euvGtduPbG9HWrngyp0K8AtwLL4WJzB9+2JDlfzdlmlrxuNnxFTPgzcwyOYVnIRcL/z8g3ZvdGTAYElvIj+zmayG4mPYhcV7NDbT0qPQKsLh1qY+KtWKu2imYAQUTK1vYL2ydnqsa1oyoXofXGfYYpTK4aoACOYcd7HrhLEVzTa3KyLjIwlyOqEsJdUmU=~djAy; tvl=2eoVRy4Kbf7XZfKrqFEqgxDAJT6G1F3uk4GeJ+uVKgdebqKqmCSB3d3BWBxZeBTV95/1K/cEfIZT8kWNudB3OwpEYoEvmahe1DXCpleOPTK0n4kkzugVoKoeyppCu0NV9hzcOvxXmZYTrdGjOUvTyQQKDWTMuizenbFCIWbBUC/xrYZZSLEvBoLN1IhC1a6LFCld7urI52khKFZ8d7SloWAFk1yvU49qd18O7dhdI4eWbtbYJIh/IXBB5sh1bIon1hZHHFyHG3M=~djAy; _dd_s=rum=0&expire=1713360588577&logs=1&id=1cd5c70f-f6f7-401c-b913-c89d9a10454e&created=1713359612359" }

body ={
    "fields": [],
    "data": {
        "checkInDate": {"year": "2024", "month": "5", "day": "04"},
        "checkOutDate": {"year": "2024", "month": "5", "day": "05"},
        "numOfNights": 1,
        "currency": "USD",
        "numAdults": 1,
        "numChildren": 0,
        "childAges": [],
        "numInfants": 0,
        "numRooms": 1,
        "ccGuaranteeOptions": {
            "ccInfoPreferences": ["CC_TOKEN", "CC_FULL_INFO"],
            "ccGuaranteeRequirementOptions": ["CC_GUARANTEE"]
        },
        "rateTypes": ["PAY_NOW", "PAY_AT_PROPERTY"],
        "isJustLogin": False,
        "backdate": False,
        "geoId": "4002968815",
        "monitoringSpec": {
            "lastKeyword": "Paris",
            "referrer": "https://www.traveloka.com/en-en",
            "searchId": None,
            "searchFunnelType": None,
            "isPriceFinderActive": None,
            "dateIndicator": None,
            "bannerMessage": "",
            "displayPrice": None
        },
        "showHidden": False,
        "locationName": "Paris",
        "sourceType": "HOTEL_GEO",
        "isExtraBedIncluded": True,
        "supportedDisplayTypes": ["INVENTORY", "INVENTORY_LIST", "HEADER", "INVENTORY_WITH_HEADER"],
        "userSearchPreferences": [],
        "uniqueSearchId": None,
        "highlightedHotelId": None,
        "basicFilterSortSpec": {
            "accommodationTypeFilter": [],
            "starRatingFilter": [True, True, True, True, True],
            "facilityFilter": [],
            "hasFreeCancellationRooms": False,
            "minPriceFilter": None,
            "quickFilterId": None,
            "ascending": False,
            "basicSortType": "POPULARITY",
            "chainIds": None,
            "skip": 0,
            "top": 25
        },
        "criteriaFilterSortSpec": None,
        "boundaries": None,
        "contexts": {
            "isFamilyCheckbox": False,
            "abTestPageSpeedVariant": "variant1"
        }
    },
    "clientInterface": "desktop"
}

while True:
    body["data"]["basicFilterSortSpec"]["skip"] = (page - 1) * offset

    response = requests.post(url, headers=headers, json=body)

    if response.status_code == 200:
        response_content = response.json()
        data_slot = response_content.get('data', {}).get('entries', [])

        if not data_slot:
            break  
        for entry in data_slot:
            hotel_data = entry.get('data', {})
            hId = hotel_data.get('id')
            name = hotel_data.get('name')
            rating = hotel_data.get('starRating')

            room_data['rates'].append({
                "roomId": hId,
                "ranking": ranking,
                "name": name,
                "rating": rating
            })

            ranking += 1

        page += 1  
    else:
        print(f"Request failed with status code: {response.status_code}")
        break

with open('ranking_data.json', 'w') as json_file:
    json.dump(room_data, json_file, indent=4)