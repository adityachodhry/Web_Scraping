import requests

def get_emt_hotel_url(hotel_name, city):
    url = "https://hotelservice.easemytrip.com/api/HotelService/GetNearByCity"

    data = {
        "CityName": city,
        "name": hotel_name
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        results = response.json()

        areas = results.get("areas", [])
        for area in areas:
            if area.get("tp") == "Hotel":
                name = area.get("nm").lower()
                ecid = area.get("ecid")
                hotel_name_with_hyphen = name.replace(" ", "-")
                hotel_url = f"https://www.easemytrip.com/hotels/{hotel_name_with_hyphen}-{ecid}"
                return hotel_url

    return None  # Return None if the hotel is not found
