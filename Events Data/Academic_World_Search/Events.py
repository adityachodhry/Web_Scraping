import requests
import json
import random
from bs4 import BeautifulSoup
from datetime import datetime

def academic_world_events(city, city_code):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    event_list = []

    api_url = f"https://academicworldresearch.org/search.php?categories=&location={city}&date="

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # with open('Row_Data.html', 'w', encoding='utf-8') as file:
        #     file.write(str(soup))

        for event_row in soup.find_all('tr', class_=''):
            link_tag = None
            href_value = None
            h3_text = None
            location_text = None
            event_day_month = None
            
            # Attempt to find the 'name' td and its 'a' element
            td_name = event_row.find('td', class_='name')
            if td_name is not None:
                a_tag = td_name.find('a')
                if a_tag:
                    link_tag = a_tag.text.strip()
                    href_value = a_tag.get('href')
            
            if link_tag:
                # Extract event_id from the href attribute if available
                if href_value:
                    event_id = href_value.split('=')[-1]
                else:
                    event_id = None
                
                # Continue with the rest of the extraction
                event_day_month = event_row.find('td', class_='date').text.strip() if event_row.find('td', class_='date') else None
                h3_text = link_tag
                location_text = event_row.find('td', class_='venue').text.strip() if event_row.find('td', class_='venue') else None
                city_name = location_text.split(',')[0]
                event_code = random.randint(1000000, 10000000)

                # Parse and format the date
                if event_day_month:
                    # Assuming `event_day_month` is in the format 'DD-MM-YYYY'
                    date_format = '%d-%m-%Y'
                    date_obj = datetime.strptime(event_day_month, date_format)
                    # Format the date object to ISO 8601 format
                    iso_date = date_obj.strftime('%Y-%m-%dT00:00:00.000Z')
                else:
                    iso_date = None
                
                # Create event data dictionary
                e_data = {
                    "eventId": event_code,
                    "providerEventId": event_id,
                    "eventProviderId": 1071,
                    'eventName': h3_text,
                    'eventStartDateTime': {"$date": iso_date},
                    'eventEndDateTime': {"$date": iso_date},
                    'eventCityCode': city_code,
                    'eventCityName': city_name,
                    "totalOccupancy": None,
                    "eventCategory": 'Conference',
                    "eventVenue": None
                }

                # Append the event data to the list
                event_list.append(e_data)

                # print("All data extracted!")

        return event_list
    else:
        print("Failed to fetch data.")
        return []

# if __name__ == "__main__":
#     city = 'Mussoorie'
#     city_code = 'CTXMS'
#     events = academic_world_events(city, city_code)

#     if events:
#         # Save event details to a JSON file
#         with open('Mussoorie_Academic_World_Search_Event_Data.json', 'w', encoding='utf-8') as file:
#             json.dump(events, file, ensure_ascii=False, indent=4)
#         print("All data extracted!")
