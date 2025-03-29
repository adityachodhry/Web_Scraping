import requests
import json
import datetime
import re
from datetime import timedelta, timezone
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup

def scrape_booking_ranks(CityName):

    timestamp = datetime.datetime.now(timezone.utc).isoformat()
    checkin_date = datetime.datetime.now().date()
    checkout_date = checkin_date + timedelta(days=1)

    checkin_date_str = checkin_date.strftime("%Y-%m-%d")
    checkout_date_str = checkout_date.strftime("%Y-%m-%d")

    ranks = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    class BookingRankings:
        rank = 1
        offset_number = 25
        base_url = "https://www.booking.com/searchresults.html"

        @staticmethod
        def parse(html_content):
            soup = BeautifulSoup(html_content, 'html.parser')

            property_cards = soup.select('div[data-testid="property-card-container"]')

            if not property_cards:
                print("No property cards found. Please check the CSS selector.")

            for card in property_cards:
                item = {}

                # item['rank'] = BookingRankings.rank
                BookingRankings.rank += 1

                anchor = card.select_one('a[data-testid="title-link"]')['href']
                parsed_anchor = urlparse(anchor)
                query_params = parse_qs(parsed_anchor.query)
                all_sr_blocks = query_params.get("all_sr_blocks")
                item['otaPId'] = str(all_sr_blocks[0].split("_")[0][:-2])
                

                ranks.append(item)

            next_page = f"{BookingRankings.base_url}?ss={CityName}&ssne={CityName}&checkin={checkin_date_str}&checkout={checkout_date_str}" + f'&offset={BookingRankings.offset_number}/'

            if BookingRankings.offset_number < 100:
                BookingRankings.offset_number += 25
                return next_page

        @staticmethod
        def scrape_data():
            url = f"{BookingRankings.base_url}?ss={CityName}&ssne={CityName}&checkin={checkin_date_str}&checkout={checkout_date_str}"

            response = requests.get(url, headers=headers)

            while response.status_code == 200:
                next_page = BookingRankings.parse(response.content)
                if next_page:
                    response = requests.get(next_page, headers=headers)
                else:
                    break

    # Initialize and run the scraping process
    booking_rankings_instance = BookingRankings()
    booking_rankings_instance.scrape_data()

    print(f'OTA : 3 | Hotel : {CityName} | Checkin : {checkin_date_str}')

    return ranks



    # result_ranks = scrape_booking_ranks(CityName)

# city_name = input("Enter the city name: ")


# output_filename = f"{city_name}_booking_ranks.json"

# with open(output_filename, 'w') as json_file:
#     json.dump(result_ranks, json_file)
