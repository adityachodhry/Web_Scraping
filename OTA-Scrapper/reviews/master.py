import json
from flask import Flask, request, jsonify
from agoda_bookingReview import get_agoda_booking_reviews
from mmtReviews import get_mmt_hotel_reviews
from bookingReview import get_booking_reviews
from goibiboReviews import get_goibibo_reviews
import pymongo
from threading import Thread

app = Flask(__name__)

def get_all_reviews(hId):

    client = pymongo.MongoClient("mongodb+srv://Retvens:JMdZt2hEPsqHuVQl@r-rate-shopper-cluster.nlstcxk.mongodb.net/")
    db = client["ratex"]
    collection = db["verifiedproperties"]

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

    reviews = {
        'agoda': get_agoda_booking_reviews(agoda_hotelId),
        'mmt': get_mmt_hotel_reviews(mmt_hotelId),
        # 'booking': get_booking_reviews(booking_hotelSlug),
        'goibibo': get_goibibo_reviews(goibibo_hotelId)
    }
    with open(f"{hId}_reviews.json", "w") as f:
        json.dump(reviews, f)


@app.route('/get_reviews', methods=['POST'])
def get_reviews():
    if request.method == 'POST':
        data = request.get_json()
        hId = data.get('hId')

        # Start a new thread to process events data
        t = Thread(target=get_all_reviews, args=(hId,))
        t.start()
        
        return jsonify({"status": "review collection started"})

if __name__ == '__main__':
    app.run(debug=True)
