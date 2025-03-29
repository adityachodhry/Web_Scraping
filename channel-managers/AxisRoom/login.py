
import time
import requests
import json
from datetime import datetime, timedelta

# Extract inventory data
current_date = datetime.now().strftime("%Y%m%d")
end_date = (datetime.now() + timedelta(days=7)).strftime("%Y%m%d")

pId = 188592

endpoint = f"https://app.axisrooms.com/api/v1/getPriceDetails?productId={pId}&start={current_date}&end={end_date}"

headers = {
  'Cookie': "access_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJvcmlnX2lhdCI6MTcxNDU2NDA4NjM5NywiZXhwIjoxNzE0NTY1ODg2Mzk3LCJlbWFpbCI6ImRhcmdlbGlzbG9kZ2VAZ21haWwuY29tIiwidXNlcm5hbWUiOiJkYXJnZWxpc2xvZGdlQGdtYWlsLmNvbSIsInVzZXJJZCI6NjA4MzAxLCJwYXNzd29yZCI6IkJsQ2JRME04bTNNYWQyVlNkbmFKUEJPUEVmTFN4bFljaWVhcVFwOGJTSXIxajBxckZCQkdZNEhuVFMzVGo4TkNDYzNITVJWZGZKUGM2K243ZkcvMFJ3XHUwMDNkXHUwMDNkIn0.uoXs24c-xcLB0n1w627H73Gm9WZEO6SvcIgRExmQqqw"
}

inventory_response = requests.request("GET", endpoint, headers=headers)

if inventory_response.status_code == 200:
    print(inventory_response.status_code)
    inventory_content = inventory_response.json()

    data = inventory_content.get('rooms')

    all_bars_data = []

    for room_id, room_data in data.items():
        room_bars_data = []
        bars = room_data.get('bar')
        print(f"Bars for Room ID {room_id}: {bars}")
        if bars:
            for date, price in bars.items():
                bar_name = date
                room_bars_data.append({
                    "date": bar_name,
                    "Price": price
                })
            all_bars_data.append({
                "roomId": room_id,
                "Room Price": room_bars_data
            })

    # Write the extracted data into a JSON file
    with open('bar_data.json', 'w') as json_file:
        json.dump(all_bars_data, json_file, indent=4)

    print("Bar data has been successfully stored in bar_data.json")
else:
    print('Failed to Retrieve Inventory Data!')



