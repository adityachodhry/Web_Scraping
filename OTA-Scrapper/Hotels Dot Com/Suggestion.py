import requests
import json, time
from urllib.parse import quote

location = "Amar kothi Udaipur"
encoded_location = quote(location)

api_url = f"https://in.hotels.com/api/v4/typeahead/{encoded_location}?client=SearchForm&format=json&listing=false&lob=HOTELS&locale=en_IN&maxresults=8&personalize=true&regiontype=2047"

response = requests.get(api_url)

if response.status_code == 200:
    response_content = response.json()

    with open("hdc_row.json", "w") as json_file:
        json.dump(response_content, json_file, indent=2)
else:
    print(f"Error: {response.status_code}")
