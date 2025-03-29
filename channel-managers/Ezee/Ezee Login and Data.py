import requests,sys,datetime

login_url = "https://live.ipms247.com/login/index.php"
headers = {
    'Cookie': 'sucuri_cloudproxy_uuid_=',
    'Origin': 'https://live.ipms247.com',
    'Referer': 'https://live.ipms247.com/login/'
}

data = {
    'action': 'login',
    'username': 'admin',
    'password': 'UK@123456',
    'hotelcode': '43354'
}

# Create a session
with requests.Session() as session:
    session.cookies.clear()
    # Perform the login
    login_response = session.post(login_url, headers=headers, data=data)

    print("Login Response status code:", login_response.status_code)

    # Extract 'status' from JSON response
    json_response = login_response.json()
    status = json_response.get('status', None)
    print("Login Status:", status)

    # Extract 'SSID' from 'Set-Cookie' header
    set_cookie_header = login_response.headers.get('Set-Cookie', '')
    ssid_index = set_cookie_header.find('SSID=')
    if ssid_index != -1:
        ssid = set_cookie_header[ssid_index + 5: set_cookie_header.find(';', ssid_index)]
        print("SSID:", ssid)

    today = datetime.date.today().strftime("%d/%m/%Y")

    # Create an empty list to store results
    results = []

    try:
        # Set up the endpoint and headers for the POST request
        endpoint = "https://live.ipms247.com/rcm/services/servicecontroller.php"
        headers = {
            'Cookie': f'SSID={ssid}',
            'Content-Type': 'application/json'
        }
        property_code = 43354

        # Set up the body for the POST request
        body = {
            "action": "getbookinglist",
            "limit": 20000,
            "offset": 0,
            "guestname": "",
            "roomtype": "",
            "source": "",
            "arrivalfrom": "",
            "arrivalto": "",
            "resfrom": "1/1/2015",
            "resto": today,
            "status": "ACTIVE",
            "restype": "",
            "arrivalflag": "false",
            "resfromflag": "true",
            "onlyunconfimpayment": "false",
            "web": "true",
            "channel": "true",
            "pmcstatus": "",
            "deptflag": "false",
            "deptFrom": "",
            "deptTo": "",
            "search": "",
            "rmsstatus": "",
            "number": "",
            "chkPMS": "false",
            "is_property": property_code,
            "exportlimit": 0,
            "ratetype": "",
            "pgtype": "",
            "datetype": 1,
            "stayoverfrom": "",
            "stayoverto": "",
            "service": "bookinglist_rcm"
        }

        # Make the POST request
        response = session.post(endpoint, headers=headers, json=body)

        # Print the response status code and content
        print(f"Status Code for account ({property_code}): {response.status_code}")
        print(response.text)
    except :
        pass