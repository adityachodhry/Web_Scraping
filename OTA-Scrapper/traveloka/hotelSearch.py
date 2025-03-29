import requests
import json
from datetime import datetime, timedelta

url = "https://www.traveloka.com/api/v1/hotel/autocomplete"

hotel_name = "Amar Kothi Udaipur"

payload = json.dumps({
  "fields": [],
  "data": {
    "query": hotel_name
  },
  "clientInterface": "desktop"
})

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
  'Cookie': '_gcl_au=1.1.1682877213.1712574295; _cs_c=1; _fbp=fb.1.1712574316399.321402342; _tt_enable_cookie=1; _ttp=5GC1QEg243caLr2zwkDfvOI5H9h; _ga_RSRSMMBH0X=deleted; countryCode=IN; cto_bundle=qvhISF9MUU5zVHBKRVJVY0ZFYUxoQWdVd0szMHoyWWNTNGpHaEl0c2VtbkNkbE0yaU5MVWRubkdjbmZqVzJ5OEladEVZS0dCV1h1WjVubGF3VTJTYnl1emQlMkZIeFMyNkFnVUVTbVpNTWwybWNyWSUyQjlDYXNQYXhZWmt5WDZjREFMOUpwUVBBQSUyQldwJTJCeGhzcDNET3hpMW9KZ1RNZlRQZVdTT0dMbG1OelZONGlabCUyRkhCd2VzUkYwdDclMkJidGNFeVFCQiUyRmxGa2RMOXJjbno4WnFubEhwMFI3T2U4d1clMkZUaTE3bDVPamJxNWlsbkpvb2dlSFhheHBqTmVFMUtqV1lmbGpaZExWekUzdGFNZGVNVll2eTV3WG9RR3lWUUlEY0FTd1ZEaFlPSFpweU91T3l6YTNLeldhUXklMkIwRXZHRWlIQWhPd21mVg; tv-repeat-visit=true; tv_user={"authorizationLevel":100,"id":null}; _gid=GA1.2.790902122.1714974031; amp_f4354c=HFYhkE3fffvc1uGWVENcQq...1ht66liss.1ht67q0lv.0.9.9; aws-waf-token=b5b7e932-f87d-44df-903e-7e734095cd1f:BQoAjfUp41YHAAAA:sK2e3hr8JcwAMtklvyz0uX6rVq9jTucbws1zpF6VrK2h9mRV4owEI0piid8slRrTFEk4CtOl09VNrF+t3BnaDTxLlgzcDTi3kB8jVItK44I+wMjP/xnRVwSjbuIvQ5nw4pY+JFdLDyZztnl5HWFJ79f82d5pYHYUIAzEt8hJI3w+qVhhXuJYtJy9HFBS09NqpNUXEIhDFljL39A=; _gat_UA-29776811-12=1; _ga_RSRSMMBH0X=GS1.1.1714974030.7.1.1714975213.56.0.0; _ga=GA1.1.452047242.1712574296; _cs_id=755aa14b-5380-a4d7-bdab-5e5425521ee7.1712574295.15.1714975213.1714974034.1.1746738295902.1; _cs_s=6.0.0.1714977013255; amp_1a5adb=7IOyruSWsUxyYNdt87vghY...1ht66lisp.1ht67q3cb.7d.9.7m; tvl=TdpfHMbFppWLl8BE8QnmTNXjJ8af3YTJWNF7DEwZ2VdrDAXtLL8X0cu6Hq5Oj4BFN0IbgupXW2NECiYOeO4xK3w08Ck0/XNITLu8kFw5/P8ihSRv2YWZU0Sv944UwpvsifuoFaK5o+7WLgMeO24bAMEfIOGaybDPQpnngJmd7EuPVZBaBCYgpqSaivSFuShbAGENmkoAgb4wgt8L+cNy7Q58RSoCpfgWmyDnYXzlTgIVOGZpbzOAxpCQGMv+GdX5/1Fbj8FeQ7I=~djAy; tvs=rjP2BQhoKnMnlVfvl6VOvkEUEfKF1jGKJr7X+uGQikLEUVY+ZlQwt9xTnfIxgZuYQRm2W8Xkce5+wL5dJqG21CRZDvHsXlmQ/if4Uh1IkBmgulM+Qtpvmdaad6PK66Aule1bW0v6nLPFjfyomkGdPJG71xuWwGtR7fL61jY/p57uUrZCtiFEPicDqWJ0QUmlJzk0nBS48KZIJRFd/U5WgirPaNgE+XQMbVLPsbOuy9qv3ABbTlSsNNxFpOc90fAcKtD49/COX8qSgsz1lVuCZqRmCoLO925DW6g=~djAy; _dd_s=rum=0&expire=1714976128288&logs=1&id=3f08093c-3ae3-48ba-91b4-b1ba94578144&created=1714974006872; tvl=FhVdwcehYo32eVPo32D9MIOGY/AQqDoNa7nnxlav2NiEkWRX2bKV/aqpssDLZrOPXQAUDkEfgXJdWetugv4WFOuyBvydhwPL4fnOtVZ5xvLEkdqcqwjel1+iy5oReAFP7Cqmq2eEa1PoJq1H2Cc+0n8XMBzZnwYP9J6uWTu9I6tpa80WZ1KsKqNZRf46cI07qeDW7mf51zSt5SxNPzKYVabDMTNLWdGg3ZVqR0PLkB5lloeSiK5k40aCwpUWey/y4GXO/JyUcI0=~djAy; tvs=Rl4/5Xu1bCVgaxb8cdbw7sp9895VR7RXmSdkqDFUqxVQVcqJ7FNV43m9dbI4ZykA9z6+Uvna/YflS0kcJFxI8pOEmcsGje7AmcmcTMTLjaDgXU3rd/YbeAazYtHlG/QmmfH5CCR8+7joB0m5+iWtso6Ry41cEnnCGCWtlYKXoaAOH5nf3GAFqmmy/eKHNxPEQ3H4PyIwZLRts2r31BAVuYyh3aaL7WAHdzIBXzeeG10tjyyR64BCuubphASn3deOzVIs/9s4y4M2rAK/BYnzs5P6DASuNmFT3Es=~djAy',
  'X-Route-Prefix': 'en-en',
  'X-Domain': 'accomContent',
  'Origin': 'https://www.traveloka.com'
}

response = requests.request("POST", url, headers=headers, data=payload)

if response.status_code == 200:
    results = response.json()

    # with open('Row_Data.json', 'w') as json_file:
    #     json.dump(results, json_file, indent=2)

    hotel_info = []

    data = results.get('data').get('hotelContent').get('rows', [0])

    # Get current date
    current_date = datetime.now().strftime("%d-%m-%Y")
    check_out_date = (datetime.now() + timedelta(days=1)).strftime("%d-%m-%Y")
    
    item = data[0]
    hId = item.get('id')
    hName = item.get('displayName')
    
    url = f"https://www.traveloka.com/en-en/hotel/detail?spec={current_date}.{check_out_date}.1.1.HOTEL.{hId}"

    search_info = {
        'hId': hId,
        'hName': hName,
        'hUrl': url
    }
    hotel_info.append(search_info)
    # print(hotel_info)
    
    with open('searchInfo.json', 'w') as json_file:
        json.dump(hotel_info, json_file, indent=2)
