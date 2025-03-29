import requests
import json

def happyEasyGoLogin(username, password):

    session = requests.Session()

    loginUrl = "http://hotelebk.happyeasygo.net/outer/api/extranet/account/login"

    payload = json.dumps({
    "email": username,
    "password": password
    })

    response = session.post(loginUrl, data=payload)

    if response.status_code == 200:
        print('Successfully logged in!')
    else:
        print('Login failed!')

happyEasyGoLogin("info@welcomeinnhospitality.com", "Vrr@123456")