import requests
import json, random
from bs4 import BeautifulSoup
from datetime import datetime

def World_Conference(page_no):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    event_list = []

    api_url = f"https://www.worldconferencealerts.com/india.php?page={page_no}"

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        
        soup = BeautifulSoup(response.text, 'html.parser')

        for event_row in soup.find_all('div', class_='conf-list-detal'):

            eventId = event_row.find('span', class_='span_h2').text.strip().split(':')[1].split()[0] if event_row.find('span', class_='span_h2') else '_'
            eventName = event_row.find('span', itemprop='name').text.strip() if event_row.find('span', itemprop='name') else '_'
            eventLocation = event_row.find('span', itemprop='areaServed').text.strip() if event_row.find('span', itemprop='areaServed') else '_'
            startDate = event_row.find('span', itemprop='startDate').text.strip().split(',')[0].split('-\n ')[0].strip()
            endDate = event_row.find('span', itemprop='startDate').text.strip().split(',')[0].split('-\n ')[1].strip()

            start_date_dt = datetime.strptime(startDate, '%dth %b %Y')
            end_date_dt = datetime.strptime(endDate, '%dth %b %Y')
            
            start_date_iso = start_date_dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            end_date_iso = end_date_dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            
            event_id = random.randint(1000000, 10000000)

            event_data = {
                'eventId': event_id,
                'providerEventId': eventId,
                'eventProviderId': 1021,
                'eventName': eventName,
                'eventStartDateTime': {
                    "$date": start_date_iso
                },
                'eventEndDateTime': {
                    "$date": end_date_iso
                },
                'eventCityCode': None,
                'eventCityName': eventLocation,
                'totalOccupancy': None,
                'eventCategory': 'Conference',
                'eventVenue': None
            }
            event_list.append(event_data)

        print(f"Page {page_no} data extracted.")
    
    else:
        print(f"Failed to fetch data for page {page_no}. Status code: {response.status_code}")

    return event_list

# Fetch data from page 1
# events = World_Conference(1)

# If you want to fetch data from multiple pages, uncomment the loop and add appropriate termination condition.
# page_no = 1
# while True:
#     events += World_Conference(page_no)
#     page_no += 1
#     if termination_condition:
#         break

# # Save event details to a JSON file
# with open('World_Conference_Event_Data.json', 'w', encoding='utf-8') as file:
#     json.dump(events, file, ensure_ascii=False, indent=4)

# print("All data extracted!")
