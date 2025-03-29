import requests
import json
from datetime import datetime

event_data = []
<<<<<<< HEAD
event_id = '65f93d11f5bc1e000834e2c1'
=======
event_id = '65e4143ac060750008a24ec9'
>>>>>>> 0d790b3bad872e1af938164314ef69d83233d877
api_url = f"https://api.insider.in/home/getRelatedEvents?event_id={event_id}"

# Make the GET request
response = requests.get(api_url)

if response.status_code == 200:
    response_content = response.json()
    with open('Row_Data.json', 'w') as json_file:
        json.dump(response_content, json_file, indent=2)
    
    related = response_content.get('data', [])
    # print(related)
    for event in related:
        min_show_start_time_timestamp = event.get('min_show_start_utc_timestamp')
        # max_show_end_time_timestamp = event.get('max_show_end_time')

<<<<<<< HEAD
        min_show_start_time_timestamp = event.get('min_show_start_time')
        max_show_end_time_timestamp = event.get('max_show_end_time')

        # Convert timestamps to human-readable format
        start_time = datetime.fromtimestamp(min_show_start_time_timestamp).strftime('%Y-%m-%d')
        end_time = datetime.fromtimestamp(max_show_end_time_timestamp).strftime('%Y-%m-%d')
        
            # # Append the extracted data to the list
        e_data = {
            'eventID': event.get('_id'),
            'eventName': event.get('name'),
            'eventStartDateTime': start_time,
            'eventEndDateTime': end_time,
            'eventType': event.get('type')
        }
        event_data.append(e_data)
=======
        if min_show_start_time_timestamp is not None:
            # Convert timestamps to human-readable format
            start_time = datetime.fromtimestamp(min_show_start_time_timestamp).strftime('%Y-%m-%d')
            # end_time = datetime.fromtimestamp(max_show_end_time_timestamp).strftime('%Y-%m-%d')
            
            # Append the extracted data to the list
            e_data = {
                'eventID': event.get('_id'),
                'min_show_start_time': start_time,
                # 'max_show_end_time': end_time,
                'name': event.get('name'),
                'type': event.get('type')
            }
            # print(e_data)
            event_data.append(e_data)
            # print(event_data)
        else:
            print("Skipping event due to missing timestamps:")
    
>>>>>>> 0d790b3bad872e1af938164314ef69d83233d877
    # Save the extracted data to a new JSON file
    with open('Event_Data.json', 'w') as json_file:
        json.dump(event_data, json_file, indent=2)
else:
    print(f"Error: {response.status_code}")
