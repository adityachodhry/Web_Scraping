from maximojoRatesBulkUpdatesAPI import maximojoBulkRatePush

def main():

    username = "vrrastoria"
    password = "VRR@1234"
    propertyCode = "IN-08b8203d-78ca-434f-a6fc-b8791dca6ccb"
    roomId = "6037da39-4993-05c3-977f-641c61d19529"
    roomPlanId = "IN-08b8203d-78ca-434f-a6fc-b8791dca6ccb"
    channelCode = "MAX"
    availability = ""
    ratePerDay = 3150
    PerExtraPerson = "" 
    ExtraChildren = {
        "1": 1750
    } 
    ExtraPerson = {
        "1": 450
    } 
    Occupancy = {
        "1": 3150,
        "2": 3600
    }   
    startDate = "2024-09-09"
    endDate = "2024-09-09"

    seasonCode = ""  
    roomName = ""    
    rateTypeId = ""     
    rate = "" 
    OccupancyId = ""                 

    maximojoBulkRatePush(
        username=username,
        password=password,
        propertyCode=propertyCode,
        roomId=roomId,
        roomPlanId=roomPlanId,
        channelCode=channelCode,
        availability=availability,
        ratePerDay=ratePerDay,
        PerExtraPerson=PerExtraPerson,
        ExtraChildren=ExtraChildren,
        ExtraPerson=ExtraPerson,
        Occupancy=Occupancy,
        OccupancyId=OccupancyId,
        startDate=startDate,
        endDate=endDate,
        seasonCode=seasonCode,
        roomName=roomName,
        rateTypeId=rateTypeId,
        rate=rate
    )

# Entry point of the program
if __name__ == "__main__":
    main()
