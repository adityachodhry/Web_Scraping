# import requests
# import json

# event_data = []

# headers = {
#     "X-Requested-With": "XMLHttpRequest",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
# }
# api_url = "https://10times.com/event/search?ajax=1&for=search&q=cricket"
# params = {
#     "ajax": "1",
#     "for": "search",
#     "q": "cricket",
# }

# # Make the GET request
# response = requests.get(api_url, headers=headers, params=params)

# if response.status_code == 200:

#     response_content = response.json()

#     with open('Row_Data.json', 'w') as json_file:
#         json.dump(response_content, json_file, indent=2)
    
# #     data = response_content.get('data', [])

# #     for location in data:

# #         e_data = {
# #             'Id': location.get('id'),
# #             'cityName': location.get('name'),
# #             'country': location.get('country')
# #         }
# #         event_data.append(e_data)
# #     # Save the extracted data to a new JSON file
# #     with open('Event_Data.json', 'w') as json_file:
# #         json.dump(event_data, json_file, indent=2)
    
# else:
#     print(f"Error: {response.status_code}")
