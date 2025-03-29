import re
import requests
import json
import random
from bs4 import BeautifulSoup
from datetime import datetime

def ACA():
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    url = "https://www.allconferencealert.com/top-conferences-list.html"

    response = requests.get(url, headers=headers)

    # Check if the response is successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        events = []
        event_containers = soup.find_all("div", class_="col-sm-10 pl-1")

        for event in event_containers:
            event_data = {}

            # Get the event name and URL
            event_name_tag = event.find("h5").find("a")
            if event_name_tag:
                event_name = event_name_tag.text
                event_url = event_name_tag["href"]
                event_id = event_url.split('=')[1].split('&')[0]

            # Get the event date
            date_tag = event.find("p")
            if date_tag and "Date :" in date_tag.text:
                date_string = date_tag.text.replace("Date :", "").strip()
                date_string_cleaned = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_string)
                date_string_cleaned = date_string_cleaned.replace(',', ', ')
                date_object = datetime.strptime(date_string_cleaned, "%d %b, %Y")
                event_date = date_object.isoformat() + "Z"

            # Get the event venue
            venue_tag = event.find("div")
            if venue_tag and "Venue :" in venue_tag.text:
                event_venue = venue_tag.text.replace("Venue :", "").strip()
                city_name = event_venue.split(',')[0]

            organizer_tag = event.find("div", text=lambda x: x and "Organized by:" in x)
            if organizer_tag:
                organizer = organizer_tag.find_next("strong").text

            event_code = random.randint(1000000, 10000000)

            # Convert date to required format
            event_start_datetime = {"$date": event_date}

            # Create event data dictionary
            e_data = {
                'eventId': event_code,
                'providerEventId': event_id,
                'eventProviderId': 1051,
                'eventName': event_name,
                'eventStartDateTime': event_start_datetime,
                'eventEndDateTime': event_start_datetime,
                'eventCityName': city_name,
                'eventCityCode': None,
                'totalOccupancy': None,
                'eventCategory': 'Conference',
                'eventVenue': None
            }

            # Add the event data to the events list
            events.append(e_data)
            
        return events
    
    # print("Data Extracted!")

        # Uncomment the following lines to save the events data to a JSON file
        # with open('Mussoorie_ACA_Event_Data.json', 'w', encoding='utf-8') as json_file:
        #     json.dump(events, json_file, ensure_ascii=False, indent=4)

        # Print a message to indicate that data extraction is completed
        

# Call the function to execute the scraping logic and obtain the events data
# extracted_events = ACA()
