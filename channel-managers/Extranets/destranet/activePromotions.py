import requests
import json
from datetime import datetime
from pymongo import MongoClient

def destranetPromotion(username, password):
    url = "https://destranet.desiya.com/extranet-controller/login"
    payload = json.dumps({
        "username": username,
        "password": password,
        "usertype": "DES"
    })
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.post(url, headers=headers, data=payload)
    
    if response.status_code == 200:
        response_content = response.json()
        tokenData = response_content.get('data', {})
        tokenId = tokenData.get('token')
        print('Successfully logged in!')
    else:
        print('Login failed!')
        return

    allPropertyList = f"https://destranet.desiya.com/extranet-controller/vendors?token={tokenId}"
    property_response = requests.get(allPropertyList)

    if property_response.status_code == 200:
        property_data = property_response.json()
        propertyCodes = [property.get('vendorId') for property in property_data.get('data', [])]
        # print("Fetched property codes:", propertyCodes)

    client = MongoClient("mongodb://localhost:27017/")
    db = client["local"]
    collection = db["info"]

    all_promotions_data = []  

    for propertyCode in propertyCodes:

        activepromotionsurl = f"https://destranet.desiya.com/extranet-controller/vendors/{propertyCode}/promotions?token={tokenId}"
        activepromotionsResponse = requests.get(activepromotionsurl)
        
        if activepromotionsResponse.status_code == 200:
            response_content = activepromotionsResponse.json()
            promotionsDataSlot = response_content.get('data', {}).get('liveRateRules', [])

            formatted_data = {
                "propertyCode": propertyCode,
                "timeStamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "promotions": []
            }
            
            current_date = datetime.now().date()
            date_format = "%d %b %Y"
            
            for promotion in promotionsDataSlot:
                promotionId = promotion.get('promotionId')
                discountTypeValue = promotion.get('discountType')
                discountType = 'Percentage' if discountTypeValue == 'PR' else discountTypeValue

                allAppliedDays = f"https://destranet.desiya.com/extranet-controller/vendors/{propertyCode}/promotions/{promotionId}?token={tokenId}"
                allAppliedDaysResponse = requests.get(allAppliedDays)

                daysOfWeek = []
                if allAppliedDaysResponse.status_code == 200:
                    allAppliedDays_content = allAppliedDaysResponse.json()
                    daysOfWeek = allAppliedDays_content.get('data', {}).get('daysOfWeek', [])

                valid_from = promotion.get('validFrom')
                valid_to = promotion.get('validTo')
                stay_period_from = promotion.get('stayPeriodFrom')
                stay_period_to = promotion.get('stayPeriodTo')
                
                valid_from_date = datetime.strptime(valid_from, date_format).date() if valid_from else None
                valid_to_date = datetime.strptime(valid_to, date_format).date() if valid_to else None
                start_date = valid_from_date.strftime("%Y-%m-%d") if valid_from_date else ""
                end_date = valid_to_date.strftime("%Y-%m-%d") if valid_to_date else ""
                status = True if (valid_from_date and valid_to_date and valid_from_date <= current_date <= valid_to_date) else False

                stay_from = datetime.strptime(stay_period_from, date_format).strftime("%Y-%m-%d") if stay_period_from else ""
                stay_to = datetime.strptime(stay_period_to, date_format).strftime("%Y-%m-%d") if stay_period_to else ""
                
                stay_blackout_dates = promotion.get('stayBlackoutDates', [])
                converted_blackout_dates = [
                    {
                        "startDate": blackout.get("sd"),
                        "endDate": blackout.get("ed")
                    }
                    for blackout in stay_blackout_dates
                ]

                formatted_data["promotions"].append({
                    "promotionId": promotionId,
                    "promotionName": promotion.get('promotionName', ''),
                    "validFrom": start_date,
                    "validTo": end_date,
                    "discount": promotion.get('discountValue', ''),
                    "discountType": discountType,
                    "stayPeriodFrom": stay_from,
                    "stayPeriodTo": stay_to,
                    "status": status,
                    "lengthOfStay": promotion.get('lengthOfStay', ''),
                    "promotionType": promotion.get('promotionType', ''),
                    "daysOfWeek": daysOfWeek,
                    "stayBlackoutDates": converted_blackout_dates
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

destranetPromotion('reservations@paramparacoorg.com', 'parampara123')
