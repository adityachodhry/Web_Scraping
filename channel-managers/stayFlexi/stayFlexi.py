import requests
import json
from datetime import datetime
from mongo import push_to_mongodb
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Run the script with CLI options')
    parser.add_argument('--propertyCode', required=True)
    parser.add_argument('--username', required=True)
    parser.add_argument('--password', required=True)
    return parser.parse_args()

# Get command-line arguments
args = parse_args()

# Function to fetch hotel details
def fetch_hotel_details(email, hotel_id):
    url = f"https://api.stayflexi.com/common/hotel-detail?isGroupProperty=False&emailId={email}&hotel_id={hotel_id}"
    response = requests.get(url)
    data = response.json()
    if data:
        return data[0]
    else:
        return None

# Function to transform booking report data
def transform_booking_report(data):
    transformed_data = []
    for entry in data["report_data"]:
        # Calculate lead value
        arrival_date = datetime.strptime(entry["checkin"], "%b %d, %Y %I:%M %p")
        booking_date = datetime.strptime(entry["booking_made_on"], "%b %d, %Y %I:%M %p")
        lead = (arrival_date - booking_date).days

        # Determine isActive value
        is_active = "true" if entry["status"] != "CANCELLED" else "false"

        transformed_entry = {
            "hotelName": hotel_details["hotelName"],
            "res": entry["bookingid_display_name"],
            "bookingDate": booking_date.strftime("%Y-%m-%d"),
            "guestName": entry["customer_name"],
            "arrivalDate": arrival_date.strftime("%Y-%m-%d"),
            "deptDate": datetime.strptime(entry["checkout"], "%b %d, %Y %I:%M %p").strftime("%Y-%m-%d"),
            "room": entry["roomtypes"],
            "pax": f"{entry['adults_pax']}\\{entry['children_pax']}",
            "ADR": entry["room_revenue"],
            "source": entry["source"],
            "noOfNights": int(entry["room_nights"]),
            "lead": lead,
            "totalCharges": entry["booking_amount"],
            "hotelCode": hotel_details["hotelId"],
            "isActive": is_active
        }
        transformed_data.append(transformed_entry)
    return transformed_data

# Hotel details API parameters
email = args.username
hotel_id = args.propertyCode

# Fetch hotel details
hotel_details = fetch_hotel_details(email, hotel_id)

if hotel_details:
    # Get today's date
    today = datetime.now().strftime("%Y-%m-%d")

    # Booking report API parameters with today's date as end date
    booking_report_url = f"https://api.stayflexi.com/api/v2/reports/getReportData/?report_type=unifiedBookingReport&start_date=2015-11-27&end_date={today}&date_filter_mode=created&hotelId={hotel_id}"

    # Fetch booking report
    booking_response = requests.get(booking_report_url)
    booking_data = booking_response.json()

    # Transform booking report data
    transformed_booking_data = transform_booking_report(booking_data)

    push_to_mongodb(transformed_booking_data)
