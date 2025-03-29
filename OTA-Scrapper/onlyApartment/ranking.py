import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json

city = "New Delhi"

num_days = 1
today = datetime.now()
rankingData = {
    "timestamp": today.strftime("%Y-%m-%d %H:%M:%S"),
    "rankingData": []
}

check_in_date = (today + timedelta(days=num_days)).strftime("%Y-%m-%d")
check_out_date = (today + timedelta(days=num_days + 1)).strftime("%Y-%m-%d")

ranking = 1  

url = f"https://only-apartments.com/apartments-in-paris.117549.html?date={check_in_date}&length=1n"

response = requests.get(url)

if response.status_code == 200:
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    ranking_data = []

    hotel_divs = soup.find_all("div", class_="flex-grow-1 col-info wrapper v-box v-box-sm extra-padding marginless")
    price_divs = soup.find_all("div", class_="total-price")
    rating_divs = soup.find_all("span", class_="ratings-oa")
    hotel_id_divs = soup.find_all("div", class_="property row row-full d-flex flew-row")

    for hotel_div, price_div, rating_div, hotel_id_div in zip(hotel_divs, price_divs, rating_divs, hotel_id_divs):
        h5_element = hotel_div.find("h5", class_="with-stars stars_5")
        if h5_element:
            a_element = h5_element.find("a")
            if a_element:
                hotel_name = a_element.text.strip()

                price_span = price_div.find("span", class_="currency-small")
                if price_span:
                    currency = price_span.text.strip()

                price_value = price_div.text.strip().replace(currency, '').replace(',', '')

                rating_value = rating_div.find("strong").text.strip()

                hotel_id = hotel_id_div.get("data-id")

                ranking_data.append({
                    "hId": hotel_id,
                    # "hotelName": hotel_name,
                    "rating": float(rating_value),
                    "ranking": ranking,
                })
                ranking += 1 

with open('ranking_data.json', 'w') as json_file:
    json.dump(ranking_data, json_file, indent=4)
