import requests
import json

username = "fom.rsgl@royalorchidhotels.com"
password = "From@12345"
url = "https://unitycoreadminapi.rategain.com/unityadminapi/api/Login/AuthenticateUser"

payload = json.dumps({
  "loginname": username,
  "password": password
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

if response.status_code == 200:
    response_content = response.json()

    # print(response.status_code)
    message = response_content.get('message')
    if message == 'SUCCESS':
        print('Login Successful!')
    else:
        print('Wrong Credential')
else:
    print('Login Failed!')
