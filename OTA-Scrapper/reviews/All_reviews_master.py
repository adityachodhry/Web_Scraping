from pymongo import MongoClient

from master import get_all_reviews

client = MongoClient("mongodb+srv://Retvens:JMdZt2hEPsqHuVQl@r-rate-shopper-cluster.nlstcxk.mongodb.net/")
db = client["ratex"]
collection = db["verifiedproperties"]

rProperties = collection.find({"isRetvens":True,"isActive":True})

for r in rProperties :
    try :
        hId = r.get("hId")
        print(f'{hId }reviews saved')
        
        get_all_reviews(hId)
    except :
        print("Error in hid",hId)