import requests
import json
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

# The page number you want to scrape
page_no = 10
city = 'Udaipur'
event_list = []

# Run the loop for only page number 10
api_url = f"https://academicworldresearch.org/scientific-event.php?search={city}&pageno={page_no}"

# Make the GET request
response = requests.get(api_url, headers=headers)

if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract event details from each <tr> element
    for event_row in soup.find_all('tr', class_=''):
        event_day_month = event_row.find('td', class_='date').text.strip() if event_row.find('td', class_='date') else '_'
        h3_text = event_row.find('a').text.strip() if event_row.find('a') else '_'
        location_text = event_row.find('td', class_='venue').text.strip() if event_row.find('td', class_='venue') else '_'

        # Create event data dictionary
        e_data = {
            'eventStartDateTime': event_day_month,
            'eventName': h3_text,
            'eventCityName': location_text
        }
        event_list.append(e_data)

    print(f"Page {page_no} data extracted.")
else:
    print(f"Failed to fetch data for page {page_no}. Status code: {response.status_code}")

# Save event details to a JSON file
with open('Event_Data.json', 'w', encoding='utf-8') as file:
    json.dump(event_list, file, ensure_ascii=False, indent=4)

print("All data extracted!")
