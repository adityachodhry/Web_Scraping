import json
from datetime import datetime
from EaseMyTrip.easeMyTrip import final
# from HappyEasyGo.HappyEasyGoRates import get_hotel_rates
from HRS.hrsRates import fetch_hotel_rates
from Trip_Dot_Com.TripDotComRates import extract_hotel_data

def main():

    # # EaseMyTrip
    # hId = 20401
    # hotel_id = "1612961"
    # results_ease_my_trip = final(hotel_id)

    # final_data_emt = {
    #     "hId": hId,
    #     "otaId": 6,
    #     "otaPId": str(hotel_id),
    #     "timestamp": datetime.now().strftime("%Y-%m-%d"),
    #     "rates": results_ease_my_trip
    # }
    # with open(f'{hotel_id}_emt_rates_{datetime.now().strftime("%Y%m%d")}.json', 'w') as json_file:
    #     json.dump(final_data_emt, json_file, indent=4)

    # # HRS
    # hId = 20401
    # hotelID = 1068815
    # hotelName = "Regenta"
    # results_hrs = fetch_hotel_rates(hotelID, hotelName)

    # final_data_hrs = {
    #     "hId": hId,
    #     "otaId": 8,
    #     "otaPId": str(hotelID),
    #     "timestamp": datetime.now().strftime("%Y-%m-%d"),
    #     "rates": results_hrs
    # }
    # with open(f'{hotelName}_hrs_rates_{datetime.now().strftime("%Y%m%d")}.json', 'w') as json_file:
    #     json.dump(final_data_hrs, json_file, indent=4)

    # Trip.Com
    hId = 20401
    hotel_id = 47374272
    cityId = 36121
    results_trip_com = extract_hotel_data(hotel_id, cityId)

    final_data_trip_dot_com = {
        "hId": hId,
        "otaId": 9,
        "otaPId": str(hotel_id),
        "timestamp": datetime.now().strftime("%Y-%m-%d"),
        "rates": results_trip_com
    }
    with open(f'{hotel_id}_trip_com_rates_{datetime.now().strftime("%Y%m%d")}.json', 'w') as json_file:
        json.dump(final_data_trip_dot_com, json_file, indent=4)

if __name__ == "__main__":
    main()
