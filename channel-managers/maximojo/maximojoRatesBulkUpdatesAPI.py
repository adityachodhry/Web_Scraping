import requests
import json

username = 'vrrastoria'
password = 'VRR@1234'
propertyCode = "IN-08b8203d-78ca-434f-a6fc-b8791dca6ccb"
roomId = "6037da39-4993-05c3-977f-641c61d19529"
roomPlanId = "IN-08b8203d-78ca-434f-a6fc-b8791dca6ccb"
channelId = "6037da39-4993-05c3-977f-641c61d19529_IN-08b8203d-78ca-434f-a6fc-b8791dca6ccb"
channelCode = "MAX"
availability = 9
occupancyId = 1
date = "2024-09-18"
rate = 3150

def maximojoBulkRatePush(propertyCode, cmCreds, ratesConfig, channelCode, roomId, roomPlanId, availability, rate, perExtraPerson, extraChildren, extraChildrenRate, extraPerson, extraPersonRate, occupancy, occupancyRate, occupancyId, startDate, endDate):
    
    username = cmCreds.get('username')
    password = cmCreds.get('password')

    session = requests.Session()

    login_url = f"https://api.platform.maximojo.com/mantrasv5.svc/login?u={username}&p={password}"
    login_response = session.get(login_url)

    if login_response.status_code == 200:
        print("Login successfully!")
        cookies = session.cookies.get_dict()
        asp_session_id = cookies.get('ASP.NET_SessionId')
        session_id = cookies.get('session-id')
    else:
        print("Invalid credentials!")
        return

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
    
    for config in ratesConfig.get('info', []):
        channelCode = config.get('channelCode')
        
        for room in config.get('roomInfo', []):
            roomId = room.get('roomId')
            
            for roomPlan in room.get('roomPlanInfo', []):
                roomPlanDetails = roomPlan.get('roomPlan', {})
                occupancyId = roomPlanDetails.get('occupancyId')
                ExtraPersonId = roomPlanDetails.get('ExtraPersonId')
                ExtraChildrenId = roomPlanDetails.get('ExtraChildrenId')
                rate = roomPlanDetails.get('rate')
                date = roomPlanDetails.get('date')

                rate_calendar_url = "https://api.platform.maximojo.com/mantrasv5.svc/FindRateCalendars"
                rate_calendar_payload = json.dumps({
                    "DomainId": domain_id,
                    "HotelId": propertyCode,
                    "ChannelCodes": [channelCode],
                    "StayDates": {
                        "Start": date,
                        "End": date
                    },
                    "IsRemote": False
                })

                rate_response = session.post(rate_calendar_url, headers=headers, data=rate_calendar_payload)

                occupancyId = {
                  "1": "PerOccupancy",
                  "2": "PerOccupancy",
                  "3": "PerOccupancy"
                }
                ExtraPersonId = {
                  "1": "ExtraPerson",
                  "2": "ExtraPerson",
                  "3": "ExtraPerson"
                }
                ExtraChildrenId = {
                  "1": "ExtraChildren",
                  "2": "ExtraChildren",
                  "3": "ExtraChildren"
                }


                if rate_response.status_code == 200:
                    result_data = rate_response.content.decode('utf-8-sig')
                    result_json = json.loads(result_data)

                    if isinstance(result_json, list) and len(result_json) > 0:
                        first_item = result_json[0]
                        room_rate_plans = first_item.get('RoomRatePlans', [])

                        for rate_detail_info in room_rate_plans:
                            existing_per_day = rate_detail_info['RoomRate'].get('PerDay')
                            existing_per_occupancy = rate_detail_info['RoomRate'].get('PerOccupancy', {})
                            existing_extra_person = rate_detail_info['RoomRate'].get('ExtraPerson', {})
                            existing_extra_children = rate_detail_info['RoomRate'].get('ExtraChildren', {})
                            existing_per_extra_person = rate_detail_info['RoomRate'].get('PerExtraPerson')


                            if occupancyId == '' or not isinstance(occupancyId, dict):
                                occupancyId = existing_per_occupancy
                            else:
                                for key, value in existing_per_occupancy.items():
                                    if key not in occupancyId or occupancyId[key] == '':
                                        occupancyId[key] = value

                            if ExtraPersonId == '' or not isinstance(ExtraPersonId, dict):
                                ExtraPersonId = existing_extra_person
                            else:
                                for key, value in existing_extra_person.items():
                                    if key not in ExtraPersonId or ExtraPersonId[key] == '':
                                        ExtraPersonId[key] = value

                            if ExtraChildrenId == '' or not isinstance(ExtraChildrenId, dict):
                                ExtraChildrenId = existing_extra_children
                            else:
                                for key, value in existing_extra_children.items():
                                    if key not in ExtraChildrenId or ExtraChildrenId[key] == '':
                                        ExtraChildrenId[key] = value

                            room_rate = {
                                "PerDay": rate if rate != '' else existing_per_day,
                                "PerOccupancy": occupancyId,
                                "ExtraPerson": ExtraPersonId,
                                "ExtraChildren": ExtraChildrenId
                            }

                            if ExtraPersonId == 1:
                              perExtraPerson = ExtraPersonId if ExtraPersonId != '' else existing_extra_person

                else:
                    print(f"Failed to fetch rate data: {rate_response.status_code}")
                    return

                rate_push_url = "https://api.platform.maximojo.com/mantrasv5.svc/BulkUpdateRateCalendarTask"
                body = {
                    "hotelId": propertyCode,
                    "bulkRateItems": [
                        {
                            "BulkRates": [
                                {
                                    "RoomTypes": [roomId],
                                    "RatePlans": [roomPlanId],
                                    "RoomRate": room_rate,
                                    "perExtraPerson": perExtraPerson
                                }
                            ],
                            "DateRanges": [
                                {
                                    "Start": f'{date}T00:00:00.000Z',
                                    "End": f'{date}T00:00:00.000Z'
                                }
                            ]
                        }
                    ],
                    "channelCodes": [channelCode],
                    "doSync": True
                }
                # print(body)

                push_response = session.post(rate_push_url, headers=headers, json=body)

                if push_response.status_code == 200:
                    print("Rates and inventory data updated successfully!")
                    print(push_response.text)
                else:
                    print(f"Failed to update rates and inventory. Status Code: {push_response.status_code}")
                    print(f"Response: {push_response.text}")



cmCreds = {
    "username": "Sales@shivacontinental.in",
    "password": "shiva@1234"
}

ratesConfig = {
    "info": [
        {
            "channelCode": "MAX",
            "roomInfo": [
                {
                    "roomId": 1912,
                    "roomPlanInfo": [
                        {
                            "roomPlan": {
                                "occupancyId": 1,
                                "rate": 4500,
                                "date": "2024-09-18"
                            }
                        },
                        {
                            "roomPlan": {
                                "ExtraPersonId": 1,
                                "rate": 4500,
                                "date": "2024-09-18"    
                            }
                        },
                        {
                            "roomPlan": {
                                "ExtraChildrenId": 1,
                                "rate": 4500,
                                "date": "2024-09-18"    
                            }
                        }
                    ]
                }
            ]
        }
    ]
}

maximojoBulkRatePush('670', cmCreds, ratesConfig)