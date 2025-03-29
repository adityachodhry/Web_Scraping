import requests
import json
import os
from bs4 import BeautifulSoup
from datetime import datetime

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

folder_name = "allResaVanueData"
os.makedirs(folder_name, exist_ok=True)

booking_no = 1100
# 4183

while True:
    headers = {
        'Cookie': formatted_cookies
    }

    second_url = f"https://cm.resavenue.com/channelcontroller/reports.do?command=getCompeleteBookingDetail&bookingId={booking_no}"
    second_response = requests.get(second_url, headers=headers)

    if second_response.status_code != 200 or "No data found" in second_response.text:
        print(f"No data found for booking number {booking_no}.")
    else:
        html_content = second_response.text
        second_soup = BeautifulSoup(html_content, 'html.parser')

        reservation_details = {
            'bookingNumber': booking_no,
            'rooms': []
        }

        tr_elements = second_soup.find_all('tr', class_='tr-data')

        room_counter = 1

        for tr in tr_elements:
            booking_detail = {}

            try:
                res_no_element = second_soup.find('div', class_='dispInlineBlock1').find('div', class_='secondary-text')
                booking_detail['res'] = f"{res_no_element.text.strip()}-{room_counter}"
            except:
                booking_detail['res'] = ''

            try:
                guest_info_element = tr.find('td', {'data-th': 'Guest Details'})
                guest_info = guest_info_element.text.strip().split('\n')
                booking_detail['guestName'] = guest_info[0].strip()

                adult_img = guest_info_element.find('img', {'src': '/channelcontroller/images/responsiveImages/pax_adult.jpg'})
                if adult_img:
                    adult_text = adult_img.find_previous(text=True).strip()
                    booking_detail['adult'] = int(adult_text.split()[0])
                else:
                    booking_detail['adult'] = 0

                child_img = guest_info_element.find('img', {'src': '/channelcontroller/images/responsiveImages/pax_child.jpg'})
                if child_img:
                    child_text = child_img.find_previous(text=True).strip()
                    booking_detail['child'] = int(child_text.split()[0])
                else:
                    booking_detail['child'] = 0

            except:
                booking_detail['guestName'] = ''

            try:
                room_details_element = tr.find('td', {'data-th': 'Room Details'}).find('div', class_='eff fadeIn secondary-text')
                room_details_text = room_details_element.text.strip()
                room_details_parts = [part.strip() for part in room_details_text.split('\n') if part.strip()]
                booking_detail['roomName'] = room_details_parts[0].split('...')[0].strip()
                booking_detail['roomplan'] = room_details_parts[-1].split(':')[-1].strip()
            except:
                booking_detail['roomName'] = ''
                booking_detail['roomplan'] = ''

            try:
                checkindatetime_element = tr.find('td', {'data-th': 'Check-In'}).find('div', class_='secondary-text')
                checkindatetime = checkindatetime_element.text.strip().split('\n')[0]
                checkin_date = checkindatetime.split(',')[0].strip()
                checkin_date_year = checkindatetime.split(',')[1].strip()
                checkin_full_date = f"{checkin_date} {checkin_date_year}"
                checkin_datetime = datetime.strptime(checkin_full_date, '%d %b %Y')
                booking_detail['checkInDate'] = checkin_datetime.strftime('%Y-%m-%d')
            except:
                booking_detail['checkInDate'] = ''

            try:
                payment_status_element = second_soup.find('div', class_='pay-status').find('div', class_='secondary-text')
                booking_detail['paymentStatus'] = payment_status_element.text.strip()
            except:
                booking_detail['paymentStatus'] = ''

            try:
                current_status_element = second_soup.find('div', class_='booking-status').find('div', class_='secondary-text')
                booking_detail['currentStatus'] = current_status_element.text.strip().split('\n')[0]
            except:
                booking_detail['currentStatus'] = ''

            try:
                number_of_nights_element = tr.find('td', {'data-th': 'Nights #'}).find('div', class_='secondary-text')
                booking_detail['nights'] = int(number_of_nights_element.text.strip())
            except:
                booking_detail['nights'] = 0

            try:
                room_rate_element = tr.find('td', {'data-th': 'Sell Rate'}).find('div', class_='eff fadeIn secondary-text')
                booking_detail['roomCost'] = float(room_rate_element.text.strip().split()[1])
            except:
                booking_detail['roomCost'] = 0.0

            try:
                totalCharges_element = tr.find('td', {'data-th': 'Net Rate'}).find('div', class_='eff fadeIn secondary-text')
                booking_detail['totalCharges'] = float(totalCharges_element.text.strip().split()[1])
            except:
                booking_detail['totalCharges'] = 0.0

            try:
                contact_details = tr.find('td', {'data-th': 'Contact Details'}).text.strip()
                if contact_details == '-NA-':
                    booking_detail['emailId'] = ''
                    booking_detail['number'] = ''
                elif contact_details:
                    contact_details_parts = contact_details.split('\n')
                    booking_detail['emailId'] = contact_details_parts[0].strip()
                    booking_detail['number'] = contact_details_parts[1].strip()
                else:
                    booking_detail['emailId'] = ''
                    booking_detail['number'] = ''
            except:
                booking_detail['emailId'] = ''
                booking_detail['number'] = ''

            if booking_detail['guestName'] or booking_detail['roomName'] or booking_detail['checkInDate']:
                reservation_details['rooms'].append(booking_detail)

            room_counter += 1
            if room_counter > 2:
                break

        if reservation_details['rooms']:
            json_file_path = os.path.join(folder_name, f"booking_{booking_no}.json")
            with open(json_file_path, "w", encoding='utf-8') as json_file:
                json.dump(reservation_details, json_file, ensure_ascii=False, indent=4)
                print(f'Extracted data for booking number {booking_no} saved to {json_file_path}')

    booking_no += 1
