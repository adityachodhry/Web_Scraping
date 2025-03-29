import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

# Initialize variables
total_iterations = 100
matches_data = []

# Function to extract data from a given URL
def extract_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        dates = soup.find_all('div', class_='cb-col-100 cb-col')
        for date in dates:
            date_element = date.find('div', class_='cb-lv-grn-strip text-bold')
            series = date.find_all('div', class_='cb-col-100 cb-col')
            for series_element in series:
                series_name = series_element.find('a', class_='cb-col-33 cb-col cb-mtchs-dy text-bold').text.strip()
                matches = series_element.find_all('div', class_='cb-ovr-flo cb-col-60 cb-col cb-mtchs-dy-vnu cb-adjst-lst')
                for match in matches:
                    match_element = match.find('a', title=True)
                    location_element = match.find('div', itemprop='location')
                    stadium_element = location_element.find('span', itemprop='name')
                    locality_element = location_element.find('span', itemprop='addressLocality')

                    # Extracting time and timestamp
                    time_element = match.find_next_sibling('div', class_='cb-col-40 cb-col cb-mtchs-dy-tm cb-adjst-lst')
                    timestamp = time_element.find('span', class_='schedule-date')['timestamp']
                    time_text = time_element.find('div', class_='cb-font-12').text.strip()

                    m_data = {
                        'date': date_element.text.strip() if date_element else '_',
                        'series': series_name,
                        'match': match_element.text.strip() if match_element else '_',
                        'stadium': stadium_element.text.strip()[:-1] if stadium_element else '_',
                        'location': locality_element.text.strip() if locality_element else '_',
                        'time': time_text,
                        'timestamp': timestamp
                    }

                    matches_data.append(m_data)

# Initialize timestamp for the first request
timestamp = int(datetime.now().timestamp()) * 1000

# Run the loop for a fixed number of times
for _ in range(total_iterations):
    api_url = f"https://www.cricbuzz.com/cricket-schedule/upcoming-series/all/paginate/{timestamp}/2"
    extract_data(api_url)

    # Update timestamp for the next request
    if matches_data:
        last_match_timestamp = matches_data[-1]['timestamp']
        timestamp = last_match_timestamp

# Save the extracted data to a JSON file
with open('Events_Data.json', 'w') as json_file:
    json.dump(matches_data, json_file, indent=2)
