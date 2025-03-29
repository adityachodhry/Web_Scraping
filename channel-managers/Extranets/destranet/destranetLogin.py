import requests
import json

def destranetLogin(username, password):

    url = "https://destranet.desiya.com/extranet-controller/login"

    payload = json.dumps({

    "username": username,
    "password": password,
    "usertype": "DES"
    })

    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        print('Successfully logged in!')
    else:
        print('Login failed!')

destranetLogin('reservations@paramparacoorg.com', 'parampara123')
