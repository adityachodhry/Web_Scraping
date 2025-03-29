import json
import requests
from datetime import datetime, timedelta

url = "https://www.zenhotels.com/api/site/multicomplete.json?query=Hotel Amar Kothi, Udaipur&locale=en"

# headers = {
#   'Cookie': '__cf_bm=JG.t4rFfJow7rIuz18eIxnD1847zpd6fqx6rGpZhYtg-1714734404-1.0.1.1-U.rl5FIsJ_a9t4NrZQPnscIrOo3WbNR.rYq3XLrjBYmU8L003LV.wVxt0F7mlD7LSGFkVqI194VHXeX.j0Z.OQ; is_auth=0; sessionid=O9FGaE5zJz_VmnwqZrFS2AR06H4cA0pSrALfz6NMgAY:1s2oGp:CwnN8jvShEdeshM3YaSZVLcrW7V85vctKXwA9y7skjE; uid=TfTb5GY0oAuNAAbqCFreAg==; user_language=en; userlucky=51'
# }

# Get current date
current_date = datetime.now().strftime("%d.%m.%Y")
check_out_date = (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y")

response = requests.request("GET", url)

if response.status_code == 200:
    results = response.json()

    # with open('Row_Data.json', 'w') as json_file:
    #     json.dump(results, json_file, indent=2)

    search_info = []
    
    data = results.get('hotels', [])

    hotel = data[0]

    hotel_id = hotel.get('master_id')
    hotel_name = hotel.get('hotel_name')
    city_name = hotel.get('region_name')
    country_name = hotel.get('country_name')
    city_id = hotel.get('otahotel_id')
    region_id = hotel.get('region_id')

    url = f"https://www.zenhotels.com/hotel/{country_name}/{city_name}/mid{hotel_id}/{city_id}/?q={region_id}&dates={current_date}-{check_out_date}&guests=2"
    # print(url)

    search_details = {
        'hId': hotel_id,
        'hName': hotel_name,
        'cityName': city_name,
        'url': url
    }
    search_info.append(search_details)
    # print(search_info)

    with open('Zen Hotel Search Info', 'w') as json_file:
        json.dump(search_info, json_file, indent=2)
    print('Hotel Search Data Extracted!')
else:
    print("Failed to fetch data. Status code:", response.status_code)
