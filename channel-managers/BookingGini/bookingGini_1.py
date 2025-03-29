import time
import requests
import random
import json
from datetime import datetime, timedelta
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from pymongo import MongoClient
from bs4 import BeautifulSoup


current_date = datetime.now()

results = []

accounts = [
    {"email":"dir@zorisboutiquehotel.com","password":"Zoris@6262"}
]

for account in accounts:
        email = account['email']
        password = account['password']

        def login(email , password):

            body = {
                "email": email, 
                "password": password,
                "browser": "Chrome", 
                "creation_mode": "WEBSITE"
                }

            login_url = "https://kernel.bookingjini.com/extranetv4/admin/auth"
            login_request = requests.post(login_url, body)

            login_response = login_request.json()
            message = login_response['message']
            hotelId = login_response['hotel_id']
            userId = login_response['admin_id']

            if message == "User authentication successful":
                print(message)
            elif message == "Authentication failed":
                print(message)

            return userId,hotelId
            

        hotelId,propertyId = login(email , password)

        def get_hotel_id(userid,hotelId):
            endpoint = f"https://kernel.bookingjini.com/extranetv4/get-user-details/{userid}/{hotelId}"
            request = requests.get(endpoint)

            response = request.json()

            hotel_id = response['user_details']['organization_id']

            return hotel_id


        hotelId = get_hotel_id(hotelId,propertyId)

        headers = {
            'Content-Type': 'application/json',
        }

        body = {
            "from_date": "2022-10-01",
            "to_date": "2024-04-19",
            "date_type": "1",
            "source": [
                11992,
                12002,
                12085,
                12157,
                -5,
                -2,
                -3,
                -1,
                -4,
                -6
            ],
            "booking_status": "confirm",
            "hotel_id": hotelId,
            "booking_id": ""
        }

        post_endpoint = "https://be.bookingjini.com/extranetv4/booking-lists"
        post_response = requests.post(post_endpoint, headers=headers, json=body)

        response_data = post_response.json()
        booking_details = response_data['data']

        results = []

        for booking in booking_details:
            bkgDetails = {}

            booking_id = booking['unique_id']
            source = booking['channel_name']

            get_endpoint = f"https://be.bookingjini.com/extranetv4/voucher-display/{booking_id}/{source}"
            get_response = requests.get(get_endpoint)

            html_content = get_response.text
            with open("bookingGini.html", "w", encoding="utf-8") as file:
                file.write(html_content)
            soup = BeautifulSoup(html_content, 'html.parser')

            try:
                # Extract Room Details
                room_details_table = soup.find('p', string='Room Details ')

                # Extract other details
                bkgDetails['hotelName'] = "Zoris Boutique Hotel"
                # bkgDetails['hotelName'] = soup.find(
                #     'font', class_='legend-content').get_text(strip=True)
                bkgDetails['res'] = booking_id
                bookingDate_obj = soup.find(
                    'font', class_='legend-font', string='Booking Date : ').find_next_sibling().get_text(strip=True)

                bookingDate = datetime.strptime(bookingDate_obj, "%d %b %Y %H:%M:%S")

                # Keep only the date part
                formatted_date = bookingDate.strftime("%Y-%m-%d")
                bkgDetails['bookingDate'] = formatted_date

                guest_details_table = soup.find('p', string='Guest Details ')

                if guest_details_table:
                    guest_name_elements = soup.find_all(
                        'font', class_='legend-font', string=' Guest Name : ')

                    if guest_name_elements:
                        guest_name_element = next((element.find_next(
                            'font', class_='legend-content') for element in guest_name_elements), None)
                        if guest_name_element:
                            guest_name = guest_name_element.get_text()
                            bkgDetails['guestName'] = guest_name
                        else:
                            bkgDetails['guestName'] = "Not found"
                    else:
                        print("Guest name element not found")
                else:
                    print("Guest details not found")

                checkinDate_obj = soup.find(
                    'font', class_='legend-font', string='Checkin Date : ').find_next_sibling().get_text(strip=True)
                checkinDate = datetime.strptime(
                    checkinDate_obj, "%Y-%m-%d").strftime("%Y-%m-%d")
                bkgDetails['arrivalDate'] = checkinDate

                checkoutDate = soup.find('font', class_='legend-font',
                                        string='Checkout Date : ').find_next_sibling().get_text(strip=True)
                bkgDetails['deptDate'] = checkoutDate

                if room_details_table:
                    room_details_table = soup.find(
                        'p', string='Room Details ').find_next('table')
                    room_rows = room_details_table.find_all('tr', class_='row')[
                        1:]  # Skip the header row

                    for row in room_rows:
                        room_type = row.find(
                            'td', class_='col-md-3').get_text(strip=True)
                        rate_plan = row.find(
                            'td', class_='col-md-3').find_next('td').get_text(strip=True)
                        rooms = row.find('td', class_='col-md-2').get_text(strip=True)
                        adults = row.find(
                            'td', class_='col-md-2').find_next('td').get_text(strip=True)
                        children = row.find(
                            'td', class_='col-md-2').find_next('td').find_next('td').get_text(strip=True)

                        # Concatenate room_type and rate_plan into a single string
                        bkgDetails['room'] = f"{room_type} - {rate_plan}"
                        bkgDetails['pax'] = f"{adults}/{children}"

                bkgDetails['source'] = soup.find(
                    'font', class_='legend-font', string='Channel Name : ').find_next_sibling().get_text(strip=True)

                bkgDetails['noOfNights'] = int(soup.find(
                    'font', class_='legend-font', string='No of Nights : ').find_next_sibling().get_text(strip=True))

                pricing_details_sections = soup.find_all('section')

                for section in pricing_details_sections:
                    total_amount_elem = section.find(
                        'font', class_='legend-font', string=' Total Amount : ')

                    if total_amount_elem:
                        total_amount_str = total_amount_elem.find_next(
                            'font', class_='legend-content').get_text(strip=True)
                        bkgDetails['totalAmount'] = float(
                            ''.join(filter(lambda x: x.isdigit() or x == '.', total_amount_str)))

                lead_time = (datetime.strptime(
                    checkinDate, "%Y-%m-%d") - bookingDate).days
                bkgDetails['lead'] = lead_time

                bkgDetails['isActive'] = "true"
            except Exception as e:
                print(f"An error occurred: {e}")
                # Handle the exception as per your requirements

            results.append(bkgDetails)
            print(results)

        # Save the final results to a JSON file after processing all date ranges
        with open('bookingGiniResponse_data.json', 'w') as json_file:
            json.dump(response_data, json_file, indent=2)
        with open("bookingGini.html", "w", encoding="utf-8") as file:
            file.write(html_content)
        with open('bookingGini.json', 'w') as json_file:
            json.dump(results, json_file, indent=2)
