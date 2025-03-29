import requests
import json
from datetime import datetime, timedelta

departure_city = "Indore"
arrival_city = "Mumbai"

num_days = 5
today = datetime.now()


output_data = {
    "departure_city": departure_city,
    "arrival_city": arrival_city,
    "timestamp": today.strftime("%Y-%m-%d %H:%M:%S"),
    "bus_info": []
}

for day in range(num_days):
    
    journey_date = today + timedelta(days=day)
    journey_date_str = journey_date.strftime("%d-%m-%Y")

    url = "https://www.bus.irctc.co.in/IrctcBus/api/busmst/getAvailTrip"

    body = {
        "sourceId": "58723",  
        "destId": "23336",   
        "journeyDate": journey_date_str
    }

    response = requests.post(url, json=body)

    if response.status_code == 200:
        response_content = response.json()

        # with open('bus.json','w') as json_file:
        #     json.dump(response_content, json_file, indent = 4)

        data_slot = response_content['data']
        for data in data_slot:
            journeyDate = data.get('journeyDate')
            servicename = data.get('serviceName')
            bustype = data.get('busTypeName')
            depart = data.get('departureTime')
            arrival = data.get('arrivalTime')
            traveltime = data.get('travelTime')
            fare = data.get('fare')
            availableSeat = data.get('availableSeats')

            bus_info = {
                "journeyDate": journeyDate,
                "serviceName": servicename,
                "busTypeName": bustype,
                "departureTime": depart,
                "arrivalTime": arrival,
                "travelTime": traveltime,
                "fare": fare,
                "availableSeats": availableSeat
            }

            output_data['bus_info'].append(bus_info)

       
        with open('bus_info.json', 'w') as json_file:
            json.dump(output_data, json_file, indent=4)

        print(f"Bus information stored for {journey_date_str}")
