import requests
import json
from datetime import datetime, timedelta

def search_hotels(city_code, checkin=None, checkout=None):
    if checkin is None:
        checkin = datetime.now().strftime("%Y-%m-%d")
    if checkout is None:
        checkout = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    url = "https://mapi.makemytrip.com/clientbackend/cg/search-hotels/DESKTOP/2"
    filter_url = "https://mapi.makemytrip.com/clientbackend/cg/filter-count/DESKTOP/2"

    payload = json.dumps({
      "deviceDetails": {
        "appVersion": "121",
        "deviceId": "13434",
        "bookingDevice": "DESKTOP",
        "deviceType": "DESKTOP"
      },
      "searchCriteria": {
        "checkIn": checkin,
        "checkOut": checkout,
        "limit": 100,
        "topHtlId": "",
        "roomStayCandidates": [
          {
            "rooms": 1,
            "adultCount": 2,
            "childAges": []
          }
        ],
        "countryCode": "IN",
        "cityCode": city_code,
        "locationId": city_code,
        "locationType": "city",
        "currency": "INR",
        "personalizedSearch": True,
        "nearBySearch": False
      },
      "requestDetails": {
        "visitorId": "121",
        "visitNumber": 1,
        "funnelSource": "HOTELS",
        "idContext": "B2C",
        "pageContext": "LISTING"
      },
      "featureFlags": {
        "soldOut": True,
        "staticData": True,
        "extraAltAccoRequired": False,
        "freeCancellation": True,
        "coupon": True,
        "walletRequired": True,
        "poisRequiredOnMap": True,
        "mmtPrime": False,
        "checkAvailability": True,
        "reviewSummaryRequired": True,
        "persuasionSeg": "P1000",
        "persuasionsRequired": True,
        "persuasionsEngineHit": True,
        "shortlistingRequired": False,
        "similarHotel": False,
        "personalizedSearch": True,
        "originListingMap": False,
        "selectiveHotels": False,
        "seoDS": False
    },
      "imageDetails": {
        "types": [
          "professional"
        ],
        "categories": [
          {
            "type": "H",
            "count": 1,
            "height": 162,
            "width": 243,
            "imageFormat": "webp"
          }
        ]
      },
      "reviewDetails": {
        "otas": [
          "MMT"
        ],
        "tagTypes": [
          "BASE"
        ]
      },
      "expData": "{PDO:PN}"
    })
    headers = {
        "Usr-Mcid": "121",
        "Tid": "avc",
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    response = requests.post(url, headers=headers, data=payload)
    response_data = response.json()
    with open('search.json', 'w') as json_file:
      json.dump(response_data, json_file, indent=2)

    filter_response = requests.post(filter_url,headers=headers,data=payload)
    filter_response_data = filter_response.json()
    if 'response' in filter_response_data :
      total_property_count = filter_response_data['response']['filteredCount']
      filter_list = filter_response_data['response']['filterList']

      filters = []
      for filter in filter_list :
          try : 
            filter_title = filter['title']
            if filter_title == "Star Category" :
                star_filter = []
                for filt in filter['filters'] :
                  star_filter.append({filt['title'] : filt['count']})
            elif filter_title == "Property Type" :
               type_filter = []
               for filt in filter['filters'] :
                  type_filter.append({filt['title'] : filt['count']})
          except:
            pass
      
      filters.append({"Property Type":type_filter})
      filters.append({"Star Category":star_filter})

    return filters,total_property_count,response_data

def extract_hotel_info(response_json):
    hotels_info = []
    
    # Check if the response has the required structure
    if 'response' in response_json and 'personalizedSections' in response_json['response']:
        for section in response_json['response']['personalizedSections']:
            if 'hotels' in section:
                for hotel in section['hotels']:
                    image_urls = [
                        media['url'].split('?')[0].replace('//', 'https://')
                        for media in hotel.get('media', [])
                        if media['mediaType'] == 'IMAGE'
                    ]
                    try : 
                       ReviewSummary = {
                            'RatingScore': hotel['reviewSummary']['cumulativeRating'],
                            'RatingCount': hotel['reviewSummary']['totalRatingCount'],
                            'ReviewCount': hotel['reviewSummary']['totalReviewCount']
                        }
                    except :
                      ReviewSummary = None

                    hotel_info = {
                        'otaPId' : str(hotel.get('id')),
                        'Name': hotel.get('name', 'N/A'),
                        'Rating': hotel.get('starRating', 'N/A'),
                        'Location': ', '.join(hotel.get('locationPersuasion', [])),
                        'Price': hotel['priceDetail']['discountedPrice'],
                        'ImageUrls': image_urls,
                        'DetailLink': hotel.get('detailDeeplinkUrl', 'N/A'),
                        'ReviewSummary': ReviewSummary
                    }
                    hotels_info.append(hotel_info)
    return hotels_info