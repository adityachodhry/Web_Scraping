import requests
import argparse
from bs4 import BeautifulSoup

url = "https://live.ipms247.com/snslogin/index.php"

def parse_args():
    parser = argparse.ArgumentParser(description='Run the script with CLI options')
    parser.add_argument('--username', required=True, help='User username')
    parser.add_argument('--password', required=True, help='User password')
    return parser.parse_args()

args = parse_args()

# Define the payload in a more readable format
payload = {
    'username': args.username,
    'password': args.password,
    'btn_login_s1': ''
}

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

response = requests.post(url, headers=headers, data=payload)

# Check if the response contains a multifactor authentication form
soup = BeautifulSoup(response.text, 'html.parser')
mfa_form = soup.find('form', {'id': 'qrcode_verify'})

if mfa_form:
    print("Login Successful")
else:
    print("Unsuccessfull")