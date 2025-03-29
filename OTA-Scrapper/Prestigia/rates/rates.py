import requests
from bs4 import BeautifulSoup

url = "https://www.prestigia.com/en/produit.php?idTarget=359036&arrivee=2024-04-10&depart=2024-04-11&guestsParams=W3siYWR1bHRzIjoyLCJjaGlsZHJlbiI6MCwiYWdlcyI6W119XQ==&dev=20"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Cookie": "new_dd=1; clientLocalPrefs=%5B%22en%22%2C20%2C1%5D; b=dd0b6051a1ee01c106fb06562dca5f88; a=eJyrVjIyMDLRNQAiUwVDYytDCytjEyUrS0tDM3PTWgBhQAZv; _ga=GA1.1.612292256.1712315919; rskxRunCookie=0; rCookie=9bnpcwj6zviun0dwlvqkfblumkos10; PHPSESSID=lrlvmkppepnlvrp6bu568snds6; _ga_GPP0EDLB79=GS1.1.1712557091.4.1.1712557121.30.0.0; cto_bundle=44G6ul9sNWVtODFueVRpRDljZk1UVkhPJTJGWnhPJTJCb29TZjQ2WUxwdkhySEF5SzFuYnc4SyUyRm9oMyUyRiUyQjdJMVBzQ2JzaVNHRjhPY3NKMVZMWW4zblZ4Z3AzRXBBSVk4Y3dWJTJGVjdPJTJCN0pyZkt5U3hnRzJQeW5JY3pwYmglMkJyUm15Z2klMkZYWkpDQWh4bkVHdlp5Q2NnazRhWndMdmpXejdROVA2VFpYYXNaZVpKaUNJVmdTTEFZQlk4c29yT3ZleFZmQjRDU1BVJTJGZzNnMlVtOFBhNTklMkZZbHROd1NvM1BWZyUzRCUzRA; lastRskxRun=1712557124793"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    html_content = response.text
    soup = BeautifulSoup(response.content, 'html.parser')

    with open("prestigiaRates.html", "w", encoding="utf-8")as html_file:
        html_file.write(html_content)

    room_elements = soup.find_all("div", class_="room-item")

    for room in room_elements:
        # Room Name
        room_name_element = room.find("div", class_="room-name")
        room_name = room_name_element.get_text(strip=True) if room_name_element else "N/A"

        rate_type_elements = soup.find_all("span", class_="flex font-medium text-base sm:text-base uppercase items-center flex-row room-name")

        print(f"Room Name: {room_name}")
        print("-" * 30)

else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")