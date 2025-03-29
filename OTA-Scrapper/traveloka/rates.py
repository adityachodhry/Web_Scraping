import requests
from datetime import datetime, timedelta
import json  

hotel_id = 1000000242768

num_days = 90

today = datetime.now()
room_data = {
    "timestamp": today.strftime("%Y-%m-%d %H:%M:%S"),
    "rates": []
}

for day in range(num_days):
    check_in_date = (today + timedelta(days=day)).strftime("%Y-%m-%d")
    check_out_date = (today + timedelta(days=day + 1)).strftime("%Y-%m-%d")

    url = "https://www.traveloka.com/api/v2/hotel/searchRooms"

    body = {
        "fields": [],
        "data": {
            "contexts": {
                "bookingId": None,
                "sourceIdentifier": "HOTEL_DETAIL",
                "shouldDisplayAllRooms": False,
                "inventoryRateKey": "tCI74RobDcii8TFR6EO8dfBoDgXZAdJDba/+b/yo7vncPHLhtRgs+YZfWTpOTkqS9i9DiwhZIGlXZ+YbVxCoyh4Yf3vvGdvfXkHeauMGbsfIrzEYheZ704cJ2YST+A9Nd26KBECrxfbtSxvlVdzChmtfU1Qe4lcomxL2cMoHk+V6MhVfB+MGvASBIrnW994jIvEWeildVo7nbHxIWcXPVNGysXwP9P/6jQTjnyKeTv+yqYmxSenRKFEfSHS0XO3kZfZPEEhT4qTyZ4NnGlioFk6ay4RXlsebEjOdYqJCyZZxlxUTHNffO2l8jiZZrGWdUlC0pGAd/FCWUuUDDhiFZh+63/J5iVUer3ukbLNduJUXpJ0bHLQQVJp2wmAG7TQABNB7QBD931UhfqgPfe4yNVc4KxuembJV6Yiv2h/CVOFOp0R4OFkOPO024pKj5xIA/SuwOWK5kwvZrG2Mg2Yuu37ItLeYSJAdbGUYSeqwSrwawREkALkeOydfvV5TtbB+TEz1OwP3IrAA8Jugwb1nItK86GilTqHjHMsEEFrul1Z8CS/WFNqllBTLDfKALgAatbkPrlGHYMvOxUcd8gSuE9olaRmAWbSrbAx4lGVLBha/zTvZV0gOgy8QojE2ombEtMM9W5F3LU+3MiLXiG/crZ+cjOcshP/lnzDiU9VoWjc="
            },
            "prevSearchId": "1798010602935833993",
            "numInfants": 0,
            "ccGuaranteeOptions": {
                "ccInfoPreferences": [
                    "CC_TOKEN",
                    "CC_FULL_INFO"
                ],
                "ccGuaranteeRequirementOptions": [
                    "CC_GUARANTEE"
                ]
            },
            "rateTypes": [
                "PAY_NOW",
                "PAY_AT_PROPERTY"
            ],
            "isJustLogin": False,
            "isReschedule": False,
            "preview": True,
            "monitoringSpec": {
                "lastKeyword": "Shangri-La Eros, New Delhi",
                "referrer": "https://www.traveloka.com/en-en/hotel/search?spec=04-05-2024.05-05-2024.1.1.HOTEL_GEO.4008347332.New%20Delhi.1",
                "isPriceFinderActive": "null",
                "dateIndicator": "null",
                "displayPrice": "null"
            },
            "hotelId": "1000000242768",
            "currency": "USD",
            "labelContext": {},
            "isExtraBedIncluded": True,
            "hasPromoLabel": True,
            "supportedRoomHighlightTypes": [
                "ROOM"
            ],
            "checkInDate": {
                "day": "4",
                "month": "5",
                "year": "2024"
            },
            "checkOutDate": {
                "day": "5",
                "month": "5",
                "year": "2024"
            },
            "numOfNights": 1,
            "numAdults": 1,
            "numRooms": 1,
            "numChildren": 0,
            "childAges": [],
            "tid": "6a91d8b6-a3ca-4eb3-ba72-ba79464775fb"
        },
        "clientInterface": "desktop"
    }

    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'X-Domain' : 'accomRoom',
        'X-Route-Prefix' : 'en-en',
        'Referer' : 'https://www.traveloka.com/en-en/hotel/detail?spec=04-05-2024.05-05-2024.1.1.HOTEL.1000000242768.Shangri-La%20Eros%2C%20New%20Delhi.1&contexts=%7B%22inventoryRateKey%22%3A%22tCI74RobDcii8TFR6EO8dfBoDgXZAdJDba%2F%2Bb%2Fyo7vncPHLhtRgs%2BYZfWTpOTkqS9i9DiwhZIGlXZ%2BYbVxCoyh4Yf3vvGdvfXkHeauMGbsfIrzEYheZ704cJ2YST%2BA9Nd26KBECrxfbtSxvlVdzChmtfU1Qe4lcomxL2cMoHk%2BV6MhVfB%2BMGvASBIrnW994jIvEWeildVo7nbHxIWcXPVNGysXwP9P%2F6jQTjnyKeTv%2ByqYmxSenRKFEfSHS0XO3kZfZPEEhT4qTyZ4NnGlioFk6ay4RXlsebEjOdYqJCyZZxlxUTHNffO2l8jiZZrGWdUlC0pGAd%2FFCWUuUDDhiFZh%2B63%2FJ5iVUer3ukbLNduJUXpJ0bHLQQVJp2wmAG7TQABNB7QBD931UhfqgPfe4yNVc4KxuembJV6Yiv2h%2FCVOFOp0R4OFkOPO024pKj5xIA%2FSuwOWK5kwvZrG2Mg2Yuu37ItLeYSJAdbGUYSeqwSrwawREkALkeOydfvV5TtbB%2BTEz1OwP3IrAA8Jugwb1nItK86GilTqHjHMsEEFrul1Z8CS%2FWFNqllBTLDfKALgAatbkPrlGHYMvOxUcd8gSuE9olaRmAWbSrbAx4lGVLBha%2FzTvZV0gOgy8QojE2ombEtMM9W5F3LU%2B3MiLXiG%2FcrZ%2BcjOcshP%2FlnzDiU9VoWjc%3D%22%7D&loginPromo=1&prevSearchId=1798010602935833993',
        'Cookie' : '_gcl_au=1.1.1682877213.1712574295; _cs_c=1; _fbp=fb.1.1712574316399.321402342; _tt_enable_cookie=1; _ttp=5GC1QEg243caLr2zwkDfvOI5H9h; _ga_RSRSMMBH0X=deleted; tv-repeat-visit=true; countryCode=IN; _gid=GA1.2.1410051140.1714716526; tv_user={"authorizationLevel":100,"id":null}; amp_f4354c=HFYhkE3fffvc1uGWVENcQq...1hsum4t4u.1hsuokmqj.0.9.9; _ga=GA1.2.452047242.1712574296; _gat_UA-29776811-12=1; cto_bundle=XY4P819MUU5zVHBKRVJVY0ZFYUxoQWdVd0slMkJ2NFhSV2EyOVRIb09kYmMzc1hmeFYxOHVPeExVSXhmUEdGem5zVXRqJTJGc2xVSHJuJTJCVjhxcEI3WjFYcmQyZzRDWkQ5Y1hwclpBSmtZamQxQnRSJTJCQnhqa1ZrSEQ5UHhXaElOMmk3eE9wbUFXY2Y2ZmxXQ1FDUmRjQVdRJTJGeGtVcWklMkJjVnA5YXhLWFMydnowRkt5NFFheG5velc0M3RkWHVJRFpNRWNCZGZUMkhmVDdLd20zdXVXV05ZYXVwaVNrdjlJODJIa1d5WUxBbnZHS25kRnE3SWF4NGVIVFRIeXJqVTBUTjdSZVlQRUFxY2dLUyUyRjdXMHBYJTJCMWgxOVBLVnpBTlZlODBQTk5tYWx4QXNRVEt4Rmg4RVhVY0dDNk5NdmhqQld5dWtJUzJlcks; aws-waf-token=d0756c9d-9fc6-4dc9-b8ee-a26f986c800e:HgoAor44+I8JAAAA:UJGTy2w66rGLPi1ynBsQcDjApasKSP6POEwt+MDef9gVkBEuHJL6zsysK4h/WLHcMF/loqgl4E552wWsUFZ4+ZV+ii/dafKWs7pZm71PJlm6Ie2oSbz0fioFQIsZ//oAZ0YXSsjXaIPZCbCypdwdXClt0IdEGDSJbgEZXNBsuwOcDdB6OVZOgcIPO2A38G81uRLTyFhokPRM3Dc=; tvl=c43e2qO9dC3KCb29oX6UE9DCNr1t6tcBnZQ9n73mf8dLjLMRosr7xcVkiO33M7oEdNQmmkW7RqQHzL1vGak1BjRS7dIQ5cTbBahw8oN6ZAPBSNXMFeCjPSJJra6q73gcuwkSI3DlPRcnaiQX0xtFhYVCDyDutEZUZOIrZPX5xZ8OcLDYY82NHEYIcHTAwQhw28NK76jOKSzkv7BzvpvggNxcNsYrQtkQAMjXX/9vw03rffY4UufCTRarT73wsQqwpYg4y4DCN44=~djAy; tvs=DbdtD/dxB4oP1cZ6ucoIf+aiCABQgad1EMIBfTMKw977xjJoCOF1+OLR60Tfh0eXoowB2xBqmqsnvkAC9+PlLg9+qUZSQKjrIJBZRTByhdXudhjrqJ7RXPj/6bFN0q/cCeK31Ddzpnt2Xw3mOkHq9/KVI2sK9JKHAupScedndbQNXPliwhYAsadYBMz9JdqMBL+tlr/ViYP0RiwH4MgvT2S+FqxWrlx8ROONAe00cBC27MzuZhrOqC65jAifkg5tsyppuSGe/2JbGlhhGDdkpGxBz8Iwl9UzkuM=~djAy; amp_1a5adb=7IOyruSWsUxyYNdt87vghY...1hsum4t4q.1hsuol4e6.6n.9.70; _cs_id=755aa14b-5380-a4d7-bdab-5e5425521ee7.1712574295.13.1714724442.1714720376.1.1746738295902.1; _cs_s=6.5.0.1714726242860; _ga_RSRSMMBH0X=GS1.1.1714721809.5.1.1714724450.36.0.0; _dd_s=expire=1714725351441&rum=0&logs=1&id=fa870d1a-bc59-4f90-909b-4e0d8fdcf8d6&created=1714722724954'
    }

    response = requests.post(url, json= body, headers= headers)

    if response.status_code == 200:
        response_content = response.json()
        # print(response_content)

        # with open('travelokaRates.json', 'w') as json_file:
        #     json.dump(response_content, json_file, indent=4)

        data_slot = response_content.get('data', {}).get('recommendedEntries', [])
        for data in data_slot:
            rooms = data.get('roomList', [])

            for roomlist in rooms:
                roomId = roomlist.get('hotelRoomId')
                roomName = roomlist.get('name')
                ratedisplay_str = roomlist.get('rateDisplay', {}).get('baseFare', {}).get('amount')

                ratedisplay = int(ratedisplay_str) / 100 if ratedisplay_str else None
            
                currency = roomlist.get('rateDisplay', {}).get('baseFare', {}).get('currency')

                isBreakfastIncluded = roomlist.get('isBreakfastIncluded')
                roomPlan = "CP" if isBreakfastIncluded else "EP"

                room_data['rates'].append({
                    "roomId": roomId,
                    "name": roomName,
                    "checkIn": check_in_date,
                    "checkOut": check_out_date,
                    "roomPlan": roomPlan,
                    "displayPrice": f"{currency} {ratedisplay:.2f}" if ratedisplay is not None else None
                })

    print(f'HotelID : {hotel_id} rates for Checkin: {check_in_date}')

with open('rates_data.json', 'w') as json_file:
    json.dump(room_data, json_file, indent=4)


               