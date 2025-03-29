from pymongo import MongoClient
import json

saved_data = None

def push_to_mongodb(data):

    hname = data[0]['hotelName']
    saved_data = data
    json_file_name = f"C:\\Users\\Retvens\\Documents\\HI Automation\\channel-managers\\TempRecords\\{hname}_data.json"
    
    with open(json_file_name, 'w') as json_file:
        json.dump(saved_data, json_file)

    print(f"Data saved to {json_file_name}")

    try:
        mongo_uri = "mongodb+srv://doadmin:3Q47p2nS098GIXe6@r-own-backend-8e41357f.mongo.ondigitalocean.com"
        client = MongoClient(mongo_uri)
        db = client["HDA"]
        collection = db["hotelrecords"]

        collection.insert_many(data)

        print(f"Data pushed to MongoDB.")

    except Exception as e:
        print(f"An error occurred while pushing data to MongoDB: {str(e)}")

    finally:
        if client:
            client.close()