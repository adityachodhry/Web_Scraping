import requests
import json
from urllib.parse import urlencode
from datetime import datetime
from pymongo import MongoClient

def easeMyTripPromotions(username, password):

    client = MongoClient("mongodb://localhost:27017/")
    db = client["local"]
    collection = db["info"]

    login_url = "https://inventory.easemytrip.com/Dashboard/Login"

    login_payload = urlencode({
        'mailOrMob': username,
        'pass': password
    })

    with requests.Session() as session:
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        
        response = session.post(login_url, headers=headers, data=login_payload)

        if response.ok:
            print("Login successful!")

            # Get session cookies
            cookies = session.cookies.get_dict()
            sescookie_value = cookies.get('sescookie')

            propertyListUrl = "https://inventory.easemytrip.com/Api/SupHotel/GetGiataHotelCollection"
            payload = json.dumps({
                "HotelName": "",
                "City": "",
                "status": "all",
                "EmtId": "",
                "State": "",
                "Address": "",
                "StarRating": "",
                "limit": 100,
                "skip": 0,
                "token": sescookie_value
            })

            headers = {
                'Content-Type': 'application/json'
            }

            property_response = session.post(propertyListUrl, headers=headers, data=payload)
            response_content = property_response.json()
            
            property_codes = []
            if "APIData" in response_content:
                try:
                    api_data_clean = json.loads(response_content["APIData"])
                    property_codes = [data.get('EMTHotel', 'UnknownCode') for data in api_data_clean]
                    print(property_codes)
                except json.JSONDecodeError as e:
                    print("Error decoding APIData:", e)
                    return

            all_promotions_data = []

            # Loop through each property code to fetch promotions
            for property_code in property_codes:
                promotion_url = "https://inventory.easemytrip.com/Api/SupHotel/GetOfferDetails"
                promotion_payload = json.dumps({
                    "Token": sescookie_value,
                    "Offertype": "Discount",
                    "pageSize": "2",
                    "pageNumber": 1,
                    "SupHotelCode": property_code,
                    "IsActive": "True",
                    "CityName": "promt"
                })

                promotion_response = session.post(promotion_url, headers=headers, data=promotion_payload)
                formatted_data = {
                    "propertyCode": property_code,
                    "timeStamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "promotions": []
                }

                if promotion_response.status_code == 200:
                    promotion_result = promotion_response.json()
                    promotion_data_slot = promotion_result.get('OfferList', [])

                    for offer in promotion_data_slot:
                        formatted_data["promotions"].append({
                            "promotionId": offer.get('id'),
                            "promotionName": offer.get('PromotionName'),
                            "validFrom": offer.get('FromDate'),
                            "validTo": offer.get('ToDate'),
                            "discount": offer.get('Discount'),
                            "discountType": offer.get('DiscountType'),
                            "stayPeriodFrom": offer.get('BookingStartDate'),
                            "stayPeriodTo": offer.get('BookingEndDate'),
                            "status": offer.get('IsActive'),
                            "promotionType": offer.get('PromotionType'),
                            "daysOfWeek": offer.get('AppliedDay'),
                            "stayBlackoutDates": offer.get('BlackOutDates'),
                            "mobileDiscount": offer.get('Mobile_App_Discount'),
                            "websiteDiscount": offer.get('Website_Public_Discount'),
                            "platform": offer.get('Platform'),
                            "userType": offer.get('UserType')
                        })
                    
                    collection.update_one(
                        {"propertyCode": property_code},
                        {"$set": formatted_data},
                        upsert=True
                    )
                    print(f"Updated promotions for property code {property_code}")
                
            print("All promotions data has been updated in MongoDB.")
            return all_promotions_data

            #         all_promotions_data.append(formatted_data)
            #     else:
            #         print(f"Failed to fetch promotions for property code {property_code}")

            # # Save all promotions data to a JSON file
            # with open('Promotions.json', 'w') as json_file:
            #     json.dump(all_promotions_data, json_file, indent=4)
            
            # print("All promotions data has been saved successfully.")
            # return all_promotions_data


easeMyTripPromotions("reservations@retvensservices.com", "May@2024")
