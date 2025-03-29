import requests
import json
from datetime import datetime, timedelta

username = 'vrrastoria'
password = 'VRR@1234'
propertyCode = "IN-08b8203d-78ca-434f-a6fc-b8791dca6ccb"
roomId = "6037da39-4993-05c3-977f-641c61d19529"
roomPlanId = "IN-08b8203d-78ca-434f-a6fc-b8791dca6ccb"
channelId = "6037da39-4993-05c3-977f-641c61d19529_IN-08b8203d-78ca-434f-a6fc-b8791dca6ccb"
channelCode = "MAX"
availability = 9
baseAvailability = 0
sold = 2
totalAvailability = 11
occupancy = [1, 2, 3]
occupancyRate = [3150, 3600, 10750]
extraPerson = ""
extraPersonRate = ""
extraChildren = ""
extraChildrenRate = ""
perExtraPerson = ""
startDate = "2024-09-11"
endDate = "2024-09-11"
rate = 3150
minStay = 1
maxStay = 0

def maximojoBulkRatePushAPI(username, password, propertyCode, roomId, roomPlanId, channelCode, availability, rate, perExtraPerson, extraChildren, extraChildrenRate, extraPerson, extraPersonRate, occupancy, occupancyRate, baseAvailability, sold, totalAvailability, minStay, maxStay, startDate, endDate):

  session = requests.Session()

  login_url = f"https://api.platform.maximojo.com/mantrasv5.svc/login?u={username}&p={password}"

  login_response = session.get(login_url)

  if login_response.status_code == 200:
      print("Login successfully!")
      
      cookies = session.cookies.get_dict()
      asp_session_id = cookies.get('ASP.NET_SessionId')
      session_id = cookies.get('session-id')

      print("Extracted Cookies:")
      print(f"ASP.NET_SessionId: {asp_session_id}")
      print(f"session-id: {session_id}")

  else:
      print("Invalid Credential!")
      exit()

  domain_url = "https://api.platform.maximojo.com/mantrasv5.svc/getRateCalendarSnapshot"
  domain_payload = json.dumps({
      "hotelId": propertyCode,
      "startDate": startDate,
      "endDate": endDate
  })

  headers = {
      'session-id': session_id,
      'Content-Type': 'application/json'
  }

  domain_response = session.post(domain_url, headers=headers, data=domain_payload)

  if domain_response.status_code == 200:
      domain_result = json.loads(domain_response.content.decode('utf-8-sig'))
      if isinstance(domain_result, list) and len(domain_result) > 0:
          domain_id = domain_result[0].get('DomainId')
      else:
          print("No domain data found.")
          return
  else:
      print(f"Failed to get domain data: {domain_response.status_code}")
      return

  rate_calendar_url = "https://api.platform.maximojo.com/mantrasv5.svc/FindRateCalendars"
  
  rate_calendar_payload = json.dumps({
      "DomainId": domain_id,
      "HotelId": propertyCode,
      "ChannelCodes": [channelCode],
      "StayDates": {
          "Start": startDate,
          "End": endDate
      },
      "IsRemote": False
  })

  rate_response = session.post(rate_calendar_url, headers=headers, data=rate_calendar_payload)

  if rate_response.status_code == 200:
      result_data = rate_response.content.decode('utf-8-sig')
      result_json = json.loads(result_data)

      with open("Row.json", 'w') as json_file:
          json.dump(result_json, json_file, indent=2)

      if isinstance(result_json, list) and len(result_json) > 0:
          first_item = result_json[0]
          room_rate_plans = first_item.get('RoomRatePlans', [])

          for rate_detail_info in room_rate_plans:
              existing_availability = rate_detail_info.get('Availability')
              existing_baseAvailability = rate_detail_info.get('BaseAvailability')
              existing_sold = rate_detail_info.get('Sold')
              existing_totalAvailability = rate_detail_info.get('TotalAvailability')
              existing_minStay = rate_detail_info.get('MinStay')
              existing_maxStay = rate_detail_info.get('MaxStay')
              existing_advPurchase = rate_detail_info.get('AdvPurchase')
              existing_manualEditType = rate_detail_info.get('ManualEditType')
              existing_per_day = rate_detail_info['RoomRate'].get('PerDay')
              existing_per_occupancy = rate_detail_info['RoomRate'].get('PerOccupancy', {})
              existing_extra_person = rate_detail_info['RoomRate'].get('ExtraPerson', {})
              existing_extra_children = rate_detail_info['RoomRate'].get('ExtraChildren', {})
              existing_per_extra_person = rate_detail_info['RoomRate'].get('PerExtraPerson')

              if availability == '':
                  availability = existing_availability
              
              if baseAvailability == '':
                  baseAvailability = existing_baseAvailability
              
              if sold == '':
                  sold = existing_sold
              
              if totalAvailability == '':
                  totalAvailability = existing_totalAvailability
              
              if minStay == '':
                  minStay = existing_minStay
              
              if maxStay == '':
                  maxStay = existing_maxStay

              if occupancy == '' or not isinstance(occupancy, dict):
                  occupancy = existing_per_occupancy
              else:
                  for key, value in existing_per_occupancy.items():
                      if key not in occupancy or occupancy[key] == '':
                          occupancy[key] = value

              if extraPerson == '' or not isinstance(extraPerson, dict):
                  extraPerson = existing_extra_person
              else:
                  for key, value in existing_extra_person.items():
                      if key not in extraPerson or extraPerson[key] == '':
                          extraPerson[key] = value

              if extraChildren == '' or not isinstance(extraChildren, dict):
                  extraChildren = existing_extra_children
              else:
                  for key, value in existing_extra_children.items():
                      if key not in extraChildren or extraChildren[key] == '':
                          extraChildren[key] = value

              room_rate = {
                  "PerDay": rate if rate != '' else existing_per_day,
                  "PerOccupancy": occupancy,
                  "ExtraPerson": extraPerson,
                  "ExtraChildren": extraChildren
              }

              perExtraPerson = perExtraPerson if perExtraPerson != '' else existing_per_extra_person
  else:
      print(f"Failed to fetch rate data: {rate_response.status_code}")

  url = "https://api.platform.maximojo.com/mantrasv5.svc/SaveMasterRateCalendar"

  payload = json.dumps({
    "rateCalendarItems": [
      {
        "Id": None,
        "DomainId": domain_id,
        "HotelId": propertyCode,
        "ChannelCode": channelCode,
        "StayDate": startDate,
        "RoomRatePlans": [
          {
            "Id": channelId,
            "ChannelCode": channelCode,
            "RoomTypeId": roomId,
            "RatePlanId": roomPlanId,
            "Availability": availability,
            "BaseAvailability": baseAvailability,
            "Sold": sold,
            "TotalAvailability": totalAvailability,
            "IsClosed": False,
            "AvailabilityRatio": None,
            "RoomRate": room_rate,
            "perExtraPerson": perExtraPerson,
            "MinStay": minStay,
            "MaxStay": maxStay,
            "AdvPurchase": existing_advPurchase,
            "MinAdvPurchaseDays": None,
            "MaxAdvPurchaseDays": None,
            "Source": "Manual",
            "CTA": False,
            "CTD": False,
            "Tags": {
              "SyncRRP": ""
            },
            "RateMgrLock": False,
            "ManualEditType": existing_manualEditType
          }
        ],
        "SaveTimestamp": None,
        "SyncTimestamp": None
      }
    ],
    "ChannelCodes": [
      channelCode
    ],
    "manualOverride": True
  })

  headers = {
    'session-id': session_id,
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  print(response.text)


maximojoBulkRatePushAPI(username, password, propertyCode, roomId, roomPlanId, channelCode, availability, rate, perExtraPerson, extraChildren, extraChildrenRate, extraPerson, extraPersonRate, occupancy, occupancyRate, startDate, endDate)

