from flask import Flask, request, jsonify
import json
from datetime import datetime
from BookingDotCom.bookingRanks import scrape_booking_ranks
from EaseMyTrip.EaseMyTripRankings import get_EMT_rankings
from HappyEasyGo.HappyEasyGoRankings import get_HEG_rankings
from HRS.hrsRanks import get_HRS_rankings
from Cleartrip.ClearTripRankings import get_Cleartrip_rankings

app = Flask(__name__)

@app.route('/run_rankings', methods=['POST'])
def run_rankings():
    data = request.json
    city_name = data.get('city_name')
    
    if city_name:
        # Return message before running the code
        response = jsonify({"message": "Your ranking data is prepared"}), 200
        
        # Booking.com Ranks
        BookingDotCom_ranking = scrape_booking_ranks(city_name)

        # Prepare final data for Booking.com
        final_data_bookingDotCom = {
            "timestamp": datetime.now().strftime("%Y-%m-%d"),
            "otaId": 3,
            "cityCode": "CTAMD",
            "ranking": BookingDotCom_ranking[:100]
        }

        with open(f'{city_name}_BookingDotCom_Ranks{datetime.now().strftime("%Y-%m-%d")}.json', 'w') as json_file:
            json.dump(final_data_bookingDotCom, json_file, indent=4)

        # Clear Trip Ranks
        state_name = data.get('state_name', "")
        country_code = data.get('country_code', "")
        cityId = data.get('cityId', "")
        cleartrip_ranking = get_Cleartrip_rankings(city_name, state_name, country_code, cityId)

        # Prepare final data for Cleartrip
        final_data_cleartrip = {
            "timestamp": datetime.now().strftime("%Y-%m-%d"),
            "otaId": 5,
            "cityCode": "CTBHO",
            "ranking": cleartrip_ranking[:100]
        }

        with open(f'{city_name}_Cleartrip_Ranks{datetime.now().strftime("%Y-%m-%d")}.json', 'w') as json_file:
            json.dump(final_data_cleartrip, json_file, indent=4)

        # EaseMyTrip
        EMT_rankings = get_EMT_rankings(city_name)
        
        # Prepare final data for EaseMyTrip
        final_data_emt = {
            "timestamp": datetime.now().strftime("%Y-%m-%d"),
            "otaId": 6,
            "cityCode": "CTIDR",
            "ranking": EMT_rankings[:100]
        }
        
        with open(f'{city_name}_EMT_Ranks_{datetime.now().strftime("%Y-%m-%d")}.json', 'w') as json_file:
            json.dump(final_data_emt, json_file, indent=4)
        
        # HEG.Com
        HEG_rankings = get_HEG_rankings(city_name)

        # Prepare final data for HappyEasyGo
        final_data_HEG = {
            "timestamp": datetime.now().strftime("%Y-%m-%d"),
            "otaId": 7,
            "cityCode": city_name,
            "ranking": HEG_rankings[:100]
        }

        with open(f'{city_name}_HEG_Ranks{datetime.now().strftime("%Y-%m-%d")}.json', 'w') as json_file:
            json.dump(final_data_HEG, json_file, indent=4)

        # HRS Ranking
        locationID = data.get('locationID', "")
        HRS_rankings = get_HRS_rankings(city_name, locationID)

        # Prepare final data for HRS
        final_data_HRS = {
            "timestamp": datetime.now().strftime("%Y-%m-%d"),
            "otaId": 8,
            "cityCode": "CTJAI",
            "ranking": HRS_rankings[:100]
        }

        with open(f'{city_name}_HRS_Ranks{datetime.now().strftime("%Y-%m-%d")}.json', 'w') as json_file:
            json.dump(final_data_HRS, json_file, indent=4)
        
        return response
    else:
        return jsonify({"error": "City name not provided."}), 400

if __name__ == "__main__":
    app.run(debug=True)
