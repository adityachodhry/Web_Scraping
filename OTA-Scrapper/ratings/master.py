import json
from pymongo import MongoClient
from mmt import save_mmt_data
from goibibo import save_goibibo_data
from agoda import save_agoda_data

def get_all_rating():
    # Connect to MongoDB
    mongo_client = MongoClient("mongodb+srv://Retvens:JMdZt2hEPsqHuVQl@r-rate-shopper-cluster.nlstcxk.mongodb.net/")
    db = mongo_client["ratex"]
    collection = db["verifiedproperties"]

    rProperties = collection.find()

    for details in rProperties:
        active_ota = details.get("activeOta")
        hId = details["hId"]

        if active_ota:
            for ota in active_ota:
                if ota.get('otaId') == 1:
                    mmthId = ota.get('otaPId')
                elif ota.get('otaId') == 2:
                    gohId = ota.get('otaPId')
                elif ota.get('otaId') == 4:
                    agodahId = ota.get('otaPId')

            # MakeMyTrip
            try:
                mmt_rating = save_mmt_data(hId, mmthId)
                if mmt_rating:
                    with open(f'{hId}_MMT_Ranking.json', 'w') as json_file:
                        json.dump(mmt_rating, json_file, indent=2)
                    print(f"{hId} MMT ranking data saved successfully.")
                else:
                    print(f"{hId} Failed to fetch MMT ranking data.")
            except:
                pass
            
            # Goibibo
            try:
                goibibo_rating = save_goibibo_data(hId, gohId)
                if goibibo_rating:
                    with open(f'{hId}_Goibibo_Ranking.json', 'w') as json_file:
                        json.dump(goibibo_rating, json_file, indent=2)
                    print(f"{hId} Goibibo ranking data saved successfully.")
                else:
                    print(f"{hId} Failed to fetch Goibibo ranking data.")
            except:
                pass

            # Agoda
            try:

                agoda_rating = save_agoda_data(hId, agodahId)
                if agoda_rating:
                    with open(f'{hId}_Agoda_Ranking.json', 'w') as json_file:
                        json.dump(agoda_rating, json_file, indent=2)
                    print(f"{hId} Agoda ranking data saved successfully.")
                else:
                    print(f"{hId} Failed to fetch Agoda ranking data.")
            except:
                pass

get_all_rating()

