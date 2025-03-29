import time
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
import urllib.parse
from urllib.parse import urlunparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def getCurrentStatus(status,checkInDate,checkOut) :
    today = datetime.now()
    if status == "ok" :
        if checkInDate <= today :
            if checkOut <= today:
                finalStatus = "CO"
            if checkOut > today:
                finalStatus = "CI"
        elif checkInDate > today :
            finalStatus = "CFB"
    elif status == "cancelled_by_hotel" or status == "cancelled_by_guest":
        finalStatus = "CN"
    elif status == "no_show" :
        finalStatus = "NS"
    else :
        finalStatus = "UCB"

    return finalStatus

def bookingReservations(username, password, hotelCode=[]):
    finalReservation = []

    hotelCodes = []

    for hotelC in hotelCode :
        hotelCodes.append(int(hotelC))

    # Initialize the Chrome driver
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)

    # Open the URL
    driver.get('https://admin.booking.com')

    # Optional: Wait for the page to fully load
    driver.implicitly_wait(10)

    # Login process
    login_field = driver.find_element(By.ID, 'loginname')
    login_field.clear()
    login_field.send_keys(username)

    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_button.click()
    time.sleep(1)

    login_field = driver.find_element(By.ID, 'password')
    login_field.clear()
    login_field.send_keys(password)

    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_button.click()
    time.sleep(6)
    cookies = driver.get_cookies()

    optanon_consent_cookie = next((cookie['value'] for cookie in cookies if cookie['name'] == 'OptanonConsent'), None)

    # Parse the cookie value and extract the landingPath
    parsed_cookie = urllib.parse.parse_qs(optanon_consent_cookie)
    landing_path = parsed_cookie.get('landingPath', [None])[0]
    decoded_landing_path = urllib.parse.unquote(landing_path)
    parsed_landing_path = urllib.parse.urlparse(decoded_landing_path)
    query_params = urllib.parse.parse_qs(parsed_landing_path.query)
    ses_value = query_params.get('ses', [None])[0]

    driver.get(f"https://admin.booking.com/hotel/hoteladmin/groups/reservations/index.html?lang=xu&ses={ses_value}")
    time.sleep(5)

    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')

    # Find the script tag with the specific type
    script_tag = soup.find('script', type='application/json', attrs={'data-capla-application-context': True})

    if script_tag:
        # Load the JSON data from the script tag
        json_data = json.loads(script_tag.string)
        
        # Extract the partnerAccountId
        partner_account_id = json_data['partnerIdentity']['partnerAccountId']
    else:
        return {
            'loginStatus' : False
        }
    
    session = requests.Session()
    cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
    cookie_string = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
    session.cookies.update(cookie_dict)

    today = datetime.today()
    end_date = today
    start_date = today - timedelta(days=2*365)  # Start from two years ago
    date_interval = timedelta(days=90)  # 3 months interval

    # Loop through the date ranges
    while start_date < end_date:
        current_end_date = min(start_date + date_interval, end_date)

        # Initialize page number for pagination
        page_number = 0
        rows_per_page = 200
        print(current_end_date)
        while True:
            print(page_number)
            payload = json.dumps({
                "operationName": "searchReservations",
                "variables": {
                    "paymentStatusFeatureActive": True,
                    "input": {
                        "propertyIds": hotelCodes if hotelCode else [],
                        "typeOfDate": "BOOKING",
                        "dateFrom": start_date.strftime('%Y-%m-%d'),
                        "dateTo": current_end_date.strftime('%Y-%m-%d'),
                        "onlyPendingRequests": False,
                        "statusCriteria": {
                            "showCancelled": False,
                            "showOk": False,
                            "showNoShow": False,
                            "showPaidOnline": False
                        },
                        "pagination": {
                            "rowsPerPage": rows_per_page,
                            "offset": page_number
                        },
                        "accountId": partner_account_id
                    }
                },
                "extensions": {},
                "query": "query searchReservations($input: SearchReservationInput!, $paymentStatusFeatureActive: Boolean = false) {\n  partnerReservation {\n    searchReservations(input: $input) {\n      properties {\n        address\n        countryCode\n        cityName\n        extranetHomeUrl\n        status\n        name\n        id\n        __typename\n      }\n      reservations {\n        actualCommissionRaw\n        aggregatedRoomStatus\n        amountInvoicedOrRoomPriceSum\n        amountInvoicedOrRoomPriceSumRaw\n        bookerFirstName\n        bookerLastName\n        createdAt\n        currencyCode\n        propertyId\n        id\n        isGeniusUser\n        checkout\n        checkin\n        occupancy {\n          guests\n          adults\n          children\n          childrenAges\n          __typename\n        }\n        pendingGuestRequestCount\n        paymentStatus @include(if: $paymentStatusFeatureActive)\n        __typename\n      }\n      reservationsHavePaymentCharge\n      totalRecords\n      __typename\n    }\n    __typename\n  }\n}\n"
            })

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                'Referer': urlunparse(parsed_landing_path),
                'Content-Type': 'application/json',
                'Cookie': cookie_string
            }

            url = f"https://admin.booking.com/dml/graphql.json?lang=xu&ses={ses_value}"

            response = requests.post(url, headers=headers,data=payload, allow_redirects=False)
            # print(response.text)
            
            try :
                with open(f'bookingRaw.json', 'w') as json_file:
                    json.dump(response.json(), json_file, indent=2)
                response_data = response.json().get('data').get('partnerReservation').get('searchReservations').get('reservations')
            except :
                break

            if not response_data:
                break  # Break the loop if no more reservations are found

            for res in response_data:
                checkIn = datetime.strptime(res.get('checkin'), '%Y-%m-%d')
                checkOut = datetime.strptime(res.get('checkout'), '%Y-%m-%d')

                status = getCurrentStatus(res.get('aggregatedRoomStatus'),checkIn,checkOut)
                los = (checkOut - checkIn).days
                hCode = str(res.get('propertyId'))
                reservation_number = res.get('id')

                reservation = {
                    "hotelCode": hCode,
                    "reservationNumber": reservation_number,
                    "source": "Booking.com",
                    "sourceSegment": "OTA",
                    "isGroup": False,
                    "guestDetails": {
                        "name": f"{res.get('bookerFirstName')} {res.get('bookerLastName')}"
                    },
                    "bookingDetails": {
                        "arrivalDate": res.get('checkin'),
                        "departureDate": res.get('checkout'),
                        "totalNights": los,
                        "currentStatus": status,
                        "bookingType": "CHANNEL",
                        "roomDetails": {
                            "pax": {
                                "totalAdults": res.get('occupancy').get('guests'),
                                "totalChildren": 0
                            }
                        },
                        "createdOn": res.get('createdAt')
                    },
                    "paymentDetails": {
                        "status": "Fully Paid" if float(res.get('amountInvoicedOrRoomPriceSumRaw')) > 0 else "Not Paid",
                        "amount": float(res.get('amountInvoicedOrRoomPriceSumRaw')),
                    },
                    "priceSummary": {
                        "roomCost": float(res.get('amountInvoicedOrRoomPriceSumRaw')) - float(res.get('actualCommissionRaw')),
                        "totalCost": float(res.get('amountInvoicedOrRoomPriceSumRaw')),
                        "commissionAmount": float(res.get('actualCommissionRaw'))
                    }
                }

                finalReservation.append(reservation)

            page_number += 1

        # Move to the next 3-month period
        start_date += date_interval

    # Close the browser after use
    driver.quit()

    return finalReservation

# finalRes = bookingReservations('Retvensnew', 'October@2024',[])

# with open(f'bookingRes.json', 'w') as json_file:
#     json.dump(finalRes, json_file, indent=2)