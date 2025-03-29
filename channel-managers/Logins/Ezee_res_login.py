import requests

url = "https://live.ipms247.com/login/index.php"
headers = {
    'Cookie': 'sucuri_cloudproxy_uuid_=',
    'Origin': 'https://live.ipms247.com',
    'Referer': 'https://live.ipms247.com/login/'
}

data = {
    'username': 'Retvens',
    'password': 'Retvens@123',
    'hotelcode': '',
    'loginpnl' : 1,
    'login_username' : 'Retvens'
}

response = requests.post(url, headers=headers, data=data)
with open ("ww.html",'w',encoding='utf-8') as w :
    w.write(response.text)
# Extract 'SSID' from 'Set-Cookie' header
set_cookie_header = response.headers.get('Set-Cookie', '')
ssid_index = set_cookie_header.find('SSID=')
if ssid_index != -1:
    ssid = set_cookie_header[ssid_index + 5 : set_cookie_header.find(';', ssid_index)]
    print("SSID:", ssid)