from flask import Flask, request, jsonify
from destranet.destranetPropertyList import destranetPropertyList
from cleartrip.cleartripPropertyList import cleartripPropertyList
from agoda.agoda_propertyList import agodaPropertyList
from easeMyTrip.easeMyTrip_propertyList import easeMyTripPropertyList

app = Flask(__name__)

def propertyList(extranetId, username, password):

    if extranetId == 103:
        propertyListData = agodaPropertyList(username, password)
        print("Agoda property list fetched successfully.")
        return propertyListData

    elif extranetId == 104:
        propertyListData = cleartripPropertyList(username, password)
        print("Cleartrip property list fetched successfully.")
        return propertyListData

    elif extranetId == 105:
        propertyListData = destranetPropertyList(username, password)
        print("Destranet property list fetched successfully.")
        return propertyListData

    elif extranetId == 107:
        propertyListData = easeMyTripPropertyList(username, password)
        print("EaseMyTrip property list fetched successfully.")
        return propertyListData

@app.route('/fetch-property-list', methods=['POST'])
def fetch_property_list():
    data = request.json  
    extranetId = data.get('extranetId')
    username = data.get('username')
    password = data.get('password')

    if not all([extranetId, username, password]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        result = propertyList(extranetId, username, password)
        return jsonify({"status": "success", "data": result}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
