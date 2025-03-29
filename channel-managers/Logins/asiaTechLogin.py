import argparse
import requests

requests.packages.urllib3.disable_warnings()
def parse_args():
    parser = argparse.ArgumentParser(description='Run the script with CLI options')
    parser.add_argument('--username', required=True, help='User username')
    parser.add_argument('--accountType', required=True, help='User accountType')
    parser.add_argument('--password', required=True, help='User password')
    return parser.parse_args()

args = parse_args()

print(args)

if args.accountType == 'Admin' :
    url = "https://www.asiatech.in/booking_engine/admin/ajaxrequest/loginphp.php"

    form_data = {
    "form_token": "",
    "login_email": args.username,
    "login_password": args.password,
    "login_type": 0
    }
elif args.accountType == 'User' :
    url = "https://www.asiatech.in/booking_engine/admin/ajaxrequest/masterrequest.php"

    form_data = {
    "admin_email": args.username,
    "admin_password": args.password,
    "login_type": 2
    }

headers = {
    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

response = requests.post(url , headers=headers,data=form_data,verify=False)

print("Status Code:",response.status_code)
print(response.text)

if "2" in response.text:
    print("Login Successful")
elif "Enter Password is Wrong" in response.text:
    print("Login failed: Invalid password")
elif "This Username Does Not Exist" in response.text:
    print("Login failed: Invalid username")