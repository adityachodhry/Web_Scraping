import requests
import json


rating_data = []

api_url = "https://www.expedia.com/api/v4/typeahead/Amar%20Kothi?browser=Chrome&client=SearchForm&dest=true&device=Desktop&expuserid=-1&features=consistent_display%7Cgoogle&format=json&guid=43cf74ce-8a58-459e-9997-a97639df1d75&listing=false&lob=HOTELS&locale=en_US&maxresults=8&personalize=true&regiontype=2047&siteid=1&trending=true"

headers = {
    "Accept-Language":"en-US,en;q=0.9",
    # "Cookie": "MC1=GUID=43cf74ce8a58459e9997a97639df1d75; DUAID=43cf74ce-8a58-459e-9997-a97639df1d75; s_ecid=MCMID%7C06288231474205004321743737088849011152; EG_SESSIONTOKEN=dFwlotn26NSNin2Ne09vseBV24LO7BK649sZrByS75CbVE:ERYbcKgrEqjFyjhB9IsFbYF8XFBwY5pVhXlMFb_u-7OI1LOmtrskgTghbF9qcDe23cZEliHPlkhiYXCDbP43bA; xdid=8a9b59bb-3b66-477a-941a-b5bd14975774|1695652604|expedia.com; s_fid=55F1BAC5837A5B44-0F64084840AB63B8;",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
response = requests.get(api_url, headers=headers)

if response.status_code == 200:
  
    response_content = response.json()
    
    with open('Row_Data.json', 'w') as json_file:
        json.dump(response_content, json_file, indent=2)

else:
    print(response)
