import requests
import json
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def djuboRoomConfig(username, password):

# def djuboDataExtraction(username, password, roomId, roomName, rateTypeId, channelId):
    driver = webdriver.Chrome()

        try:
            url = 'https://apps.djubo.com/sign-in/'
            driver.get(url)

            driver.find_element(By.NAME, 'email_address').send_keys(username)
            driver.find_element(By.NAME, 'password').send_keys(password)
            driver.find_element(By.CLASS_NAME, 'submitBtn').click()

            time.sleep(4)

            if driver.current_url != url:
                print("Login Successful. The Provided Credentials are Correct.")

                cookies = driver.get_cookies()

                authorization = next(
                    (cookie['value'] for cookie in cookies if cookie['name'] == 'auth_token_7'), None)

                if not authorization:
                    print(f"SSID cookie not found for account {username}. Skipping.")
                else:
                    print(f'SSID for account {username}  {authorization}')
            else:
                print("Login failed. Please Check Your Username and Password.")

            roomIdEndpoint = "https://apps.djubo.com/core-data/properties"

            headers = {
                'cookie': f'auth_token_7={authorization}',
                'x-requested-with': 'XMLHttpRequest',
                'djng-remote-method': 'update_rate_plan_rates'
            }

            response = requests.get(roomIdEndpoint, headers=headers)

            if response.status_code == 200:
                result_data = response.json()

                # with open('Row.json', 'w') as json_file:
                #     json.dump(result_data, json_file, indent=2)

                structured_data = []

                if isinstance(result_data, list) and len(result_data) > 0:
                    first_item = result_data[0]

                    accountId = first_item['account_id']
                    print(f"accountId: {accountId}")
                    propertyCode = first_item['id']
                    propertyName = first_item['name']
                    data_slot = first_item.get('room_categories', [])

                    property_info = {
                        "propertyCode": propertyCode,
                        "propertyName": propertyName,
                        "info": []
                    }

                    channelIdEndpoint = f"https://apps.djubo.com/core-data/accounts/{accountId}/properties/{propertyCode}/rate-types?property_id={propertyCode}"
                    response1 = requests.get(channelIdEndpoint, headers=headers)

                    if response1.status_code == 200:
                        channelData = response1.json()

                        for channelInfo in channelData:
                            rateTypeId = channelInfo['id']
                            channelId = channelInfo['channel']
                            channelName = channelInfo['name']

                            channel_info = {
                                "ratePalnId": rateTypeId,
                                "channelId": channelId,
                                "channelName": channelName,
                                "roomInfo": []
                            }

                            for roomInfo in data_slot:
                                roomId = roomInfo.get('id')
                                roomName = roomInfo.get('name')
                                mealPlanData = roomInfo.get('meal_plans', [])

                                room_plan_info = {
                                    "roomId": roomId,
                                    "roomName": roomName,
                                    "roomPlanInfo": []
                                }

                            for mealInfo in mealPlanData:
                                mealPlanId = mealInfo.get('id')
                                mealPlanName = mealInfo.get('meal_plan_name')

                                room_plan_info["roomPlanInfo"].append({
                                    "roomPlanId": mealPlanId,
                                    "roomPlanName": mealPlanName
                                })

                                channel_info["roomInfo"].append(room_plan_info)

                            property_info["info"].append(channel_info)

                    structured_data.append(property_info)

                    # try:
                    #     manage_property_link = WebDriverWait(driver, 10).until(
                    #         EC.presence_of_element_located((By.CSS_SELECTOR, "li[title='Manage this Property'] a.manage-property"))
                    #     )
                    #     WebDriverWait(driver, 10).until(EC.visibility_of(manage_property_link))

                    #     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li[title='Manage this Property'] a.manage-property")))

                    #     manage_property_link.click()
                    #     print("Manage this Property page opened!")

                    #     rateId = manage_property_link.find_element('ul', class_='djng-form-errors').text.strip()
                    #     print(rateId)

                    # except Exception as e:
                    #     print(f"Could not find or click the Manage this Property link: {e}")

                    # time.sleep(2)

                    # ratePlanIdurl = f"https://apps.djubo.com/rates-admin/accounts/{accountId}/properties/{propertyCode}/rates/rate-plans/"

                    # headers = {
                    #     'cookie': f'auth_token_7={authorization}',
                    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
                    #     'upgrade-insecure-requests': '1'
                    # }

                    # response = requests.get(ratePlanIdurl, headers=headers)

                    # if response.status_code == 200:
                    #     response_html = response.text  

                    #     rates_plan_match = re.search(r'name="rates_plan" value="(.+?)"', response_html)
                    #     if rates_plan_match:
                    #         rates_plan_value = rates_plan_match.group(1)

                    #         rates_plan_value = rates_plan_value.replace("&quot;", '"')

                    #         rates_plan_list = json.loads(rates_plan_value)

                    #         for plan in rates_plan_list:
                    #             seasonId = plan.get('id')
                    #             seasonName = plan.get('name')
                    #             print(f"seasonName: {seasonName}")
                    #             print(f"seasonId: {seasonId}")
                    #             print() 

                    #     else:
                    #         print("No 'rates_plan' input field found.")
                else:
                    print(f"Failed to retrieve the page. Status code: {response.status_code}")

                with open('hotel_data.json', 'w') as json_file:
                    json.dump(structured_data, json_file, indent=2)

                print("Data has been successfully stored in 'hotel_data.json'.")
            
            # return djuboDataExtraction

        finally:
            if 'driver' in locals():
                driver.quit()

djuboRoomConfig('online@corbettnirvanaresort.com', 'djubo123')