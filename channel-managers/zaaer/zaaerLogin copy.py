import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json

email = 'cro@retvensservices.com'
password = 'Aa@11223344'
accessCode = '00950'

def get_login(email, password, accessCode):
    url = "https://www.zaaer.co/login"
    session = requests.Session()

    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('meta', attrs={'name': 'csrf-token'})['content']

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    payload = f'_token={csrf_token}&email={email}&password={password}&access_code={accessCode}'

    response = session.post(url, headers=headers, data=payload, allow_redirects=False)
    location = response.headers.get('Location')

    if location == 'https://www.zaaer.co/reservation/dashboard':
        print('Login Successfully!')
        return session
    else:
        print('Login failed, please check user credentials!')
        return None

def fetch_data_for_date_interval(session, check_in_date_from, check_in_date_to, hotel_code):

    # session_cookie = session.cookies.get_dict()

    # headers = {
    # 'Cookie': f"zaaer_session={session_cookie.get('zaaer_session')}",
    # 'Content-Type': 'application/x-www-form-urlencoded'
    # }
    """Fetch data for a specific date interval."""
    headers = {
        'Cookie': "zaaer_session=eyJpdiI6Iktlc24vMTNCZ1RLWkpPMHptREtyOXc9PSIsInZhbHVlIjoiVkYvSExxMHIwM0FEZmNSb3h4WExUUkluaXEzanliQndrckVyclZiemtKMytwY3dYZTdoaHBKUER5SUMrbjVOUHhKSWVJTCtmTUhpQ0xudTdpck1DczNsZ1B4NHpEakV0S21BOUV2bEQ0djQwejJveS8xZnRteUlqZ01KUkhoeVYiLCJtYWMiOiI4MTgzOGMxYWNlY2RkZDJhN2MzNmI1NmYwN2MwMDUzMmIxMjNiN2EzMTNhZGIwZTA1YTNiNTMxNzUzZTFkMjhhIiwidGFnIjoiIn0%3D"
    }
    page = 1
    all_data = []
    
    while True:
        url = f"https://www.zaaer.co/reports/guest-reservations?check_in_date_from={check_in_date_from}&check_in_date_to={check_in_date_to}&hotel_id%5B0%5D={hotel_code}&page={page}"
        print(f"Fetching URL: {url}")
        response = session.get(url, headers=headers)
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')

        # Check for "No record found"
        no_record_element = soup.find('td', colspan="15")
        if no_record_element and "No record found" in no_record_element.text.strip():
            print(f"No records found for {check_in_date_from} to {check_in_date_to} on page {page}.")
            return False  # Indicate no records found

        # Extract table headers
        table_headers = []
        header_rows = soup.find_all('tr', class_='bg-gray-100')
        for row in header_rows:
            th_elements = row.find_all('th')
            if th_elements and all(th.get('colspan') is None for th in th_elements):
                table_headers = [th.text.strip() for th in th_elements]
                break

        # Extract table rows
        table_body = soup.find('tbody', id='sort_table')
        table_rows = table_body.find_all('tr') if table_body else []

        data = []
        status_mapping = {
            "Confirmed": "CFB",
            "Unconfirmed": "UCB",
            "Checked-In": "CI",
            "Checked-Out": "CO",
            "Cancelled": "CN",
            "No-Show" : "NS"
        }

        if table_rows:
            for row in table_rows:
                columns = row.find_all('td')
                row_data = [col.text.strip() for col in columns]
                if len(row_data) == len(table_headers):
                    data_entry = dict(zip(table_headers, row_data))
                    # all_data.append(data_entry)
                    # print(data_entry)

                    try:
                        paid_amount = float(data_entry.get("Paid", "0").replace(',', '') or 0.00)
                        balance_amount = float(data_entry.get("Balance", "0").replace(',', '') or 0.00)
                        total_cost = float(data_entry.get("Total", "0").replace(',', '') or 0.00)
                        no_of_units = int(data_entry.get("No. of units", 1))

                        check_in_date = data_entry.get("Check-In", "")
                        check_out_date = data_entry.get("Check-Out", "")
                        created_on = data_entry.get('Booking date', "")

                        check_in_date = datetime.strptime(check_in_date, "%d/%m/%Y").strftime("%Y-%m-%d") if check_in_date else ""
                        check_out_date = datetime.strptime(check_out_date, "%d/%m/%Y").strftime("%Y-%m-%d") if check_out_date else ""
                        created_on = datetime.strptime(created_on, "%d/%m/%Y").strftime("%Y-%m-%d") if created_on else ""

                        current_status = status_mapping.get(data_entry.get("Status", ""), data_entry.get("Status", ""))
                        room_cost_per_unit = total_cost / no_of_units if no_of_units > 0 else total_cost

                        for i in range(no_of_units):
                            reservation_number = data_entry.get("Res. No", "Unknown").split('\n')[0]
                            if no_of_units > 1:
                                reservation_number += f" - {i+1}"

                            room_number = "Not Available" if "Group" in data_entry.get("Unit", "") else data_entry.get("Unit", "Unknown")
                            room_type_name = data_entry.get("Unit Type", "").split(', ')[i] if i < len(data_entry.get("Unit Type", "").split(', ')) else data_entry.get("Unit Type", "Unknown")

                            transformed_data = {
                                "hotelCode": str(hotel_code),
                                "reservationNumber": reservation_number,
                                "isGroup": no_of_units > 1,
                                "source": data_entry.get("Source", "Unknown"),
                                "guestDetails": {
                                    "guestInfo": {
                                        "name": data_entry.get("Guest", "Unknown"),
                                        "contactInfo": {
                                            "phones": [
                                                {
                                                    "number": data_entry.get('Mobile Number', "Unknown")
                                                }
                                            ]
                                        }
                                    }
                                },
                                "source_segment": "PMS" if data_entry.get("Source", "Unknown") == "Reception" else "OTA",
                                "bookingDetails": {
                                    "arrivalDate": check_in_date,
                                    "departureDate": check_out_date,
                                    "totalNights": int(data_entry.get("Period", "0").split()[0]),
                                    "currentStatus": current_status,
                                    "roomDetails": {
                                        "roomTypeName": room_type_name,
                                        "roomNumber": room_number
                                    },
                                    "createdOn": created_on,
                                    "createdBy": None if data_entry.get('Employee', '--') == '--' else data_entry.get('Employee')
                                },
                                "paymentDetails": {
                                    "status": "Fully Paid" if paid_amount > 0 and balance_amount == 0.0 else "Partially Paid" if 0 < balance_amount < paid_amount else "Not Paid",
                                    "amount": paid_amount,
                                    "outstanding": balance_amount
                                },
                                "priceSummary": {
                                    "roomCost": room_cost_per_unit,
                                    "totalCost": total_cost
                                }
                            }

                            all_data.append(transformed_data)
                            print(transformed_data)

                    except Exception as e:
                        print(f"Error processing row data: {e}")

            # Store data in JSON file after processing all pages
            if all_data:
                with open('guest_reservations.json', 'w') as json_file:
                    json.dump(all_data, json_file, indent=4)

        else:
            print(f"No records found for {check_in_date_from} to {check_in_date_to} on page {page}.")
            return False  # No records found, stop pagination
        
        page += 1

def main():
    session = get_login(email, password, accessCode)
    if not session:
        return

    hotel_code = 612
    today = datetime.now()
    end_date = today
    start_date = today - timedelta(days=10)  # Start with a 10-day interval

    while True:
        check_in_date_to = end_date.strftime("%d%%2F%m%%2F%Y")
        check_in_date_from = start_date.strftime("%d%%2F%m%%2F%Y")
        print(f"Fetching data from {check_in_date_from} to {check_in_date_to}...")

        # Fetch data for the current date interval
        records_found = fetch_data_for_date_interval(session, check_in_date_from, check_in_date_to, hotel_code)

        # If no records are found, move 10 days back and reset pagination
        if not records_found:
            # Move dates back by 10 days
            end_date = start_date
            start_date = start_date - timedelta(days=10)

            # Stop if we go beyond a year from today
            if end_date < today - timedelta(days=20):
                break
        else:
            # Move to next date interval
            end_date = start_date - timedelta(days=1)
            start_date = end_date - timedelta(days=10)

if __name__ == "_main_":
    main()