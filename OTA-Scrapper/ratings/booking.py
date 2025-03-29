# import requests
# from bs4 import BeautifulSoup
# import json
# from datetime import datetime

# hId = 20211
# hotel_id = 7534455

# def save_booking_data(hotel_id):
    
#     if hotel_id == "-" :
#         return

#     url = hotel_id

#     response = requests.get(url)

#     today_date = datetime.now().strftime("%Y-%m-%d")

#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#         script_tag = soup.find('script', {'type': 'application/ld+json'})

#         if script_tag:
#             script_content = script_tag.string
#             # Load the content as JSON
#             json_content = json.loads(script_content)
#             # with open('booking.json', 'w', encoding='utf-8') as file:
#             #         json.dump(json_content, file, ensure_ascii=False, indent=2)
#             rating_score = json_content["aggregateRating"]["ratingValue"]
#             total_reviews = json_content["aggregateRating"]["reviewCount"]

#             formatted_data = {
#             "hId": hId,
#             "otaId": 3,
#             "timestamp": today_date,
#             "reputation": [
#                 {
#                     "ratingCount": float(rating_score),
#                     "totalRatingCount": 10,
#                     "totalReviews": int(total_reviews)
#                 }
#             ]
#             }

#             with open("Booking_Ranking", 'w') as json_file:
#                 json.dump(formatted_data, json_file, indent=2)
            
#             print("Booking.Com Rating Extracted!")
#         else:
#             print("Script not found on the page.")
#     else:
#         print("Failed to retrieve the page. Status code:", response.status_code)

# save_booking_data(hId, hotel_id)
