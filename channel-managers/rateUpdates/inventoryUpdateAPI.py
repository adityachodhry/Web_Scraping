from flask import Flask, request, jsonify
from maximojoRatesBulkUpdatesAPI import maximojoBulkRatePush
from axisroom_inventory import axisRoom_inventoryUpdate
from axisRoom_inventoryBulkUpdate import axisRoom_inventoryBulkUpdate
from pymongo import MongoClient
import threading

app = Flask(__name__)

def update_inventory(common_params):
    try:

        axisRoom_inventoryUpdate(**common_params)
        axisRoom_inventoryBulkUpdate(**common_params)
        maximojoBulkRatePush(**common_params)

        print("Rates data updated successfully!")
        # return jsonify({"message": "Rates and inventory data updated successfully!"}), 200 
        
    except Exception as e:
        print(f"Error occurred during rate update: {e}")

@app.route('/updateRates/<int:hId>/<string:update_type>', methods=['POST'])
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
            "perExtraPerson": data.get('perExtraPerson', ''),
            "extraChildren": data.get('extraChildren', ''),
            "extraPerson": data.get('extraPerson', ''),
            "occupancy": data.get('occupancy', ''),
            "occupancyId": data.get('occupancyId', ''),
            "startDate": data.get('startDate', ''),
            "endDate": data.get('endDate', ''),
            "seasonCode": data.get('seasonCode', ''),
            "roomName": data.get('roomName', ''),
            "rateTypeId": data.get('rateTypeId', ''),
            "displayOrderId": data.get('displayOrderId', ''),
            "selectWeekdays": data.get('selectWeekdays', '')
        }

        thread = threading.Thread(target=update_inventory, args=(common_params,))
        thread.start()

        return jsonify({"message": "Your rate and inventory data is starting to update"}), 202

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
