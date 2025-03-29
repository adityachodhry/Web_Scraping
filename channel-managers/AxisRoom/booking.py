import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
# from mongo import push_to_mongodb
import json

# Define username and password
username = "reservations@paramparacoorg.com"
password = "Parampara@123"
property_code = 103772

accounts = [{'username': username, 'password': password}]

driver = webdriver.Chrome()

for account in accounts:
    username = account['username']
    password = account['password']
    url = 'https://app.axisrooms.com/'

    driver.get(url)
    time.sleep(4)

    driver.find_element(By.ID, 'emailId').send_keys(username)
    driver.find_element(By.ID, 'password').send_keys(password)

    # Wait for the login process
    time.sleep(4)

    driver.find_elements(By.CLASS_NAME, 'g-recaptcha')[0].click()

    # Wait for the login process to complete
    time.sleep(4)

    bookings_button = driver.find_element(
        By.CSS_SELECTOR, 'li[data-menu-name="Bookings"] a').click()

    time.sleep(4)

    cookies = driver.get_cookies()

    access_token = None

    for cookie in cookies:
        if cookie['name'] == 'access_token':
            access_token = cookie['value']
            break

def fetch_booking_report(from_date, to_date):
    url = "https://app.axisrooms.com/supplier/arcHotelBookingReport.html"

    payload = f'download=false&booking_id=%20&searchType=GENERATION_TIME&fromdate={from_date}&todate={to_date}&channelId={property_code}&city_id=-1&productId=-1&room_id=-1&status=-1&nightCount=-1&modeofpayment=-1&chartAxis=1'

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': f'access_token={access_token}'
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        response_content = response.text
        with open("bookingRaw.html", "w", encoding="utf-8") as html_file:
            html_file.write(response_content)
        
        soup = BeautifulSoup(response_content, 'html.parser')
        
        table = soup.find('table', {'class': 'col-lg-12 reportTables table table-bordered table-hover'})
        
        # Extracting the table headers
        headers = []
        thead = table.find('thead')
        if thead:
            header_row = thead.find('tr')
            headers = [th.text.strip() for th in header_row.find_all('th')]

        data = []
        tbody = table.find('tbody')
        if tbody:
            for row in tbody.find_all('tr'):
                row_data = [td.text.strip() for td in row.find_all('td')]
                data.append(row_data)

        formatted_data = []
        for row in data:
            entry = {headers[i]: row[i] for i in range(min(len(headers), len(row)))}
            formatted_data.append(entry)

        final_formatted_data = []
        today = datetime.now().date()
        for entry in formatted_data:
            no_of_rooms = int(entry.get("No Of Rooms", "1"))
            amount = float(entry.get("Amount", "0"))
            
            check_in_date = entry.get("Check In", "")
            check_out_date = entry.get("Check Out", "")
            booking_time = entry.get("Booking Time", "")

            if check_in_date:
                try:
                    check_in_date = datetime.strptime(check_in_date, "%d/%m/%Y").strftime("%Y-%m-%d")
                except ValueError:
                    check_in_date = ""

            if check_out_date:
                try:
                    check_out_date = datetime.strptime(check_out_date, "%d/%m/%Y").strftime("%Y-%m-%d")
                except ValueError:
                    check_out_date = ""

            if booking_time:
                try:
                    booking_time = datetime.strptime(booking_time, "%d/%m/%Y %H:%M").strftime("%Y-%m-%d %H:%M").split()[0]
                except ValueError:
                    booking_time = ""

            current_status = ""
            if "Cancelled" in entry.get("OTA Reference Id", ""):
                current_status = "CN"
            else:
                if check_in_date and check_out_date:
                    check_in_date_obj = datetime.strptime(check_in_date, "%Y-%m-%d").date()
                    check_out_date_obj = datetime.strptime(check_out_date, "%Y-%m-%d").date()

                    if today > check_out_date_obj:
                        current_status = "CO"
                    elif today > check_in_date_obj and today < check_out_date_obj:
                        current_status = "CI"
                    elif today < check_in_date_obj:
                        current_status = "Confirm"
                else:
                    current_status = "Confirm"

            try:
                total_nights = int(entry.get("Room Nights", "0"))
            except ValueError:
                total_nights = 0

            for i in range(no_of_rooms):
                room_cost = amount / no_of_rooms
                reservation_number = entry.get("OTA Reference Id", "").split('\n')[0]
                if no_of_rooms > 1:
                    reservation_number += f" - {i+1}"
                formatted_entry = {
                    "hotelCode": property_code,
                    "reservationNumber": reservation_number,
                    "isGroup": True if no_of_rooms > 1 else False,
                    "source": entry.get("Channel", ""),
                    "guestDetails": {
                        "guestInfo": {
                            "name": entry.get("Guest Name", "")
                        }
                    },
                    "sourceSegment": "OTA",
                    "bookingDetails": {
                        "arrivalDate": check_in_date,
                        "departureDate": check_out_date,
                        "totalNights": total_nights,
                        "currentStatus": current_status,
                        "roomDetails": {
                            "roomTypeName": entry.get("Room Name", ""),
                            "pax": {
                                "totalAdults": entry.get("Total Guest", "")
                            }
                        },
                        "payAtHotel": False if entry.get("Mode of payment", "") == "Prepaid" else True,
                        "paymentNotes": entry.get('Mode of payment'),
                        "createdOn": booking_time
                    },
                    "paymentDetails": {
                        "status": "fully paid" if entry.get("Mode of payment", "") == "Prepaid" else "not paid",
                        "amount": float(room_cost),
                    },
                    "priceSummary": {
                        "roomCost": float(room_cost),
                        "totalCost": float(amount),
                    },
                    "otherDetails": {
                        "specialInstructions": entry.get("Guest Request", "")
                    }
                }
                final_formatted_data.append(formatted_entry)

        for entry in final_formatted_data:
            print(entry)

        with open("formatted_data.json", "w", encoding="utf-8") as json_file:
            json.dump(final_formatted_data, json_file, ensure_ascii=False, indent=4)
    else:
        print(f"Failed to fetch data: {response.status_code}")

from_date = "01/09/2024"
to_date = "30/09/2024"

fetch_booking_report(from_date, to_date)
