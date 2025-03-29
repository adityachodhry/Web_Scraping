import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup


page_no = 1
property_id = 1008
# Request parameters

initial_number_str = '00000006993'
current_number_int = int(initial_number_str)

# Headers with cookies
headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Cookie": "staahMaxThemeType=max1_grey; PHPSESSID=hr75452h6c8icoq6jjp2f17u8n; staahAuth=082d5c25411b319a1ca2d1c25a2f6fe5; TawkConnectionTime=0; twk_uuid_5a11f413198bd56b8c03c13a=%7B%22uuid%22%3A%221.PUnOsjQCmEqokMDY4y2eZdacZo83MTI7aKVQTVcBRE88DZnbzUNjQmsEQ2gWmNM6Nmt98Sz3jiYiN4oG7HXDjigD2ms1JkTmqGwIvHfUQ4ai4Vozv%22%2C%22version%22%3A3%2C%22domain%22%3A%22staah.net%22%2C%22ts%22%3A1706771771721%7D; AWSALB=vBo0mM0WYuMAc48YJmUEUDYLbDpASEBROw2zuM+2HtjdmRGBO3gxTJm+uwO9LqzF4eY2emKm/e6G0OQGPJlvFvz+fNOZhRHBQdlYc4w7CF3A/vC3B6L7bdS1p7hv; AWSALBCORS=vBo0mM0WYuMAc48YJmUEUDYLbDpASEBROw2zuM+2HtjdmRGBO3gxTJm+uwO9LqzF4eY2emKm/e6G0OQGPJlvFvz+fNOZhRHBQdlYc4w7CF3A/vC3B6L7bdS1p7hv"}
# Make the POST request with cookies

for i in range(8):

    new_number_str = str(current_number_int).zfill(len(initial_number_str))
    
    url = f'https://max.staah.net/hotels/booking_details.php?gb_propertyId={property_id}&bookingsId={property_id}{new_number_str}'
    print(url)

    current_number_int -= 1

    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        content = response.text
        with open('staah_content.html', 'w', encoding='utf-8') as html_file:
            html_file.write(content)

        print("HTML content saved to 'staah_content.html'")
        soup = BeautifulSoup(content, 'html.parser')

        # # Extracting data from the HTML code
        # reservation_details = soup.find('td', class_='headingRow').text.strip()

        # booking_date = soup.find('td', text='Booking Date').find_next('td').text.strip()
        # # Remove the timezone information (IST) and then parse the date
        # booking_date = datetime.strptime(re.sub(r'\s\(.*\)', '', booking_date), "%d-%b-%Y %I:%M:%S %p")
        # print(booking_date)

        # guest_name = soup.find('td', text='Name').find_next('td').text.strip()
        # print(guest_name)

        # arrival_date = soup.find('td', text='From').find_next('td').text.strip()
        # arrival_date = datetime.strptime(arrival_date, "%d %b %Y")

        # departure_date = soup.find('td', text='To').find_next('td').text.strip()
        # departure_date = datetime.strptime(departure_date, "%d %b %Y")

        # room_details = soup.find('td', class_='left').text.strip()

        # adults = int(re.search(r'Adults: (\d+)', room_details).group(1))

        # source = soup.find('td', text='Channel Name').find_next('td').text.strip()

        # total_charges = soup.find('td', class_='amountpaid').text.strip()
        # total_charges = float(re.search(r'INR (\d+,\d+\.\d+)', total_charges).group(1).replace(',', ''))

        # no_of_nights = int(re.search(r'No Of Nights : (\d+)', room_details).group(1))

        # Additional information can be extracted in a similar way

        # Formatting the data into the desired structure
        # formatted_data = {
        #     "res": reservation_details,
        #     "bookingDate": booking_date.strftime("%Y-%m-%d %H:%M:%S"),
        #     "guestName": guest_name,
        #     "arrivalDate": arrival_date.strftime("%Y-%m-%d"),
        #     "deptDate": departure_date.strftime("%Y-%m-%d"),
        #     "room": room_details,
        #     "pax": adults,
        #     # You may need to extract ADR from the relevant part of the HTML
        #     "ADR": None,
        #     "source": source,
        #     "totalCharges": total_charges,
        #     "noOfNights": no_of_nights,
        #     # Lead information may need to be extracted from the HTML
        #     "lead": None
        # }

        # print(formatted_data)

    else:
        print(
            f"Failed to get a valid response. Status code: {response.status_code}")
