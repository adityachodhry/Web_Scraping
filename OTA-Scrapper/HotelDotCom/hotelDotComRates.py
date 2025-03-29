import requests , json 
from datetime import datetime
import time


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept-Language':'en-US,en;q=0.9',
    # 'Client-Info':'shopping-pwa,unknown,unknown',
    'Connection':'keep-alive',
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate, br'
}
endpoint = 'https://in.hotels.com/graphql'

try:
    get_url = 'https://in.hotels.com/api/v4/typeahead/Amar kothi Udaipur?client=SearchForm&format=json&listing=false&lob=HOTELS&locale=en_IN&maxresults=8&personalize=true&regiontype=2047'

    response = requests.get(get_url, headers=headers)
    print(response.status_code)
    
    # Add a delay of 1 second between requests
    time.sleep(1)

    cookie = response.cookies
    print(cookie)
except requests.RequestException as e:
    print(f"Request failed: {e}")
    print(response.text)
    pass