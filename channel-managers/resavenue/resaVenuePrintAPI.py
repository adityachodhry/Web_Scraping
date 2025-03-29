import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json

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

page_number = 0

url = f"https://cm.resavenue.com/channelcontroller/reports.do?command=recentBookingDetailReportDashboard&todate={to_date}&date={from_date}&arrDept=booking&iPageCount={page_number}&iPageRecords=50&vApplyFlag=selectedProperty"

headers = {
    'Cookie': formatted_cookies
}

response = requests.request("POST", url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    data = []

    table = soup.select_one('table.persist-area2')
    tableBody = table.select_one('tbody.scrollContent')
    booking_records = tableBody.select('tr')
    print(len(booking_records))
    i = 0
    for record in booking_records:
        i += 1
        print(i)
        try:
            div = record.find('div', class_='dispInlineBlock1 padding20 paddingLR_only hyperLink1 getBookingDetails')
            booking_no = div['rel2']
            booking_id = div['rel']
            print(booking_id)

            third_url = f"https://cm.resavenue.com/channelcontroller/reports.do?command=recordPrintView&bookingNo={booking_id}&flag=newReport"
            third_response = requests.request("GET", third_url, headers=headers)

            third_soup = BeautifulSoup(third_response.text, 'html.parser')

            # Extract the required booking details
            hotel_name = third_soup.find('strong', text='Hotel Name :').next_sibling.strip()
            hotel_address = third_soup.find('strong', text='Hotel Address :').next_sibling.strip()
            phone = third_soup.find('strong', text='Phone :').next_sibling.strip()
            booking_no_detail = third_soup.find('strong', text='Booking No. :').next_sibling.strip()
            channel_name = third_soup.find('strong', text='Channel Name :').next_sibling.strip()
            booked_rooms = third_soup.find('strong', text='Booked Rooms :').next_sibling.strip()
            booking_date = third_soup.find('strong', text='Booking Date :').next_sibling.strip()
            checkin_date = third_soup.find('strong', text='CheckIn Date :').next_sibling.strip()
            status = third_soup.find('strong', text='Status :').next_sibling.strip()
            amount = third_soup.find('strong', text='Amount :').next_sibling.strip().replace('INR', '').replace(',', '').strip()
            amount_float = float(amount)

            # Format booking date
            booking_datetime = datetime.strptime(booking_date, '%d %b , %Y')
            formatted_booking_date = booking_datetime.strftime('%Y-%m-%d')

            # Extract guest details
            guest_details_row = third_soup.select('table')[2].select('tr')[1]
            room_package = guest_details_row.select('td')[0].text.strip()
            guest_name = guest_details_row.select('td')[1].text.strip()

            checkinDate = guest_details_row.select('td')[2].text.strip().split(',')[0].strip()
            checkinYear = guest_details_row.select('td')[2].text.strip().split(',')[1].strip()
            checkin_full_date = f"{checkinDate} {checkinYear}"
            checkin_datetime = datetime.strptime(checkin_full_date, '%d %b %Y')
            formatted_checkin_date = checkin_datetime.strftime('%Y-%m-%d')

            checkoutDate = guest_details_row.select('td')[3].text.strip().split(',')[0].strip()
            checkoutYear = guest_details_row.select('td')[3].text.strip().split(',')[1].strip()
            checkOut_full_date = f"{checkoutDate} {checkoutYear}"
            checkOut_datetime = datetime.strptime(checkOut_full_date, '%d %b %Y')
            formatted_checkOut_date = checkOut_datetime.strftime('%Y-%m-%d')

            adults = int(guest_details_row.select('td')[4].text.strip())
            children = int(guest_details_row.select('td')[5].text.strip())
            rooms = int(guest_details_row.select('td')[6].text.strip())

            booking_details = {
                "hotel_name": hotel_name,
                "hotel_address": hotel_address,
                "phone": phone,
                "booking_no": booking_no_detail,
                "channel_name": channel_name,
                "booked_rooms": booked_rooms,
                "booking_date": formatted_booking_date,
                "checkin_date": formatted_checkin_date,
                "status": status,
                "amount": amount_float,
                "room_package": room_package,
                "guest_name": guest_name,
                "checkin": formatted_checkin_date,
                "checkout": formatted_checkOut_date,
                "adults": adults,
                "children": children,
                "rooms": rooms
            }

            data.append(booking_details)
        
        except Exception as e:
            print(f"Error processing record: error: {e}")

    # Print or save the extracted data
    for booking in data:
        print(booking)

    # Optionally, save data to a file
    with open('resaVenueReservation.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

else:
    print(f"Failed to retrieve data: {response.status_code}")
