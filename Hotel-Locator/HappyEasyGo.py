import requests

def get_happyEasyGo_Hotel_url(hotel_name, city):
    # Create the URL for the API endpoint
    api_url = f"https://www.happyeasygo.com/hotel_api/web/city?name={hotel_name} {city}"

    # Make a GET request to the API endpoint
    response = requests.get(api_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract relevant information
        hotel_info = data["data"]["cityHotelList"][0]

        code = hotel_info["code"]
        flag = hotel_info["flag"]
        cityName = hotel_info["cityName"]

        # Construct and return the hotel URL
        hotel_url = f"https://hotel.happyeasygo.com/hotels/{cityName}/{flag}_{code}/"
        return hotel_url
    else:
        # Return None if the request was not successful
        print("Error:", response.status_code)
        return None