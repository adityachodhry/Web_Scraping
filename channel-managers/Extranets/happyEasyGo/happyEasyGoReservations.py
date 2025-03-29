import requests
import json

def happyEasyGoLogin(username, password):

    session = requests.Session()

    loginUrl = "http://hotelebk.happyeasygo.net/outer/api/extranet/account/login"

    payload = json.dumps({
    "email": username,
    "password": password
    })

    headers = {
      'Content-Type': 'application/json',
      'Cookie': 'JSESSIONID=wo8Y3BTc88jhqEJHyAzzIpVIuP-Jq7WSj6g1Vg5h'
    }

    response = session.post(loginUrl, headers=headers, data=payload)

    if response.status_code == 200:
        print('Successfully logged in!')
    else:
        print('Login failed!')

happyEasyGoLogin("info@welcomeinnhospitality.com", "Vrr@123456")