import requests
from bs4 import BeautifulSoup
import json
import time

city = 'taj-lake-palace-udaipur'

url = f"https://{city}.booked.net/"

response = requests.get(url)

if response.status_code == 200:
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # with open("reviews.html", "w", encoding="utf-8")as html_file:
    #     html_file.write(html_content)

    review_count_elem = soup.find("span", {"itemprop": "reviewCount"})

    reviews_count = int(review_count_elem.text.strip())
    rating_elem = soup.find("span", {"itemprop": "ratingValue"})
    rating_value = float(rating_elem.text.strip())
    
    hotel_data = {
        'reviewsCount': reviews_count,
        'reviewsRating': rating_value
    }

with open('reputation.json', 'w') as json_file:
    json.dump(hotel_data, json_file, indent=4)

