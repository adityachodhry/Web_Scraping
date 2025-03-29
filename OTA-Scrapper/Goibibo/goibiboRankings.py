import requests
import json

endpoint = "https://hermes.goibibo.com/hotels/v13/search/data/v3/6727020267875173073/20240221/20240222/1-2-0/then"


response = requests.get(endpoint)
print(response.text)
if response.status_code == 200:
    response_data = response.json()
    print(response_data)

    with open("goibiboRanksData.json", "w") as json_file:
        json.dump(response_data, json_file, indent=2)
else:
    print(response.status_code)
