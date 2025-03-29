import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime, timedelta

city = 'Paris'
num_days = 1
today = datetime.now()

check_in_date = (today + timedelta(days=num_days)).strftime("%Y-%m-%d")
check_out_date = (today + timedelta(days=num_days + 1)).strftime("%Y-%m-%d")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
}

room_data = {
    "timestamp": today.strftime("%Y-%m-%d %H:%M:%S"),
    "rates": []
}

page = 1
has_more_pages = True

while has_more_pages:
    url = "https://m.getaroom.com/searches/show?amenities%5B%5D=&check_in=05%2F08%2F2024&check_out=05%2F09%2F2024&destination=Paris&lucky=undefined&page=1&property_name=&rinfo=%5B%5B18%5D%5D&sort_order=undefined"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        script_tags = soup.find_all('script', type='text/javascript')

        data_found = False
        for script in script_tags:
            if 'window.gar.propertySearchResults' in script.text:
                json_pattern = r'window\.gar\.propertySearchResults\s*=\s*({.*?});'
                match = re.search(json_pattern, script.text)
                if match:
                    json_data = match.group(1)
                    property_search_results = json.loads(json_data)
                    data_slot = property_search_results.get('search_results', [])

                    for data in data_slot:
                        room_data['rates'].append({
                            "hId": data.get('uuid'),
                            "starRating": data.get('star_rating'),
                            "ranking": len(room_data['rates']) + 1
                        })
                    data_found = True
    else:
        print("Failed to fetch data for page", page)
        has_more_pages = False