import requests
from lxml import html
import json
from datetime import datetime, timedelta

check_in_date = datetime.now().strftime("%m%d%Y")
check_out_date = (datetime.now() + timedelta(days=1)).strftime("%m%d%Y")

current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# hId = 20211
# mmthId = 201409011100103353

def save_mmt_data(hId, mmthId):

    url = f'https://www.makemytrip.com/hotels/hotel-details/?hotelId={mmthId}&checkin={check_in_date}&checkout={check_out_date}&roomStayQualifier=2e0e'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }

    # Send GET request to the URL with headers
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Parse HTML using lxml
        tree = html.fromstring(response.content)

        # Use XPath to extract script content
        script_content = tree.xpath(
            '//script[contains(., "window.__INITIAL_STATE__")]/text()')

        if script_content:
            # Find and replace "window.__INITIAL_STATE__"
            replaced_content = script_content[0].replace(
                "window.__INITIAL_STATE__ =", "")

            # Load the content as JSON
            json_content = json.loads(replaced_content)

            # with open('mmt.json', 'w') as json_file:
            #     json.dump(json_content, json_file, indent=2)

            data = json_content["hotelDetail"]["staticDetail"]
            try:
                review_summary = data["reviewSummary"]
                try:
                    mmt_ratings = review_summary["MMT"]
                except:
                    mmt_ratings = review_summary["EXT"]

                cumulative_rating = mmt_ratings.get("cumulativeRating", 0)
                # print(cumulative_rating)
                total_review_count = mmt_ratings.get("totalReviewCount", 0)
                total_rating_count = mmt_ratings.get("totalRatingCount", 0)

            except:
                review_summary = None

            formatted_data = {
                "hId": hId,
                "otaId": 1,
                "otaPId": mmthId,
                "timestamp": current_date,
                "reputation": [
                    {
                        "ratingCount": float(cumulative_rating),
                        "totalRatingCount": 5,
                        "totalRatings": int(total_rating_count),
                        "totalReviews": int(total_review_count)
                    }
                ]
            }
            
            return formatted_data
        
#             with open('MMT_Ranking', 'w') as json_file:
#                 json.dump(formatted_data, json_file, indent=2)
#         else:
#             print("Script content not found.")
#     else:
#         print(f"Failed to fetch content. Status code: {response.status_code}")

# save_mmt_data(hId, mmthId)
