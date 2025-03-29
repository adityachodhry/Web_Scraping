import requests
import time
import json
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

            time.sleep(5)
            driver.refresh()

            cookies = driver.get_cookies()
            auth_token_7 = next((cookie['value'] for cookie in cookies if cookie['name'] == 'auth_token_7'), None)
            csrftoken = next((cookie['value'] for cookie in cookies if cookie['name'] == 'csrftoken'), None)

            roomIdEndpoint = "https://apps.djubo.com/core-data/properties"

            headers = {
                'cookie': f'auth_token_7={auth_token_7}',
                'x-requested-with': 'XMLHttpRequest',
                'djng-remote-method': 'update_rate_plan_rates'
            }

            response = requests.get(roomIdEndpoint, headers=headers)

            if response.status_code == 200:
                result_data = response.json()

                if isinstance(result_data, list) and len(result_data) > 0:
                    first_item = result_data[0]

                    accountId = first_item['account_id']
                    # propertyCode = first_item['id']
                
                for conf in ratesConfig:
                    date = conf.get('date')
                    channelCode = conf.get('channelCode')
                    roomId = conf.get('roomId')
                    roomName = conf.get('roomName')
                    rateTypeId = conf.get('rateTypeId')
                    mealPlanId = conf.get('mealPlanId')
                    occupancy = conf.get('occupancy')
                    seasonCode = conf.get('seasonCode')
                    displayOrderId = conf.get('displayOrderId')
                    selectWeekdays = conf.get('selectWeekdays')
                    selectWeekdaysRate = conf.get('selectWeekdaysRate')
                    startDate = conf.get('startDate')

                    ratePushResponseUrl = f"https://apps.djubo.com/rates-admin/accounts/{accountId}/properties/{propertyCode}/rates/rate-plans/{seasonCode}/"

                    headers = {
                        'cookie': f'auth_token_7={auth_token_7}; csrftoken={csrftoken}',
                        'x-requested-with': 'XMLHttpRequest',
                        'djng-remote-method': 'fetch_rates_by_rate_type',
                        'Content-Type': 'application/json'
                    }

                    payload = json.dumps({
                        "rate_plan": seasonCode,
                        "rate_type": rateTypeId,
                        "property_meal_plans": [
                            {
                            "name": "Room Only",
                            "short_name": "EP",
                            "constant_id": 1,
                            "display_order": 1
                            },
                            {
                            "name": "Breakfast",
                            "short_name": "CP",
                            "constant_id": 2,
                            "display_order": 2
                            },
                            {
                            "name": "Breakfast and Lunch/Dinner",
                            "short_name": "MAP",
                            "constant_id": 3,
                            "display_order": 3
                            },
                            {
                            "name": "Breakfast,Lunch and Dinner",
                            "short_name": "AP",
                            "constant_id": 4,
                            "display_order": 4
                            },
                            {
                            "name": "MAPAI",
                            "short_name": "MAPAI",
                            "constant_id": 5,
                            "display_order": 5
                            },
                            {
                            "name": "APAI",
                            "short_name": "APAI",
                            "constant_id": 6,
                            "display_order": 6
                            }
                        ]
                    })

                    ratePushResponseData = requests.post(ratePushResponseUrl, headers=headers, data=payload)

                    if ratePushResponseData.status_code == 200:
                        result_data = ratePushResponseData.json()

                        if isinstance(result_data, list) and len(result_data) > 0:
                            first_item = result_data[0]

                            current_rates = {
                                "weekday_sun_rate": int(float(first_item.get('weekday_sun_rate', 0))),
                                "weekday_mon_rate": int(float(first_item.get('weekday_mon_rate', 0))),
                                "weekday_tue_rate": int(float(first_item.get('weekday_tue_rate', 0))),
                                "weekday_wed_rate": int(float(first_item.get('weekday_wed_rate', 0))),
                                "weekday_thu_rate": int(float(first_item.get('weekday_thu_rate', 0))),
                                "weekday_fri_rate": int(float(first_item.get('weekday_fri_rate', 0))),
                                "weekday_sat_rate": int(float(first_item.get('weekday_sat_rate', 0)))
                            }

                            day_map = {
                                "Sun": "weekday_sun_rate",
                                "Mon": "weekday_mon_rate",
                                "Tue": "weekday_tue_rate",
                                "Wed": "weekday_wed_rate",
                                "Thu": "weekday_thu_rate",
                                "Fri": "weekday_fri_rate",
                                "Sat": "weekday_sat_rate"
                            }

                            changedRates = []
                            for i, day in enumerate(selectWeekdays):
                                if day in day_map:
                                    day_key = day_map[day]
                                    current_rates[day_key] = selectWeekdaysRate[i]
                                    changedRates.append(day_key)

                            selectDateUrl = f"https://apps.djubo.com/rates-admin/accounts/{accountId}/properties/{propertyCode}/rates/bar-calendar/"

                            date_list = [date.strip() for date in startDate.split(',')] 

                            payload = json.dumps([{
                                "date": date,
                                "rate_plan_id": seasonCode,
                                "is_deleted": False
                            } for date in date_list]) 

                            headers = {
                                'cookie': f'auth_token_7={auth_token_7}',
                                'x-requested-with': 'XMLHttpRequest',
                                'djng-remote-method': 'map_calendar_rates',
                                'Content-Type': 'application/json'
                            }

                            selectDateResponse = requests.post(selectDateUrl, headers=headers, data=payload)

                            if selectDateResponse.status_code == 200:
                                response_content = selectDateResponse.json()
                                print(response_content)
                                # print("Date(s) selected successfully!")
                            else:
                                print("Failed to select date(s).")

                            payload = json.dumps({
                                "rates_meta_data": [
                                    {
                                        "category": {
                                            "id": roomId,
                                            "name": roomName,
                                            "display_order": displayOrderId
                                        },
                                        "occupancy": occupancy,
                                        "meal_plan": mealPlanId,
                                        "weekday_sun_rate": current_rates["weekday_sun_rate"],
                                        "weekday_mon_rate": current_rates["weekday_mon_rate"],
                                        "weekday_tue_rate": current_rates["weekday_tue_rate"],
                                        "weekday_wed_rate": current_rates["weekday_wed_rate"],
                                        "weekday_thu_rate": current_rates["weekday_thu_rate"],
                                        "weekday_fri_rate": current_rates["weekday_fri_rate"],
                                        "weekday_sat_rate": current_rates["weekday_sat_rate"],
                                        "last_updated_utc_timestamp": f'{startDate}T00:00:00Z',
                                        "changedRates": changedRates,
                                        "changeOccupancy": True
                                    },
                                ],
                                "rate_type_id": rateTypeId,
                                "channel_id": channelCode,
                                "copy_to_all_channel": True,
                                "allRateTypeChannelsIds": [channelCode],
                                "check_zero_rates": True
                            })
                            # print(payload)

                            headers = {
                                'cookie': f'auth_token_7={auth_token_7}; csrftoken={csrftoken}',
                                'x-requested-with': 'XMLHttpRequest',
                                'djng-remote-method': 'update_rate_plan_rates',
                                'Content-Type': 'application/json'
                            }

                            ratePushResponse = requests.post(ratePushResponseUrl, headers=headers, data=payload)

                            if ratePushResponse.status_code == 200:
                                print(ratePushResponse.text)
                            else:
                                print("Failed to update rates.")
                    else:
                        print("Failed to fetch current rates.")

        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("Login failed. Please check your credentials.")

    driver.quit()

# cmCreds = {
#     "username" : "Sales@shivacontinental.in",
#     "password" : "shiva@1234"
# }
# ratesConfig = [{
    # "startDate": "2024-09-11",
    # "selectWeekdays": ["Wed", "Thu"],
    # "selectWeekdaysRate": [2800, 2800],
    # "seasonCode": 70211,
    # "occupancy": 1,
    # "mealPlanId": 1,
    # "rateTypeId": 2892,
    # "roomId": 1912,
    # "roomName": "Deluxe with balcony (Non view | limited parking)",
    # "channelCode": 101,
    # "displayOrderId": 1
# }]
# djuboRatePush('670', cmCreds, ratesConfig)
