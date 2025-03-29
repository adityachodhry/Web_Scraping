from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import datetime
import requests
import time

def get_cookies_and_formtoken(url):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)  # Keep browser open after script exits
    driver = webdriver.Chrome(options=options)
    
    driver.get(url)
    cookies = driver.get_cookies()
    script_element = driver.find_element(By.ID, "__R9_HYDRATE_DATA__")
    script_content = script_element.get_attribute("innerHTML")
    parsed_data = json.loads(script_content)
    formtoken_value = parsed_data['serverData']['global']['formtoken']
    print('; '.join([f"{cookie['name']}={cookie['value']}" for cookie in cookies]))
    print(formtoken_value)
    return driver, cookies, formtoken_value

def get_hotel_rates(check_in_date, check_out_date, hid, cookies, formtoken_value):
    url = f"https://www.kayak.co.in/i/api/search/v1/hotels/rates?rooms=1&adults=2&priceMode=nightly-total&checkout={check_out_date}&checkin={check_in_date}&hid={hid}"

    headers = {
        'X-Csrf': formtoken_value,
        'Referer': 'https://www.kayak.co.in/hotels/p58595-h351128-details/',
        'Cookie': '; '.join([f"{cookie['name']}={cookie['value']}" for cookie in cookies]),
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    print(response.text)
    response_data = response.json()
    data = response_data["groups"]
    rates = extract_rates(data, check_in_date, check_out_date)
    return rates

def extract_rates(data, check_in_date, check_out_date):
    rates = []
    for x in data :
        for deal in x['rows']:
            for option in deal['bookingOptions']:
                rate = {
                    'checkin': check_in_date,
                    'checkout': check_out_date,
                    'provider': option['localizedProviderName'],
                    'room_type': deal['localizedDescription'],
                    'price': option['price']['price'],
                    'currency': option['price']['currency'],
                    'freebies': [freebie['localizedName'] for freebie in option['freebies']]
                }
                rates.append(rate)
    return rates

if __name__ == "__main__":
    today = datetime.datetime.now()
    hid = 2406159
    url = "https://www.kayak.co.in/hotels/Amar-Kothi,Udaipur,RJ,India-p58595-h351128-details/2024-02-21/2024-02-22/2adults"

    driver, cookies, formtoken_value = get_cookies_and_formtoken(url)

    all_rates = []
    for day in range(10):
        check_in_date = (today + datetime.timedelta(days=day)).strftime("%Y-%m-%d")
        check_out_date = (today + datetime.timedelta(days=day + 1)).strftime("%Y-%m-%d")
        
        rates = get_hotel_rates(check_in_date, check_out_date, hid, cookies, formtoken_value)
        all_rates.extend(rates)

    with open(f'{hid}_kayak_rates.json', 'w') as json_file:
        json.dump(all_rates, json_file, indent=2)

    print("Rates extracted and saved in 'hotel_rates.json'")

