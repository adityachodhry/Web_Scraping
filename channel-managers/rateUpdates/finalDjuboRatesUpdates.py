import requests
import time
import json, re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime


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
        print("Clicked 'Manage this Property' link.")
    except Exception as e:
        print("Error while clicking 'Manage this Property':", e)
    
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

    rate_planner_url = f"http://apps.djubo.com/rates-admin/accounts/{accountId}/properties/{propertyCode}/rates/bar-calendar/"
    driver.get(rate_planner_url)
    print("Navigated to 'Rate Planner'.")

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


    for config in ratesConfig.get('info', []):
        rateTypeId = config.get('rateTypeId')
        channelCode = config.get('channelCode')
        
        for room in config.get('roomInfo', []):
            roomId = room.get('roomId')
            
            for roomPlan in room.get('roomPlanInfo', []):
                roomPlanDetails = roomPlan.get('roomPlan', {})
                mealPlanId = roomPlanDetails.get('mealPlanId')
                occupancyId = roomPlanDetails.get('occupancyId')
                rate = roomPlanDetails.get('rate')
                date = roomPlanDetails.get('date')
        
                date_season_map = {}

                for plan in rates_plan_list:
                    givenDate = plan.get('date')
                    seasonCode = plan.get('rate_plan')

                    if givenDate == date:
                        date_season_map[givenDate] = seasonCode
                        break

                date_obj = datetime.strptime(date, "%Y-%m-%d")
                day_name = date_obj.strftime("%a") 


                selectDateUrl = f"https://apps.djubo.com/rates-admin/accounts/{accountId}/properties/{propertyCode}/rates/bar-calendar/"

                headers = {
                    'cookie': f'auth_token_7={auth_token_7}',
                    'x-requested-with': 'XMLHttpRequest',
                    'djng-remote-method': 'map_calendar_rates',
                    'Content-Type': 'application/json'
                }

                if date in date_season_map:
                    payload_entry = {
                        "date": date,
                        "rate_plan_id": date_season_map[date],  
                        "is_deleted": False
                    }

                    selectDateResponse = requests.post(selectDateUrl, headers=headers, data=payload_entry)

                    if selectDateResponse.status_code == 200:
                        response_content = selectDateResponse.json()
                        print(response_content)
                else:
                    print(f"Warning: No season code found for the date '{date}'. Skipping this entry.")
                    continue
                    
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

                        for item in result_data:
                            room_id = item['category']['id']
                            room_name = item['category']['name']


                            if roomId == room_id:
                                RoomName = room_name
                                break

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
                        rate_field = day_map.get(day_name)

                        changedRates = []
                        if rate_field:
                            current_rates[rate_field] = rate
                            changedRates.append(rate_field)

                        payload = json.dumps({
                            "rates_meta_data": [
                                {
                                    "category": {
                                        "id": roomId,
                                        "name": RoomName
                                        # "display_order": displayOrderId
                                    },
                                    "occupancy": occupancyId,
                                    "meal_plan": mealPlanId,
                                    "weekday_sun_rate": current_rates["weekday_sun_rate"],
                                    "weekday_mon_rate": current_rates["weekday_mon_rate"],
                                    "weekday_tue_rate": current_rates["weekday_tue_rate"],
                                    "weekday_wed_rate": current_rates["weekday_wed_rate"],
                                    "weekday_thu_rate": current_rates["weekday_thu_rate"],
                                    "weekday_fri_rate": current_rates["weekday_fri_rate"],
                                    "weekday_sat_rate": current_rates["weekday_sat_rate"],
                                    "last_updated_utc_timestamp": f'{date}T00:00:00Z',
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


# cmCreds = {
#     "username": "Sales@shivacontinental.in",
#     "password": "shiva@1234"
# }

# ratesConfig = {
#     "info": [
#         {
#             "rateTypeId": 2891,
#             "channelCode": 100,
#             "roomInfo": [
#                 {
#                     "roomId": 1912,
#                     "roomPlanInfo": [
#                         {
#                             "roomPlan": {
#                                 "mealPlanId": 1,
#                                 "occupancyId": 1,
#                                 "rate": 4500,
#                                 "date": "2024-09-14"
#                             }
#                         },
#                         {
#                             "roomPlan": {
#                                 "mealPlanId": 1,
#                                 "occupancyId": 1,
#                                 "rate": 4500,
#                                 "date": "2024-09-15"    
#                             }
#                         }
#                     ]
#                 }
#             ]
#         },
#         {
#             "rateTypeId": 2891,
#             "channelCode": 100,
#             "roomInfo": [
#                 {
#                     "roomId": 1913,
#                     "roomPlanInfo": [
#                         {
#                             "roomPlan": {
#                                 "mealPlanId": 1,
#                                 "occupancyId": 1,
#                                 "rate": 4500,
#                                 "date": "2024-09-14"
#                             }
#                         },
#                         {
#                             "roomPlan": {
#                                 "mealPlanId": 1,
#                                 "occupancyId": 1,
#                                 "rate": 4500,
#                                 "date": "2024-09-15"
#                             }
#                         }
#                     ]
#                 }
#             ]
#         }
#     ]
# }

# djuboRatePush('670', cmCreds, ratesConfig)
