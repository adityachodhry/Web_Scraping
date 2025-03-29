import requests
import json

def get_via_hotel_url(hotel_name):
    url = "https://in.via.com/apiv2/hotels/hotel-auto"
    params = {
        "gsjr": "true",
        "term": hotel_name,
        "flowType": "NODE",
        "ajax": "true",
        "jsonData": "false"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        results = response.json()

        with open('Row_Data.json', 'w') as json_file:
            json.dump(results, json_file, indent=2)

        if "locations" in results:
            locations = results["locations"]
            if "Hotels" in locations and isinstance(locations["Hotels"], list) and len(locations["Hotels"]) > 0:
                hotel = locations["Hotels"][0]
                return {
                    "hotel_name": hotel.get("label"),
                    "via_id": hotel.get("sdi"),
                    # "url": hotel.get("url")
                }
    return None

def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def main():
    hotel_name = "Amar Kothi Udaipur"
    via_info = get_via_hotel_url(hotel_name)
    if via_info:
        filename = "Hotel_Info.json"
        save_to_json(via_info, filename)
        print(f"Data saved to {filename}")
    else:
        print("No information found for the hotel.")

if __name__ == "__main__":
    main()
