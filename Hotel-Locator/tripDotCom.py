import requests , json ,datetime

checkin = datetime.datetime.today()
checkout = checkin + datetime.timedelta(days=1)
checkin_str = checkin.strftime('%Y-%m-%d')
checkout_str = checkout.strftime('%Y-%m-%d')

def get_tripDotCom_url(hotel_name,hotel_city):

    body = {
        "keyword":f"{hotel_name} {hotel_city}",
        "head":{}
    }
    endpoint = f"https://us.trip.com/restapi/soa2/14975/homepageSuggest"
    response = requests.post(endpoint , json=body)

    if response.status_code == 200:
        response_data = response.json()

        results = response_data['result']
        for result in results:
            if result['resourceType']  == "hotel":
                hotel_id = result['id']
                break
            else :
                pass
    else:
        pass
    
    return f"https://www.trip.com/hotels/detail/?hotelId={hotel_id}&checkIn={checkin_str}&checkOut={checkout_str}&curr=INR"