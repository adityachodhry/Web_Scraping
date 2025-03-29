import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json

city = "New Delhi"

num_days = 1
today = datetime.now()
rankingData = {
    "timestamp": today.strftime("%Y-%m-%d %H:%M:%S"),
    "ranking": []
}

check_in_date = (today + timedelta(days=num_days)).strftime("%Y/%m/%d")
check_out_date = (today + timedelta(days=num_days + 1)).strftime("%Y/%m/%d")

ranking = 1

url = f"https://onefinerate.com/Search/GetHotelListPartial?cId=177865&cType=city&cName={city}&sCheckIn={check_in_date}&sCheckOut={check_out_date}&sRoomData=%5B%7B%22room%22%3A1%2C%22adult%22%3A2%2C%22child%22%3A0%2C%22ChildAge%22%3A%5B%5D%7D%5D&isSpecialDeal=false"

response = requests.get(url)

if response.status_code == 200:
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    # with open("onefineRating.html", "w", encoding="utf-8")as html_file:
    #     html_file.write(html_content)
    
    hotel_blocks = soup.find_all('div', class_='bookNow showpointer lazy marginbottom20 propertyIdDiv hotel-list-main')

    for hotel in hotel_blocks:
        property_name = hotel['data-propertyname']
        property_id = hotel['data-id']
        price = hotel['data-price']
        star_rating = hotel['data-star']
        tripadvisor_rating = hotel.get('data-tripadvisor', 'N/A')  
        internal_property_id = hotel['data-propertyid']
        sproperty_code = hotel['data-spropertycode']

        rankingData['ranking'].append({
            "hId" : sproperty_code,
            # 'name' : property_name,
            'starRating' : star_rating,
            'ranking' : ranking

        })
        ranking +=1

    with open('ranking_data.json', 'w') as json_file:
        json.dump(rankingData, json_file, indent=4)
