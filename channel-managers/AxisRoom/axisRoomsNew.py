import json
import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime

def getAxisRoomsReservations(email, username, password,property_code):
    from_date = "01/01/2022"

    today = datetime.today().strftime("%d/%m/%Y")

    driver = webdriver.Chrome()

    url = 'https://app.axisrooms.com/'

    driver.get(url)
    time.sleep(4)

    if username :
        driver.find_element(By.ID, 'supplierUser').click()
        driver.find_element(By.ID, 'name').send_keys(username)

    driver.find_element(By.ID, 'emailId').send_keys(email)
    driver.find_element(By.ID, 'password').send_keys(password)

    # Wait for the login process
    time.sleep(4)

    driver.find_elements(By.CLASS_NAME, 'g-recaptcha')[0].click()

    # Wait for the login process to complete
    time.sleep(7)

    driver.find_element(By.CSS_SELECTOR, 'li[data-menu-name="Bookings"] a').click()

    time.sleep(4)

    cookies = driver.get_cookies()

    for cookie in cookies:
        if cookie['name'] == 'access_token':
            access_token = cookie['value']
            break

    url = "https://app.axisrooms.com/supplier/arcHotelBookingReport.html"

    payload = f'download=false&booking_id=%20&searchType=GENERATION_TIME&fromdate={from_date}&todate={today}&channelId=-1&city_id=-1&productId={property_code}&room_id=-1&status=-1&nightCount=-1&modeofpayment=-1&chartAxis=1'

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': f'access_token={access_token}'
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        # with open("bookingRaw.html", "w", encoding="utf-8") as html_file:
        #     html_file.write(response_content)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
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
        today = datetime.now()
        for entry in formatted_data:
            no_of_rooms = entry.get("No Of Rooms")
            # print(no_of_rooms)
            if no_of_rooms is None :
                continue
            no_of_rooms = int(no_of_rooms)

            try:
                amount = float(entry.get("Amount", "0").replace(',', '').strip() or 0)
            except ValueError:
                amount = 0.0
            try:
                totalAmount = float(entry.get("Supplier Amount", "0").replace(',', '').strip() or 0)
            except ValueError:
                totalAmount = 0.0
            
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
            
            current_status = entry.get("OTA Reference Id", "")
            print(current_status)

            current_status = ""
            if "Cancelled" in entry.get("OTA Reference Id", ""):
                current_status = "CN"
            else:
                if check_in_date and check_out_date:
                    check_in_date_obj = datetime.strptime(check_in_date, "%Y-%m-%d")
                    check_out_date_obj = datetime.strptime(check_out_date, "%Y-%m-%d")

                    if today > check_out_date_obj:
                        current_status = "CO"
                    elif today >= check_in_date_obj and today < check_out_date_obj:
                        current_status = "CI"
                    elif today < check_in_date_obj:
                        current_status = "CFB"
                else:
                    current_status = "CFB"

            try:
                total_nights = int(int(entry.get("Room Nights", "0"))/no_of_rooms)
            except ValueError:
                total_nights = 0

            for i in range(no_of_rooms):
                total_cost = amount / no_of_rooms
                room_cost = totalAmount / no_of_rooms
                reservation_number = entry.get("OTA Reference Id", "").split('\n')[0]
                if no_of_rooms > 1:
                    reservation_number += f"-{i+1}"
                formatted_entry = {
                    "hotelCode": property_code,
                    "reservationNumber": reservation_number,
                    "isGroup": True if no_of_rooms > 1 else False,
                    "source": entry.get("Channel", ""),
                    "guestDetails": {
                            "name": entry.get("Guest Name", "")
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
                                "totalAdults": int(entry.get("Total Guest", ""))
                            }
                        },
                        "payAtHotel": False if entry.get("Mode of payment", "") == "Prepaid" else True,
                        "paymentNotes": entry.get('Mode of payment'),
                        "createdOn": booking_time
                    },
                    "paymentDetails": {
                        "status": "Fully Paid" if entry.get("Mode of payment", "") == "Prepaid" else "Not Paid",
                        "amount": float(room_cost),
                    },
                    "priceSummary": {
                        "roomCost": float(room_cost),
                        "totalCost": float(total_cost),
                    },
                    "otherDetails": {
                        "specialInstructions": entry.get("Guest Request", "")
                    }
                }
              
                final_formatted_data.append(formatted_entry)

        return final_formatted_data
    else:
        print(f"Failed to fetch data: {response.status_code}")

email = "reservations@presidencyhotel.com"
password = "Password@123"
property_code = "63906"

reservations = getAxisRoomsReservations(email,password, property_code)
with open('reservations.json', 'w', encoding='utf-8') as json_file:
    json.dump(reservations, json_file, indent=4)