import requests
import datetime

checkin = datetime.datetime.today()
checkout = checkin + datetime.timedelta(days=1)

# Format the dates as strings
checkin_str = checkin.strftime('%m%d%Y')
checkout_str = checkout.strftime('%m%d%Y')

def get_mmt_goibibo_links(hotel_name,city):
    # Get city code
    city_url = f"https://mapi.goibibo.com/autosuggest/v5/search?q={city}"
    city_response = requests.get(city_url)
    city_data = city_response.json()
    city_data = [item for item in city_data if item.get("type") == "city"]
    if not city_data:
        return "City not found"
    city_code = city_data[0].get("cityCode")

    # Get hotel information
    hotel_url = f"https://mapi.goibibo.com/autosuggest/v5/search?q={hotel_name}&c={city_code}&brand=GI"
    hotel_response = requests.get(hotel_url)
    parsed_data = hotel_response.json()

    # Extract information from the response
    hotel_url_list = []
    for item in parsed_data:
        id_value = item["id"]
        city_code = item["cityCode"]
        voy_id = item["voyId"]
        city_name = item["cityName"]

        hotel_name_with_hyphen = hotel_name.replace(" ", "-")

        # Append the extracted information to the list
        hotel_url_list.append({
            "MakeMyTrip" : f"https://www.makemytrip.com/hotels/hotel-details/?checkin={checkin_str}&checkout={checkout_str}&city={city_code}&hotelId={id_value}",
            "Goibibo" : f"https://www.goibibo.com/hotels/{hotel_name_with_hyphen}-hotel-in-{city_name}-{voy_id}"
        })

    return hotel_url_list
