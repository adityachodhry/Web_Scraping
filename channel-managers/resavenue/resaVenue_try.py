import requests
import json, re
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
print(formatted_cookies)

url = "https://cm.resavenue.com/channelcontroller/reports.do?command=recentBookingDetailReportDashboard&iPropId=0&todate=17-05-2024&date=01-05-2024&arrDept=booking&iPageCount=0&iPageRecords=10&vApplyFlag=selectedProperty"

payload = {}
headers = {
    'Cookie': formatted_cookies
}

response = requests.request("POST", url, headers=headers, data=payload)

if response.status_code == 200:
    response_content = response.text

    soup = BeautifulSoup(response_content, 'html.parser')

    data = {
        'canceled': int(soup.select_one('div.Cancelled span').text),
        'confirmed': int(soup.select_one('div.Confirmed span').text),
        'channels_by_bookings': [],
        'channels_by_revenue': [],
        'booking_detail_records': [],
        'room_details': []
    }

    channels_bookings = soup.select('div.channels-booking div.reservation_data')
    for booking in channels_bookings:
        channel_name = booking.select_one('div.total').text.strip()
        total_bookings = booking.select_one('div.totalAmt.pull-right').text.strip()
        data['channels_by_bookings'].append({
            'channel_name': channel_name,
            'total_bookings': int(total_bookings)
        })

    channels_revenue = soup.select('div.channels-revenue div.reservation_data')
    for revenue in channels_revenue:
        channel_name = revenue.select_one('div.total').text.strip()
        total_Revenue = revenue.select_one('div.totalAmt.pull-right span.total_amount').text.strip()
        data['channels_by_revenue'].append({
            'channelName': channel_name,
            'totalRevenue': float(total_Revenue)
        })

    booking_records = soup.select('div.primary-text')
    for record in booking_records:
        try:
            guest_name = record.contents[0].strip()
            res = record.select_one('span.secondary-text').next_sibling.strip()
            
            arrival_info = record.contents[4].strip()
            arrival_date = arrival_info.split(':')[-1].strip().split('&nbsp;')[0].split(',')[0].strip()
            arrival_date_year = arrival_info.split(':')[-1].strip().split('&nbsp;')[0].split(',')[1].split('(')[0].strip()

            arrival_full_date = f"{arrival_date} {arrival_date_year}"
            arrival_datetime = datetime.strptime(arrival_full_date, '%d %b %Y')
            formatted_arrival_date = arrival_datetime.strftime('%Y-%m-%d')

            number_of_nights_text = arrival_info.split('(')[-1].split('&nbsp;')[0].split('&')[0]
            number_of_nights = int(re.search(r'\d+', number_of_nights_text).group())

            booking_detail = {
                'guestName': guest_name,
                'res': res,
                'arrivalDate': formatted_arrival_date,
                'numberOfNights': number_of_nights
            }
            data['booking_detail_records'].append(booking_detail)
        except Exception as e:
            print(f"Error processing record: {record}, error: {e}")

    room_details = soup.select('div.primary-text.paddingB_none.property-title')
    for detail in room_details:
        try:
            room_info = detail.text.strip()
            room = room_info.split('|')[0].strip().replace('\t', '')

            rooms = room_info.split('|')[1].split(':')[1].strip().split()[0]
            pax = room_info.split('|')[2].split(':')[1].strip().split()[0]

            next_div_text = detail.find_next_sibling('div').text
            booking_amount = next_div_text.split('INR')[1].split()[0].strip()
            booking_date_time_full = next_div_text.split('| Bkg Dt. & Time:')[1].split('|')[0].strip()
            booking_date_time = booking_date_time_full.split('-')[0].strip().replace(',', '')
            booking_date_time_formatted = datetime.strptime(booking_date_time, '%d %b %Y').strftime('%Y-%m-%d')

            payment_status = next_div_text.split('| Pay Status:')[1].strip()

            room_data = {
                'room': room,
                'rooms': int(rooms),
                'pax': int(pax),
                'totalCharges': float(booking_amount),
                'bookingDate': booking_date_time_formatted,
                'paymentStatus': payment_status,
                'ADR': float(booking_amount)/int(rooms),
            }
            data['room_details'].append(room_data)
        except Exception as e:
            print(f"Error processing room detail: {e}")

    with open("resaVenueReservation_1.json", "w", encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
        print('Extracted data saved to extracted_data.json')

else:
    print(f"Failed to retrieve data: {response.status_code}")
