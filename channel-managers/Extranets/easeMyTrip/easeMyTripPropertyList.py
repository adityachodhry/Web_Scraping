import requests
import json
from urllib.parse import urlencode

def login(username, password):
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

            cookies = session.cookies.get_dict()
            sescookie_value = cookies.get('sescookie')

            url = "https://inventory.easemytrip.com/Api/SupHotel/GetGiataHotelCollection"

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

            response = session.post(url, headers=headers, data=payload)

            response_content = response.json()

            property_list = []

            if "APIData" in response_content:
                try:

                    api_data_clean = json.loads(response_content["APIData"])
                    response_content["APIData"] = api_data_clean

                    for data in api_data_clean:
                        property_code = data.get('EMTHotel', 'UnknownCode')
                        print(property_code)
                        property_name = data.get('name', 'UnknownName')

                        property_list.append({
                            "propertyCode": property_code,
                            "propertyName": property_name
                        })

                except json.JSONDecodeError:
                    print("Error: Failed to decode the APIData field.")

            output_data = {
                "loginStatus": True,
                "propertyList": property_list
            }

            # with open('propertyList.json', 'w') as json_file:
            #     json.dump(output_data, json_file, indent=4)

            print("Property list saved successfully!")
            return output_data

        else:
            print("Login failed! Status code:", response.status_code)
            print("Response text:", response.text)


login("reservations@retvensservices.com", "May@2024")
