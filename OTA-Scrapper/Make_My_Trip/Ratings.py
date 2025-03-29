import requests
import json

rating_data = []
api_url = "https://mapi.makemytrip.com/clientbackend/cg/search-hotels/DESKTOP/2?language=eng&region=in&currency=INR&idContext=B2C&countryCode=IN&ck=4d55d48f-319f-4654-9240-4dbf32f06f71"

headers = {
    "Visitor-Id":"a742bd8c-e191-4839-a4c8-b889b6121400",
    "Usr-Mcid":"2133",
    "Tid":"avc",
    "Server": "b2c",
    "Accept-Encoding": "gzip, deflate, br",
    "Cookie": "dvid=31fb109f-2801-4758-a225-47c741933996",
    "Accept-Language":"en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
    "Vid": "a742bd8c-e191-4839-a4c8-b889b6121400",
    "Mmt-Auth": "MAT1c4f069ae88e1c97a79485456270b75c5baee444b895693b69ab021670e176a1f7fe3eb63bf9377ee66bf892ea4ae3ce7P",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

body = {
    "deviceDetails": {
        "appVersion": "120.0.0.0",
        "deviceId": "31fb109f-2801-4758-a225-47c741933996",
        "bookingDevice": "DESKTOP",
        "networkType": "WiFi",
        "deviceType": "DESKTOP",
        "deviceName": None
    },
    "filterRemovedCriteria": None,
    "searchCriteria": {
        "checkIn": "2024-02-15",
        "checkOut": "2024-02-16",
        "limit": 20,
        "roomStayCandidates": [
            {
                "adultCount": 2
            }
        ],
        "countryCode": "IN",
        "cityCode": "CTUDR",
        "currency": "INR",
        "lastHotelId": "",
        "lastHotelCategory": "",
        "personalizedSearch": True,
        "nearBySearch": False,
        "totalHotelsShown": None,
        "personalCorpBooking": False,
        "rmDHS": False,
        "lastFetchedWindowInfo": ""
    },
    "requestDetails": {
        "visitorId": "a742bd8c-e191-4839-a4c8-b889b6121400",
        "visitNumber": 134,
        "trafficSource": None,
        "funnelSource": "HOTELS",
        "idContext": "B2C",
        "pageContext": "LISTING",
        "channel": "B2Cweb",
        "journeyId": "-185485837131fb109f-2801-4758-a225-47c741933996",
        "requestId": "b58a6388-7d1b-4a69-8077-0dfa88a9cf57",
        "couponCount": 2,
        "seoCorp": False,
        "loggedIn": True,
        "forwardBookingFlow": False
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
            "MMT",
            "TA"
        ],
        "tagTypes": [
            "BASE",
            "WHAT_GUESTS_SAY"
        ]
    },
    "filterCriteria": [],
    "matchMakerDetails": {
        "latLng": [
            {
                "latitude": 24.58215,
                "longitude": 73.66984,
                "name": "Amar Kothi"
            }
        ]
    },
    "sortCriteria": None,
    "expData": "{APE:10,PAH:5,PAH5:T,WPAH:F,BNPL:T,MRS:T,PDO:PN,MCUR:T,ADDON:T,CHPC:T,AARI:T,NLP:Y,RCPN:T,PLRS:T,MMRVER:V3,BLACK:T,IAO:F,BNPL0:T,EMIDT:2,HAFC:T,ALC:T,LSTNRBY:T,HIS:DEFAULT,VIDEO:0,MLOS:T,CV2:T,SOU:T,APT:T,AIP:T,HFC:F,PERNEW:T,RTBC:T,FLTRPRCBKT:T,CRF:B}",
    "userLocation": None
}


response = requests.post(api_url, headers=headers, json=body) 


if response.status_code == 200:

    response_content = response.json()

    with open('Row_Data.json', 'w') as json_file:
        json.dump(response_content, json_file, indent=2)

else:
    print(response)