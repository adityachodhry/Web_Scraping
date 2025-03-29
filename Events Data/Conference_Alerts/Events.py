import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
import random

def CA_Events(city, city_code):
    event_data = []

    api_url = "https://www.conferencealerts.in/city_load_pagi_data/"

    target_year = 2024

    page_no = 1

    while True:
        body = {
            "city": city,
            "page": page_no,
            "param2": "",
            "date": ""
        }
        response = requests.post(api_url, data=body)

        # Check the response status code
        if response.status_code != 200:
            print(f"Failed to fetch data for page {page_no}. Status code: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')

        events = soup.find_all('tr', class_='data1')
        if not events:
            break

        # Iterate through each event row and extract data
        for event in events:
            date_str = event.find('td').find('span').text.strip()

            # Convert the date string to a datetime object with the target year
            full_date_str = f"{date_str} {target_year} 00:00:00"
            event_datetime = datetime.strptime(full_date_str, "%d %b %Y %H:%M:%S")

            # Convert the datetime object to ISO 8601 format with milliseconds and UTC timezone
            event_timestamp = {
                "$date": event_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            }

            # Find the first `td` element that contains the `a` tag with the event link
            link_tag = event.find('td').find('a')
            href_value = link_tag['href']
            event_id = href_value.split('=')[-1]

            # Extract event name and location
            event_name = event.find_all('td')[1].find('a').text.strip()
            location = event.find_all('td')[2].find('a').text.strip()
            city_name = location.split(',')[0]

            event_code = random.randint(1000000, 10000000)

            # Create a dictionary for event details
            event_details = {
                'eventId': event_code,
                'providerEventId': event_id,
                'eventProviderId': 1081,
                'eventName': event_name,
                'eventStartDateTime': event_timestamp,
                'eventEndDateTime': event_timestamp,
                'eventCityCode': city_code,
                'eventCityName': city_name,
                'totalOccupancy': None,
                'eventCategory': 'Conference',
                'eventVenue': None
            }

            event_data.append(event_details)

        # Move to the next page
        page_no += 1

        print(f"Page {page_no} data extracted!")

    return event_data

# # Example usage:
# city = 'Mussoorie'
# city_code = 'CTXMS'
# events = CA_Events(city, city_code)
# print(json.dumps(events, indent=2))
