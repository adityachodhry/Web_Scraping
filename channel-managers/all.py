from pymongo import MongoClient
import pandas as pd

# Connect to MongoDB
client = MongoClient("mongodb+srv://Retvens:JMdZt2hEPsqHuVQl@r-rate-shopper-cluster.nlstcxk.mongodb.net/")
db = client['ratex']
collection = db['verifiedproperties']

# Query to filter properties
query = {
    "isActive": True,
    "isRetvens": True
}

# Fetch data from the collection
properties = collection.find(query, {"hId": 1, "propertyName": 1, "_id": 0})

# Convert to DataFrame
data = list(properties)
if data:
    df = pd.DataFrame(data)
    # Save to Excel
    df.to_excel("properties.xlsx", index=False, sheet_name="Properties")
    print("Data saved to properties.xlsx")
else:
    print("No matching records found.")
