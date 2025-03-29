import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta

hotelSlug = 'le-bristol-paris-an-oetker-collection-hotel-lstY1DGZG'

url = f"https://only-apartments.com/paris/{hotelSlug}?date=2024-05-14&length=1n"

response = requests.get(url)

if response.status_code == 200:
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    # with open("reputation.html", "w", encoding="utf-8")as html_file:
    #     html_file.write(html_content)

    details_ratings_div = soup.find('div', class_='details-ratings')

    if details_ratings_div:

        hotels_data = []
        
        review_count_span = details_ratings_div.find('span', itemprop='reviewCount')
        review_count = review_count_span.get_text() if review_count_span else "Review count not available"

        star_rating_span = details_ratings_div.find('span', itemprop='ratingValue')
        star_rating = star_rating_span.get_text(strip=True)

        hotel_data = {
                    'reviewsRating': star_rating,
                    'reviewsCount': review_count
                }
        hotels_data.append(hotel_data)
    else:
        print(f"Failed to retrieve content from {url}")

with open('reputation.json', 'w') as json_file:
    json.dump(hotels_data, json_file, indent=4)