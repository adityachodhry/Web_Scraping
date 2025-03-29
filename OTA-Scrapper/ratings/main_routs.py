import json 
import threading
from flask import Flask, request, jsonify
from pymongo import MongoClient
from mmt import save_mmt_data
from goibibo import save_goibibo_data
from agoda import save_agoda_data

app = Flask(__name__)

def extract_ratings(hId):
    # Connect to MongoDB
    mongo_client = MongoClient("mongodb+srv://Retvens:JMdZt2hEPsqHuVQl@r-rate-shopper-cluster.nlstcxk.mongodb.net/")
    db = mongo_client["ratex"]
    collection = db["verifiedproperties"]

    # Find property details based on hId
    property_details = collection.find_one({"hId": hId, "isRetvens": True, "isActive": True})

    if not property_details:
        return None

    active_ota = property_details.get("activeOta")

    if not active_ota:
        return None

    mmthId, gohId, agodahId = None, None, None

    for ota in active_ota:
        if ota.get('otaId') == 1:
            mmthId = ota.get('otaPId')
        elif ota.get('otaId') == 2:
            gohId = ota.get('otaPId')
        elif ota.get('otaId') == 4:
            agodahId = ota.get('otaPId')

    # Fetch ratings from each OTA
    mmt_rating = save_mmt_data(hId, mmthId)
    goibibo_rating = save_goibibo_data(hId, gohId)
    agoda_rating = save_agoda_data(hId, agodahId)

    # MakeMyTrip
    if mmt_rating:
        with open(f'{hId}_MMT_Ranking.json', 'w') as json_file:
            json.dump(mmt_rating, json_file, indent=2)
        print(f"{hId} MMT ranking data saved successfully.")
    
    # Goibibo
    if goibibo_rating:
        with open(f'{hId}_Goibibo_Ranking.json', 'w') as json_file:
            json.dump(goibibo_rating, json_file, indent=2)
        print(f"{hId} Goibibo ranking data saved successfully.")
    
    # Agoda
    if agoda_rating:
        with open(f'{hId}_Agoda_Ranking.json', 'w') as json_file:
            json.dump(agoda_rating, json_file, indent=2)
        print(f"{hId} Agoda ranking data saved successfully.")
        

def get_all_rating(hId):
    # Start a new thread to extract ratings data
    extraction_thread = threading.Thread(target=extract_ratings, args=(hId,))
    extraction_thread.start()

    return {"status": "rating collection started"}

@app.route('/get_rating', methods=['POST'])
def get_rating():
    # Get hId from request body
    request_data = request.get_json()
    hId = request_data.get('hId')

    if not hId:
        return jsonify({'error': 'hId is required in the request body'}), 400

    # Get status message
    status_message = get_all_rating(hId)
    
    return jsonify(status_message)

if __name__ == '__main__':
    app.run(debug=True)
