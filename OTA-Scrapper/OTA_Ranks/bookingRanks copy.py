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

    result_data = {
        "Booking": {
            "TotalPropertyCountToday": 0,
            "TopProperties": []
        }
    }

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

            # Extract the number of properties found
            properties_found_element = soup.find('h1', class_='f6431b446c')
            if properties_found_element:
                properties_found_text = properties_found_element.text
                num_properties_found = re.search(r'\d+', properties_found_text)
                num_properties = int(num_properties_found.group()) if num_properties_found else 0
            else:
                num_properties = 0

            # Store the number of properties found in the JSON
            ranks.append({"TotalPropertyCountToday": num_properties})
            # result_data["Booking"]["TotalPropertyCountToday"] = num_properties

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
                
                # Hotel Name
                name_element = card.select_one('div[data-testid="title"]')
                if name_element:
                    item['Name'] = name_element.text.strip()
                else:
                    item['Name'] = '_'
                
                # # Hotel URL
                # anchor = card.select_one('a.a83ed08757.f88a5204c2.a1ae279108.b98133fb50')['href']
                # parsed_url = urlparse(anchor)
                # hotel_base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
                # item['DetailLink'] = hotel_base_url
                
                # # Extracting hotel image URL
                # image_elements = card.select('img[data-testid="image"]')
                # item['ImageUrls'] = [image['src'] for image in image_elements] if image_elements else '_'


                try:
                    star_category_element = card.select('div[data-testid="rating-stars"] span')
                    item['Rating'] = len(star_category_element) if star_category_element else '-'
                except:
                    item['starCategory'] = '-'

                item['ReviewSummary'] = {}
                user_rating_element = card.select_one('div[data-testid="review-score"] div:nth-child(1)')
                item['ReviewSummary']['RatingScore'] = float(user_rating_element.text) if user_rating_element else '-'

                rating_count_element = card.select_one('div[data-testid="review-score"] div:nth-child(2)')
                raw_rating_count = rating_count_element.text if rating_count_element else '-'

                # Use regular expression to remove non-number characters
                cleaned_rating_count = re.sub(r'\D', '', raw_rating_count)
                item['ReviewSummary']['ReviewCount'] = int(cleaned_rating_count) if cleaned_rating_count else '-'

                # price_element = card.select_one('span[data-testid="price-and-discounted-price"]')
                # item['Price'] = int(price_element.text.split(' ')[1].replace(",", "")) if price_element else '-'

                location_element = card.select_one('span.aee5343fdb.def9bc142a[data-testid="address"]')
                item['Location'] = location_element.text.strip() if location_element else '-'

                result_data["Booking"]["TopProperties"].append(item)


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
