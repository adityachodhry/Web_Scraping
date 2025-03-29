import requests
from bs4 import BeautifulSoup
import json

event_data = []

api_url = "https://www.eventbrite.com/d/india/events/"

response = requests.get(api_url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    with open('Row_Data.html', 'w', encoding='utf-8') as file:
        file.write(str(soup))

    # Find all event titles using BeautifulSoup
    event_titles = []
    for event_title_elem in soup.find_all("h2", class_="Typography_root__487rx #3a3247 Typography_body-lg__487rx event-card__clamp-line--two Typography_align-match-parent__487rx"):
        event_titles.append(event_title_elem.text.strip())

        extracted_data = {
            "eventTitles": event_titles
        }
        event_data.append(extracted_data)

    # Save the event titles as a list to a JSON file
    with open('Event_Data.json', 'w', encoding='utf-8') as json_file:
        json.dump(event_data, json_file, ensure_ascii=False, indent=4)
