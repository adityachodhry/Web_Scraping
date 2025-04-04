import requests
import json

event_data = []
#hwhw
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
api_url = "https://api.insider.in/event/getBySlug/ritviz-in-indore-april17-2024"

# Make the GET request
response = requests.get(api_url, headers= headers)

if response.status_code == 200:

    response_content = response.json()

    # with open('Row_Data.json', 'w') as json_file:
    #     json.dump(response_content, json_file, indent=2)
    
    data = response_content.get('data', []).values()
    
    for detail in data:
        
        e_data = {
            'eventId': detail.get('_id'),
            'name': detail.get('name')
        }
        event_data.append(e_data)

    # Save the extracted data to a new JSON file
    with open('Event_Data.json', 'w') as json_file:
        json.dump(event_data, json_file, indent=2)

else:
    print(f"Error: {response.status_code}")

# API expired

