import requests
from bs4 import BeautifulSoup
import json
import datetime
from datetime import timedelta, timezone
from urllib.parse import urlparse, parse_qs

checkin_date = datetime.datetime.now().date() + timedelta(days=1)
checkout_date = checkin_date + timedelta(days=1)

checkin_date_str = checkin_date.strftime("%Y-%m-%d")
checkout_date_str = checkout_date.strftime("%Y-%m-%d")

ranks = []
rank = 1  

def BookingRankings(url, next_page, headers):

    response = requests.get(url, next_page, headers=headers)

    if response.status_code == 200:

        soup = BeautifulSoup(response.content, 'html.parser')
        property_cards = soup.select('div[data-testid="property-card-container"]')
        return property_cards
    
    else:
        print("Failed to fetch property cards")
        return []

def parse_card(card):
    global rank  
    item = {}

    item['rank'] = rank
    rank += 1  

    anchor = card.select_one('a[data-testid="title-link"]')['href']
    parsed_anchor = urlparse(anchor)
    query_params = parse_qs(parsed_anchor.query)
    all_sr_blocks = query_params.get("all_sr_blocks")
    
    if all_sr_blocks:
        item['OtaPId'] = str(all_sr_blocks[0].split("_")[0][:-2])

    ranks.append(item)

def main():
    url = f"https://www.booking.com/searchresults.html?ss=Ahmedabad&checkin={checkin_date_str}&checkout={checkout_date_str}"
    
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }
    offset_number = 0  
    while offset_number <= 100:
        next_page = f"https://www.booking.com/searchresults.html?ss=Ahmedabad&ssne=Indore&checkin={checkin_date_str}&checkout={checkout_date_str}&offset={offset_number}/"
        
        property_cards = BookingRankings(url, next_page, headers)

        for card in property_cards:
            parse_card(card)

        offset_number += 25  

    # Saving data to JSON file
    final_data = {
        "timestamp": str(datetime.datetime.now(timezone.utc)),
        "otaId": 3,
        "cityCode": "CTAMD",
        "ranking": ranks[:100]
    }

    with open('Ahmedabad_hotels_booking_071123.json', 'w', encoding='utf-8') as json_file:
        json.dump(final_data, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()