import requests
import json
from datetime import datetime
from pymongo import MongoClient

def cleartripPromotions(username, password):

    client = MongoClient("mongodb://localhost:27017/")
    db = client["local"]
    collection = db["info"]

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
    
    propertyList = "https://suite.cleartrip.com/aggregator/ho/v1/platform/007/properties?payloadSize=6&pageNo=1&searchType=NAME&filterBy=ALL&sortBy=MODIFIED_DATE&sortOrder=DESC"
    headers = {
        'cookie': f'x-device-id=yKmXAdW7QneZPDKbOhp8v-1729070470830; x-platform=desktop; {formatted_cookies}',
        'Content-Type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }

    propertyResponse = session.get(propertyList, headers=headers)
    propertyResult = propertyResponse.json()
    propertyListDataSlot = propertyResult.get('response', {}).get('propertiesList', [])

    propertyCodes = [property.get('entityId') for property in propertyListDataSlot]
    # print(propertyCodes)

    all_promotions_data = []

    # Iterate through each propertyCode
    for propertyCode in propertyCodes:

        activePromotionUrl = f"https://suite.cleartrip.com/aggregator/v1/hotel/{propertyCode}/promotions?type=ACTIVE&promoCategory=PROMOTION&page=0&size=100"

        headers = {
            'Cookie': f'x-device-id=yKmXAdW7QneZPDKbOhp8v-1729070470830; x-platform=desktop; {formatted_cookies}',
            'content-type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
        }

        activePromotionResponse = session.get(activePromotionUrl, headers=headers)

        if activePromotionResponse.status_code == 200:
            activePromotionResult = activePromotionResponse.json()

            # with open('Raw.json', 'w') as json_file:
            #     json.dump(activePromotionResult, json_file, indent=4)

            activePromotionDataSlot = activePromotionResult.get('response', {}).get('items', [])

            formatted_data = {
                "propertyCode": propertyCode,
                "timeStamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "promotions": []
            }
            
            for promotion in activePromotionDataSlot:
                promotionId = promotion.get('promoId')
                promotionName = promotion.get('promoName')
                promotionType = promotion.get('promoCategory')
                status = promotion.get('syncStatus')
                expiryStatus = promotion.get('expiryStatus')
                totalRevenue = promotion.get('totalRevenue')
                lengthOfStay = promotion.get('totalRoomNights')
                discountType = promotion.get('promoOffer', {}).get('offerType')
                discount = promotion.get('promoOffer', {}).get('offerValue')

                stayDates = promotion.get('applicableConditions', {}).get('stayDates', [])
                stayPeriodFrom = stayDates[0].get('startDate').split('T')[0] if stayDates and 'startDate' in stayDates[0] else None
                stayPeriodTo = stayDates[0].get('endDate').split('T')[0] if stayDates and 'endDate' in stayDates[0] else None

                bookingDates = promotion.get('applicableConditions', {}).get('bookingDates', [])
                validFrom = bookingDates[0].get('startDate').split('T')[0] if bookingDates and 'startDate' in bookingDates[0] else None
                validTo = bookingDates[0].get('endDate').split('T')[0] if bookingDates and 'endDate' in bookingDates[0] else None

                
                stayBlackoutDates = promotion.get('applicableConditions', {}).get('blackoutDates', [])
                daysOfWeek = promotion.get('applicableConditions', {}).get('stayDays', [])

                formatted_data["promotions"].append({
                    "promotionId": promotionId,
                    "promotionName": promotionName,
                    "promotionType": promotionType,
                    "status": status,
                    "expiryStatus": expiryStatus,
                    "totalRevenue": totalRevenue,
                    "lengthOfStay": lengthOfStay,
                    "discountType": discountType,
                    "discount": discount,
                    "stayPeriodFrom": stayPeriodFrom,
                    "stayPeriodTo": stayPeriodTo,
                    "validFrom": validFrom,
                    "validTo": validTo,
                    "stayBlackoutDates": stayBlackoutDates,
                    "daysOfWeek": daysOfWeek
                })
            
            collection.update_one(
                {"propertyCode": propertyCode},
                {"$set": formatted_data},
                upsert=True
            )
            print(f"Updated promotions for property code {propertyCode}")
        
    print("All promotions data has been updated in MongoDB.")
    return all_promotions_data
            
        #     all_promotions_data.append(formatted_data)
            
        # with open('Promotions.json', 'w') as json_file:
        #     json.dump(all_promotions_data, json_file, indent=4)
        
        # print("Promotions data has been saved successfully.")

        # return formatted_data


cleartripPromotions('reservations@hoteltheroyalvista.com', 'Mahadev@123456')
