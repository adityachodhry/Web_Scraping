from flask import Flask, request, jsonify
from asiaTech import asiaTechInventory
from ezee import getEzeeReservations
from eGlobe import eGlobeInventory
from axisRooms import axisRoomsInventory
from djubo import djuboInventory
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb+srv://Retvens:JMdZt2hEPsqHuVQl@r-rate-shopper-cluster.nlstcxk.mongodb.net/")
db = client['ratex']
collection = db['channelmanagers']

# Define the POST endpoint
@app.route('/inventory', methods=['POST'])
def get_inventory():
    # Get hId from request body
    data = request.get_json()
    hId = data.get('hId')

    if hId:
        # Fetch channel data based on hId
        channel = collection.find_one({"hId": hId})

        if channel:
            userCredential = channel.get("userCredential")
            if userCredential:
                username = userCredential.get("username")
                password = userCredential.get("password")
                property_code = userCredential.get("propertyCode")
                accountType = userCredential.get('accountType')

                cmid = channel.get("cmId")
                if cmid is not None:
                    # Call respective inventory function based on cmId
                    if cmid == 101:
                        inventory = getEzeeReservations(username, password, property_code)
                    elif cmid == 102:
                        inventory = djuboInventory(username, password)
                    elif cmid == 103:
                        inventory = asiaTechInventory(username, password)
                    elif cmid == 105:
                        inventory = eGlobeInventory(username, password)
                    elif cmid == 106:
                        inventory = axisRoomsInventory(username, password, property_code)
                    else:
                        return jsonify({"error": f"No function specified for cmId: {cmid}"}), 400

                    return jsonify({"status": "Preparing your inventory data"}), 200
                else:
                    return jsonify({"error": "No cmId found for the provided hId."}), 400
            else:
                return jsonify({"error": "No userCredential found for the provided hId."}), 400
        else:
            return jsonify({"error": "No document found for the provided hId."}), 400
    else:
        return jsonify({"error": "hId not provided in request body."}), 400

if __name__ == '__main__':
    app.run(debug=True)
