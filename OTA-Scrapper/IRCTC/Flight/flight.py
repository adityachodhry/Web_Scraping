import requests
import json
from datetime import datetime, timedelta

departure_city = "Indore"
arrival_city = "Mumbai"
num_days = 10

rates = []

today = datetime.now()

for day in range(num_days):

    departure_date = (today + timedelta(days=day)).strftime("%Y-%m-%d")

    url = "https://www.air.irctc.co.in/airstqcNewUser/air/search"

    body = {
        "tripType": "O",
        "departureDate": departure_date,
        "noOfAdults": "1",
        "noOfChildren": "0",
        "noOfInfants": "0",
        "origin": "IDR",
        "destination": "BOM",
        "destinationCity": arrival_city,
        "originCity": departure_city,
        "classOfTravel": "Economy",
        "airline": "",
        "src": "web",
        "originCountry": "IN",
        "destinationCountry": "IN"
    }
    response = requests.post(url, json=body)

    if response.status_code == 200:
        response_content = response.json()
        
        # with open('flights_raw.json','w') as json_file:
        #     json.dump(response_content, json_file, indent = 4)

        data_slot = response_content.get('data', {})
        flights = data_slot.get('flights', [])

        for flight_details in flights:
            depart_date = flight_details.get('departureDate')
            departure_time = flight_details.get('departureTime')
            arrival_time = flight_details.get('arrivalTime')
            duration = flight_details.get('duration')
            fare_price = flight_details.get('price')

            flight = flight_details.get('lstFlightDetails', [])
            for airline_info in flight:
                airline = airline_info.get('airline')
                flight_num = airline_info.get('flightNumber')

            flight_data = {
                "DepartureDate": depart_date,
                "Airline": airline,
                "FlightNumber": flight_num,
                "DepartureTime": departure_time,
                "ArrivalTime": arrival_time,
                "Duration": duration,
                "FarePrice": fare_price
            }

            rates.append(flight_data)

    final_data = {
        "DepartureCity": departure_city,
        "ArrivalCity": arrival_city,
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "FlightDetails": rates
    }
    print(f"Flight rates stored for {departure_date}")

with open('flight_data.json', 'w') as json_file:
    json.dump(final_data, json_file, indent=4)

