import requests
from bs4 import BeautifulSoup

email = 'cro@retvensservices.com'
password = 'Aa@11223344'
accessCode = '00950'

def getLogin(email, password, accessCode):

  url = "https://www.zaaer.co/login"

  session = requests.Session()

  response = session.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')
  csrf_token = soup.find('meta', attrs={'name': 'csrf-token'})['content']

  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }

  payload = f'_token={csrf_token}&email={email}&password={password}&access_code={accessCode}'

  response = session.request("POST", url, headers=headers, data=payload, allow_redirects=False)

  location = response.headers.get('Location')

  if location == 'https://www.zaaer.co/reservation/dashboard':

      print('Login Successfully!')

  else:
      print('Login failed, please check user credentials!')
  
  return response


# getLogin(email, password, accessCode)



