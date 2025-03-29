import sys
import requests
from mongo import push_to_mongodb
import datetime

# Check if the correct number of command line arguments is provided
if len(sys.argv) != 4:
    print("Usage: python common.py <property_code> <hotel_name> <SSID>")
    sys.exit(1)

# Extract command line arguments
property_code = sys.argv[1]
hotel_name = sys.argv[2]
ssid = sys.argv[3]

today = datetime.date.today().strftime("%d/%m/%Y")

# Create an empty list to store results
results = []

try:
    # Set up the endpoint and headers for the POST request
    endpoint = "https://live.ipms247.com/rcm/services/servicecontroller.php"
    headers = {
        'Cookie': f'SSID={ssid}',
        'Content-Type': 'application/json'
    }

    # Set up the body for the POST request
    body = {
        "action": "getbookinglist",
        "limit": 20000,
        "offset": 0,
        "guestname": "",
        "roomtype": "",
        "source": "",
        "arrivalfrom": "",
        "arrivalto": "",
        "resfrom": "1/1/2022",
        "resto": today,
        "status": "ACTIVE",
        "restype": "",
        "arrivalflag": "false",
        "resfromflag": "true",
        "onlyunconfimpayment": "false",
        "web": "true",
        "channel": "true",
        "pmcstatus": "",
        "deptflag": "false",
        "deptFrom": "",
        "deptTo": "",
        "search": "",
        "rmsstatus": "",
        "number": "",
        "chkPMS": "false",
        "is_property": int(property_code),
        "exportlimit": 0,
        "ratetype": "",
        "pgtype": "",
        "datetype": 1,
        "stayoverfrom": "",
        "stayoverto": "",
        "service": "bookinglist_rcm"
    }

    # Make the POST request
    response = requests.post(endpoint, headers=headers, json=body)

    # Print the response status code and content
    print(f"Status Code for account ({property_code}): {response.status_code}")

    response_content = response.json()

    entries = response_content['0']['data']

    for entry in entries:
        bkg_details = {}
        Adult = entry.get('adult')
        Child = entry.get('child')

        bkg_details['hotelName'] = entry.get('hotel_name')
        bkg_details['res'] = entry.get('ResNo')
        bkg_details['bookingDate'] = datetime.datetime.strptime(entry.get('transaction_date'), "%d/%m/%Y").strftime("%Y-%m-%d")
        bkg_details['guestName'] = entry.get('GuestName')
        bkg_details['arrivalDate'] = datetime.datetime.strptime(entry.get('FullArrivalDate'), "%d/%m/%Y").strftime("%Y-%m-%d")
        bkg_details['deptDate'] = datetime.datetime.strptime(entry.get('FullDepartureDate'), "%d/%m/%Y").strftime("%Y-%m-%d")
        bkg_details['room'] = entry.get('roomtype')
        bkg_details['pax'] = f'{Adult}\{Child}'
        bkg_details['ADR'] = float(entry.get('ADR'))
        bkg_details['source'] = entry.get('Source')
        bkg_details['totalCharges'] = int(entry.get('ADR')) * int(entry.get('noofnights'))
        bkg_details['noofnights'] = int(entry.get('noofnights'))
        bkg_details['hotelCode'] = str(property_code)
        bkg_details['isActive'] = "true"

    # Append the result to the list
        results.append(bkg_details)

except Exception as e:
    print(f"An error occurred for account ({property_code}): {str(e)}")

push_to_mongodb(results)