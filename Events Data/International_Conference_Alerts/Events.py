from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime
import random

def International_Events(page_no, month, topic, subtopic, country):

    headers = {
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    current_year = datetime.now().year

    api_url = f"https://internationalconferencealerts.com/pagination/searchfresult/fetch_data?country={country}&topic={topic}&subtopic={subtopic}&month={month}&page={page_no}"

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # with open('Row_Data.html', 'w', encoding='utf-8') as html_file:
        #     html_file.write(response.text)

        t_scroll_element = soup.find('div', class_='t-scroll')
        
        if t_scroll_element:
            event_data = []
            
            conf_list_elements = t_scroll_element.find_all('div', class_='conf-list')
            
            for conf in conf_list_elements:
                event_id = conf['data-val']
                
                # Extract the event name (h3 text), date (h6 text), and location (div class='c-loc')
                h3_text = conf.find('h3').text.strip()
                h5_text = conf.find('h5').text.strip()
                h6_text = conf.find('h6').text.strip()
                location_text = conf.find('div', class_='c-loc').text.strip()
                city_name = location_text.split(',')[0]
                
                # Concatenate the date strings and current year to form a complete date
                event_day_month = f"{h6_text}-{h5_text}-{current_year}"
                event_date = datetime.strptime(event_day_month, "%d-%b-%Y")
                
                # Convert the datetime object to MongoDB's timestamp format
                formatted_date = {
                    "$date": event_date.isoformat() + "Z"
                }
                
                event_code = random.randint(4000000, 40000000)
                
                # Create event data dictionary
                e_data = {
                    'eventId': event_code,
                    'providerEventId': event_id,
                    'eventProviderId': 1041,
                    'eventName': h3_text,
                    'eventStartDateTime': formatted_date,
                    'eventEndDateTime': formatted_date,
                    'eventCityCode': None,
                    'eventCityName': city_name,
                    'totalOccupancy': None,
                    'eventCategory': 'Conference',
                    'eventVenue': None
                }
                event_data.append(e_data)
        
        return event_data
    # International_Events()
    
# page_no = 1
# month = 'null'
# topic = 'null'
# subtopic = 'null'
# country = 'India'

            
#         # Save the extracted data to a JSON file
#         with open('Mussoorie_International_Conference_Alerts_Event_data.json', 'w', encoding='utf-8') as json_file:
#             json.dump(event_data, json_file, indent=2)
        
#         print("Data extracted and saved to International_Conference_Alerts_Event_data.json!")
#     else:
#         print("No element with class 't-scroll' found in the HTML.")
# else:
#     print(f"Error: {response.status_code}")
