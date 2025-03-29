import requests


def get_cleartrip_hotel_url(hotel_name, city):
    url = "https://www.cleartrip.com/prefixy/ui/autoSuggest/getSuggestions"

    data = {
        "prefix": f"{hotel_name} {city}",
        "useCaseContext": "HOTEL_HOME_PAGE"
    }

    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    response = requests.post(url, json=data,headers=headers)

    if response.status_code == 200:
        results = response.json()

        suggestions = results.get("suggestions", [])
        for suggestion in suggestions:
            if suggestion.get("suggestionType") == "HOTEL":
                hotelId = suggestion.get("hotelId")
                hotel_url = f"https://www.cleartrip.com/hotels/details/{hotelId}"
                return hotel_url

    return None  # Return None if the hotel is not found
