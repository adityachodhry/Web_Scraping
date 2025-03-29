import json
from datetime import datetime
from SearchMMTHotels import get_filtered_hotels_info
from SearchGoibiboHotels import search_and_extract_hotels
from bookingRanks import scrape_booking_ranks
from SearchAgodaHotels import get_and_extract_hotels
from EaseMyTripRankings import get_EMT_rankings
from HappyEasyGoRankings import get_HEG_rankings
from hrsRanks import get_HRS_rankings
from ClearTripRankings import fetch_cleartrip_hotel_rankings

def main():

<<<<<<< HEAD
    # # MMT Ranks
    # city_code = "CTUDR"
    # filters, total_property_count, MMT_ranking = get_filtered_hotels_info(city_code)

    # # Prepare final data for MMT
    # final_data_MMT = {
    #     "timestamp": datetime.now().strftime("%Y-%m-%d"),
    #     "otaId": 1,
    #     "cityCode": "CTUDR",
    #     "TotalPropertyCountToday": total_property_count,
    #     "rankings": MMT_ranking[:100]
    # }
=======
    # MMT Ranks
    city_code = "CTUDR"
    filters, total_property_count,MMT_ranking = get_filtered_hotels_info(city_code)

    # Prepare final data for MMT
    final_data_MMT = {
        "timestamp": datetime.now().strftime("%Y-%m-%d"),
        "otaId": 1,
        "cityCode": "CTUDR",
        "filters" : filters,
        "totalPropertyCount" : total_property_count,
        "ranking": MMT_ranking
    }
>>>>>>> 658ef70d1d68efdb4da6a56a82a28635a936a16c

    # with open(f'{city_code}_MMT_Ranks_{datetime.now().strftime("%Y-%m-%d")}.json', 'w') as json_file:
    #     json.dump(final_data_MMT, json_file, indent=4)

<<<<<<< HEAD
    # # Goibibo Ranks
    # mmt_city_code = "CTUDR"
    # city_code = 3369724356477798574
    # Goibibo_ranking = search_and_extract_hotels(mmt_city_code, city_code)

    # # Prepare final data for MMT
    # final_data_Goibibo = {
    #     "timestamp": datetime.now().strftime("%Y-%m-%d"),
    #     "otaId": 2,
    #     "cityCode": "CTUDR",
    #     "rankings": Goibibo_ranking[:100]
    # }

    # with open(f'{mmt_city_code}_Goibibo_Ranks{datetime.now().strftime("%Y-%m-%d")}.json', 'w') as json_file:
    #     json.dump(final_data_Goibibo, json_file, indent=4)
=======
    # Goibibo Ranks
    city_code = 3369724356477798574
    ranks = []
    Goibibo_ranking,next = search_and_extract_hotels(city_code)
    ranks.extend(Goibibo_ranking)
    while True :
        try :
            Goibibo_ranking,next = search_and_extract_hotels(city_code,next_page=next)
            ranks.extend(Goibibo_ranking)
        except :
            break

    # Prepare final data for MMT
    final_data_Goibibo = {
        "timestamp": datetime.now().strftime("%Y-%m-%d"),
        "otaId": 2,
        "cityCode": "CTUDR",
        "ranking": ranks
    }

    with open(f'{city_code}_Goibibo_Ranks{datetime.now().strftime("%Y-%m-%d")}.json', 'w') as json_file:
        json.dump(final_data_Goibibo, json_file, indent=4)
>>>>>>> 658ef70d1d68efdb4da6a56a82a28635a936a16c

    # # Booking.com Ranks
    # CityName = "Ahmedabad"
    # BookingDotCom_ranking, num_properties = scrape_booking_ranks(CityName)

<<<<<<< HEAD
    # # Prepare final data for Booking.com
    # final_data_bookingDotCom = {
    #     "timestamp": datetime.now().strftime("%Y-%m-%d"),
    #     "otaId": 3,
    #     "cityCode": "CTAMD",
    #     "TotalPropertyCountToday": num_properties,
    #     "rankings": BookingDotCom_ranking[:100]
    # }
=======
    # Prepare final data for Booking.com
    final_data_bookingDotCom = {
        "timestamp": datetime.now().strftime("%Y-%m-%d"),
        "otaId": 3,
        "cityCode": "CTAMD",
        "ranking": BookingDotCom_ranking
    }
>>>>>>> 658ef70d1d68efdb4da6a56a82a28635a936a16c

    # with open(f'{CityName}_BookingDotCom_Ranks{datetime.now().strftime("%Y-%m-%d")}.json', 'w') as json_file:
    #     json.dump(final_data_bookingDotCom, json_file, indent=4)
        
    # # Agoda Ranks
    # city_id = "3667"
    # total_properties, Agoda_ranking = get_and_extract_hotels(city_id)  # Call the function and capture total properties and rankings

<<<<<<< HEAD
    # # Prepare final data for Agoda
    # final_data_Agoda = {
    #     "timestamp": datetime.now().strftime("%Y-%m-%d"),
    #     "otaId": 4,
    #     "cityCode": city_id,  # Assuming city_id is the city code
    #     "TotalPropertyCountToday": total_properties,  # Add the total properties here
    #     "rankings": Agoda_ranking[:100]  # Assuming you want the top 100 rankings
    # }
=======
    # Prepare final data for Agoda
    final_data_Agoda = {
        "timestamp": datetime.now().strftime("%Y-%m-%d"),
        "otaId": 4,
        "cityCode": 12345,
        "ranking": Agoda_ranking
    }
>>>>>>> 658ef70d1d68efdb4da6a56a82a28635a936a16c

    # with open(f'{city_id}_Agoda_Ranks{datetime.now().strftime("%Y-%m-%d")}.json', 'w') as json_file:
    #     json.dump(final_data_Agoda, json_file, indent=4)

    # # Clear Trip Ranks
    # city_name = "Indore"
    # state_name = "Madhya Pradesh"
    # country_code = "IN"
    # cityId = "33923"

<<<<<<< HEAD
    # hotel_count, cleartrip_ranking = fetch_cleartrip_hotel_rankings(city_name, state_name, country_code, cityId)
=======
    # Prepare final data for Cleartrip
    final_data_cleartrip = {
        "timestamp": datetime.now().strftime("%Y-%m-%d"),
        "otaId": 5,
        "cityCode": "CTBHO",
        "ranking": cleartrip_ranking
    }
>>>>>>> 658ef70d1d68efdb4da6a56a82a28635a936a16c

    # # Prepare final data for Cleartrip
    # final_data_cleartrip = {
    #     "timestamp": datetime.now().strftime("%Y-%m-%d"),
    #     "otaId": 5,
    #     "cityCode": "CTBHO",
    #     "TotalPropertyCountToday": hotel_count,
    #     "rankings": cleartrip_ranking
    # }

    # with open(f'{city_name}_Cleartrip_Ranks{datetime.now().strftime("%Y-%m-%d")}.json', 'w') as json_file:
    #     json.dump(final_data_cleartrip, json_file, indent=4)

    # # EaseMyTrip
    # CityName = "Indore"
    # EMT_rankings = get_EMT_rankings(CityName)
    
<<<<<<< HEAD
    # # Prepare final data for EaseMyTrip
    # final_data_emt = {
    #     "timestamp": datetime.now().strftime("%Y-%m-%d"),
    #     "otaId": 6,
    #     "cityCode": "CTIDR",
    #     "rankings": EMT_rankings[:100]
    # }
=======
    # Prepare final data for EaseMyTrip
    final_data_emt = {
        "timestamp": datetime.now().strftime("%Y-%m-%d"),
        "otaId": 6,
        "cityCode": "CTIDR",
        "ranking": EMT_rankings
    }
>>>>>>> 658ef70d1d68efdb4da6a56a82a28635a936a16c
    
    # with open(f'{CityName}_EMT_Ranks_{datetime.now().strftime("%Y-%m-%d")}.json', 'w') as json_file:
    #     json.dump(final_data_emt, json_file, indent=4)
    
    # HEG.Com
    cityName = 'Udaipur'
    HEG_rankings = get_HEG_rankings(cityName)

    # Prepare final data for HappyEasyGo
    final_data_HEG = {
        "timestamp": datetime.now().strftime("%Y-%m-%d"),
        "otaId": 7,
        "cityCode": cityName,
<<<<<<< HEAD
        "rankings": HEG_rankings[:100]
=======
        "ranking": HEG_rankings
>>>>>>> 658ef70d1d68efdb4da6a56a82a28635a936a16c
    }

    with open(f'{cityName}_HEG_Ranks{datetime.now().strftime("%Y-%m-%d")}.json', 'w') as json_file:
        json.dump(final_data_HEG, json_file, indent=4)

    # # HRS Ranking
    # cityName = "Berlin"
    # locationID = 55133
    # HRS_rankings = get_HRS_rankings(cityName, locationID)

<<<<<<< HEAD
    # # Prepare final data for HRS
    # final_data_HRS = {
    #     "timestamp": datetime.now().strftime("%Y-%m-%d"),
    #     "otaId": 8,
    #     "cityCode": "CTJAI",
    #     "rankings": HRS_rankings[:100]
    # }
=======
    # Prepare final data for HRS
    final_data_HRS = {
        "timestamp": datetime.now().strftime("%Y-%m-%d"),
        "otaId": 8,
        "cityCode": "CTJAI",
        "ranking": HRS_rankings
    }
>>>>>>> 658ef70d1d68efdb4da6a56a82a28635a936a16c

    # with open(f'{cityName}_HRS_Ranks{datetime.now().strftime("%Y-%m-%d")}.json', 'w') as json_file:
    #     json.dump(final_data_HRS, json_file, indent=4)

    
if __name__ == "__main__":
    main()
