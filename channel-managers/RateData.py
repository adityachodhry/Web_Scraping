import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from datetime import datetime

file_path = "D:\\Downloads\\RateDates.xlsx"
excel_data = pd.read_excel(file_path)

dates_to_check = excel_data.iloc[:, 0].tolist()

url = "https://live.ipms247.com/booking/rmdetails"

month_prices = {}

for checkin_date in dates_to_check:
    checkin_date_str = checkin_date.strftime("%d-%m-%Y")

    payload = {
        'checkin': checkin_date_str,
        'gridcolumn': 1,
        'adults': 1,
        'child': 0,
        'nonights': 1,
        'ShowSelectedNights': 'true',
        'DefaultSelectedNights': 1,
        'calendarDateFormat': 'dd-mm-yy',
        'rooms': 1,
        'HotelId': '44715',
        'isLogin': 'lf',
        'modifysearch': 'false',
        'layoutView': 2,
        'ShowMinNightsMatchedRatePlan': 'false',
        'LayoutTheme': 2,
        'w_showadult': 'false',
        'w_showchild_bb': 'false',
        'w_showchild': 'true',
        'ischeckavailabilityclicked': 1
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': 'PHPSESSID=37p0bcju74bi3t5t4mi7bvgine; AWSALB=vVBceob/+HvOUVdjW0uXIKce2WzO5T8xa4Zj4dvGia+iz2PmpyewAcXOWuccxz4KzksvbuUMcvPoKY8ZHj9fwnKWhyjR02/dz5N1bnE8EJRDZisxXSfmbVtDtbjs049spxC1HrQXoFupf1cpdfL0qxJmXkFE4lYZm09U0Kjz+NPwk9/86yI2qQgx3qLs7A==; AWSALBCORS=vVBceob/+HvOUVdjW0uXIKce2WzO5T8xa4Zj4dvGia+iz2PmpyewAcXOWuccxz4KzksvbuUMcvPoKY8ZHj9fwnKWhyjR02/dz5N1bnE8EJRDZisxXSfmbVtDtbjs049spxC1HrQXoFupf1cpdfL0qxJmXkFE4lYZm09U0Kjz+NPwk9/86yI2qQgx3qLs7A==',
        'Origin': 'https://live.ipms247.com',
        'Referer': 'https://live.ipms247.com/booking/book-rooms-obrigadobycraftels',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        price_elem = soup.find('span', class_='rate2')

        if price_elem:
            price_text = price_elem.text.strip()
            price_value = float(price_text.replace('$', '').replace(',', ''))

            month_prices[checkin_date.strftime("%Y-%m-%d")] = {
                'checkin_date': checkin_date_str,
                'price': price_value
            }
        else:
            print(f"No price found for {checkin_date_str}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {checkin_date_str}: {e}")

with open('daily_prices.json', 'w', encoding='utf-8') as json_file:
    json.dump(month_prices, json_file, ensure_ascii=False, indent=4)

print("Daily prices extracted and stored in 'daily_prices.json'.")
