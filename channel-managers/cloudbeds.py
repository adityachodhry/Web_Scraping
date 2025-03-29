import requests
import json
from datetime import datetime

url = "https://hotels.cloudbeds.com/connect/reservations/get_reservations"

payload = {
    'sEcho': 1,
    'iColumns': 13,
    'sColumns': ',,,,,,,,,,,,,',
    'iDisplayStart': 0,
    'iDisplayLength': 1000,
    'mDataProp_0': 'id',
    'sSearch_0': '',
    'bRegex_0': False,
    'bSearchable_0': True,
    'bSortable_0': False,
    'mDataProp_1': 'identifier',
    'sSearch_1': '',
    'bRegex_1': False,
    'bSearchable_1': True,
    'bSortable_1': True,
    'mDataProp_2': 'first_name',
    'sSearch_2': '',
    'bRegex_2': False,
    'bSearchable_2': True,
    'bSortable_2': True,
    'mDataProp_3': 'last_name',
    'sSearch_3': '',
    'bRegex_3': False,
    'bSearchable_3': True,
    'bSortable_3': True,
    'mDataProp_4': 'booking_date',
    'sSearch_4': '',
    'bRegex_4': False,
    'bSearchable_4': True,
    'bSortable_4': True,
    'mDataProp_5': 'hotel_name',
    'sSearch_5': '',
    'bRegex_5': False,
    'bSearchable_5': True,
    'bSortable_5': True,
    'mDataProp_6': 'room_numbers',
    'sSearch_6': '',
    'bRegex_6': False,
    'bSearchable_6': True,
    'bSortable_6': False,
    'mDataProp_7': 'checkin_date',
    'sSearch_7': '',
    'bRegex_7': False,
    'bSearchable_7': True,
    'bSortable_7': True,
    'mDataProp_8': 'checkout_date',
    'sSearch_8': '',
    'bRegex_8': False,
    'bSearchable_8': True,
    'bSortable_8': True,
    'mDataProp_9': 'nights',
    'sSearch_9': '',
    'bRegex_9': False,
    'bSearchable_9': True,
    'bSortable_9': True,
    'mDataProp_10': 'grand_total',
    'sSearch_10': '',
    'bRegex_10': False,
    'bSearchable_10': True,
    'bSortable_10': True,
    'mDataProp_11': '',
    'sSearch_11': '',
    'bRegex_11': False,
    'bSearchable_11': True,
    'bSortable_11': True,
    'mDataProp_12': '',
    'sSearch_12': '',
    'bRegex_12': False,
    'bSearchable_12': True,
    'bSortable_12': True,
    'sSearch': '',
    'bRegex': False,
    'iSortCol_0': 4,
    'sSortDir_0': 'desc',
    'iSortingCols': 1,
    'date_start[0]': '',
    'date_start[1]': '',
    'date_end[0]': '',
    'date_end[1]': '',
    'booking_date[0]': '',
    'booking_date[1]': '',
    'status': 'confirmed,not_confirmed,canceled,checked_in,checked_out,no_show',
    'query': '',
    'room_types': '',
    'roomsData[0]': 'room_types_names',
    'source': '',
    'date_stay[0]': '',
    'date_stay[1]': '',
    'breakfastIncluded': '',
    'property_id': 307408,
    'group_id': 307408,
    'version': 'https://front.cloudbeds.com/mfd-root/app.js',
    'frontVersion': '18.23.7',
    'csrf_accessa': 'ac6cd5bb5624f33249b959f0cd3f60b5',
    'billing_portal_id': 20057010,
    'is_bp_setup_completed': 1,
    'billing_offers': ''
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-IN,en;q=0.9,mr-IN;q=0.8,mr;q=0.7,hi-IN;q=0.6,hi;q=0.5,en-GB;q=0.4,en-US;q=0.3',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'acessa_session=fb25e574a5526fc580c8fe72fc1e2c1a4cf64022',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

response = requests.request("POST", url, headers=headers, data=payload)
response_content = response.json()
reservations_data = response_content.get("aaData")

def transform_reservation(reservation):
    # Set status to "cancelled" if the status is "canceled", otherwise set it to "confirm"
    status = "cancelled" if reservation["status"] == "canceled" else "confirm"

    # Convert date strings to datetime objects
    booking_date = datetime.strptime(reservation["booking_date"], "%Y-%m-%d")
    arrival_date = datetime.strptime(reservation["checkin_date"], "%Y-%m-%d")

    # Calculate lead time in days
    lead_time = (arrival_date - booking_date).days


    transformed_reservation = {
        "hotelName": "MIDTOWN INN",
        "res": reservation["identifier"],
        "bookingDate": reservation["booking_date"],
        "guestName": f"{reservation['first_name']} {reservation['last_name']}",
        "arrivalDate": reservation["checkin_date"],
        "deptDate": reservation["checkout_date"],
        "room": reservation["room_types_names"],
        "pax": f"{reservation['number_of_guests']} \\ 0",  # Assuming second value represents children
        "ADR": float(reservation["grand_total"])/int(reservation["nights"]),
        "source": reservation["source_name"],
        "totalCharges": float(reservation["grand_total"]),
        "noOfNights": int(reservation["nights"]),
        "lead": lead_time,
        "hotelCode": reservation["property_id"],  # Set your hotel code here
        "status": status
    }
    return transformed_reservation

# Transform each reservation and store in a list
transformed_reservations = [transform_reservation(reservation) for reservation in reservations_data]

with open('midtownInn.json', 'w') as json_file:
                    json.dump(transformed_reservations, json_file, indent=2)