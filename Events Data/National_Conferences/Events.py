import re
import requests
from bs4 import BeautifulSoup
import json
import random
from datetime import datetime, timedelta, date

def national_events(place, city_code):
    
    def get_formatted_date(date):
        return date.strftime('%Y-%m-%d')

    def split_date_and_location(date_and_location):
        parts = date_and_location.split('/')
        date_part = parts[0].strip()
        location_part = parts[1].strip()
        city_name = location_part.split(',')[0].strip()
        return {'date': date_part, 'location': city_name}

    def get_iso_utc_timestamp(date):
        current_time = datetime.utcnow()
        combined_datetime = datetime.combine(date, current_time.time())
        iso_utc_timestamp = combined_datetime.isoformat() + 'Z'
        return iso_utc_timestamp

    event_data = []

    start_date = date.today()
    end_date = datetime(2024, 6, 30)

    current_date = start_date

    while current_date <= end_date.date():
        formatted_date = get_formatted_date(current_date)
        iso_utc_timestamp = get_iso_utc_timestamp(current_date)

        api_url = f"https://nationalconferences.org/conference.php?dt={formatted_date}&place={place}"

        try:
            response = requests.get(api_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            events = soup.find_all('div', class_='psdt')

            for event in events:
                date_and_location = event.find('h3').text.strip()
                split_data = split_date_and_location(date_and_location)

                topic_div = event.find_next_sibling('div', class_='pstopic')
                topic_name = topic_div.find('p').text.strip()
                event_div = topic_div.find('a')
                event_href = event_div.get('href')
                provider_event_id = re.search(r'/(\d+)/', event_href).group(1)

                event_code = random.randint(3000000, 30000000)

                event_data.append({
                    'eventId': event_code,
                    'providerEventId': provider_event_id,
                    'eventProviderId': 1031,
                    'eventName': topic_name,
                    'eventStartDateTime': {
                        "$date": iso_utc_timestamp
                    },
                    'eventEndDateTime': {
                        "$date": iso_utc_timestamp
                    },
                    'eventCityCode': city_code,
                    'eventCityName': split_data['location'],
                    'totalOccupancy': None,
                    'eventCategory': 'Conference',
                    'eventVenue': None
                })
        except requests.RequestException as e:
            print(f"Error fetching data for {formatted_date}: {e}")
        
        current_date += timedelta(days=1)
        print(f"Date {formatted_date} data extracted.")

    return event_data

# Example usage:
# place = 'Mussoorie'
# city_code = 'CTXMS'
# event_data = national_events(place, city_code)

# Save data to JSON file
# with open('Mussoorie_National_Conferences_Event_data.json', 'w', encoding='utf-8') as json_file:
#     json.dump(event_data, json_file, ensure_ascii=False, indent=2)

# print("All Data Extracted Successfully!")
