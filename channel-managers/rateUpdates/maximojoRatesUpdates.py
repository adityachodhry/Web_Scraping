import requests
import json
from datetime import datetime, timedelta

username = 'vrrastoria'
password = 'VRR@1234'
propertyCode = "IN-08b8203d-78ca-434f-a6fc-b8791dca6ccb"
roomId = "6037da39-4993-05c3-977f-641c61d19529"
roomPlanId = "IN-08b8203d-78ca-434f-a6fc-b8791dca6ccb"
channelId = "6037da39-4993-05c3-977f-641c61d19529_IN-08b8203d-78ca-434f-a6fc-b8791dca6ccb"
channelCode = ["GIB", "EXP", "BDC", "TLG", "AGO"]
domainId = "fab40c6a-5b74-b7cb-0b51-a153498791b3"

def maximojoBulkRatePushAPI(username, password):

  session = requests.Session()

  login_url = f"https://api.platform.maximojo.com/mantrasv5.svc/login?u={username}&p={password}"

  login_response = session.get(login_url)

  if login_response.status_code == 200:
      print("Login successfully!")
      
      cookies = session.cookies.get_dict()
      asp_session_id = cookies.get('ASP.NET_SessionId')
      session_id = cookies.get('session-id')

      print("Cookies Extracted Successfully:")
      print(f"ASP.NET_SessionId: {asp_session_id}")
      print(f"session-id: {session_id}")

  else:
      print("Invalid Credential!")
      exit()

  # Date setup
  current_date = datetime.now()
  end_date = current_date + timedelta(days=1)

  start_date_str = current_date.strftime("%Y-%m-%dT00:00:00.000Z")
  end_date_str = end_date.strftime("%Y-%m-%dT00:00:00.000Z")

  url = "https://api.platform.maximojo.com/mantrasv5.svc/SaveMasterRateCalendar"

  payload = json.dumps({
  "rateCalendarItems": [
    {
      "Id": None,
      "DomainId": "fab40c6a-5b74-b7cb-0b51-a153498791b3",
      "HotelId": "IN-08b8203d-78ca-434f-a6fc-b8791dca6ccb",
      "ChannelCode": "MAX",
      "StayDate": "2024-09-06T00:00:00Z",
      "RoomRatePlans": [
        {
          "Id": "6037da39-4993-05c3-977f-641c61d19529_IN-08b8203d-78ca-434f-a6fc-b8791dca6ccb",
          "ChannelCode": "MAX",
          "RoomTypeId": "6037da39-4993-05c3-977f-641c61d19529",
          "RatePlanId": "IN-08b8203d-78ca-434f-a6fc-b8791dca6ccb",
          "Availability": 12,
          "BaseAvailability": 0,
          "Sold": 0,
          "TotalAvailability": 12,
          "IsClosed": False,
          "AvailabilityRatio": None,
          "RoomRate": {
            "PerDay": 3150,
            "PerOccupancy": {
              "1": 3150,
              "2": 3600,
              "3": 10750
            },
            "ExtraPerson": {
              "1": 450
            },
            "ExtraChildren": {
              "1": 1750,
              "2": 6250
            },
            "PerExtraPerson": 450
          },
          "MinStay": 1,
          "MaxStay": 0,
          "AdvPurchase": 0,
          "MinAdvPurchaseDays": None,
          "MaxAdvPurchaseDays": None,
          "Source": "Manual",
          "CTA": False,
          "CTD": False,
          "Tags": {
            "SyncRRP": ""
          },
          "RateMgrLock": False,
          "ManualEditType": 3
        },
        {
          "Id": "6037da39-4993-05c3-977f-641c61d19529_15d3ac29-c92f-877d-ddb1-679f61573cf1",
          "ChannelCode": "MAX",
          "RoomTypeId": "6037da39-4993-05c3-977f-641c61d19529",
          "RatePlanId": "15d3ac29-c92f-877d-ddb1-679f61573cf1",
          "Availability": 12,
          "BaseAvailability": 0,
          "Sold": 0,
          "TotalAvailability": 12,
          "IsClosed": False,
          "AvailabilityRatio": None,
          "RoomRate": {
            "PerDay": 3850,
            "PerOccupancy": {
              "1": 3850,
              "2": 4300,
              "3": 11050
            },
            "ExtraPerson": {
              "1": 450
            },
            "ExtraChildren": {
              "1": 2050,
              "2": 6550
            },
            "PerExtraPerson": 450
          },
          "MinStay": 1,
          "MaxStay": 0,
          "AdvPurchase": 0,
          "MinAdvPurchaseDays": None,
          "MaxAdvPurchaseDays": None,
          "Source": "Manual",
          "CTA": False,
          "CTD": False,
          "Tags": {
            "SyncRRP": ""
          },
          "RateMgrLock": False,
          "ManualEditType": 3
        },
        {
          "Id": "b9086912-d0a7-86ad-a0e0-32f896d43833_IN-08b8203d-78ca-434f-a6fc-b8791dca6ccb",
          "ChannelCode": "MAX",
          "RoomTypeId": "b9086912-d0a7-86ad-a0e0-32f896d43833",
          "RatePlanId": "IN-08b8203d-78ca-434f-a6fc-b8791dca6ccb",
          "Availability": 3,
          "BaseAvailability": 0,
          "Sold": 1,
          "TotalAvailability": 4,
          "IsClosed": False,
          "AvailabilityRatio": None,
          "RoomRate": {
            "PerDay": 3600,
            "PerOccupancy": {
              "1": 3600,
              "2": 4000,
              "3": 5000
            },
            "ExtraPerson": {
              "1": 400,
              "2": 1000
            },
            "ExtraChildren": {
              "1": 2250,
              "2": 6750
            },
            "PerExtraPerson": 1000
          },
          "MinStay": 1,
          "MaxStay": 0,
          "AdvPurchase": 0,
          "MinAdvPurchaseDays": None,
          "MaxAdvPurchaseDays": None,
          "Source": "Manual",
          "CTA": False,
          "CTD": False,
          "Tags": {
            "SyncRRP": ""
          },
          "RateMgrLock": False,
          "ManualEditType": 7
        },
        {
          "Id": "aaae1411-ab81-bdf1-20bb-78853f96e5cc_IN-08b8203d-78ca-434f-a6fc-b8791dca6ccb",
          "ChannelCode": "MAX",
          "RoomTypeId": "aaae1411-ab81-bdf1-20bb-78853f96e5cc",
          "RatePlanId": "IN-08b8203d-78ca-434f-a6fc-b8791dca6ccb",
          "Availability": 63,
          "BaseAvailability": 0,
          "Sold": 0,
          "TotalAvailability": 63,
          "IsClosed": False,
          "AvailabilityRatio": None,
          "RoomRate": {
            "PerDay": 4300,
            "PerOccupancy": {
              "1": 4300,
              "2": 4720,
              "3": 5720,
              "4": 6720
            },
            "ExtraPerson": {
              "1": 420,
              "2": 1000,
              "3": 1000
            },
            "ExtraChildren": {
              "1": 2750,
              "2": 7250
            },
            "PerExtraPerson": 1000
          },
          "MinStay": 1,
          "MaxStay": 0,
          "AdvPurchase": 0,
          "MinAdvPurchaseDays": None,
          "MaxAdvPurchaseDays": None,
          "Source": "Manual",
          "CTA": False,
          "CTD": False,
          "Tags": {
            "SyncRRP": ""
          },
          "RateMgrLock": False,
          "ManualEditType": 7
        },
        {
          "Id": "b9086912-d0a7-86ad-a0e0-32f896d43833_15d3ac29-c92f-877d-ddb1-679f61573cf1",
          "ChannelCode": "MAX",
          "RoomTypeId": "b9086912-d0a7-86ad-a0e0-32f896d43833",
          "RatePlanId": "15d3ac29-c92f-877d-ddb1-679f61573cf1",
          "Availability": 3,
          "BaseAvailability": 0,
          "Sold": 0,
          "TotalAvailability": 3,
          "IsClosed": False,
          "AvailabilityRatio": None,
          "RoomRate": {
            "PerDay": 4300,
            "PerOccupancy": {
              "1": 4300,
              "2": 4720,
              "3": 6020
            },
            "ExtraPerson": {
              "1": 420,
              "2": 1300
            },
            "ExtraChildren": {
              "1": 2550,
              "2": 7050
            },
            "PerExtraPerson": 1300
          },
          "MinStay": 1,
          "MaxStay": 0,
          "AdvPurchase": 0,
          "MinAdvPurchaseDays": None,
          "MaxAdvPurchaseDays": None,
          "Source": "Manual",
          "CTA": False,
          "CTD": False,
          "Tags": {
            "SyncRRP": ""
          },
          "RateMgrLock": False,
          "ManualEditType": 7
        },
        {
          "Id": "aaae1411-ab81-bdf1-20bb-78853f96e5cc_15d3ac29-c92f-877d-ddb1-679f61573cf1",
          "ChannelCode": "MAX",
          "RoomTypeId": "aaae1411-ab81-bdf1-20bb-78853f96e5cc",
          "RatePlanId": "15d3ac29-c92f-877d-ddb1-679f61573cf1",
          "Availability": 63,
          "BaseAvailability": 0,
          "Sold": 0,
          "TotalAvailability": 63,
          "IsClosed": False,
          "AvailabilityRatio": None,
          "RoomRate": {
            "PerDay": 5000,
            "PerOccupancy": {
              "1": 5000,
              "2": 5500,
              "3": 6800,
              "4": 8100
            },
            "ExtraPerson": {
              "1": 500,
              "2": 1300,
              "3": 1300
            },
            "ExtraChildren": {
              "1": 3050,
              "2": 7550
            },
            "PerExtraPerson": 1300
          },
          "MinStay": 1,
          "MaxStay": 0,
          "AdvPurchase": 0,
          "MinAdvPurchaseDays": None,
          "MaxAdvPurchaseDays": None,
          "Source": "Manual",
          "CTA": False,
          "CTD": False,
          "Tags": {
            "SyncRRP": ""
          },
          "RateMgrLock": False,
          "ManualEditType": 7
        }
      ],
      "SaveTimestamp": None,
      "SyncTimestamp": None
    }
  ],
  "ChannelCodes": [
    "GIB",
    "EXP",
    "BDC",
    "TLG",
    "AGO",
    "CLT"
  ],
  "manualOverride": True
})
  
  headers = {
    'session-id': session_id,
    'Content-Type': 'application/json',
    'Cookie': f'ASP.NET_SessionId={asp_session_id}; session-id={session_id}'
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  if response.status_code == 200:

    # response_content = response.json()
    print(response)
    print("Rates and Inventory Data Updated Successfully!")

  else:
    print("Failed to update rates.")

maximojoBulkRatePushAPI(username, password)

