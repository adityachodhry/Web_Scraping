import requests
import json

endpoint = "https://www.adanione.com/flight/uimw/api/flight/search?ref=mweb"

originLocation = 'Indore'
destinationLocation = 'Pune'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Agentid': 'cce4ee48-7247-41bc-acac-463aabd55c8c',
    'Traceid': 'QCRmxZNrCZGqwLiDue8MH6HFEUYAAFDe'
}

body = {
    "passengers": [
        {
            "type": "ADT",
            "count": 1
        }
    ],
    "processingInfo": {
        "countryCode": "IN",
        "isSpecialFare": False,
        "sectorInd": "D",
        "tripType": "O"
    },
    "travelPreferences": {
        "farePref": {
            "fareDisplayCurrency": "INR"
        },
        "cabinPref": [
            {
                "cabin": "Economy"
            }
        ]
    },
    "originDestinationInformation": [
        {
            "rph": 1,
            "departureDateTime": {
                "windowAfter": "28-03-2024",
                "windowBefore": "28-03-2024"
            },
            "originLocation": {
                "radius": "",
                "location": originLocation,
                "countryCode": "IN",
                "locationCode": "IDR"
            },
            "destinationLocation": {
                "location": destinationLocation,
                "countryCode": "IN",
                "locationCode": "PNQ"
            }
        }
    ]
}

flight_info = []

try:
    response = requests.post(endpoint, headers=headers, json=body)
    if response.status_code == 200:
        response_content = response.json()
        with open('Row_Data.json', 'w') as json_file:
            json.dump(response_content, json_file, indent=2)
        
        # Print the entire response JSON
        # print(response_content)
        
        data = response_content.get('data', {}).get('results', {}).get('O', [])
        Timing = response_content.get('data', {}).get('results', {}).get('O', [])
        # dTime = response_content.get('data', {}).get('results', {}).get('O', [])[0].get('segs', {})
        departure = response_content.get('data', {}).get('filters', {}).get('labels', {}).get('departO', {}).get('heading', {}).get('desktop')
        arrival = response_content.get('data', {}).get('filters', {}).get('labels', {}).get('arrivalO', {}).get('heading', {}).get('desktop')
        

        for time in Timing:
            w = time.get('segs', {})
            for dot in w.values():
                rates = time.get('price', {}).get('value')
                departure_date = dot.get('dtd', {}).get('dd')
                departure_time = dot.get('dtd', {}).get('dt')
                arrival_date = dot.get('atd', {}).get('ad')
                arrival_time = dot.get('atd', {}).get('at')
                flight_number = dot.get('fn')
                departure_duration = dot.get('du')
                airline = dot.get('airline', {}).get('code')
                airline_name = dot.get('airline', {}).get('name')

                # Concatenating flight number and airline code
                flight_identifier = f"{airline}-{flight_number}"

                details = {
                    'departure': departure,
                    'arrival': arrival,
                    'price': rates,
                    'departureDate': departure_date,
                    'departureTime': departure_time,
                    'arrivalDate': arrival_date,
                    'arrivalTime': arrival_time,
                    'flightNumber': flight_identifier,  
                    'flightDuration': departure_duration,
                    # 'airlineCode': airline,
                    'airlineName': airline_name
                }

                flight_info.append(details)


            # print(flight_info)

        with open('Flights_Data.json', 'w') as json_file:
            json.dump(flight_info, json_file, indent=2)
    else:
        print("Error:", response.status_code)
except requests.RequestException as e:
    print("Request failed:", e)
except json.JSONDecodeError as e:
    print("JSON decoding failed:", e)




# data.results.O[0].price.value
# data.filters.labels.departO.list["0"].id
# data.filters.labels.departO.heading.desktop
# data.filters.labels.arrivalO.heading.desktop
# data.results.O[0].segs["0"].atd