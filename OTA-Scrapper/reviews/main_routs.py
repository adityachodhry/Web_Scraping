import json
from flask import Flask, request, jsonify
from agoda_bookingReview import get_agoda_booking_reviews
from mmtReviews import get_mmt_hotel_reviews
from bookingReview import get_booking_reviews
from goibiboReviews import get_goibibo_reviews
import pymongo

app = Flask(__name__)

# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://Retvens:JMdZt2hEPsqHuVQl@r-rate-shopper-cluster.nlstcxk.mongodb.net/")
db = client["ratex"]
collection = db["verifiedproperties"]

def get_all_reviews(agoda_hotelId, mmt_hotelId, goibibo_hotelId):
    reviews = {
        'agoda': get_agoda_booking_reviews(agoda_hotelId),
        'mmt': get_mmt_hotel_reviews(mmt_hotelId),
        # 'booking': get_booking_reviews(booking_hotelSlug),
        'goibibo': get_goibibo_reviews(goibibo_hotelId)
    }

    return reviews

@app.route('/get_reviews', methods=['POST'])
def get_reviews():
    if request.method == 'POST':
        data = request.get_json()
        hId = data.get('hId')

        # Retrieve hotel details from MongoDB
        hotel = collection.find_one({"hId": hId})
        if hotel:
            active_ota = hotel.get('activeOta')
            if active_ota:
                for ota in active_ota:
                    if ota.get('otaId') == 1 :
                        mmt_hotelId = ota.get('otaPId')
                    if ota.get('otaId') == 2 :
                        goibibo_hotelId = ota.get('otaPId')
                    if ota.get('otaId') == 4 :
                        agoda_hotelId = ota.get('otaPId')

            reviews = get_all_reviews(agoda_hotelId, mmt_hotelId, goibibo_hotelId)

            # Save reviews to JSON file
            with open(f"{hId}_reviews.json", "w") as f:
                json.dump(reviews, f)

            return jsonify(reviews)

        return jsonify({"error": "No supported OTA found for the hotel"}), 404
    else:
        return jsonify({"error": "No active OTA found for the hotel"}), 404

if __name__ == '__main__':
    app.run(debug=True)
