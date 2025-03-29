import requests
import json

def cleartripPropertyList(username, password):

    session = requests.Session()

    url = "https://suite.cleartrip.com/aggregator/v1/platform/authenticate/login"

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

    response = session.post(url, data=payload, headers=headers)

    # Prepare result object
    result = {
        "loginStatus": False,
        # "message": "Login failed",
        "propertyList": []
    }

    if response.status_code == 200:
        print('Successfully logged in!')
        result["loginStatus"] = True
        # result["message"] = "Successfully logged in"
        
        cookies = session.cookies.get_dict()
        formatted_cookies = '; '.join([f"{key}={value}" for key, value in cookies.items()])
        
        propertyList = "https://suite.cleartrip.com/aggregator/ho/v1/platform/007/properties?payloadSize=6&pageNo=1&searchType=NAME&filterBy=ALL&sortBy=MODIFIED_DATE&sortOrder=DESC"
        headers = {
            'cookie': f'x-device-id=yKmXAdW7QneZPDKbOhp8v-1729070470830; x-platform=desktop; {formatted_cookies}',
            'Content-Type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
        }

        propertyResponse = session.get(propertyList, headers=headers)
        propertyResult = propertyResponse.json()
        
        propertyListDataSlot = propertyResult.get('response', {}).get('propertiesList', [])

        for property in propertyListDataSlot:
            propertyCode = property.get('entityId')
            propertyName = property.get('entityData', {}).get('name')
            if propertyCode and propertyName:
                result["propertyList"].append({
                    "propertyCode": propertyCode,
                    "propertyName": propertyName
                })

    # with open('PropertyList.json', 'w') as output_file:
    #     json.dump(result, output_file, indent=4)

    return result

# cleartripPropertyList('reservations@hoteltheroyalvista.com', 'Mahadev@123456')
