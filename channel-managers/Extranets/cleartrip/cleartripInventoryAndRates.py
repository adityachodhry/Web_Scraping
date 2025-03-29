import requests
import json
from datetime import datetime, timedelta
import time  

def cleartripLogin(username, password, propertyCode):
    session = requests.Session()

    loginUrl = "https://suite.cleartrip.com/aggregator/v1/platform/authenticate/login"
    payload = json.dumps({
        "loginIdentifier": username,
        "password": password,
        "authenticationType": "PASSWORD"
    })

    headers = {
        'cookie': 'x-device-id=yKmXAdW7QneZPDKbOhp8v-1729070470830; x-platform=desktop;', 
        'Content-Type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }

    response = session.post(loginUrl, data=payload, headers=headers)

    if response.status_code == 200:
        print('Successfully logged in!')
        cookies = session.cookies.get_dict()
        formatted_cookies = '; '.join([f"{key}={value}" for key, value in cookies.items()])
    else:
        print('Login failed!')
        return
    
    totalDays = 371
    noOfDays = 7  
    today = datetime.now()

    hotelData = {
        "hotelCode": propertyCode,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "inventory": []
    }

    roomInventoryData = {}

    # Loop to fetch data for 30 days in chunks of 7 days
    for start in range(0, totalDays, noOfDays):
        startDate = today + timedelta(days=start)

        InventoryAndRateUrl = f"https://suite.cleartrip.com/aggregator/v1/hotel/{propertyCode}/rate-n-inventory/prices-calendar?ratePlanType=B2C&startDate={startDate.strftime('%Y-%m-%d')}&noOfDays={noOfDays}"

        headers = {
            'cookie': f'x-device-id=yKmXAdW7QneZPDKbOhp8v-1729070470830; x-platform=desktop; {formatted_cookies}',
            'Content-Type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
        }

        ratesAndInventoryResponse = session.get(InventoryAndRateUrl, headers=headers)

        if ratesAndInventoryResponse.status_code == 200:
            inventoryResult = ratesAndInventoryResponse.json()

            # with open('Raw.json', 'w') as json_file:
            #     json.dump(inventoryResult, json_file, indent=4)

            inventoryDataSlot = inventoryResult.get('response', {}).get('roomBasedARIDetails', {})
            
            for roomId, roomDetails in inventoryDataSlot.items():
                roomName = roomDetails.get('roomInfo', {}).get('roomName', None)
                inventoryInfo = roomDetails.get('inventoryInfo', [])
                ratePlanARIInfo = roomDetails.get('ratePlanARIInfo', {})
                
                # Initialize room entry if not already done
                if roomId not in roomInventoryData:
                    roomInventoryData[roomId] = {
                        "roomId": roomId,
                        "roomName": roomName,
                        "inventory": []  
                    }

                dateWiseInventory = {}

                for inventory in inventoryInfo:
                    date = inventory.get('date', None)
                    available = inventory.get('available', '') 
                    sold = inventory.get('sold', '')  
                    totalRooms = 0

                    if available != '':
                        available = int(available)
                    else:
                        available = 0  

                    if sold != '':
                        sold = int(sold)
                    else:
                        sold = 0  

                    totalRooms = available + sold
                    
                    # Initialize entry for the date if not present
                    if date not in dateWiseInventory:
                        dateWiseInventory[date] = {
                            "totalRooms": totalRooms,
                            "availableRooms": available,
                            "rate": None  
                        }

                # Extract all rates from ratePlanARIInfo
                for ratePlanKey, ratePlanDetails in ratePlanARIInfo.items():
                    basePrices = ratePlanDetails.get('basePrices', {})
                    nightlyPriceList = basePrices.get('nightlyPrice', [])
                    
                    # Collect only the first nightly rate and store by date
                    for nightlyPrice in nightlyPriceList:
                        rateDate = nightlyPrice.get('date', None)
                        rate = nightlyPrice.get('value', None)
                        if rateDate and rateDate in dateWiseInventory and rate is not None:
                            if dateWiseInventory[rateDate]["rate"] is None:
                                dateWiseInventory[rateDate]["rate"] = rate

                # Append collected data for each date to room inventory
                for date, data in dateWiseInventory.items():
                    roomInventoryData[roomId]["inventory"].append({
                        "arrivalDate": date,
                        "totalRooms": data.get("totalRooms"),
                        "availableRooms": data.get("availableRooms"),
                        "rate": data.get("rate")  
                    })

            print(f'Data fetched for starting date {startDate.strftime("%Y-%m-%d")}')

        else:
            print('Failed to fetch rates and inventory for', startDate.strftime("%Y-%m-%d"))

        time.sleep(3)  

    # Convert collected data into final structure
    hotelData["inventory"] = list(roomInventoryData.values())

    with open('HotelInventoryData.json', 'w') as json_file:
        json.dump(hotelData, json_file, indent=2)

    print('Data saved to HotelInventoryData.json')

    return hotelData

cleartripLogin('reservations@hoteltheroyalvista.com', 'Mahadev@123456', '4271423')
