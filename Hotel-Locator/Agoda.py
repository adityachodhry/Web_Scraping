import requests
import datetime

def make_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def get_hotel_url_from_personalization(object_id):
    personalization_url = f"https://www.agoda.com/api/personalization/PersonalizeRecommendedProperties/v1?recommendationType=1&hotelId={object_id}"
    personalization_data = make_request(personalization_url)

    if personalization_data:
        personalized_properties = personalization_data.get("PersonalizedRecommendedProperties", [])

        for property in personalized_properties:
            if property.get("PropertyId") == object_id:
                return property.get("HotelUrl")

    return None

def get_agoda_url(hotel_name, city_name):
    checkin = datetime.datetime.today()
    checkout = checkin + datetime.timedelta(days=1)
    checkin_str = checkin.strftime('%Y-%m-%d')
    checkout_str = checkout.strftime('%Y-%m-%d')

    api_url = f"https://www.agoda.com/api/cronos/search/GetUnifiedSuggestResult/3/1/1/0/en-us/?searchText={hotel_name} {city_name}"

    api_data = make_request(api_url)

    if api_data:
        suggestion_list = api_data.get("SuggestionList", [])

        for suggestion in suggestion_list:
            if suggestion.get("ObjectTypeID") == 7:
                object_id = suggestion.get("ObjectID")
                hotel_url = get_hotel_url_from_personalization(object_id)
                if hotel_url:

                    return f"https://www.agoda.com/en-in{hotel_url}&checkIn={checkin_str}&checkOut={checkout_str}&rooms=1&adults=2&childs=0&priceCur=INR&los=1"

    return None
