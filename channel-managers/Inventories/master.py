from asiaTech import asiaTechInventory
from ezeeInventory import getEzeeInventories
from eGlobeInventoryAndRates import eGlobeInventory
from axisRoomsInventory import axisRoomsInventory
from djubo import djuboInventory
from maximojoInventoryAndRates import maximojoInventories
from bjiniInventoryAndRates import getBookingJiniInventory
from staahInventoryAndRates import staahInventory
from resAvenue import resAvenueInventory
from pymongo import MongoClient

client = MongoClient("mongodb+srv://Retvens:JMdZt2hEPsqHuVQl@r-rate-shopper-cluster.nlstcxk.mongodb.net/")
db = client['ratex']
collection = db['channelmanagers']

hId = 293888

channel = collection.find_one({"hId": hId})

if channel:
    property_code = channel.get('channelManagerHotelId')
    print(property_code)
    userCredential = channel.get("userCredential")
    if userCredential:
        username = userCredential.get("username")
        print(username)
        email = userCredential.get("email")
        print(email)
        password = userCredential.get("password")
        print(password)
        accountType = userCredential.get('accountType')

        cmid = channel.get("cmId")
        if cmid is not None:
            if cmid == 101:
                inventory = getEzeeInventories(username, password, property_code)
            elif cmid == 102:
                inventory = djuboInventory(username, password, property_code)
            elif cmid == 103:
                inventory = asiaTechInventory(username, password, property_code)
            elif cmid == 104:
                pass
            elif cmid == 105:
                inventory = eGlobeInventory(username, password, property_code)
            elif cmid == 106:
                inventory = axisRoomsInventory(email, password, property_code)
            elif cmid == 107:
                pass
            elif cmid == 108:
                inventory = staahInventory(email, password, property_code)
            elif cmid == 109:
                inventory = resAvenueInventory(username, password, property_code)
            elif cmid == 110:
                inventory = getBookingJiniInventory(email, password, property_code)
            elif cmid == 111:
                inventory = maximojoInventories(username, password, property_code)
            else:
                print(f'{hId} not in cmid')
        else:
            print("No cmId found for the provided hId.")
    else:
        print("No userCredential found for the provided hId.")
else:
    print("No document found for the provided hId.")
