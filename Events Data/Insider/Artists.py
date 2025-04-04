import requests
import json
from datetime import datetime

event_data = []
city = 'pune'

api_url = f"https://api.insider.in/tag/getArtistsForCity?city={city}"

# Make the GET request
response = requests.get(api_url)

if response.status_code == 200:

    response_content = response.json()

    # with open('Row_Data.json', 'w') as json_file:
    #     json.dump(response_content, json_file, indent=2)
    
    artists = response_content.get('data', {}).get('artists', [])

    for event in artists:

        e_data = {
            'eventID': event.get('_id'),
            'name': event.get('name'),
            'activeEvents': event.get('active_events'),
            'description': event.get('description')
        }
        event_data.append(e_data)

    # Save the extracted data to a new JSON file
    with open('Event_Data.json', 'w') as json_file:
        json.dump(event_data, json_file, indent=2)
    
else:
    print(f"Error: {response.status_code}")
