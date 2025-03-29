
import requests
from datetime import datetime
import json

url = "https://rz.rategain.com/RezGain/read"

payload = {
    'METHOD': 'reservationsearch/search',
    'Parameter': '{"reservationsearch":{"searchon":"Arrival Date","searchfrom":"08/03/2023","searchto":"07/04/2024","requeststatus":"0","channels":[{"channel":"Booking.com","channelid":221,"channeltype":-1,"Selected":false,"editstatus":null,"selected":true},{"channel":"Expedia","channelid":434,"channeltype":-1,"Selected":false,"editstatus":null,"selected":true},{"channel":"TravelGuru–Yatra","channelid":787,"channeltype":-1,"Selected":false,"editstatus":null,"selected":true},{"channel":"Goibibo-MakeMyTrip_V3","channelid":792,"channeltype":-1,"Selected":false,"editstatus":null,"selected":true},{"channel":"Agoda","channelid":1011,"channeltype":-1,"Selected":false,"editstatus":null,"selected":true},{"channel":"Simplotel","channelid":1103,"channeltype":-1,"Selected":false,"editstatus":null,"selected":true},{"channel":"EaseMyTrip","channelid":2221,"channeltype":-1,"Selected":false,"editstatus":null,"selected":true}],"reservations":null,"showdelloglink":false,"unitycallparam":"","allowUpdatelog":""},"dnldfilepath":""}'
}

headers = {
    'Cookie': 'ASP.NET_SessionId=5gr5vxebldqujddls4ftwsvc; dtfmt=dd/MM/yyyy;UIVersion=20240305;',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept-Encoding': 'gzip, deflate, br',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
}

response = requests.post(url, headers=headers, data=payload)
# print(response)
response_data = response.json()

reservations = response_data['reservationsearch']['reservations']

def calculate_lead_time(booking_date, arrival_date):
    booking_datetime = datetime.strptime(booking_date, "%d/%m/%Y")
    arrival_datetime = datetime.strptime(arrival_date, "%d/%m/%Y")
    lead_time = (arrival_datetime - booking_datetime).days
    return lead_time

def transform_reservation(reservation):
    is_active = reservation["status"].lower() == "confirmed"
    lead_time = calculate_lead_time(reservation["bookeddate"], reservation["checkindate"])
    
    transformed_reservation = {
        "hotelName": "Regenta SGS Greenotel",
        "res": str(reservation["reservationid"]),
        "bookingDate": datetime.strptime(reservation["bookeddate"], "%d/%m/%Y").strftime("%Y-%m-%d"),
        "guestName": reservation["guestname"],
        "arrivalDate": datetime.strptime(reservation["checkindate"], "%d/%m/%Y").strftime("%Y-%m-%d"),
        "deptDate": datetime.strptime(reservation["checkoutdate"], "%d/%m/%Y").strftime("%Y-%m-%d"),
        "room": reservation["roomtype"],
        "pax": f"{reservation['norooms']}\\{reservation['noroomtypes']}",
        "ADR": float(reservation["grossrate"]) / float(reservation["noofroomnight"]) if reservation["noofroomnight"] is not None else None,
        "source": reservation["channel"],
        "totalCharges": float(reservation["grossrate"]),
        "noOfNights": reservation["noofroomnight"],
        "lead": lead_time,
        "hotelCode": "1689",
        "isActive": str(is_active).lower()
    }
    return transformed_reservation

# Transform each reservation
transformed_reservations = [transform_reservation(reservation) for reservation in reservations]

with open('Regenta.json','w') as file :
    json.dump(transformed_reservations,file,indent=2)

print(transformed_reservations)