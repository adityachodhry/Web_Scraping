import requests
import json
import os
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

email = "aditi.ntrpriss@gmail.com"
password = "Velvet!23"

url = "https://cm.resavenue.com/channelcontroller/registeration.do"

body = {
    "command": "checkUserExist",
    "sEmailAddress": email,
    "sPassword": password
}

response = requests.post(url, data=body)

if response.status_code == 200:
    if "Invalid username and/or password." not in response.text:
        print("Login successful.")
    else:
        print("Invalid email or password.")
else:
    print(f"HTTP Error: {response.status_code}")

cookies = response.cookies

formatted_cookies = "; ".join([f"{cookie.name}={cookie.value}" for cookie in cookies])
print(formatted_cookies)

today = datetime.now()
from_date = (today - timedelta(days=60)).strftime("%d-%m-%Y")
to_date = today.strftime("%d-%m-%Y")

headers = {
    'Cookie': formatted_cookies
}

booking_no = 1100
data = []

folder_name = "allResaVanueData"
os.makedirs(folder_name, exist_ok=True)

while True:
    second_url = f"https://cm.resavenue.com/channelcontroller/reports.do?command=getCompeleteBookingDetail&bookingId={booking_no}"
    second_response = requests.request("GET", second_url, headers=headers)

    if second_response.status_code != 200 or "No data found" in second_response.text:
        print(f"No data found for booking number {booking_no}. Skipping.")
        booking_no += 1
        continue

    html_content = second_response.text
    second_soup = BeautifulSoup(html_content, 'html.parser')

    try:
        guest_info_element = second_soup.find('td', {'data-th': 'Guest Details'})
        guest_info = guest_info_element.text.strip().split('\n')
        guest_name = guest_info[0].strip()
        adult = guest_info[1].strip()
    except:
        guest_name = ''
        adult = 0

    try:
        res_no_element = second_soup.find('div', class_='dispInlineBlock1').find('div', class_='secondary-text')
        res_no = res_no_element.text.strip()
    except:
        res_no = ''

    try:
        noOfRooms_element = second_soup.find('div', class_='eff fadeIn textAlignL secondary-text margin5 marginB_only')
        noOfRooms = noOfRooms_element.text.strip().split('Room')[1].strip()
    except:
        noOfRooms = 0

    try:
        room_details_element = second_soup.find('td', {'data-th': 'Room Details'}).find('div', class_='eff fadeIn secondary-text')
        room_details_text = room_details_element.text.strip()
        room_details_parts = [part.strip() for part in room_details_text.split('\n') if part.strip()]
        room_name = room_details_parts[0].split('...')[0].strip()
        room_plan = room_details_parts[-1].split(':')[-1].strip()
    except:
        room_name = ''
        room_plan = ''

    try:
        bookingdatetime_element = second_soup.find('div', class_='booking-date').find('div', class_='secondary-text')
        bookingdatetime = bookingdatetime_element.text.strip()
        booked_date = bookingdatetime.split('|')[0].split(',')[0].strip()
        booked_date_year = bookingdatetime.split('|')[0].split(',')[1].strip()
        booked_full_date = f"{booked_date} {booked_date_year}"
        booked_datetime = datetime.strptime(booked_full_date, '%d %b %Y')
        formatted_booked_date = booked_datetime.strftime('%Y-%m-%d')
    except:
        formatted_booked_date = ''

    try:
        checkindatetime_element = second_soup.find('div', class_='check-in').find('div', class_='secondary-text')
        checkindatetime = checkindatetime_element.text.strip().split('\n')[0]
        checkin_date = checkindatetime.split(',')[0].strip()
        checkin_date_year = checkindatetime.split(',')[1].strip()
        checkin_full_date = f"{checkin_date} {checkin_date_year}"
        checkin_datetime = datetime.strptime(checkin_full_date, '%d %b %Y')
        formatted_checkin_date = checkin_datetime.strftime('%Y-%m-%d')
    except:
        formatted_checkin_date = ''

    try:
        payment_status_element = second_soup.find('div', class_='pay-status').find('div', class_='secondary-text')
        payment_status = payment_status_element.text.strip()
    except:
        payment_status = ''

    try:
        current_status_element = second_soup.find('div', class_='booking-status').find('div', class_='secondary-text')
        current_status = current_status_element.text.strip().split('\n')[0]
    except:
        current_status = ''

    try:
        number_of_nights_element = second_soup.find('td', {'data-th': 'Nights #'})
        number_of_nights = number_of_nights_element.text.strip()
    except:
        number_of_nights = 0

    try:
        room_rate_element = second_soup.find('td', {'data-th': 'Sell Rate'}).find('div', class_='eff fadeIn secondary-text')
        room_rate = room_rate_element.text.strip().split()[1]
    except:
        room_rate = 0.0

    try:
        totalCharges_element = second_soup.find('td', {'data-th': 'Net Rate'}).find('div', class_='eff fadeIn secondary-text')
        totalCharges = totalCharges_element.text.strip().split()[1]
    except:
        totalCharges = 0.0

    contact_details = second_soup.find('td', {'data-th': 'Contact Details'}).text.strip()
    if contact_details == '-NA-':
        emailId = ''
    elif contact_details:
        emailId = contact_details.split('\n')[0].strip()
    else:
        emailId = ''

    contact_details = second_soup.find('td', {'data-th': 'Contact Details'}).text.strip()
    if contact_details == '-NA-':
        phoneNumber = ''
    elif contact_details:
        phoneNumber = contact_details.split('\n')[1].strip()
    else:
        phoneNumber = ''

    try:
        net_amount = second_soup.select_one('tr.total-amt-col-room .final_amt div.title-dark-text').text.strip()
        netAmountOn = net_amount.split()[1]
    except:
        netAmountOn = 0.0

    try:
        tax_applied = second_soup.select('tr.total-amt-col-room .final_amt div.title-dark-text')[1].text.strip()
        taxAppliedAmount = tax_applied.split()[1]
    except:
        taxAppliedAmount = 0.0

    try:
        commission = second_soup.select('tr.total-amt-col-room .final_amt div.title-dark-text')[2].text.strip()
        commissionOn = commission.split()[1]
    except:
        commissionOn = 0.0

    try:
        total_booking_amount = second_soup.select('tr.total-amt .final_amt div.title-dark-text')[3].text.strip()
        totalCountAmount = total_booking_amount.split()[1]
    except:
        totalCountAmount = 0.0

    booking_detail = {
        'res': res_no,
        'guestName': guest_name,
        'roomName': room_name,
        'noOfRooms': int(noOfRooms),
        'totalCharges': float(totalCharges),
        'bookingDate': formatted_booked_date,
        'paymentStatus': payment_status,
        'currentStatus': current_status,
        'emailId': emailId,
        'number': phoneNumber,
        'roomplan': room_plan,
        'adult': int(adult),
        'checkInDate': formatted_checkin_date,
        'nights': int(number_of_nights),
        'roomCost': float(room_rate),
        'netAmount': float(netAmountOn),
        'taxApplied': float(taxAppliedAmount),
        'commission': float(commissionOn),
        'totalBookingAmount': float(totalCountAmount)
    }
    
    json_file_path = os.path.join(folder_name, f"{res_no}_booking_{booking_no}.json")
    with open(json_file_path, "w", encoding='utf-8') as json_file:
        json.dump(booking_detail, json_file, ensure_ascii=False, indent=4)
        print(f'Extracted data for booking number {booking_no} saved to {json_file_path}')

    booking_no += 1
