from Agoda import SearchAgodaHotels
from BookingDotCom import SearchBookingHotels
from Goibibo import SearchGoibiboHotels
from Make_My_Trip import SearchMMTHotels
import argparse
from datetime import datetime


def get_agoda_data(city_code):
    result = SearchAgodaHotels.get_hotels_for_city(city_code)
    total_property_count_today, top_properties = SearchAgodaHotels.extract_hotel_info(result)
    return {
        "TotalPropertyCountToday": total_property_count_today,
        "TopProperties": top_properties
    }

def get_booking_data(booking_id):
    data  = SearchBookingHotels.scrape_booking_ranks(booking_id)
    return data

def get_goibibo_data(mmt_city_code,goibibo_id):
    hotelcount,result = SearchGoibiboHotels.search_hotels(mmt_city_code,goibibo_id)
    hotel_info, next_page = SearchGoibiboHotels.extract_hotel_info(result)
    # Run search_hotels_2 up to 10 times
    try :
        for _ in range(10):
            if not next_page:
                break

            result_2 = SearchGoibiboHotels.search_hotels_2(goibibo_id, next_page)
            hotels_info_2, next_page = SearchGoibiboHotels.extract_hotel_info(result_2)
            hotel_info.extend(hotels_info_2)
    except :
        pass
    return {
        "TotalPropertyCountToday": hotelcount,
        "TopProperties": hotel_info
    }

def get_mmt_data(mmt_id):
    filters,hotel_count,result = SearchMMTHotels.search_hotels(mmt_id)
    hotel_info = SearchMMTHotels.extract_hotel_info(result)
    return {
        "Filters" : filters,
        "TotalPropertyCountToday": hotel_count,
        "TopProperties": hotel_info
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get hotel data based on OTA and city code")
    parser.add_argument("--makemytrip", type=str, help="MMT city code")
    parser.add_argument("--goibibo", type=str, help="Goibibo city code")
    parser.add_argument("--booking", type=str, help="Booking.com city code")
    parser.add_argument("--agoda", type=str, help="Agoda city code")

    args = parser.parse_args()

    all_data = {}

    all_data["cityCode"] = args.makemytrip
    all_data["DateStamp"] = datetime.now().strftime("%Y-%m-%d")

    if args.agoda:
        agoda_data = get_agoda_data(args.agoda)
        all_data['Agoda'] = agoda_data

    if args.booking:
        booking_data = get_booking_data(args.booking)
        all_data.update(booking_data)

    if args.goibibo:
        goibibo_data = get_goibibo_data(args.makemytrip,args.goibibo)
        all_data['Goibibo'] = goibibo_data

    if args.makemytrip:
        mmt_data = get_mmt_data(args.makemytrip)
        all_data['MMT'] = mmt_data
