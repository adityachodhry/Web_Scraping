import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json

def get_booking_reviews(hotel_slug):

    hotelSlug = None

    booking_hotel_reviews = []

    url = f"https://www.booking.com/reviewlist.en-gb.html?cc1=in&pagename={hotel_slug}&offset=0&rows=20&sort=f_recent_desc"
    headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
	}
    response = requests.get(url,headers=headers)
    # print(response.text)
    # with open("reviews.html",'w',encoding="utf-8") as html :
    #     html.write(response.text)
    
    soup = BeautifulSoup(response.text, 'html.parser')


    reviews = soup.find_all('li', class_='review_list_new_item_block')

    for review in reviews:
        # print(review)
        publishDate = datetime.strptime(review.find('div', class_='c-review-block__right').find('span', class_='c-review-block__date').text.strip().replace('Reviewed:', '').strip(),'%d %B %Y').strftime('%Y-%m-%d')
        guest_name = review.find('span', class_='bui-avatar-block__title').text.strip()
        
        rating = int(float(review.find('div', class_='bui-review-score__badge').text.strip()))
        review_title = review.find('h3', class_='c-review-block__title').text.strip()
        try :
            liked_comment = review.find('span', class_='c-review__prefix--color-green').find_next('span', class_='c-review__body').text.strip()
            # print(liked_comment)
        except :
            liked_comment = None

        try :
            disliked_comment = review.find('span', class_='c-review__prefix--color-green').find_next('span', class_='c-review__prefix').find_next('span', class_='c-review__body').text.strip()
        except :
            disliked_comment = None

        if liked_comment and disliked_comment :
            if len(liked_comment) > len(disliked_comment) :
                review_text = liked_comment
            else :
                review_text = disliked_comment
        else :
            review_text = review.find('span', class_='c-review__body').text.strip()

        try :
            room_type = review.find('div', class_='c-review-block__room-info-row').find('div', class_='bui-list__body').text.strip()
        except :
            room_type = None
        try :
            guest_type = review.find('ul', class_='review-panel-wide__traveller_type').find('div', class_='bui-list__body').text.strip()
        except :
            guest_type = None

        try :
            response = review.find('span', class_='c-review-block__response__body bui-u-hidden').text.strip()
        except :
            response = None

        if review_text == 'There are no comments available for this review' :
            continue

        booking_hotel_reviews.append({
                "hId" : 20671,
                "otaPId" : hotelSlug,
                "publishDate": {
                    "$date": publishDate
                },
                "guestName": guest_name,
                "rating": rating,
                "reviewTitle": review_title,
                "reviewText": review_text,
                "roomType": room_type,
                "guestType": guest_type,
                "responses": response
            })
    return booking_hotel_reviews

