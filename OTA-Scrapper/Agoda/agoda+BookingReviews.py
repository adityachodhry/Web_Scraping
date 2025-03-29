import requests , json , datetime
from datetime import datetime

hotel_id = 29525108
page_no = 1
reviews_data = []

body = {
    "hotelId": hotel_id,
    "hotelProviderId": 3038,
    "demographicId": 0,
    "pageNo": page_no,
    "pageSize": 100,
    "sorting": 1,
    "reviewProviderIds": [
        332,
        3038,
        27901,
        28999,
        29100,
        27999,
        27980,
        27989,
        29014
    ],
    "isReviewPage": False,
    "isCrawlablePage": True,
    "paginationSize": 1
}

endpoint = "https://www.agoda.com/api/cronos/property/review/HotelReviews"

response = requests.post(endpoint , json=body)

if response.status_code == 200:

    response_data = response.json()

    with open("agoda+BookingReviewsData.json","w") as json_file:
        json.dump(response_data ,json_file,indent=2)
    
    reviewsData = response_data["commentList"]["comments"]
  
    for data in reviewsData:
        
        roomType = data.get('roomTypeName')
        if not roomType:
            roomType = "NA"

        reviewText = data.get('reviewComments')
        if not reviewText:
            reviewText = "NA"

        response_details = []

        if "responseText" in data:
            responseDate = data.get('responseDateText')
            responseText = data.get('responseText')

            # Split the responseDate to extract the date part
            date_parts = responseDate.split(" ")[1:]
            date_parts[1] = date_parts[1].replace(',', '')
            date_string = ' '.join(date_parts) 
            
            response_date_obj = datetime.strptime(date_string, "%B %d %Y")
            response_date_formatted = response_date_obj.strftime("%Y-%m-%d")

            response_details.append({
                "responseDate": response_date_formatted,
                "responseText": responseText
            })
        else:
            response_details = "null"

        publish_date_str = data.get('formattedReviewDate')
        publish_date = datetime.strptime(publish_date_str, "%B %d, %Y")
        formatted_publish_date = publish_date.strftime("%Y-%m-%d")
    
        e_data = {
            'publishDate': formatted_publish_date,
            'rating': data.get('rating'),
            'reviewText': reviewText,
            'roomType': roomType,
            'guestType': data.get('reviewerInfo', {}).get('reviewGroupName'),
            'response': response_details
        }
        reviews_data.append(e_data)
        
    # Save the extracted data to a new JSON file with the desired format
    file_name = f"{hotel_id}agoda+BookingReviews{datetime.now().strftime('%Y%m%d')}.json"
    with open(file_name, 'w') as json_file:
        json.dump(reviews_data, json_file, indent=4)