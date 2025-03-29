import requests
import json
import datetime
from bs4 import BeautifulSoup

today = datetime.datetime.now()
rates = []
hid = 2406159

initial_url = "https://www.kayak.co.in/hotels/p58595-h351128-details/"

def extract_rates(data):

    for deal in data['rows']:
        for option in deal['bookingOptions']:
            rate = {
                'checkin' : check_in_date,
                'checkout' : check_out_date,
                'provider': option['localizedProviderName'],
                'room_type': deal['localizedDescription'],
                'price': option['price']['price'],
                'currency': option['price']['currency'],
                'freebies': [freebie['localizedName'] for freebie in option['freebies']]
            }
            rates.append(rate)
    return rates

for day in range(10) :
    check_in_date = (today + datetime.timedelta(days=day)).strftime("%Y-%m-%d")
    check_out_date = (today + datetime.timedelta(days=day + 1)).strftime("%Y-%m-%d")
    
    url = f"https://www.kayak.co.in/i/api/search/v1/hotels/rates?rooms=1&adults=2&priceMode=nightly-total&checkout={check_out_date}&checkin={check_in_date}&hid={hid}"

    headers = {
    'X-Csrf': 'VKVruLBqbSTumfa225laIjM8eeqyj_P9ChENWK9$DLo-I9V6V$6cUYUeSk_iGTEC7NVEn8A7TK5V8f8vGXM7erQ',
    'Referer' : 'https://www.kayak.co.in/hotels/p58595-h351128-details/',
    'Cookie': 'mst_ADIrlA=2nYj-YqfzuQ78qzF8AlF3KcDre1qiJwPCR5-rASrrlIOWqx-v5Np4Y_wgnzP94dp1HBovjzJPRf40piSha1MZA; csid=aa7f475f-ca72-4d67-8c75-895bf83e68aa; mst_iBfK2w=p6avOuJQvGj5lFw3dI1Ds6cDre1qiJwPCR5-rASrrlIscZNyXO9qTiDtWTRdC36EUJFPOHC-o4KCm_398qUfVQ; kayak.mc=AcBmTMT_DP0NAKHdlT9m1-UbqXHe2IhUiM5pIpe3h939kbVM4SNhLXNWw_VJAZ8liw5rW_rYaUGAPeNW3_E-2w-lS3G6zWMPOqpCSlkJwb7knzfwL4Ua7jfsTtYH8TyVEVmIv4l8u6gIh7MXec3npOUCLyGgy0Wss9r-vXU6dbfwwCjrdQPs2BkpokyRhkV-Nkw7K_1igaMcT3-pOFSV28tlO2jiAuyyKk6kqWRvKXtJdu7Y3bs7CBRIOvDdCzVLvgCJTPB9rjIRPBNyNMxuOAo; p1.med.sid=R-5lLTXX756UTGtR5k2OwjT-zk7TnLXsvbRCYzqZ5VsxzxH0UENDg_mZ7SVUMYRnl; kayak=T5Xs_3pxfh74yg$zgFLl; kmkid=A_dFd40OzF1lUR7mOL6KD1E; cluster=5; Apache=c$Ke6g-AAABjfSQNB8-c5-TKKxog',
    'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }

    response =  requests.get(url, headers=headers)

    response_data=response.json()
    data  = response_data["groups"]
    
    for x in data :
        print(x)
        extract_rates(data=x)

with open(f'{hid}_kayak_rates.json', 'w') as json_file:
    json.dump(rates, json_file, indent=2)

print("Rates extracted and saved in 'hotel_rates.json'")