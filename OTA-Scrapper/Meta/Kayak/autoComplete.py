import requests
import pymongo
import json

def get_hotel_id(hotel_name):
    url = f"https://www.kayak.co.in/mvm/smartyv2/search?where={hotel_name}"

    response = requests.request("POST", url)
    
    response_data = response.json()

    for r in response_data:
        if r.get('loctype') == 'hotel':
            otapid = r.get('id')
            return otapid  # Return the first hotel id found

    return None  # Return None if no hotel id is found

# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://Retvens:JMdZt2hEPsqHuVQl@r-rate-shopper-cluster.nlstcxk.mongodb.net/")
db = client.rateshopper
collection = db.properties  # Replace 'your_collection' with the actual collection name

# Iterate through documents in the collection
result_list = []

for document in collection.find():
    h_name = document.get('hName')
    h_id = get_hotel_id(h_name)
    
    if h_id:
        print(f"Done for {h_name}")
        result_list.append({"hId": document.get('hId'), "hName": h_name, "hotelId": h_id})

        # Store the result in a JSON format
        with open("result.json", "w") as json_file:
            json.dump(result_list, json_file,indent=2)

# Close MongoDB connection
client.close()
