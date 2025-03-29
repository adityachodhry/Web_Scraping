import requests
import json
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

page_no = 1
# country = 'Mumbai'
event_list = []

# while True:

api_url = f"https://www.worldconferencealerts.com/india.php?page={page_no}"

# Make the GET request
response = requests.get(api_url, headers=headers)

if response.status_code == 200:
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Save the HTML content to a file
    with open('Row_Data.html', 'w', encoding='utf-8') as file:
        file.write(str(soup))

    # Extract event details from each <tr> element
    for event_row in soup.find_all('div', class_='conf-list-detal'):
        # print(event_row)

        eventId = event_row.find('span', class_='span_h2').text.strip().split(':')[1].split()[0] if event_row.find('span', class_='span_h2') else '_'
        eventName = event_row.find('span', itemprop='name').text.strip() if event_row.find('span', itemprop='name') else '_'
        eventLocation = event_row.find('span', itemprop='areaServed').text.strip() if event_row.find('span', itemprop='areaServed') else '_'
        startDate = event_row.find('span', itemprop='startDate').text.strip().split(',')[0].split('-\n ')[0].strip()
        endDate = event_row.find('span', itemprop='startDate').text.strip().split(',')[0].split('-\n ')[1].strip()

        # Create event data dictionary
        e_data = {
            'eventId': eventId,
            'eventName': eventName,
            'startDate': startDate,
            'endDate' : endDate,
            'location': eventLocation
        }
        event_list.append(e_data)

    print(f"Page {page_no} data extracted.")
    page_no += 1

else:
    print(f"Failed to fetch data for page {page_no}. Status code: {response.status_code}")

# Save event details to a JSON file
with open('Event_Data.json', 'w', encoding='utf-8') as file:
    json.dump(event_list, file, ensure_ascii=False, indent=4)

print("All data extracted!")
