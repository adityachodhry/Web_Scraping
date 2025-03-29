import requests
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Run the script with CLI options')
    parser.add_argument('--email', required=True)
    parser.add_argument('--password', required=True)
    return parser.parse_args()

args = parse_args()

url = "https://api.stayflexi.com/user/hotelAdmin/login"

body = {
    "username":args.email,
    "password":args.password
}

headers = {
    "Content-Type":"application/json",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.post(url , headers=headers,json= body)

if "success" in response.text:
    print("Login Successful")
elif "Unauthorized" in response.text:
    print("Login failed: Invalid username or password")