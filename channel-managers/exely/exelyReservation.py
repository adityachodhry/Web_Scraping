import time
import json, re
import requests
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

def exelyReservation(username, password):
    session = requests.Session()

    driver = webdriver.Chrome()
    login_url = 'https://secure.exely.com/secure/Enter.aspx'
    driver.get(login_url)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="username"]')))
    driver.find_element(By.CSS_SELECTOR, 'input[name="username"]').send_keys(username)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
    driver.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys(password)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn.btn-md.btn-primary')))
    driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-md.btn-primary').click()

    time.sleep(5)  
    if "Invalid username or password" in driver.page_source:
        print("Login Unsuccessful")
        driver.quit()
        return
    else:
        print("Login Successful")

    selenium_cookies = driver.get_cookies()
    for cookie in selenium_cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    years_ago = 3 
    today = datetime.now().strftime('%Y-%m-%d')
    date_start = (datetime.now() - timedelta(days= years_ago * 365)).strftime('%d.%m.%Y')
    date_end = datetime.now().strftime('%d.%m.%Y')

    columnsUrl = "https://secure.exely.com/secure/Extranet/service/application/extranet-host-data"

    response1 = session.get(columnsUrl)

    if response1.status_code == 200:
        results1 = response1.json()
        columnsId = results1.get('userSettings', {}).get('report-columns')

    url = f"https://secure.exely.com/secure/Extranet/service/reports?columns={columnsId}&dateEnd={date_end}&dateStart={date_start}&dateType=booking_date&searchForText=&withoutDate=false"

    response = session.get(url)

    if response.status_code == 200:
        results = response.json()

        # with open('Row.json', 'w') as json_file:
        #     json.dump(results, json_file, indent=4)
        
        data_slot = results.get('bookings', [])
        structured_reservations = []
        
        all_responses_html = []  

        for booking in data_slot:
            booking_id = booking.get('number')
            guestCount = booking.get('guestCount')
            creationDateTime = booking.get('creationDateTime').split('T')[0]
            paymentDate = booking.get('paymentDate')
            startDate = booking.get('startDate').split('T')[0]
            endDate = booking.get('endDate').split('T')[0]
            checkInTime = booking.get('startDate').split('T')[1]
            checkOutTime = booking.get('endDate').split('T')[1]
            nights = booking.get('nights')
            price = booking.get('price')
            roomTypeQty = booking.get('roomTypeQty')
            paymentMethodTitle = booking.get('paymentMethodTitle')

            webPmsBooking = booking.get('webPmsBooking')
            room_stays = webPmsBooking.get('roomStays', []) if webPmsBooking else []

            for room in room_stays:
                roomTypeId = room.get('roomTypeId')
                status = room.get('status')

                if status == 'Confirmed' and startDate <= today <= endDate:
                    current_status = 'CI'
                elif status == 'Confirmed' and today > endDate:
                    current_status = 'CO'
                elif status == 'Confirmed':
                    current_status = 'CFB'
                elif status == 'Cancelled':
                    current_status = 'CN'
                else:
                    current_status = 'NA'

            eachReservation = f"https://secure.exely.com/secure/ManagementOld/booking?number={booking_id}&receiver=provider"
            response2 = session.get(eachReservation)

            if response2.status_code == 200:
                response_text = response2.text 
                all_responses_html.append(response_text)

                # with open('Row.html', 'w', encoding='utf-8') as response_html: 
                #     for response in all_responses_html:
                #         response_html.write(response + "\n") 

                soup = BeautifulSoup(response_text, 'html.parser')

                try:
                    hotel_name = soup.find('td', {'test-id': 'header-hotel-name'}).text.strip() if soup.find('td', {'test-id': 'header-hotel-name'}) else None
                    hotel_code = soup.find('td', {'test-id': 'header-hotel-id'}).text.strip() if soup.find('td', {'test-id': 'header-hotel-id'}) else None

                    booking_source_div = soup.find('div', {'test-id': 'booking-source'})
                    if booking_source_div and booking_source_div.find('b'):
                        booking_source = booking_source_div.find('b').get_text(strip=True).split(' (')[0]
                except:
                    booking_source = None
                    hotel_code = None

                try:
                    arrival_time = soup.find('div', {'test-id': 'booking-info-arrival-time'}).text.strip() if soup.find('div', {'test-id': 'booking-info-arrival-time'}) else None
                    departure_time = soup.find('div', {'test-id': 'booking-info-departure-time'}).text.strip() if soup.find('div', {'test-id': 'booking-info-departure-time'}) else None
                    agent_rate_plan = soup.find('td', {'test-id': 'room-stay-details-agent-rate-plan'}).text.strip() if soup.find('td', {'test-id': 'room-stay-details-agent-rate-plan'}) else None
                    agent_room_type = soup.find('td', {'test-id': 'room-stay-details-agent-room-type'}).text.strip() if soup.find('td', {'test-id': 'room-stay-details-agent-room-type'}) else None
                except:
                    arrival_time = None
                    departure_time = None
                    agent_rate_plan = None
                    agent_room_type = None

                totalAdults = 0
                totalChildren = 0

                try:
                    guests_count = soup.find('td', {'test-id': 'room-stay-details-guests'}).text.strip() if soup.find('td', {'test-id': 'room-stay-details-guests'}) else None
                    if guests_count:
                        adults_match = re.search(r'(\d+)\s*adult', guests_count)
                        children_match = re.search(r'(\d+)\s*child', guests_count)

                        if adults_match:
                            totalAdults = int(adults_match.group(1)) 
                        if children_match:
                            totalChildren = int(children_match.group(1))
                except:
                    pass
                
                try:
                    customer_fullname = (
                        soup.find('td', {'test-id': 'customer-info-fullname'}).text.strip() 
                        if soup.find('td', {'test-id': 'customer-info-fullname'}) else None
                    )
                    
                    customer_phone_number = (
                        soup.find('td', {'test-id': 'customer-info-phone-number'}).text.strip().replace(' ', '').strip() 
                        if soup.find('td', {'test-id': 'customer-info-phone-number'}) else None
                    )
                    
                    customer_email = (
                        soup.find('td', {'test-id': 'customer-info-email'}).find('a').text.strip() 
                        if soup.find('td', {'test-id': 'customer-info-email'}) and soup.find('td', {'test-id': 'customer-info-email'}).find('a') else None
                    )
                    
                    customer_country = (
                        soup.find('td', {'test-id': 'customer-info-citizenship'}).text.strip() 
                        if soup.find('td', {'test-id': 'customer-info-citizenship'}) else None
                    )
                    
                    customer_address = (
                        soup.find('td', {'test-id': 'customer-info-full-address'}).text.strip() 
                        if soup.find('td', {'test-id': 'customer-info-full-address'}) else None
                    )

                except:
                    customer_fullname = None
                    customer_phone_number = None
                    customer_email = None
                    customer_country = None
                    customer_address = None
                
                try:
                    total_cost_td = soup.find('td', {'test-id': 'booking-summary-price-before-tax'})
                    total_amount = None

                    if total_cost_td:
                        total_amount_text = total_cost_td.get_text(strip=True).split('INR')[0].strip()
                        
                        total_amount = float(total_amount_text.replace(',', '').replace('₹', ''))
                        
                except Exception as e:
                    print(f"Error extracting total cost: {e}")
                    total_amount = None

                guests = booking.get('guests', [])
                for guest in guests:
                    city = guest.get('city')
                    postalCode = guest.get('postalCode')
                    region = guest.get('region')
                
                try:
                    room_cost = None  
                    room_cost_td_elements = soup.select('table.room-stay-rates td.price-summary-col')
                    
                    for td in room_cost_td_elements:
                        room_cost_text = td.get_text(strip=True)
                        if room_cost_text:
                           
                            room_cost = float(room_cost_text.replace(',', '').replace('$', ''))
                            break  
                except Exception as e:
                    print(f"Error extracting room cost: {e}")
                    room_cost = None
                    
                isGroup = roomTypeQty > 1
                
                for room_index in range(roomTypeQty):
                    if roomTypeQty > 1:
                        reservationNumber = f"{datetime.now().strftime('%Y%m%d')}-{booking_id}-{room_index + 1}"
                    else:
                        reservationNumber = f"{datetime.now().strftime('%Y%m%d')}-{booking_id}"
                    structured_reservation = {
                        "hotelCode": hotel_code,
                        # "noOfRooms": roomTypeQty,
                        "reservationNumber": reservationNumber,
                        "isGroup": isGroup,
                        "source": booking_source,
                        "guestDetails": {
                            "guestInfo": {
                                "name": customer_fullname,
                                "contactInfo": {
                                    "email": customer_email,
                                    "phones": [
                                        {
                                            "number": customer_phone_number
                                        }
                                    ]
                                },
                                "address": {
                                    "streetAddress": customer_address,
                                    "guestCity": city,
                                    "guestCountry": customer_country,
                                    "guestZipCode": postalCode,
                                    "guestNationality": region
                                },
                            }
                        },
                        "bookingDetails": {
                            "arrivalDate": startDate,
                            "departureDate": endDate,
                            "totalNights": nights,
                            "checkInTime": checkInTime,
                            "checkOutTime": checkOutTime,
                            "currentStatus": current_status,
                            "bookingType": paymentMethodTitle,
                            "roomDetails": {
                                "roomTypeId": str(roomTypeId),
                                "roomTypeName": agent_room_type,
                                "roomPlan": agent_rate_plan,
                                "pax": {
                                    "totalAdults": totalAdults,
                                    "totalChildren": totalChildren
                                }
                            },
                            "createdOn": creationDateTime,
                        },
                        "paymentDetails": {
                            # "status": None,
                            "amount": total_amount,
                        },
                        "priceSummary": {
                            "roomCost": room_cost,
                            "totalCost": total_amount,
                            # "taxAmount": None,
                        }
                    }

                    structured_reservations.append(structured_reservation)  

            with open('exelyReservations.json', 'w') as json_file:
                json.dump(structured_reservations, json_file, indent=4)

                return structured_reservations

    driver.quit()

exelyReservation('TL-503098-REV', 'NEST@786*1263')
