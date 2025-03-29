import requests
import json
from datetime import datetime, timedelta

city = "bali"
limit = 10

num_days = 1
today = datetime.now()
rankingData = {
    "timestamp": today.strftime("%Y-%m-%d %H:%M:%S"),
    "ranking": []
}

check_in_date = (today + timedelta(days=num_days)).strftime("%Y/%m/%d")
check_out_date = (today + timedelta(days=num_days + 1)).strftime("%Y/%m/%d")

ranking = 1

url = f"https://api.hoterip.com/api/v1/hotels/search?check_in={check_in_date}&check_out={check_out_date}&city={city}&limit=50&number_of_night=1&area=[29,30,31,32,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,58,59,60,126,127,128,129,130,222,256,384,413,424,428,439,440,441,509,982,1210,1237]"

payload = {}
headers = {
  'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
  'Cookie':'AWSALB=1RjBma7P1xXBD9H5vgbdCAFqLGffOAyriLHWTJBE4jOymKLnD4q/cQ3ey0hh6EBK9YRdj4MtjVC84y5rcIldvX8NpmQsomHYJfmep+4br4hWo4liAQK8xZEYyZUQ; AWSALBCORS=1RjBma7P1xXBD9H5vgbdCAFqLGffOAyriLHWTJBE4jOymKLnD4q/cQ3ey0hh6EBK9YRdj4MtjVC84y5rcIldvX8NpmQsomHYJfmep+4br4hWo4liAQK8xZEYyZUQ; XSRF-TOKEN=eyJpdiI6IkprZjN6dlFxR0RnaFgwXC9wNFpSYmJ3PT0iLCJ2YWx1ZSI6IndlalJ0ZU4rY0krSVFoRGZzNFV2TjlYWFdoWWdQS0xvTVNBK3JcL1ZTWUN2YTFUYk16aGEwVkY5OTlYdGFOZXdCIiwibWFjIjoiNDQ1NjdkNjU0NDQ4NDNhOTU3ZmU0NWY0NjRmYWMyYWUwYTNkNzQ1ZDM0ZGNkNjI5NDIxY2FmNzIyMDBjODI1MCJ9; laravel_session=BfBZQETcQYxMtMqf251HrSouzGGl5yL0Gh1LFfS7'
}

response = requests.get(url, headers= headers)
if response.status_code == 200:

    response_content = response.json()
    with open('ranking_raw.json','w') as json_file:
        json.dump(response_content, json_file, indent = 4)

    data_slot = response_content['data']
    for data in data_slot:
        hId = data.get('hotel_id')
        name = data.get('hotel_name')
        starsRating = data.get('stars')
        ranking = ranking

        rankingData['ranking'].append({
            "hId" : hId,
            # 'name' : name,
            'starRating' : starsRating,
            'ranking' : ranking

        })
        ranking +=1

with open('ranking_data.json', 'w') as json_file:
    json.dump(rankingData, json_file, indent=4)




