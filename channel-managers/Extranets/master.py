from destranet.destranetPropertyList import destranetPropertyList
from cleartrip.cleartripPropertyList import cleartripPropertyList
from agoda.agoda_propertyList import agodaPropertyList
from easeMyTrip.easeMyTrip_propertyList import easeMyTripPropertyList


def propertyList(extranetId, username, password):

    if extranetId == 103:
        propertyListData = agodaPropertyList(username, password)
        print("Agoda property list fetched successfully.")
        return propertyListData

    elif extranetId == 104:
        propertyListData = cleartripPropertyList(username, password)
        print("Cleartrip property list fetched successfully.")
        return propertyListData

    elif extranetId == 105:
        propertyListData = destranetPropertyList(username, password)
        print("Destranet property list fetched successfully.")
        return propertyListData

    elif extranetId == 107:
        propertyListData = easeMyTripPropertyList(username, password)
        print("EaseMyTrip property list fetched successfully.")
        return propertyListData

propertyList(105, 'reservations@paramparacoorg.com', 'parampara123')
