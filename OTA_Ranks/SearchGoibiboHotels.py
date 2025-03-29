import requests
from datetime import datetime, timedelta

def search_and_extract_hotels(mmt_city_code, city_code, checkin=None, checkout=None, next_page=None):
    if checkin is None:
        checkin = datetime.now().strftime("%Y%m%d")
    if checkout is None:
        checkout = (datetime.now() + timedelta(days=1)).strftime("%Y%m%d")

    if next_page is None:
        url = f'https://hermes.goibibo.com/hotels/v13/search/data/v3/{city_code}/{checkin}/{checkout}/1-2-0?s=popularity&cur=INR'
    else:
        url = f"https://hermes.goibibo.com/hotels/v13/search/data/v3/{city_code}/{checkin}/{checkout}/1-2-0/then?s=popularity&cur=INR&next={next_page}&tmz=-330"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Web-Dvid': '307e0603-0b72-469b-a968-01eb2d67a622'
    }

    response = requests.get(url, headers=headers)
    response_data = response.json()

    hotels_info = []
    if "data" not in response_data:
        print("Invalid JSON format. 'data' key not found.")
        return None, None

    next_page = response_data.get('next', '')

    all_hotels = response_data["data"]
    for hotel_info in all_hotels:
        # Extracting specific fields
        hotel_id = hotel_info.get("hc", "")
        hotel_name = hotel_info.get("hn", "")
        star_rating = hotel_info.get("hr", "")
        location = hotel_info.get("l", "")
        rating = hotel_info.get("gr", 0)
        ratings_count = hotel_info.get("grc", 0)
        price = hotel_info.get('spr', 'Sold Out')
        ImgUrls = [Image.split('?')[0] for Image in hotel_info.get('si', [])]

        # Creating a dictionary to store the extracted information
        extracted_info = {
            "otaPId" : hotel_id,
            "Name": hotel_name,
            "Rating": star_rating,
            "Location": location,
            'Price': price,
            'ImageUrls': ImgUrls,
            'DetailLink': f'https://www.goibibo.com/hotels/-{hotel_info.get("hc")}/',
            'ReviewSummary': {
                'RatingScore': rating,
                'RatingCount': ratings_count
            }
        }
        hotels_info.append(extracted_info)

    return hotels_info, next_page

# # Example usage:
# mmt_city_code = "DEL"  # Example MMT city code
# city_code = "6574517509493133854"  # Example city code

# hotels_info, next_page = search_and_extract_hotels(city_code)

