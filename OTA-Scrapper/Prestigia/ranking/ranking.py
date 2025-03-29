import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

targetid = 138
num_days = 1

today = datetime.now()
room_data = {
    "timestamp": today.strftime("%Y-%m-%d %H:%M:%S"),
    "rates": []
}

for day in range(num_days):
    check_in_date = (today + timedelta(days=day)).strftime("%Y/%m/%d")
    check_out_date = (today + timedelta(days=day + 1)).strftime("%Y/%m/%d")

    url = f"https://www.prestigia.com/en/hotels.php?idTarget={targetid}&checkin={check_in_date}&checkout={check_out_date}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        script_tag = soup.find('script', id='__NUXT_DATA__')

        if script_tag:
            json_data = script_tag.contents[0]

            parsed_data = json.loads(json_data)

            with open('ranking.json', 'w') as json_file:
                json.dump(parsed_data, json_file, indent=4)

        else:
            print("Script tag with id='__NUXT_DATA__' not found")

    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
