import requests
import json
import random
from datetime import datetime

def get_townscript_events(city_name, city_code, size=10, distance=100, page_no=0):
    # Fetch city data
    city_url = f"https://www.townscript.com/listings/place/city?code={city_name}"
    response_city = requests.get(city_url)

    if response_city.status_code == 200:
        city_data = response_city.json()
        data = city_data.get('data', {})
        lat = data.get('latitude')
        long = data.get('longitude')
    else:
        print(f"Error fetching city data: {response_city.status_code}")
        return None

    # Fetch event data
    api_url = f"https://www.townscript.com/listings/event/radar?lat={lat}&lng={long}&radarDistance={distance}&page={page_no}&size={size}"
    body = {"minScore": 1}
    response = requests.post(api_url, json=body)

    if response.status_code == 200:
        response_content = response.json()
        data = response_content.get('data', {}).get('data', [])

        event_data = []
        for event in data:
            tickets_sold = event.get('ticketsSold')
            tickets_remaining = event.get('ticketsRemaining')
            total_occupancy = int(tickets_sold) + int(tickets_remaining)

            start_time = datetime.fromisoformat(event.get('startTime')).isoformat() + 'Z'
            end_time = datetime.fromisoformat(event.get('endTime')).isoformat() + 'Z'

            event_id = random.randint(1000000, 10000000)
            event_provider_id = str(event.get('eventId'))

            e_data = {
                'eventId': event_id,
                'providerEventId': event_provider_id,
                'eventProviderId': 1011,
                'eventName': event.get('displayName'),
                'eventStartDateTime': {'$date': start_time},
                'eventEndDateTime': {'$date': end_time},
                'eventCityCode': city_code,
                'eventCityName': event.get('city'),
                'totalOccupancy': total_occupancy,
                'eventCategory': None,
                'eventVenue': None
            }
            event_data.append(e_data)

        return event_data
    else:
        print(f"Error fetching event data: {response.status_code}")
        return None

# Example usage
# city_name = 'mussoorie'
# city_code = 'CTXMS'
# events = get_townscript_events(city_name, city_code)

# if events:
#     with open('Mussoorie_Town_Script_Event_Data.json', 'w') as json_file:
#         json.dump(events, json_file, indent=2)
