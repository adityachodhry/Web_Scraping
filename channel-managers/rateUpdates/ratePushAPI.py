from flask import Flask, request, jsonify
from maximojoRatesBulkUpdatesAPI import maximojoBulkRatePush
from djuboRatesUpdatesAPI import djuboRatePush
from axisroomRatesUpdate import axisRoom_ratesUpdate
from axisRoomRatesBulkUpdateRoomWise import axisRoomRateBulkUpdate
import threading

app = Flask(__name__)

def update_rates(common_params):
    try:

        # djuboRatePush(**common_params)
        # maximojoBulkRatePush(**common_params)
        # axisRoom_ratesUpdate(**common_params)
        axisRoomRateBulkUpdate(**common_params)

        print("Rates data updated successfully!")
        # return jsonify({"message": "Rates and inventory data updated successfully!"}), 200 
        
    except Exception as e:
        print(f"Error occurred during rate update: {e}")

@app.route('/updateRates', methods=['POST'])
def updateRateAndInventory():
    try:
        data = request.get_json()

        common_params = {
            "username": data.get('username'),
            "password": data.get('password'),
            "propertyCode": data.get('propertyCode'),
            "roomId": data.get('roomId'),
            "roomPlanId": data.get('roomPlanId', ''),
            "mealPlanId": data.get('mealPlanId', ''),
            "channelCode": data.get('channelCode', ''),
            "availability": data.get('availability', ''),
            "rate": data.get('rate', ''),
            "perExtraPerson": data.get('perExtraPerson', ''),
            "extraChildren": data.get('extraChildren', ''),
            "extraChildrenRate": data.get('extraChildrenRate', ''),
            "extraPerson": data.get('extraPerson', ''),
            "extraPersonRate": data.get('extraPersonRate', ''),
            "occupancy": data.get('occupancy', ''),
            "occupancyRate": data.get('occupancyRate', ''),
            "occupancyId": data.get('occupancyId', ''),
            "startDate": data.get('startDate', ''),
            "endDate": data.get('endDate', ''),
            "seasonCode": data.get('seasonCode', ''),
            "roomName": data.get('roomName', ''),
            "rateTypeId": data.get('rateTypeId', ''),
            "displayOrderId": data.get('displayOrderId', ''),
            "selectWeekdays": data.get('selectWeekdays', ''),
            "selectWeekdaysRate": data.get('selectWeekdaysRate', '')
        }

        thread = threading.Thread(target=update_rates, args=(common_params,))
        thread.start()

        return jsonify({"message": "Your rate and inventory data is starting to update"}), 202

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
