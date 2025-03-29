# import requests
# from bs4 import BeautifulSoup
# import json

# event_data = []
# page_no = 1
# city = 'Mumbai'

# while True:

#     headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
#     'X-Requested-With' : 'XMLHttpRequest'
#     }
    
#     api_url = f"https://www.conferencealerts.in/{city}/page/{page_no}"

#     response = requests.get(api_url, headers=headers)

#     if response.status_code == 200:
#         # Parse the HTML content
#         soup = BeautifulSoup(response.text, 'html.parser')

#         # Save the HTML content to a file
#         with open('Row_Data.html', 'w', encoding='utf-8') as file:
#             file.write(str(soup))

#         events = soup.find_all('td', class_='listing-detal col-md-7')

#         if not events:
            
#             break

#         print(f"Page {page_no} data extracted.")

#         event_details = {
#             'eventName': event_name,
#             'eventStartDateTime': date,
#             'eventCityName': location
#         }

#         # Append the dictionary to the list
#         event_data.append(event_info)

#         # Increment page number for the next request
#         page_no += 1
#     else:
#         print("Failed to fetch conference data. Status code:", response.status_code)
#         break

# # Store the collected data in a JSON file
# with open('Event_Data.json', 'w', encoding='utf-8') as json_file:
#     json.dump(event_data, json_file, indent=2)
