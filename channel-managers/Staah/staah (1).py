import requests
import re , json
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

url = "https://max.staah.net/hotels/lib/bookings.php?gb_propertyId=5566&gb_returntype=json"
result = []

# Request parameters
data = {
    "Action": "displayBookings",
    "PageNo": "1",
    "channel_flag": "Y"
}

# Headers with cookies
headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Cookie":'staahMaxThemeType=max1_grey; PHPSESSID=jsdvp94rdtpsh7q1cma5g4iueo; staahAuth=37a413c5ab69c2585da5d72427944a53; twk_uuid_5a11f413198bd56b8c03c13a=%7B%22uuid%22%3A%221.PUnOsjQCmEqokMDY4y2eZdacZo83MTI7aKVQTVcBRE88DZnbzUNjQmsEQ2gWmNM6Nmt98Sz3jiYiN4oG7HXDjigD2ms1JkTmqGwIvHfUQ4ai4Vozv%22%2C%22version%22%3A3%2C%22domain%22%3A%22staah.net%22%2C%22ts%22%3A1706620048829%7D; TawkConnectionTime=1706620053819; AWSALB=6b5McsIg/cqyEKGgnO66Hcv23HIjbH3LxzTxJGBwzHCKx22ueXEHPgIriOf+lxamDzDhihx+bvO9t0Avk8/e7Q52POYifcj8T7or0RKZS2SYlJEFlj0UiLUq90Sf; AWSALBCORS=6b5McsIg/cqyEKGgnO66Hcv23HIjbH3LxzTxJGBwzHCKx22ueXEHPgIriOf+lxamDzDhihx+bvO9t0Avk8/e7Q52POYifcj8T7or0RKZS2SYlJEFlj0UiLUq90Sf'
}

# Make the POST request with cookies
response = requests.post(url, data=data, headers=headers)
json_response = response.json()
content_data = json_response.get("content", "")

# Save the "content" to a separate file

input_string = content_data

# Replace newline characters with one space
step1_result = input_string.replace("\n", " ")

# Replace "\\" with one space
final_result = step1_result.replace("\\", '')

# Save the final result to a text file
with open('content_data.txt', 'w', encoding='utf-8') as content_file:
    content_file.write(final_result)

print("Content saved to 'content_data.txt'")

if response.status_code == 200:

        soup = BeautifulSoup(final_result, 'html.parser')

        rows = soup.find_all('tr', class_=lambda x: x and 'lazy' in x)

        for row in rows:
            booking_id = row.select_one('div[data-original-title="Booked using currency - INR"]').text.strip()
            bookingDate = row.select_one('td[class=""]').text.strip()
            checkinDate = row.select_one('td:nth-of-type(3)').text.strip()
            deptDate = row.select_one('td:nth-of-type(4)').text.strip()

            source = row.find_all("td", class_=lambda x: x and 'source' in x).text.strip()

            guestName = row.select_one('.priority-icon').text.strip()
            pax = row.select_one('.text-center').text.strip()
            status = row.select_one('.confirm-status').text.strip()

            

            print(bookingDate)
            print(checkinDate)
            print(deptDate)
            print(guestName)
            print(booking_id)
            print(source)
            print(pax)
            print(status)
            
            
            break

        # print(bookingDate)
        # print(checkinDate)
        # print(deptDate)
    
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")

with open('staah_result.json', 'w') as json_file:
            json.dump(result, json_file,indent=2)