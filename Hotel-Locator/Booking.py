import requests
from bs4 import BeautifulSoup

def get_booking_hotel_url(hotel_name, city_name):
    # Define the API endpoint and payload
    autocomplete_url = "https://accommodations.booking.com/autocomplete.json"
    payload = {"query": f"{hotel_name} {city_name}"}

    # Make the POST request
    response = requests.post(autocomplete_url, json=payload)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        result_data = response.json()

        # Extract desired information
        for item in result_data["results"]:
            dest_id = item["dest_id"]
            dest_type = item["dest_type"]
            label = item["label"]

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }

            # Construct the second URL
            search_url = f"https://www.booking.com/searchresults.en-gb.html?ss={label}&dest_id={dest_id}&dest_type={dest_type}"

            # Make a GET request to the second URL
            html_content = requests.get(search_url, headers=headers)

            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(html_content.text, 'html.parser')

            # Find all 'a' tags and get the href attribute
            hrefs = [a['href'] for a in soup.find_all('a', href=True) if 'hpos=1&' in a['href']]

            if hrefs:
                # Extract the URL until ".html"
                index_html = hrefs[0].find(".html")
                url_till_html = hrefs[0][:index_html + len(".html")]

                return url_till_html

    # Return None if no valid URL is found
    return None
