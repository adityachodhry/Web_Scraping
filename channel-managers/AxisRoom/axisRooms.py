import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from mongo import push_to_mongodb
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Run the script with CLI options')
    parser.add_argument('--username', required=True)
    parser.add_argument('--password', required=True)
    return parser.parse_args()

# Get command-line arguments
args = parse_args()

accounts = [{'username': args.username, 'password': args.password}]

driver = webdriver.Chrome()

for account in accounts:
    username = account['username']
    password = account['password']
    url = 'https://app.axisrooms.com/'

    driver.get(url)
    time.sleep(4)

    # Input the credentials and submit the form
    driver.find_element(By.ID, 'emailId').send_keys(username)
    driver.find_element(By.ID, 'password').send_keys(password)

    # Wait for the login process
    time.sleep(4)

    driver.find_elements(By.CLASS_NAME, 'g-recaptcha')[0].click()

    # Wait for the login process to complete
    time.sleep(4)

    bookings_button = driver.find_element(
        By.CSS_SELECTOR, 'li[data-menu-name="Bookings"] a').click()

    time.sleep(4)

    cookies = driver.get_cookies()
    # print(cookies)

    access_token = None

    for cookie in cookies:
        if cookie['name'] == 'access_token':
            access_token = cookie['value']
            break

    print("Access Token : ", access_token)

    endpoint = "https://app.axisrooms.com/supplier/arcHotelBookingReport.html"

    headers = {
        'Cookie': f'access_token={access_token}'
    }

    result = []

    today = datetime.today().strftime("%d/%m/%Y")
    print(today)

    
    form_data = {
        "download": "false",
        "searchType": "GENERATION_TIME",
        "fromdate": "01/01/2021",
        "todate": today,
        "channelId": "-1",
        "city_id": "-1",
        "productId": "-1",
        "room_id": "-1",
        "status": "3",
        "nightCount": "-1",
        "modeofpayment": "-1",
        "chartAxis": "1"
    }
    
    response = requests.post(
        endpoint, headers=headers,  data=form_data)

    soup = BeautifulSoup(response.content, 'html.parser')

    total_bookings_element = soup.find('th', colspan="2", style="font-size:10px;")

        # Extract the total number of bookings
    if total_bookings_element:
            total_bookings_text = total_bookings_element.text.strip()
            total_bookings = int(total_bookings_text.split(":")[-1].strip())
            print("Total Number of Bookings:", total_bookings)

            # Find the table body
            table_body = soup.find('tbody')

            # Find all rows in the table
            rows = table_body.find_all('tr')

            # Iterate through rows and extract data up to total_bookings - 1
            for row in rows[:total_bookings]:
                # Find all columns in the row
                columns = row.find_all('td')
                
                hotelName = columns[2].text.strip()
                res = columns[1].text.strip()

                bookingDate_raw = columns[4].text.strip()
                bookingDate_obj = datetime.strptime(bookingDate_raw, '%d/%m/%Y %H:%M')
                bookingDate = bookingDate_obj.strftime('%Y-%m-%d')
                bookingDate_obj = datetime.strptime(bookingDate, '%Y-%m-%d')

                guestName = columns[10].text.strip()

                arrivalDate_raw = columns[6].text.strip()
                arrivalDate_obj = datetime.strptime(arrivalDate_raw, '%d/%m/%Y')
                arrivalDate = arrivalDate_obj.strftime('%Y-%m-%d')

                deptDate_raw = columns[7].text.strip()
                deptDate_obj = datetime.strptime(deptDate_raw, '%d/%m/%Y')
                deptDate = deptDate_obj.strftime('%Y-%m-%d')

                room = columns[3].text.strip()
                source = columns[0].text.strip()
                totalCharges = columns[13].text.strip()
                noOfNights = columns[5].text.strip()

                status = columns[14].text.strip()
                isActive = "true"

                hotelCode = columns[1].text.strip()

                lead_time_days = (arrivalDate_obj - bookingDate_obj).days


                payment_form = row.find('form', {'id': 'paymentConfirmationForm'})


                select_element = payment_form.find('input', {'name': 'productId'})
        
                # Check if the input element is found in the column
                if select_element:
                    # Extract the value attribute of the input element
                    hotelCode = select_element.get('value')

                    # Print the extracted data
                bkgDetails = {
                    "hotelName": hotelName,
                    "res": res,
                    "source": source,
                    "bookingDate": bookingDate,
                    "guestName": guestName,
                    "arrivalDate": arrivalDate,
                    "deptDate": deptDate,
                    "room": room,
                    "totalCharges": float(totalCharges),
                    "lead": lead_time_days,
                    "noOfNights": int(noOfNights),
                    "hotelCode" : hotelCode,
                    "isActive": isActive,
                    "ADR" : float(totalCharges) / int(noOfNights)
                    
                }
                result.append(bkgDetails)

    else:
        print(f"Request failed with status code: {response.status_code}")
    
    push_to_mongodb(result)