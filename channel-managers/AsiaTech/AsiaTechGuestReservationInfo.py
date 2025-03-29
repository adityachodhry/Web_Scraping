import requests
from bs4 import BeautifulSoup
import json

post_url = "https://www.asiatech.in/booking_engine/admin/ajaxrequest/room_chart_book_data.php"
payload = 'orderid=OTA60110123576958'
headers = {
  'Cookie': 'PHPSESSID=d45d43bfacb757533c6258d773409106; PHPSESSID=1f4a06fc9d17e16193b224d49375e50c',
  'Content-Type': 'application/x-www-form-urlencoded'
}

response = requests.post(post_url, headers=headers, data=payload)

with open('Aditya.html', 'w', encoding='utf-8') as file:
    file.write(response.text)

soup = BeautifulSoup(response.text, 'html.parser')

# form = soup.find('form', {'action': 'ajaxrequest/checkin-form.php'})

# # Getting the second div in the form
# second_row_div = form.find('div', class_='row',string='Room Category')

# print(second_row_div)

data = {
    "guestName": soup.find('a', id='user_name').text,
    "guestEmail": soup.find('a', id='user_email').text,
    "guestMobile": soup.find('a', id='user_mobile').text,
    "guestCity": soup.find('a', id='user_city').text,
    "guestState": soup.find('a', id='user_state').text,
    "guestCountry": soup.find('a', id='user_country').text,
    "internalNote": soup.find('td', string='Internal Note').find_next_sibling('td').text,
    "bookingSource": soup.find('td', string='Booking Source').find_next_sibling('td').text,
    "bookingDate": soup.find('td', string='Booking Date').find_next_sibling('td').text,
    "bookingID": soup.find('td', string='Booking ID').find_next_sibling('td').text,
    "checkInDate": soup.find('td', string='Check In Date').find_next_sibling('td').text,
    "checkOutDate": soup.find('td', string='Check Out Date').find_next_sibling('td').text,
    "roomCount": int(soup.find('td', string='Room Count').find_next_sibling('td').text),
    "adult": int(soup.find('td', string='Guest').find_next_sibling('td').text.split(',')[0].split(':')[1].strip()),
    "child": int(soup.find('td', string='Guest').find_next_sibling('td').text.split(',')[1].split(':')[1].strip()),
    "currentStatus": soup.find('span', class_='label label-success label-mini').text.strip(),
    "bookingCommission": float(soup.find('td', string='Booking Commission').find_next_sibling('td').text.strip()),
    "bookingAmount": float(soup.find('td', string='Booking Amount').find_next_sibling('td').text.strip()),
    "pOSOrders": soup.find('td', string='POS Orders').find_next_sibling('td').text.strip(),
    "extraService": soup.find('td', string='Extra Service').find_next_sibling('td').text.strip(),
    "totalAmount": float(soup.find('td', string='Total Amount').find_next_sibling('td').text.strip()),
    "receivedAmount": float(soup.find('td', string='Received Amount').find_next_sibling('td').text.strip()),
    "discountAmount": float(soup.find('td', string='Discount Amount').find_next_sibling('td').text.strip()),
    "pendingAmount": float(soup.find('td', string='Pending Amount').find_next_sibling('td').text.strip()),
    "arrivalDateTime": soup.find('input', id='arrivalstartdate')['value'].split(' ')[1],
    "departureDate": soup.find('input', id='departuredate')['value'].split(' ')[1]
}

with open('data.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print("Data has been extracted and saved to data.json")





# booking_data = {
#                             "hotelCode": str(reg_id_value),
#                             "reservationNumber": reservation_number,
#                             "isGroup": "boolean",
#                             "source": columns[2].text.strip(),
#                             "guestDetails": {
#                                 "guestInfo": {
#                                     "name": columns[4].text.strip(),
#                                     "contactInfo": {
#                                     "email": "string",
#                                     "phones": [
#                                         {
#                                             "type": "string",
#                                             "number": "string"
#                                         }
#                                     ]
#                                 },
#                                 }
#                             },
#                             "bookingDetails": {
#                                 "arrivalDate": parsed_date_1,
#                                 "departureDate": parsed_date_2,
#                                 "totalNights": int(num_nights * num_rooms_booked),
#                                 "checkInTime": "string",
#                                 "checkOutTime": "string",
#                                 "currentStatus": isActive,
#                                 "roomDetails": {
#                                     "roomTypeName": room_type,
#                                     "roomNumber": "number",
#                                     "roomPlan": "string",
#                                     "pax": {
#                                         "total_adults": "number",
#                                         "total_children": "number"
#                                     }
#                                 },
#                                 "createdOn": parsed_date,
#                             },
#                             "paymentDetails": {
#                                 "amount": int(columns[10].text.strip())
#                             },
#                             "priceSummary": {
#                                 "totalCost": int(columns[10].text.strip()),
#                             }
#                         }