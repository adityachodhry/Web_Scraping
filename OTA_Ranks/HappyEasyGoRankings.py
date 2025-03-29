import requests
import json
from datetime import datetime, timedelta

def get_HEG_rankings(cityName, output_filename='HappyEasyGoRankings.json', num_pages=3):
    ranks = []
    
    current_date = datetime.now().strftime('%Y-%m-%d')
    check_out_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

    for page_no in range(1, num_pages + 1):
        params = {
            "cityName": cityName,
            "checkInDate": current_date,
            "checkOutDate": check_out_date,
            "guests": [
                {
                    "id": 1,
                    "adult": 2,
                    "child": 0,
                    "age": []
                }
            ],
            "pageNum": page_no
        }

        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        try:
            endpoint = f'https://hotel.happyeasygo.com/api/web/hotels/New%20Delhi/hotel_list?param={params}&preview= 0'

            response = requests.get(endpoint, headers=headers, params=params)

            if response.status_code == 200:
                response_content = response.json()

                for index, hotel_data in enumerate(response_content.get('data', {}).get('hotelList', []), start=1):
                    if hotel_data['idName'] and (hotel_data['idName'].strip().lower().startswith('fab') or hotel_data['idName'].strip().lower().startswith('oyo')):
                        continue
                    hotel_id = hotel_data.get('id')
                    # hotel_name = hotel_data.get('idName')
                    # star_rating = hotel_data.get('starRating')
                    # price = hotel_data.get('lowestPrice')

                    ranks.append({
                        "rank": len(ranks) + 1,
                        'id': hotel_id,
                        # 'Name': hotel_name,
                        # 'starRating': star_rating,
                        # 'price': price,
                    })

            else:
                print(f"Error: {response.status_code}")
                print(response.content.decode('utf-8'))

        except Exception as e:
            print(f"An error occurred: {e}")
            break

    return ranks
