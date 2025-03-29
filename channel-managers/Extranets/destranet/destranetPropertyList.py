import requests
import json

def destranetPropertyList(username, password):
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

    result = {
        "loginStatus": False,
        # "message": "Login failed",
        "propertyList": []
    }

    if response.status_code == 200:
        response_content = response.json()
        tokenData = response_content.get('data', {})
        tokenId = tokenData.get('token')

        if tokenId:
            print('Successfully logged in!')
            result["loginStatus"] = True
            # result["message"] = "Successfully logged in"
            
            allPropertyList = f"https://destranet.desiya.com/extranet-controller/vendors?token={tokenId}"
            property_response = requests.get(allPropertyList)

            if property_response.status_code == 200:
                property_data = property_response.json()
                propertyDataSlot = property_data.get('data', [])

                for property in propertyDataSlot:
                    property_info = {
                        "propertyCode": property.get('vendorId'),
                        "propertyName": property.get('vendorname')
                    }
                    result["propertyList"].append(property_info)
            else:
                print('Error fetching property list!')
        else:
            print('Login failed!')

    # with open('propertyList.json', 'w') as json_file:
    #     json.dump(result, json_file, indent=4)
    
    return result

# destranetPropertyList('reservations@paramparacoorg.com', 'parampara123')
