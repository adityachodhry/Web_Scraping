import requests
import json

hotel_name = "Amar Kothi"

url = "https://www.cleartrip.com/prefixy/ui/autoSuggest/getSuggestions"

payload = json.dumps({
  "prefix": hotel_name,
  "useCaseContext": "HOTEL_HOME_PAGE"
})
headers = {
  'Content-Type': 'application/json',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  'Accept': '*/*',
  'Accept-Encoding': 'gzip, deflate, br'
}

response = requests.request("POST", url, headers=headers, data=payload)
if response.status_code == 200:
    results = response.json()

    # with open('Row_Data.json', 'w') as json_file:
    #     json.dump(results, json_file)
    
    hotel_info = []

    data_slot = results.get('suggestions')
    
    item = data_slot[0]
    hId = item.get('hotelId')
    hotelName = item.get('hotelName')
    cityName = item.get('cityName')
    url = f"https://www.cleartrip.com/hotels/details/{hId}"

    search_info = {
        'hId': hId,
        'hotelName': hotelName,
        'cityName': cityName,
        'url': url
    }
    hotel_info.append(search_info)
    # print(hotel_info)
    # with open('cleartrip_hotelSearch.json', 'w') as json_file:
    #     json.dump(hotel_info, json_file)