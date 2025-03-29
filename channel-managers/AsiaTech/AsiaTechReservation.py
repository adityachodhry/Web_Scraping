import time
import re
import requests
import json
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

accounts = [
    {'username': 'kingfisher1', 'accountType': 'Admin', 'password': 'Asiatech@123'}
]

driver = webdriver.Chrome()

for account in accounts:
    usertype = account['accountType']
    username = account['username']
    password = account['password']

    url = 'https://www.asiatech.in/booking_engine/admin/login'

    driver.get(url)
    time.sleep(4)

    driver.find_element(By.ID, 'sel_master_login').send_keys(usertype)
    driver.find_element(By.ID, 'email').send_keys(username)
    driver.find_element(By.ID, 'password').send_keys(password)

    time.sleep(4)

    driver.find_elements(By.CLASS_NAME, 'btn-block')[0].click()
    time.sleep(4)

    php_session_id = driver.get_cookie('PHPSESSID')
    if php_session_id:
        php_session_id_value = php_session_id.get('value')
        print(f"PHPSESSID: {php_session_id_value}")
    else:
        print("PHPSESSID not found.")

    hotel_name_element = driver.find_element(By.CLASS_NAME, 'username')
    hotel_name = hotel_name_element.text

    html_content = driver.page_source
    reg_id_match = re.search(r'var reg_id = "reg_id=" \+ \'(\d+)\'', html_content)

    if reg_id_match:
        reg_id_value = reg_id_match.group(1)
        print(f"Found reg_id: {reg_id_value}")
    else:
        print("No reg_id found.")
        continue

    endpoint = "https://www.asiatech.in/booking_engine/admin/ajaxrequest/showbooking/booking_result1.php"

    headers = {
        'Content-Type': 'application/json',
        'Cookie': f"PHPSESSID={php_session_id_value}"
    }

    page_headers = {
        'Cookie': f"PHPSESSID={php_session_id_value}",
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    today = datetime.now()
    from_date = (today - timedelta(days=60)).strftime("%Y-%m-%d")
    to_date = today.strftime("%Y-%m-%d")

    result = []
    page_number = 1

    while True:
        body = {
            "register_id": reg_id_value,
            "page": str(page_number),
            "ckin": from_date,
            "ckout": to_date,
            "view_type": 0,
            "search_book_status": ""
        }

        response = requests.post(endpoint, headers=headers, json=body, verify=False)
        print(f"Status Code for account {username}: {response.status_code}")
    
        response_content = response.json()
        if not response_content:
            print("No more data. Exiting loop.")
            break

        soup = BeautifulSoup(str(response_content), 'html.parser')

        try:
            table = soup.find('table')
            rows = table.find_all('tr')

            for row in rows[1:]:
                columns = row.find_all('td')

                parsed_date = datetime.strptime(columns[3].text.strip(), "%d-%b-%y").strftime("%Y-%m-%d")
                parsed_date_1 = datetime.strptime(columns[5].text.strip(), "%d-%b-%y").strftime("%Y-%m-%d")
                parsed_date_2 = datetime.strptime(columns[6].text.strip(), "%d-%b-%y").strftime("%Y-%m-%d")

                parsed_date_1_str = datetime.strptime(columns[5].text.strip(), "%d-%b-%y")
                parsed_date_2_str = datetime.strptime(columns[6].text.strip(), "%d-%b-%y")

                num_nights = (parsed_date_2_str - parsed_date_1_str).days
                lead_time_days = (parsed_date_1_str - datetime.strptime(parsed_date, "%Y-%m-%d")).days

                room_info = columns[7].text.strip()
                room_type_match = re.match(r'(.*) \((\d+)\)', room_info)

                if room_type_match:
                    room_type = room_type_match.group(1).strip()
                    num_rooms_booked = int(room_type_match.group(2))
                else:
                    room_type = room_info
                    num_rooms_booked = 1

                reservation_number = columns[1].text.strip()

                if reservation_number.startswith("OTA"):
                    sourceSegment = "OTA"
                else:
                    sourceSegment = "PMS"

                post_url = "https://www.asiatech.in/booking_engine/admin/ajaxrequest/room_chart_book_data.php"
                payload = f'orderid={reservation_number}'

                additional_response = requests.post(post_url, headers=page_headers, data=payload)

                with open('Row1.html', 'a', encoding='utf-8') as file: 
                    file.write(additional_response.text + '\n')

                if reservation_number in additional_response.text:
                    page_soup = BeautifulSoup(additional_response.text, 'html.parser')

                    try:
                        source = page_soup.find('td', string='Booking Source').find_next_sibling('td').text
                    except:
                        source = None
                    
                    try:
                        guestName = page_soup.find('a', id='user_name').text
                    except:
                        guestName = None
                    
                    try:
                        guestEmail = page_soup.find('a', id='user_email').text
                    except:
                        guestEmail = None
                    
                    try:
                        guestNumber = page_soup.find('a', id='user_mobile').text.strip()
                    except:
                        guestNumber = None
                    
                    try:
                        guestCityName = page_soup.find('a', id='user_city').text
                    except:
                        guestCityName = None
                    
                    try:
                        guestSate = page_soup.find('a', id='user_state').text
                    except:
                        guestSate = None
                    
                    try:
                        guestCountry = page_soup.find('a', id='user_country').text
                    except:
                        guestCountry = None
                    
                    try:
                        guestCompanyEmail = page_soup.find('a', id='user_email').text
                    except:
                        guestCompanyEmail = None

                    try:
                        guestArrivalDate = page_soup.find('td', string='Check In Date').find_next_sibling('td').text
                    except:
                        guestArrivalDate = None
                    
                    try:
                        guestDepartureDate = page_soup.find('td', string='Check Out Date').find_next_sibling('td').text
                    except:
                        guestDepartureDate = None
                    
                    try:
                        guestCheckInTime = page_soup.find('input', id='arrivalstartdate')['value'].split(' ')[1] 
                    except:
                        guestCheckInTime = None

                    try:
                        guestCheckOutTime = page_soup.find('input', id='departuredate')['value'].split(' ')[1]
                    except:
                        guestCheckOutTime = None

                    try:
                        totalAdults = int(page_soup.find('td', string='Guest').find_next_sibling('td').text.split(',')[0].split(':')[1].strip())
                    except:
                        totalAdults = None

                    try:    
                        totalChildren = int(page_soup.find('td', string='Guest').find_next_sibling('td').text.split(',')[1].split(':')[1].strip())
                    except:
                        totalChildren = None

                    try:    
                        createdOn = page_soup.find('td', string='Booking Date').find_next_sibling('td').text
                    except:
                        createdOn = None
                    
                    try:
                        totalCost = float(page_soup.find('td', string='Total Amount').find_next_sibling('td').text.strip())
                    except:
                        totalCost = None

                    try:
                        commissionAmount = float(page_soup.find('td', string='Booking Commission').find_next_sibling('td').text.strip())
                    except:
                        commissionAmount = None

                    try:
                        bookingRoomCost = float(page_soup.find('td', string='Booking Amount').find_next_sibling('td').text.strip())
                    except:
                        bookingRoomCost = None

                    guestCurrentStatus = page_soup.find('span', class_='label-mini').text.strip() if page_soup.find('span', class_='label-mini') else None
                    # print(guestCurrentStatus)

                    if guestCurrentStatus == 'Checked In':
                        current_status = 'CI'
                    elif guestCurrentStatus == 'Checked Out':
                        current_status = 'CO'
                    elif guestCurrentStatus == 'Confirmed':
                        current_status = 'CFB'
                    elif guestCurrentStatus == 'Cancelled':
                        current_status = 'CN'
                    elif guestCurrentStatus == 'Unpaid' and guestArrivalDate <= today <= guestDepartureDate:
                        current_status = 'CFB'
                    elif guestCurrentStatus == 'Unpaid' and today > guestDepartureDate:
                        current_status = 'CN'
                    elif guestCurrentStatus == 'Modified' or guestCurrentStatus == 'Booking On Hold':
                        current_status = 'UCB'
                    elif guestCurrentStatus == 'No Show':
                        current_status = 'NS'
                    else:
                        current_status = 'NA'
                    
                    
                    noOfRooms = int(page_soup.find('td', string='Room Count').find_next_sibling('td').text) if page_soup.find('td', string='Room Count').find_next_sibling('td').text else None

                    if noOfRooms is not None:
                        if noOfRooms > 1:
                            roomCostPerRoom = float(bookingRoomCost) / noOfRooms
                            commissionPrice = float(commissionAmount) / noOfRooms
                            totalAmountPerRoom = float(totalCost) / noOfRooms
                        else:
                            roomCostPerRoom = bookingRoomCost
                            commissionPrice = commissionAmount
                            totalAmountPerRoom = totalCost

                        isGroup = True if noOfRooms > 1 else False

                        for room_index in range(noOfRooms):
                            if noOfRooms > 1:
                                reservationNumber = f"{reservation_number}-{room_index + 1}"
                            else:
                                reservationNumber = reservation_number
                    
                    

                            booking_data = {
                                "hotelCode": str(reg_id_value),
                                "reservationNumber": reservationNumber,
                                "isGroup": isGroup,
                                "source": source,
                                "guestDetails": {
                                    "guestInfo": {
                                        "name": guestName,
                                        "contactInfo": {
                                            "email": guestEmail,
                                            "phones": [
                                                {
                                                    "number": guestNumber
                                                }
                                            ]
                                        },
                                        "address": {
                                            "guestCity": guestCityName,
                                            "guestState": guestSate,
                                            "guestCountry": guestCountry
                                        },
                                        "guestCompanyEmail": guestCompanyEmail
                                    }
                                },
                                "sourceSegment": sourceSegment,
                                "bookingDetails": {
                                    "arrivalDate": guestArrivalDate,
                                    "departureDate": guestDepartureDate,
                                    "totalNights": int(num_nights * num_rooms_booked),
                                    "checkInTime": guestCheckInTime,
                                    "checkOutTime": guestCheckOutTime,
                                    "currentStatus": current_status,
                                    "roomDetails": {
                                        "roomTypeId": None,
                                        "roomTypeName": "",
                                        "roomNumber": "",
                                        "roomPlan": "",
                                        "pax": {
                                            "totalAdults": totalAdults,
                                            "totalChildren": totalChildren
                                        }
                                    },
                                    "createdOn": createdOn
                                },
                                # "noOfRoom": noOfRooms,
                                "paymentDetails": {
                                    "amount": totalAmountPerRoom
                                },
                                "priceSummary": {
                                    "roomCost": roomCostPerRoom,
                                    "totalCost": totalAmountPerRoom,
                                    "commissionAmount": commissionPrice
                                },
                            }
                            result.append(booking_data)
                else:
                    print(f"Reservation number {reservation_number} not found in additional response. Skipping.")

            page_number += 1

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            break

    with open('asiaTechBooking.json', 'w') as json_file:
        json.dump(result, json_file, indent=2)

driver.quit()
