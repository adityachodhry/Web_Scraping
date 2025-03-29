import json
import threading
from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime, timedelta

app = Flask(__name__)

def get_url(hId):
    client = MongoClient("mongodb+srv://Retvens:JMdZt2hEPsqHuVQl@r-rate-shopper-cluster.nlstcxk.mongodb.net/")
    db = client['ratex']
    collection = db['verifiedproperties']
    properties = collection.find({'hId': hId})

    # Get current date
    current_date = datetime.now().strftime("%Y-%m-%d")
    check_out_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")


    urls = []
    for property in properties:
        activeOtas = property.get('activeOta')
        for ota in activeOtas:
            otaPId = ota.get("otaPId")
            otaId = ota.get("otaId")
            if otaId == 1:
                link = f"https://www.makemytrip.com/hotels/hotel-details/?hotelId={otaPId}&checkin=05092024&checkout=05112024&city=CTUDR"
            elif otaId == 2:
                link = f"https://www.goibibo.com/hotels/-{otaPId}"
            elif otaId == 5:
                link = f"https://www.cleartrip.com/hotels/details/{otaPId}"
            elif otaId == 6:
                link = f"https://www.easemytrip.com/hotels/EMTHOTEL-{otaPId}"
            elif otaId == 7:
                link = f"https://hotel.happyeasygo.com/hotels/jaipur/hotel_{otaPId}"
            elif otaId == 8:
                link = f"https://www.hrs.com/detail?hn={otaPId}"
            elif otaId == 9:
                link = f"https://www.trip.com/hotels/detail/?hotelId={otaPId}&checkIn={current_date}&checkOut={check_out_date}&adult=2&children=0"
            else:
                link = None 
            if link:
                urls.append(link)
                print(urls)
    return urls

def get_all_url(hId):
    urls = get_url(hId)
    return urls

@app.route('/get_url', methods=['POST'])
def get_rating():
    # Get hId from request body
    request_data = request.get_json()
    hId = request_data.get('hId')

    if hId == hId:
        return jsonify({'status': 'URL generation has started. Please wait...'}), 200

    if not hId:
        return jsonify({'error': 'hId is required in the request body'}), 400

    # Get URLs
    urls = get_all_url(hId)
    
    return jsonify({'urls': urls})

if __name__ == '__main__':
    app.run(debug=True)
