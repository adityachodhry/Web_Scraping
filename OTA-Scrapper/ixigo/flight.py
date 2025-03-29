import requests
import json
from datetime import datetime

url = "https://www.ixigo.com/api/v2/graphs/data/new?origin=IDR&destination=DEL&class=e&startDate=09042024&endDate=09042025&currency=INR"

headers = {'Uuid':'d9f663e044134ba1a765',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}

response = requests.post(url, headers=headers)

if response.status_code == 200:
    response_content = response.json()
    print(json.dumps(response_content, indent=4)) 
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")

