import requests
import json

def agodaPropertyList(username, password):
    
    login_url = "https://ycs.agoda.com/ul/api/v1/signin"

    login_payload = json.dumps({
        "credentials": {
            "password": password,
            "authType": "email",
            "username": username
        },
        "signInOption": {
            "keepMeSignIn": True
        },
        "contextParams": {},
        "captchaEnabled": True
    })

    login_headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'ul-app-id': 'ycs',
        'ul-fallback-origin': 'https://ycs.agoda.com',
        'Content-Type': 'application/json'
    }

    with requests.Session() as session:
      
        login_response = session.post(login_url, headers=login_headers, data=login_payload)

        if login_response.ok:
            print("Login successful!")

            cookies = session.cookies.get_dict()
            token = cookies.get('token')

            property_url = "https://ycs.agoda.com/mldc/en-us/api/iam/PropertySearch/FiltersInformation"

            headers = {
                'Cookie': f'tokenp={token}',
                'Content-Type': 'application/json'
            }

            response = requests.get(property_url, headers=headers)
            
            response_content = response.json()

            # print(response.text)

            # with open('agoda_propertyListRaw.json', 'w') as json_file:
            #     json.dump(response_content, json_file, indent=4)
            
            # hotelList[0].hotelName

            property_list = []

            data_slot = response_content.get('hotelList',[])
            for data in data_slot:
                hotelId = data.get('hotelId')
                name = data.get('hotelName')
                if name == "Unnamed property":
                    continue

                property_list.append({
                        "propertyCode": hotelId,
                        "propertyName": name
                    })
                
            output_data = {
                "loginStatus": True,
                "propertyList": property_list
            }

            # with open('propertyList.json', 'w') as json_file:
            #     json.dump(output_data, json_file, indent=4)

            return output_data
        
        else:
            print(f"Login failed with status code: {response.status_code}")
            print("Response Text:", response.text)

# agodaPropertyList("reservations@retvensservices.com", "Retvens@123")

