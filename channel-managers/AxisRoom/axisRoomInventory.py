import requests
import json
from datetime import datetime, timedelta

def login_to_axis_rooms():

    login_url = "https://app.axisrooms.com/accounts/signIn.html"

    username = 'dargelislodge@gmail.com'
    password = 'Lodge@123'
    
    login_payload = {
        'user_type': '1',
        'emailId': username,
        'password': password,
        'name': '',
        'g-recaptcha-response': '03AFcWeA6gL-MoO8uJdAtdHR3QNoGTQX7bIqAqqC45FbWWxzRcSiA4zT06VSyP7iJJpVwasTpxLJrNC5PEPTeEuIebQgh8BODb9ID9To4NtwlerlweMsdz5kwm43Eb4RUDY9btSeAoslywkEfYd6dwGeJTvmouVWc99b1mAI1vXaExf36EUiQFM2nB2AWXNE7u29nsw4JmxI9l17J-TBRgyc_9HccUEQnodUvdMrOc_9Q7hVy0ilN8J5GbaxBtSofl3Q58d-OufHvVlxifA4ms5t-yjKDOLVzYl6C1hwG6NpX-vYnyQ9_D1lByruniOl71SLpxusOtGsoZ7UxWOcXVORekUjgD7MgKzIurnC8jkptO5qIPCC7bYfihfFAuHGjdbqexf1dqT8T4QWnJPXCbzHLxZMjtm9pX5ITBzCBXIP7YqyBUcM0sNJ4Xkw0fSI_gkH_NgiNFKU7DeVHbcRdp7LHbmWnjw_JqyUjxEHU9345siZUfcSgAB-Bk_L_O5yG5UxLEU8fSDBoH4BZhJVthQ2C5MQkO4ZLPEbxBSU1J-eraISEKFAvapxGPvmIpKP1b02z4Vr1oBlal2sB4MlR5LVrlACFrp8mhwkEyLhnPF9oJ9gvWn4XHD5r2Kl7mzQmDGlEPg5k1RRKKsVR2KXC08sq5PWHtK_s8jFLbBQfXaCThTXpsBQb1_5jGyuHwaSmrDZ5oEbA_3Q1yD9_tXYvsmNtymnO3u2BQ9gC6AG_096fjwdakx5wn4RlISIWQGvQd4SnKAB4kbAoTdHmtLGVX_MpQSMHDSuepfA'
    }
    login_headers = {
        'Cookie': 'access_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJvcmlnX2lhdCI6MTcxNDQ1MjA3OTA1MiwiZXhwIjoxNzE0NDUzODc5MDUyLCJlbWFpbCI6ImRhcmdlbGlzbG9kZ2VAZ21haWwuY29tIiwidXNlcm5hbWUiOiJkYXJnZWxpc2xvZGdlQGdtYWlsLmNvbSIsInVzZXJJZCI6NjA4MzAxLCJwYXNzd29yZCI6IkJsQ2JRME04bTNNYWQyVlNkbmFKUEJPUEVmTFN4bFljaWVhcVFwOGJTSXIxajBxckZCQkdZNEhuVFMzVGo4TkNDYzNITVJWZGZKUGM2K243ZkcvMFJ3XHUwMDNkXHUwMDNkIn0.-oz5A6sQnvh13lDqmPr1oRB3ZqRAmhcoG3LTNV7h5yc'
    }

    login_response = requests.request("POST", login_url, headers=login_headers, data=login_payload)

    if login_response.status_code == 302:
        print(login_response.status_code)
        print('Login Successful!')
        return login_headers
    else:
        print('Login Failed!')
        return None

def fetch_inventory(login_headers):

    current_date = datetime.now().strftime("%Y%m%d")
    end_date = (datetime.now() + timedelta(days=1)).strftime("%Y%m%d")

    # Extract inventory data
    pId = 180045
    endpoint = f"https://app.axisrooms.com/api/v1/getInventory?productId={pId}&start={current_date}&end={end_date}"
    body = {
        'productId': pId,
        'start': current_date,
        'end': end_date
    }

    inventory_response = requests.request("POST", endpoint, headers=login_headers, json=body)

    if inventory_response.status_code == 200:
        inventory_content = inventory_response.json()

        # with open('Row_Data.json', 'w') as json_file:
        #     json.dump(inventory_content, json_file, indent=2)

        data = inventory_content.get('invObj', [])

        room_data = []

        for room_id, room_info in data.items():
            room_name = room_info.get('roomName')
            room_inventory = room_info.get('inventory', {})
            room_inventory_data = []

            for date, details in room_inventory.items():
                booking = details.get('booked', 0)
                available = details.get('available', 0)
                room_inventory_data.append({
                    'date': date,
                    'booking': booking,
                    'available': available
                })

            room_data.append({
                'room_id': room_id,
                'room_name': room_name,
                'inventory': room_inventory_data
            })

        return room_data
    return None

# Main code
login_headers = login_to_axis_rooms()
if login_headers:
    inventory_data = fetch_inventory(login_headers)
    if inventory_data:
        
        with open('Room_Inventory.json', 'w') as room_file:
            json.dump(inventory_data, room_file, indent=2)
        
        print('Inventory Data Extracted Successful!')
    
    else:
        print('Failed to Retrieve Inventory Data!')
        
