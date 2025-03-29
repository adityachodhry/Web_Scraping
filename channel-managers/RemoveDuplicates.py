from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb+srv://doadmin:3Q47p2nS098GIXe6@r-own-backend-8e41357f.mongo.ondigitalocean.com/HDA?tls=true&authSource=admin&replicaSet=r-own-backend')
db = client['HDA']
collection = db['hotelrecords']

# Step 1: Identify Duplicate Documents and Sort by timestamp in descending order
pipeline = [
    {
        '$sort': {'createdAt': -1}  # Sort in descending order based on the timestamp field
    },
    {
        '$group': {
            '_id': {'hotelName': '$hotelName', 'res': '$res','bookingDate' : '$bookingDate','guestName' : '$guestName','pax':'$pax','hotelCode':'$hotelCode'},
            'count': {'$sum': 1},
            'latest_id': {'$first': '$_id'},  # Select the first (latest) document ID in each group
            'ids': {'$addToSet': '$_id'}
        }
    },
    {
        '$match': {
            'count': {'$gt': 1}  # Filter groups with duplicates
        }
    }
]

duplicates = list(collection.aggregate(pipeline))

# Step 2: Create a List of Duplicate _id values excluding the latest_id
duplicate_ids = []
for group in duplicates:
    duplicate_ids.extend(group['ids'][1:])  # Exclude the first _id (latest_id)

# Log the count of duplicate documents
print("Number of duplicate documents to be deleted:", len(duplicate_ids))

# Step 3: Delete Duplicate Documents
result = collection.delete_many({'_id': {'$in': duplicate_ids}})
print("Deleted", result.deleted_count, "duplicate documents.")
