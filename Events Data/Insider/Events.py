import requests
import json
import random
from datetime import datetime

def insider_events(city, event_type, city_code):
    event_data = []
    
    api_url = f"https://api.insider.in/home?city={city}&eventType={event_type}&filterBy=go-out&norm=1&select=lite&typeFilter={event_type}"

    # Make the GET request
    response = requests.get(api_url)

    if response.status_code == 200:
        response_content = response.json()

        data = response_content.get('list', {}).get('masterList', {}).values()
        for event in data:
            min_show_start_time_timestamp = event.get('min_show_start_time')
            max_show_end_time_timestamp = event.get('max_show_end_time')

            # Convert timestamps to human-readable format
            start_time = datetime.fromtimestamp(min_show_start_time_timestamp).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            end_time = datetime.fromtimestamp(max_show_end_time_timestamp).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

            event_id = random.randint(1000000, 10000000)
            # Append the extracted data to the list
            e_data = {
                'eventId': event_id,
                'providerEventId': event.get('_id'),
                'eventProviderId': 1001,
                'eventName': event.get('name'),
                'eventStartDateTime': {"$date": start_time},
                'eventEndDateTime': {"$date": end_time},
                'eventCityCode': city_code,
                'eventCityName': event.get('city'),
                "totalOccupancy": None,
                "eventCategory": event.get('category_id', {}).get('name'),
                'eventVenue': event.get('venue_name')
            }
            event_data.append(e_data)
        
    return event_data

        # # Save the extracted data to a new JSON file
        # filename = f"{city}_Insider_Event_Data.json"
        # with open(filename, 'w') as json_file:
        #     json.dump(event_data, json_file, indent=2)

        # print(f"{city} City Data Extracted and saved to {filename}")
    # else:
    #     print(f"Error: {response.status_code}")

# Example usage:
# city = 'delhi'
# event_type = 'physical'
# city_code = 'CTXMS'

# insider_events()
