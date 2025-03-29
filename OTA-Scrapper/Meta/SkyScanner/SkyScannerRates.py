import requests
import json

url = "https://www.skyscanner.co.in/g/hotels-website/api/prices/v2/46992658?adults=2&checkin=2024-02-15&checkout=2024-02-16&currency=INR&locale=en-GB&market=IN&price_type=price-per-night&rooms=1"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}

response = requests.get(url, headers=headers, stream=True)

# Extract JSON data from the event stream
json_data = None
for line in response.iter_lines(decode_unicode=True):
    if line.startswith('data:'):
        json_data = json.loads(line.split('data: ')[1])
        break

# Save the JSON data to a file
with open('output.json', 'w', encoding='utf-8') as json_file:
    json.dump(json_data, json_file, indent=2)

print("JSON data has been saved to output.json")
