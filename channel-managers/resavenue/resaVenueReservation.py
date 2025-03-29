import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json

def resaVenueReservation(email, password):
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
            return []
    else:
        print(f"HTTP Error: {response.status_code}")
        return []

    cookies = response.cookies
    formatted_cookies = "; ".join([f"{cookie.name}={cookie.value}" for cookie in cookies])
    print(formatted_cookies)

    today = datetime.now()
    from_date = (today - timedelta(days=60)).strftime("%d-%m-%Y")
    to_date = today.strftime("%d-%m-%Y")

    page_number = 0
    data = {}

    while True:
        url = f"https://cm.resavenue.com/channelcontroller/reports.do?command=recentBookingDetailReportDashboard&todate={to_date}&date={from_date}&arrDept=booking&iPageCount={page_number}&iPageRecords=50&vApplyFlag=selectedProperty"

        headers = {
            'Cookie': formatted_cookies
        }

        response = requests.request("POST", url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            table = soup.select_one('table.persist-area2')
            if table:
                tableBody = table.select_one('tbody.scrollContent')
                booking_records = tableBody.select('tr')
            else:
                booking_records = []

            if not booking_records:
                break 

            print(len(booking_records))
            for i, record in enumerate(booking_records):
                print(f"Processing record {i + 1}")
                try:
                    div = record.find('div', class_='dispInlineBlock1 padding20 paddingLR_only hyperLink1 getBookingDetails')
                    # if not div:
                    #     pass

                    booking_no = div['rel2']
                    booking_id = div['rel']
                    print(booking_id)

                    second_url = f"https://cm.resavenue.com/channelcontroller/reports.do?command=getCompeleteBookingDetail&bookingNo={booking_no}&bookingId={booking_id}"

                    second_response = requests.request("GET", second_url, headers=headers)

                    html_content = second_response.text
                    second_soup = BeautifulSoup(html_content, 'html.parser')

                    try:
                        hotel_code_input = second_soup.find('input', {'name': 'iPropId'})
                        hotel_code = hotel_code_input['value']
                    except:
                        hotel_code = None

                    third_url = f"https://cm.resavenue.com/channelcontroller/reports.do?command=recordPrintView&bookingNo={booking_id}&flag=newReport"
                    third_response = requests.request("GET", third_url, headers=headers)

                    third_soup = BeautifulSoup(third_response.text, 'html.parser')

                    hotel_name = third_soup.find('strong', text='Hotel Name :').next_sibling.strip()
                    hotel_address = third_soup.find('strong', text='Hotel Address :').next_sibling.strip()
                    phone = third_soup.find('strong', text='Phone :').next_sibling.strip()
                    booking_no_detail = third_soup.find('strong', text='Booking No. :').next_sibling.strip()
                    channel_name = third_soup.find('strong', text='Channel Name :').next_sibling.strip()
                    booking_date = third_soup.find('strong', text='Booking Date :').next_sibling.strip()
                    checkin_date = third_soup.find('strong', text='CheckIn Date :').next_sibling.strip()

                    amount = third_soup.find('strong', text='Amount :').next_sibling.strip().replace('INR', '').replace(',', '').strip()
                    totalCharges = float(amount)

                    booking_datetime = datetime.strptime(booking_date, '%d %b , %Y')
                    formatted_booking_date = booking_datetime.strftime('%Y-%m-%d')
                    
                    try:
                        guest_details_row = third_soup.select('table')[2].select('tr')[1]
                        room_package = guest_details_row.select('td')[0].text.strip()
                        guest_name = guest_details_row.select('td')[1].text.strip()
                    except:
                        room_package = None
                        guest_name = None

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

                    try:
                        adults = int(guest_details_row.select('td')[4].text.strip())
                        children = int(guest_details_row.select('td')[5].text.strip())
                        rooms = int(guest_details_row.select('td')[6].text.strip())
                    except:
                        adults = 0
                        children = 0
                        rooms = 0
                    
                    try:
                        room_details_text = second_soup.find('td', {'data-th': 'Room Details'}).find('div', class_='eff fadeIn secondary-text').text.strip()
                        room_details_parts = [part.strip() for part in room_details_text.split('\n') if part.strip()]
                        room_name = room_details_parts[0].split('...')[0].strip()
                    except:
                        room_name = None

                    try:
                        room_plan = room_details_parts[-1].split(':')[-1].strip()
                        if room_plan == 'AP':
                            rate_plan = room_plan
                        elif room_plan == 'MAP':
                            rate_plan = room_plan
                        elif room_plan == 'CP':
                            rate_plan = room_plan
                        elif room_plan == 'EP':
                            rate_plan = room_plan
                        else:
                            rate_plan = 'NA'
                    except:
                        rate_plan = None

                    try:
                        payment_status = second_soup.find('div', class_='pay-status').find('div', class_='secondary-text').text.strip()
                    except:
                        payment_status = None

                    try:
                        number_of_nights = int(second_soup.find('td', {'data-th': 'Nights #'}).text.strip())
                    except:
                        number_of_nights = 0
                    
                    try:
                        totalRoomRate = second_soup.find('td', {'data-th': 'Sell Rate'}).find('div', class_='eff fadeIn secondary-text').text.strip().split()[1]
                    except:
                        totalRoomRate = 0.0
                    
                    try:
                        perRoomCharges = second_soup.find('td', {'data-th': 'Net Rate'}).find('div', class_='eff fadeIn secondary-text').text.strip().split()[1]
                    except:
                        perRoomCharges = 0.0

                    try:
                        contact_details = second_soup.find('td', {'data-th': 'Contact Details'}).text.strip().split('\n')
                        email_id = contact_details[0].strip()
                        phone_number = contact_details[1].strip()
                    except:
                        email_id = None
                        phone_number = None
                    
                    try:
                        net_amount = second_soup.select_one('tr.total-amt-col-room .final_amt div.title-dark-text').text.strip().split()[1]
                        tax_applied = second_soup.select('tr.total-amt-col-room .final_amt div.title-dark-text')[1].text.strip().split()[1]
                        commission = second_soup.select('tr.total-amt-col-room .final_amt div.title-dark-text')[2].text.strip().split()[1]
                        total_booking_amount = second_soup.select('tr.total-amt .final_amt div.title-dark-text')[3].text.strip().split()[1]
                    except:
                        tax_applied = 0.0
                        commission = 0.0
                        net_amount = 0.0
                        total_booking_amount = 0.0

                    try:
                        status = third_soup.find('strong', text='Status :').next_sibling.strip()

                        checkin_datetime = datetime.strptime(formatted_checkin_date, '%Y-%m-%d')
                        checkout_datetime = datetime.strptime(formatted_checkOut_date, '%Y-%m-%d')

                        if status == 'Confirmed' and checkin_datetime <= today <= checkout_datetime:
                            current_status = 'CI'
                        elif status == 'Confirmed' and today > checkout_datetime:
                            current_status = 'CO'
                        elif status == 'Confirmed' and today > checkin_datetime and today > checkout_datetime:
                            current_status = 'NS'
                        elif status == 'Confirmed':
                            current_status = 'CFB'
                        elif status == 'Cancelled':
                            current_status = 'CN'
                        else:
                            current_status = 'NA'
                    except:
                        current_status = None
                    
                    booked_rooms = int(third_soup.find('strong', text='Booked Rooms :').next_sibling.strip())
                    isActive = True if booked_rooms > 1 else False

                    for room_index in range(booked_rooms):
                        if booked_rooms > 1:
                            reservationNumber = f"{booking_no_detail}-{room_index + 1}"
                        else:
                            reservationNumber = booking_no_detail

                        commission_amount_per_room = float(commission) / booked_rooms if booked_rooms > 1 else float(commission)
                        tax_amount_per_room = float(tax_applied) / booked_rooms if booked_rooms > 1 else float(tax_applied)
                        perRoomCost = float(perRoomCharges) / booked_rooms if booked_rooms > 1 else float(perRoomCharges)
                        totalRoomAmount = float(totalRoomRate) / booked_rooms if booked_rooms > 1 else float(totalRoomRate)

                        booking_details = {
                            "hotelCode": hotel_code,
                            "reservationNumber": reservationNumber,
                            "isGroup": isActive,
                            "source": channel_name,
                            "guestDetails": {
                                "guestInfo": {
                                    "name": guest_name,
                                    "contactInfo": {
                                        "email": email_id,
                                        "phones": [
                                            {
                                                "number": phone_number
                                            }
                                        ]
                                    }
                                }
                            },
                            "bookingDetails": {
                                "arrivalDate": formatted_checkin_date,
                                "departureDate": formatted_checkOut_date,
                                "totalNights": number_of_nights,
                                "currentStatus": current_status,
                                "roomDetails": {
                                    "roomTypeName": room_package,
                                    "roomPlan": rate_plan,
                                    "pax": {
                                        "totalAdults": adults,
                                        "totalChildren": children
                                    }
                                },
                                "createdOn": formatted_booking_date,
                            },
                            "paymentDetails": {
                                "status": payment_status,
                                "amount": totalRoomAmount,
                            },
                            "priceSummary": {
                                "roomCost": perRoomCost,
                                "totalCost": totalRoomAmount,
                                "commissionAmount": commission_amount_per_room,
                                "taxAmount": tax_amount_per_room,
                            }
                        }
                        data[reservationNumber] = booking_details

                except Exception as e:
                    print(f"Error processing record: {e}")

        else:
            print(f"Failed to retrieve data: {response.status_code}")
            break
        
        page_number += 1

    unique_data = list(data.values())
    with open('resaVenueReservation.json', 'w', encoding='utf-8') as f:
        json.dump(unique_data, f, ensure_ascii=False, indent=4)

    return unique_data

# data = resaVenueReservation('aditi.ntrpriss@gmail.com', 'Velvet!23')
data = resaVenueReservation('info@redwingscastle.com', 'Redwings@#12345')
# data = resaVenueReservation('cmknmh@gmail.com', 'Abcd@12345')
print(f"Total records fetched: {len(data)}")