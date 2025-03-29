import requests
import json

def cleartripLogin(username, password):

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

    if response.status_code == 200:
        print('Successfully logged in!')
    else:
        print('Login failed!')

cleartripLogin('reservations@hoteltheroyalvista.com', 'Mahadev@123456')