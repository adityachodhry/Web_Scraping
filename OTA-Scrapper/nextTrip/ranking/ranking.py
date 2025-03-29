import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime, timedelta

num_days = 1
today = datetime.now()
room_data = {
    "timestamp": today.strftime("%Y-%m-%d %H:%M:%S"),
    "rates": []
}

check_in_date = (today + timedelta(days=num_days)).strftime("%Y/%m/%d")
check_out_date = (today + timedelta(days=num_days + 1)).strftime("%Y/%m/%d")

url = f"https://results.nexttrip.com/hotels.php?fd={check_in_date}&td={check_out_date}&hotelTo=Paris%2C+France&ap1=2&rm=1&pt=h&tripType=hotel&areaId=402"

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    scripts = soup.find_all('script')

    for script in scripts:
        if 'staticData' in str(script):
            match = re.search(r'staticData\s*:\s*({[^;]+}})', str(script))
            if match:
                static_data_str = match.group(1)

                static_data = json.loads(static_data_str)

                for key in static_data:
                    entry = static_data[key]
                    uid = entry['uid']
                    starRating = entry['star']
                    ranking = entry['dbRank']
                    
                    # Use 'uid' instead of 'id' here
                    room_data['rates'].append({
                        "hId": uid,
                        'starRating' : starRating,
                        'ranking' : ranking
                    })
                                    
with open('ranking_data.json', 'w') as json_file:
    json.dump(room_data, json_file, indent=4)
