import os
import json
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb+srv://Retvens:JMdZt2hEPsqHuVQl@r-rate-shopper-cluster.nlstcxk.mongodb.net/')
db = client['rateshopper']
collection = db['reputations']

# Specify the directory where your JSON files are located
directory_path = 'Files'

# Loop through files in the directory
for filename in os.listdir(directory_path):
    if filename.endswith(".json"):
        file_path = os.path.join(directory_path, filename)
        
        # Read the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)
            
            hId = data.get('hId')  
            otaId = data.get('otaId') 
            
            if hId and otaId:
                collection.update_one(
                    {'hId': hId, 'otaId': otaId},  
                    {'$set': data},
                    upsert=True          
                )
            else:
                print(f"No keys found in file {filename}")

# Close MongoDB connection
client.close()
