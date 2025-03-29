import requests
import re
import json
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime
import concurrent.futures
from selenium.webdriver.common.keys import Keys
import argparse
import pandas as pd

final_data = []

accounts = [
    {'property_code': 5566, 'username': 'ankur.nograhiya@retvensservices.com', 'password': 'Retvens@123456'}]

today = datetime.today().strftime("%d/%m/%Y")
driver = webdriver.Chrome()

try:
    for account in accounts:
        property_code = account['property_code']
        username = account['username']
        password = account['password']

        try:
            url = 'https://max2.staah.net/hotels/index.php'

            driver.get(url)
            time.sleep(4)

            action = webdriver.ActionChains(driver)

            driver.find_element(By.NAME, 'propertyId').send_keys(property_code)
            driver.find_element(By.NAME, 'email').send_keys(username)
            driver.find_element(By.NAME, 'password').send_keys(password)
            time.sleep(random.randint(2, 3))

            driver.find_element(By.NAME, 'password').send_keys(Keys.ENTER)

            time.sleep(random.randint(6, 8))

            cookies = driver.get_cookies()
            # print(cookies)

            page_html = driver.page_source

            soup = BeautifulSoup(page_html, 'html.parser')
            property_detail_input = soup.find('input', {'id': 'chat_propertyDetail'})
            property_detail_value = property_detail_input['value']
            hotelName = property_detail_value.split('-')[0].strip()

            driver.get("https://max2.staah.net/hotels/bookings")
            time.sleep(random.randint(6, 8))

            html_content = driver.page_source

            soup = BeautifulSoup(html_content, 'html.parser')

            table = soup.find('tbody', {'id': 'listing_moredata'})

            first_tr_class = table.find('tr')['class'][1]
            latest_booking = first_tr_class.split('-')[1].strip()

            initial_number_str = (latest_booking)[4:]
            current_number_int = int(initial_number_str)


            AWSLABCORS_Cookie = next((cookie['value'] for cookie in cookies if cookie['name'] == 'AWSALBCORS'), None)
            PHPSESSID_Cookie = next((cookie['value'] for cookie in cookies if cookie['name'] == 'PHPSESSID'), None)

            headers = {
                "X-Requested-With": "XMLHttpRequest",
                "Cookie": f"PHPSESSID={PHPSESSID_Cookie};AWSALBCORS={AWSLABCORS_Cookie}"
            }

            for i in range(10):

                new_number_str = str(current_number_int).zfill(
                    len(initial_number_str))
                
                
                data = {
                    "bookingsId": f"{property_code}{new_number_str}"
                }
                current_number_int -= 1
                print(current_number_int)

            def process_batch(start_number, end_number):
                batch_data = []
                for current_number_int in range(start_number, end_number, -1):

                    while current_number_int > 0:

                        new_number_str = str(current_number_int).zfill(
                            len(initial_number_str))

                        url = f'https://max2.staah.net/hotels/booking_details.php?gb_propertyId={property_code}&bookingsId={property_code}{new_number_str}'

                        current_number_int -= 1

                        response = requests.post(url, headers=headers)

                        if response.status_code == 200:
                            htmlContent = response.text

                            with open(f'staah_content.html', 'w', encoding='utf-8') as html_file:
                                html_file.write(htmlContent)

                            soup = BeautifulSoup(htmlContent, 'html.parser')

                            text_data = soup.get_text()

                            with open("staahText.txt", 'a', encoding='utf-8') as file:
                                file.write(text_data)

                            date_pattern = re.compile(
                                r'From (\d{2} [A-Za-z]+ \d{4}) To (\d{2} [A-Za-z]+ \d{4})')

                            match = date_pattern.search(text_data)

                            if match:
                                checkin_date = match.group(1)
                                formatted_checkin_date = datetime.strptime(
                                    checkin_date, "%d %b %Y").strftime("%Y-%m-%d")
                                checkout_date = match.group(2)
                                formatted_checkout_date = datetime.strptime(
                                    checkout_date, "%d %b %Y").strftime("%Y-%m-%d")
                            else:
                                print("Dates not found in the text.")

                            booking_details = soup.find(
                                'div', {'class': 'widget-content'})

                            bookingID = soup.find(
                                'h2', {'id': 'booking_num'}).strong.text.strip().split(': ')[1]

                            reservation_table = soup.find(
                                'table', class_='margintop20')

                            reservation_details = {}

                            for row in reservation_table.find_all('tr'):

                                cells = row.find_all(['td', 'th'])

                                if len(cells) == 2:
                                    key = cells[0].text.strip()
                                    value = cells[1].text.strip()

                                    reservation_details[key] = value

                            for key, value in reservation_details.items():
                                if "Booking Date" in key:
                                    bookingDate = value
                                    booking_date_formatted = datetime.strptime(
                                        bookingDate, "%d-%b-%Y %I:%M:%S %p (IST)").strftime("%Y-%m-%d")

                                if "Name" in key:
                                    guestName = value
                                if "Point Of Sale" in key:
                                    source = value

                            room_type = soup.find(
                                'td', class_='headingRow customheadingRow').div.text.strip()
                            if "-" in room_type and "_" in room_type:
                                if room_type.index("_") < room_type.index("-"):
                                    room = room_type.split('_')[0].strip()
                                else:
                                    room = room_type.split('-')[0].strip()
                            elif "-" in room_type:
                                room = room_type.split('-')[0].strip()
                            elif "_" in room_type:
                                room = room_type.split('_')[0].strip()

                            total_value_pattern1 = re.compile(r'Total Value\s+INR\s+([\d,]+\.\d+)')
                            total_value_pattern2 = re.compile(r'INR\s+(\d+\.\d+)$')

                            total_value_match1 = total_value_pattern1.search(text_data)
                            total_value_match2 = total_value_pattern2.search(text_data)

                            total_value = total_value_match1.group(1) if total_value_match1 else (
                                total_value_match2.group(1) if total_value_match2 else "Not found")

                            total_charges = float(total_value.replace(',', '')) if total_value != "Not found" else None

                            no_of_nights_pattern = re.compile(r'No Of Nights : (\d+)')
                            matches = no_of_nights_pattern.findall(text_data)

                            total_no_of_nights = sum(map(int, matches))

                            adults_pattern = re.compile(r'Adults: (\d+)')
                            children_pattern = re.compile(r'Children: (\d+)')

                            adults_matches = adults_pattern.findall(text_data)
                            children_matches = children_pattern.findall(text_data)

                            total_adults = sum(map(int, adults_matches))
                            total_children = sum(map(int, children_matches))

                            pax = f"{total_adults}\{total_children}"

                            adr = float(total_charges/total_no_of_nights)

                            formatted_checkin_datetime = datetime.strptime(formatted_checkin_date, "%Y-%m-%d")
                            booking_date_datetime = datetime.strptime(booking_date_formatted, "%Y-%m-%d")

                            lead = (formatted_checkin_datetime - booking_date_datetime).days

                            bkgDetails = {
                                "hotelName": hotelName,
                                "res": bookingID,
                                "bookingDate": booking_date_formatted,
                                "guestName": guestName,
                                "arrivalDate": formatted_checkin_date,
                                "deptDate": formatted_checkout_date,
                                "room": room,
                                "pax": pax,
                                "ADR": adr,
                                "source": source,
                                "totalCharges": total_charges,
                                "noOfNights": total_no_of_nights,
                                "lead": lead,
                                "hotelCode": property_code,
                                "isActive": "true"
                            }
                            final_data.append(bkgDetails)
                            with open(f"staah_{property_code}.json", "w") as json_file:
                                json.dump(final_data, json_file, indent=2)
                        else:
                            print(
                                f"Failed to get a valid response. Status code: {response.status_code}")
                            batch_data.append(bkgDetails)

                return batch_data

            batch_size = 1

            num_batches = (current_number_int // batch_size) + 1

            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []

                for i in range(num_batches):
                    start_number = current_number_int - (i * batch_size)
                    end_number = max(start_number - batch_size, 0)
                    futures.append(executor.submit(
                        process_batch, start_number, end_number))

                concurrent.futures.wait(futures)

                for future in futures:
                    final_data.extend(future.result())

                    with open("staah.json", "w") as json_file:
                        json.dump(final_data, json_file, indent=2)

                    # df = pd.DataFrame(final_data)
                    # df.to_excel('staahBooking.xlsx', index=False)

        except Exception as e:
            print(
                f"An error occurred for account {username} ({property_code}): {str(e)}")

finally:
    if 'driver' in locals():
        driver.quit()
