import requests
from bs4 import BeautifulSoup, Comment
import json
import random
from datetime import datetime

def AIC_Events():
    
    event_data = []
    page_no = 1
    country = 'india'

    for page_no in range(1, page_no + 1):
        api_url = f"https://www.allinternationalconference.com/country/{country}-conference/{page_no}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }

        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            event_elements = soup.find_all(class_='confer-featur-top')

            for event in event_elements:
                date_element = event.find('h5')
                date_text = date_element.find_next('span').text.strip() if date_element else None

                if date_text:
                    date_obj = datetime.strptime(date_text, '%Y-%m-%d')
                    formatted_date = date_obj.strftime('%Y-%m-%dT00:00:00.000Z')
                else:
                    formatted_date = None

                location_element = event.find('span', itemprop='areaServed')
                location = location_element.text if location_element else None

                event_name_element = event.find('span', itemprop='name')
                event_name = event_name_element.text if event_name_element else None

                event_id_comment = event.find(string=lambda text: isinstance(text, Comment) and 'Event ID' in text)
                event_id = event_id_comment.split(': ')[1].split('</h6>')[0] if event_id_comment else None

                event_code = random.randint(1000000, 10000000)

                event_info = {
                    'eventId': event_code,
                    "providerEventId": event_id,
                    "eventProviderId": 1061,
                    'eventName': event_name,
                    'eventStartDateTime': {"$date": formatted_date},
                    'eventEndDateTime': {"$date": formatted_date},
                    'eventCityCode': None,
                    'eventCityName': location,
                    "totalOccupancy": None,
                    "eventCategory": "Conference",
                    "eventVenue": None
                }

                event_data.append(event_info)
    
            print(f"Page {page_no} data extracted.")
        else:
            print(f"Failed to fetch data for page {page_no}. Status code: {response.status_code}")

    with open('AIC_Event_Data.json', 'w', encoding='utf-8') as json_file:
        json.dump(event_data, json_file, ensure_ascii=False, indent=2)

    print("All data extracted and saved to JSON file!")

# Call the function to execute the scraping and saving process
# AIC_Events()
