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

def bookingInventory(username, password, hotelCode=[]):

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
    print(ses_value)

    start_date = datetime.now().strftime("%Y-%m-%d")
    end_date = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")

    session = requests.Session()
    cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
    cookie_string = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
    session.cookies.update(cookie_dict)

    inventoryApi = f"https://admin.booking.com/fresa/extranet/inventory/fetch?hotel_account_id=17719935&lang=xu&hotel_id=12571777&ses={ses_value}"

    payload = json.dumps({
            "request": f"{{\"dates\":{{\"range\":true,\"dates\":[\"{start_date}\",\"{end_date}\"]}},\"hotel\":{{\"fields\":[\"rooms\",\"status\"],\"rooms\":{{\"id\":[1257177701],\"fields\":[\"status\",\"permissions\",\"rooms_to_sell\",\"net_booked\",\"rates\",\"num_guests\"],\"rates\":{{\"fields\":[\"default_policygroup_id\",\"name\",\"net_booked\",\"permissions\",\"policy_overrides\",\"price\",\"restrictions\",\"rooms_to_sell\",\"status\",\"xml\"]}}}}}}}}"
        })

    # headers = {
    #     'cookie': 'cors_js=1; bkng_sso_ses=e30; bkng_sso_session=e30; _scid=ff252826-501c-4577-b54c-ed36b381554a; FPID=FPID2.2.rVCY4utBka2%2BfEgnbPh3hHY0sYOVwyA%2F6OMo6QncIu4%3D.1707811310; px_init=0; _pin_unauth=dWlkPU1tVXlORGM0WldFdE16QXdOeTAwT0RobUxXSTFObU10T0dFeE16UmhZemt4TldNMg; pc_payer_id=25730694-105d-41db-bec6-0a011adacf3c; fsc=s%3A1247ec365000ed4002a27614c93ca68a.FQvLGJ9YSoNJyFCo225ZMRFXah1ee5zLO%2FBP13YyfJA; _yjsu_yjad=1711006522.d2ed3495-2c4e-43a5-a668-c480db9c828f; pcm_personalization_disabled=0; _sctr=1%7C1712687400000; _scid_r=ff252826-501c-4577-b54c-ed36b381554a; _ga_FPD6YLJCJ7=GS1.1.1712992163.30.1.1712992578.60.0.0; pcm_consent=analytical%3Dtrue%26countryCode%3DIN%26consentId%3D86a1fb70-6bab-4121-beea-3b3264d1c717%26consentedAt%3D2024-09-11T06%3A07%3A29.930Z%26expiresAt%3D2025-03-10T06%3A07%3A29.930Z%26implicit%3Dtrue%26marketing%3Dtrue%26regionCode%3DMP%26regulation%3Dnone%26legacyRegulation%3Dnone; _gcl_au=1.1.1529639310.1726034855; cto_bundle=chnWEl9xR0JGZWt1Z2pXQ0tiOTB6JTJGVlR4ejI4Z2F0RWtBcWJSTGRkWEVHSFM1WTBBUU5ERzM4Y2NKd2ElMkJjMmJUMTdRNFVpZHZrOEhaYmhpZGpIa3I1cDRYeGVqS1JiV2tndDFLSUNHbWVabE1WeDFhaTFQQlhSSTd0aXgwQzlUWHRybHJ2TDVrMGdIYXpnNEV1Y2FpWEhyb2tGN202bUxZdmZ6d0Z6RExhUGtWaGRxSFJwU3pYJTJGVlVvSEQ3VUNldyUyQlBiejlPJTJCeXRuTFlDWjlVUmZqcEVCS2hQZyUzRCUzRA; _ga_SEJWFCBCVM=GS1.1.1726113982.45.1.1726114014.28.0.0; _uetvid=328b26e0ca4611ee8c3f8dbbb3ca8727; _ga_A12345=GS1.1.1726113982.74.1.1726114628.0.0.383288068; BJS=-; _gid=GA1.2.1530364026.1730887501; _gac_UA-116109-18=1.1730887501.CjwKCAiAxKy5BhBbEiwAYiW--7VEBKQo3xTJWgNRMmHyAHlcMiWlLZUugOi8YJ5sv6-eIJ62z2G-xxoCnroQAvD_BwE; bkng=11UmFuZG9tSVYkc2RlIyh9YSvtNSM2ADX0BnR0tqAEmjuYH1A90FdP3kIogyjCmmbdKvG21pGIhaEpwxMQxCF1%2FWaDMausb31oAGRV5eJLAEU4E7KQ2Q2uauhHYw1o7J%2BMtK4%2Fkcg%2F99ax8Vqdr8qIFot%2ByApuwae43d4kcNJ2drWPJ3Ey0OeQX3GfAtPFHzaAXbpcLT3dFLWMpklVq2SccQ%3D%3D; bkng_bfp=a1aa9c774cc17c368edbfcb06674f841; ecid=JPvgoCac7xGyJez3xO2Rggz1; _pxvid=acde60a6-9c26-11ef-88b9-7b5616475f6f; external_host=account.booking.com; uz=e; _sfid_2a26={%22anonymousId%22:%2271f0f77d25487def%22%2C%22consents%22:[]}; _evga_c2e4={%22uuid%22:%2271f0f77d25487def%22%2C%22puid%22:%224fVUFgp0nAtEZkE9fQqj3pd9yIgfrdfcKeiDl4JzmMc5GD5TsxPtTCx-02Bi04VGuKiDFx8iY1DjGtUO7mrOO6bPXlN6-Znsob5yQ54KdcE%22}; extranet_cors_js=1; _sg_b_n=1730897248182; bkng_sso_auth=CAIQsOnuTRpmsEs4pqZ7YeRN/d8KyunN2K9pEUBB/sZEI+ZsdvFEmy67C7jryg9qBLpTqPnsC5UUMyrXilg4UEwtPwCGaEDmx3nZSoBr4U1niqj6oMiGYKTWEbhSxFJNmf1Ihai22jpBOoyYH7Q0; pxcts=71c6c7e4-9cc7-11ef-8d8d-ac2c1f11a74e; _ga=GA1.1.1278411245.1707811310; _sg_b_v=3%3B22072%3B1730956599; _pxff_cfp=1; _pxff_ddtc=1; aws-waf-token=e60a711a-59f8-4f9f-b0c7-b3833e777490:HgoAbPMlRlA1AAAA:KwkiQCns9bLvWvh1T+iUVNyRk2bdJZ+bQNGDxKiEMAbRanDmOjTQa14V4kpkXi2c3XLb3+TSm5mgS4CZ1Sk5b4mTyJM9vJAesRmO5Y/7ZHccuTFP6ka/l8yrTEeML6qTN3w/czhl3c2nWmYpNw+EisWCfJBUyTT2CtbFrIJ3agdFMDcSveKr6Gic1iO3P2xsyLtFFToVf+/aFWdZTFy+P/Uf/6YEWNiiuV4X0Ig4Y7YQPDzR; _sg_b_p=%2Fhotel%2Fhoteladmin%2Fgroups%2Fhome%2Findex.html%2C%2Fhotel%2Fhoteladmin%2Fgroups%2Fhome%2Findex.html%2C%2Fhotel%2Fhoteladmin%2Fextranet_ng%2Fmanage%2Fhome.html; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Nov+07+2024+10%3A50%3A21+GMT%2B0530+(India+Standard+Time)&version=202408.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=1d204701-9d8c-48b5-a060-486a0afea246&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0004%3A1&AwaitingReconsent=false; _ga_NQ1YHY3J83=GS1.1.1730956600.4.1.1730956821.0.0.0; _px3=6e48b5285034d7d32611a1f45b2eb57d739380d1cb3f353259e64fe773bc6d2c:gPpcSEzO+dkjtdmX3zLpS3gJmlePFukz3sl3R5r94xPVMgauKu6Dy4nknRN6JAfb7ebhuv7/0rTdKdd91ZWEQA==:1000:571W3QvOTjIJlSfQJ5obg4OER9V1MxLl70oaQhcXD4WcIg84oU8wDdPk15rQWKt+l6lywqRj61fJoha0tE024cSlo3Q3hWa+5bugiNYBN8IQyjWxP/kmIcpC7fjw6Rb8S0O5xvS+QFZvVTmYugxnJBTvIKAskVsiHyyy9gfA7/oN8Um1I4JRGCcCL3Gy4AJMrinkPyRl+2TgcBbgzhlxTgmWEV1juN0lIMXdu2YcFKs=; _pxde=72f131ed32f04eddcf1af4e281b9e5a318a453be492c3cee814e13c8b561f41a:eyJ0aW1lc3RhbXAiOjE3MzA5NTY4MjQ0NDgsImZfa2IiOjAsImlwY19pZCI6W119; esadm=02UmFuZG9tSVYkc2RlIyh9YbxZGyl9Y5%2BPUQNMW4LTWSgYrDRcyvUpJJ%2BwUKSfWPy9CCXKgs8YFvs%3D',
    #     'Content-Type': 'application/json',
    #     'x-booking-pageview-id': 'cfd759eee2d10459',
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
    # }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'Referer': urlunparse(parsed_landing_path),
        'Content-Type': 'application/json',
        'Cookie': cookie_string
    }

    response = requests.request("POST", inventoryApi, headers=headers, data=payload, allow_redirects=False)
    
    print(response.text)
    print(response.status_code)

    driver.quit()

bookingInventory('Retvensnew', 'October@2024',['12735695'])