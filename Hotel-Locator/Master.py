import json
import concurrent.futures
import time
from gommt import get_mmt_goibibo_links
from Booking import get_booking_hotel_url
from Agoda import get_agoda_url
from EaseMyTrip import get_emt_hotel_url
from Cleartrip import get_cleartrip_hotel_url
from HappyEasyGo import get_happyEasyGo_Hotel_url
from tripDotCom import get_tripDotCom_url

def fetch_url(func, *args):
    return func(*args)

hotel_name_input = "Fairfield"
city_name_input = "Indore"

tasks = [
    (get_booking_hotel_url, hotel_name_input, city_name_input),
    (get_mmt_goibibo_links, hotel_name_input, city_name_input),
    (get_agoda_url, hotel_name_input, city_name_input),
    (get_emt_hotel_url, hotel_name_input, city_name_input),
    (get_cleartrip_hotel_url, hotel_name_input, city_name_input),
    (get_happyEasyGo_Hotel_url, hotel_name_input, city_name_input),
    (get_tripDotCom_url,hotel_name_input, city_name_input)
]

final_url = {}

start_time = time.time()

with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(lambda task: fetch_url(*task), tasks)

for result, task in zip(results, tasks):
    site_name = task[0].__name__.replace('get_', '').replace('_hotel_url', '')
    site_name = ''.join(word.title() for word in site_name.split('_'))  # Convert to title case
    if site_name == 'MmtGoibiboLinks':
        for hotel_info in result:
            for key, value in hotel_info.items():
                final_url[key] = value
    else:
        final_url[site_name] = result

# Change keys
final_url["Agoda"] = final_url.pop("AgodaUrl")
final_url["HappyEasyGo"] = final_url.pop("HappyeasygoHotelUrl")
final_url["EaseMyTrip"] = final_url.pop("Emt")

with open("final_urls.json", "w") as json_file:
    json.dump(final_url, json_file, indent=2)

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution Time: {execution_time} seconds")