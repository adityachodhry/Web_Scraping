import requests
import json

url = "https://www.irctc.co.in/eticketing/protected/mapps1/altAvlEnq/TC"

body = {
    "concessionBooking": False,
    "srcStn": "INDB",
    "destStn": "MMCT",
    "jrnyClass": "",
    "jrnyDate": "20240408",
    "quotaCode": "GN",
    "currentBooking": "False",
    "flexiFlag": False,
    "handicapFlag": False,
    "ticketType": "E",
    "loyaltyRedemptionBooking": False,
    "ftBooking": False
}

headers = {
    'Greq': '1712395163663',
    'Content-Type': 'application/json',
    'Bmirak' : 'webbm'
  
}

response = requests.post(url, json=body, headers=headers)

if response.status_code == 200:
    response_content = response.json()
    print(response_content)
    
    
    # with open('train_data.json', 'w') as json_file:
    #     json.dump(response_content, json_file, indent=4)

