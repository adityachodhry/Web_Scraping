import requests
import argparse

url = "https://live.ipms247.com/login/index.php"

def parse_args():
    parser = argparse.ArgumentParser(description='Run the script with CLI options')
    parser.add_argument('--username', required=True, help='User username')
    parser.add_argument('--password', required=True, help='User password')
    parser.add_argument('--propertyCode', required=True, help='User password')
    return parser.parse_args()

args = parse_args()

headers = {
    'Cookie': 'sucuri_cloudproxy_uuid_=',
    'Origin': 'https://live.ipms247.com',
    'Referer': 'https://live.ipms247.com/login/'
}

data = {
    'action': 'login',
    'username': args.username,
    'password': args.password,
    'hotelcode': args.propertyCode
}

response = requests.post(url, headers=headers, data=data)

# Extract 'status' from JSON response
json_response = response.json()
if json_response.get('status', None) == "LOGINFAILED" :
    print("Unsuccessful")
else :
    print("Login Successful")

# # Extract 'SSID' from 'Set-Cookie' header
# set_cookie_header = response.headers.get('Set-Cookie', '')
# ssid_index = set_cookie_header.find('SSID=')
# if ssid_index != -1:
#     ssid = set_cookie_header[ssid_index + 5 : set_cookie_header.find(';', ssid_index)]
#     # print("SSID:", ssid)