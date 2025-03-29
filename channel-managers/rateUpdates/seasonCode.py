import requests
import time
import json, re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def djuboRatePush(propertyCode, cmCreds, ratesConfig):

    username = cmCreds.get('username')
    password = cmCreds.get('password')

    driver = webdriver.Chrome()

    url = 'https://apps.djubo.com/sign-in/'

    driver.get(url)

    # Log in
    driver.find_element(By.NAME, 'email_address').send_keys(username)
    driver.find_element(By.NAME, 'password').send_keys(password)
    driver.find_element(By.CLASS_NAME, 'submitBtn').click()

    time.sleep(4)

    if driver.current_url != url:
        print("Login Successful.")

    try:
        manage_property_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "li[title='Manage this Property'] a.manage-property"))
        )
        manage_property_link.click()
        print("Clicked 'Manage this Property' link.")
    except Exception as e:
        print("Error while clicking 'Manage this Property':", e)

    rate_planner_url = f"http://apps.djubo.com/rates-admin/accounts/3920/properties/{propertyCode}/rates/bar-calendar/"
    driver.get(rate_planner_url)
    print("Navigated to 'Rate Planner'.")

    time.sleep(5)
    driver.refresh()

    cookies = driver.get_cookies()
    auth_token_7 = next((cookie['value'] for cookie in cookies if cookie['name'] == 'auth_token_7'), None)
    csrftoken = next((cookie['value'] for cookie in cookies if cookie['name'] == 'csrftoken'), None)

    accountIdEndpoint = "https://apps.djubo.com/core-data/properties"

    headers = {
        'cookie': f'auth_token_7={auth_token_7}',
        'x-requested-with': 'XMLHttpRequest',
        'djng-remote-method': 'update_rate_plan_rates'
    }

    response = requests.get(accountIdEndpoint, headers=headers)

    if response.status_code == 200:
        result_data = response.json()

        if isinstance(result_data, list) and len(result_data) > 0:
            first_item = result_data[0]
            accountId = first_item['account_id']

    # To hold multiple payloads for all dates
    full_payload = []

    for conf in ratesConfig:
        date = conf.get('date')
        channelCode = conf.get('channelCode')
        roomId = conf.get('roomId')
        roomName = conf.get('roomName')
        rateTypeId = conf.get('rateTypeId')
        mealPlanId = conf.get('mealPlanId')
        occupancy = conf.get('occupancy')
        displayOrderId = conf.get('displayOrderId')
        selectWeekdays = conf.get('selectWeekdays')
        selectWeekdaysRate = conf.get('selectWeekdaysRate')

        sessonCodeAPI = f"https://apps.djubo.com/rates-admin/accounts/{accountId}/properties/{propertyCode}/rates/bar-calendar/"

        headers = {
            'cookie': f'auth_token_7={auth_token_7}; csrftoken={csrftoken}'
        }

        response = requests.get(sessonCodeAPI, headers=headers)

        if response.status_code == 200:
            response_html = response.text  

            rates_plan_match = re.search(r'name="rates_calendar" value="(.+?)"', response_html)
            if rates_plan_match:
                rates_plan_value = rates_plan_match.group(1)

                rates_plan_value = rates_plan_value.replace("&quot;", '"')

                rates_plan_list = json.loads(rates_plan_value)

                # Create a dictionary to store date and corresponding seasonCode (rate_plan_id)
                date_season_map = {}

                for plan in rates_plan_list:
                    givenDate = plan.get('date')
                    seasonCode = plan.get('rate_plan')

                    # Log the available dates and their season codes
                    print(f"Available date: {givenDate}, Season code: {seasonCode}")

                    # Check if the given date is in the provided dates
                    if givenDate == date:
                        date_season_map[givenDate] = seasonCode

                # Log the complete date_season_map
                print("Date to season code mapping:", date_season_map)

                # Now construct the payload using the date_season_map
                try:
                    if date in date_season_map:
                        payload_entry = {
                            "date": date,
                            "rate_plan_id": date_season_map[date],  # Get the corresponding seasonCode
                            "is_deleted": False
                        }
                        full_payload.append(payload_entry)  # Append to the full payload list
                    else:
                        print(f"Warning: No season code found for the date '{date}'. Skipping this entry.")
                        continue  # Skip this iteration if no season code is found for the date

                except KeyError as e:
                    print(f"KeyError: The date '{e}' was not found in date_season_map. Please check if the date exists.")
                    continue  # Skip this iteration if a KeyError occurs

        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            continue  # Skip this iteration if data retrieval fails

    # Now send the full payload
    selectDateUrl = f"https://apps.djubo.com/rates-admin/accounts/{accountId}/properties/{propertyCode}/rates/bar-calendar/"

    headers = {
        'cookie': f'auth_token_7={auth_token_7}',
        'x-requested-with': 'XMLHttpRequest',
        'djng-remote-method': 'map_calendar_rates',
        'Content-Type': 'application/json'
    }

    if full_payload:  # Ensure full_payload is not empty
        payload_json = json.dumps(full_payload)  # Convert the payload list to JSON
        print("Final Payload to be sent:", payload_json)  # Log the full payload

        selectDateResponse = requests.post(selectDateUrl, headers=headers, data=payload_json)

        if selectDateResponse.status_code == 200:
            response_content = selectDateResponse.json()
            print(response_content)
        else:
            print("Failed to select date(s).")
    else:
        print("No valid payload found to send.")


# Credentials and rate configurations
cmCreds = {
    "username": "Sales@shivacontinental.in",
    "password": "shiva@1234"
}

ratesConfig = [
    {
        "date": "2024-09-12",
        "occupancy": 1,
        "mealPlanId": 1,
        "rateTypeId": 2892,
        "roomId": 1912,
        "roomName": "Deluxe with balcony (Non view | limited parking)",
        "channelCode": 101,
        "selectWeekdays": "Thu",
        "selectWeekdaysRate": 2900,
        "displayOrderId": 1
    },
    {
        "date": "2024-09-14",
        "occupancy": 1,
        "mealPlanId": 1,
        "rateTypeId": 2892,
        "roomId": 1913,
        "roomName": "Deluxe (Non View)",
        "channelCode": 101,
        "selectWeekdays": "Thu",
        "selectWeekdaysRate": 3400,
        "displayOrderId": 1
    }
]

djuboRatePush('670', cmCreds, ratesConfig)
