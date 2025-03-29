import requests
import json

def maximojoRatePush(propertyCode, cmCreds, ratesConfig):

    username = cmCreds.get('username')
    password = cmCreds.get('password')
    
    session = requests.Session()

    for config in ratesConfig.get('info', []):
        rateTypeId = config.get('rateTypeId')
        channelCode = config.get('channelCode')
        
        for room in config.get('roomInfo', []):
            roomId = room.get('roomId')
            
            for roomPlan in room.get('roomPlanInfo', []):
                roomPlanDetails = roomPlan.get('roomPlan', {})
                occupancyId = roomPlan.get('occupancyId')
                roomPlanId = roomPlan.get('roomPlanId')
                occupancyIdRate = roomPlan.get('occupancyIdRate')
                perExtraPerson = roomPlan.get('perExtraPerson')
                extraPerson = roomPlan.get('extraPerson')
                extraPersonRate = roomPlan.get('extraPersonRate')
                extraChildren = roomPlan.get('extraChildren')
                extraChildrenRate = roomPlan.get('extraChildrenRate')
                rate = roomPlanDetails.get('rate')
                date = roomPlanDetails.get('date')

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
                    "startDate": date,
                    "endDate": date
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
        rateTypeId = config.get('rateTypeId')
        channelCode = config.get('channelCode')
        
        for room in config.get('roomInfo', []):
            roomId = room.get('roomId')
            
            for roomPlan in room.get('roomPlanInfo', []):
                roomPlanDetails = roomPlan.get('roomPlan', {})
                occupancyId = roomPlan.get('occupancyId')
                occupancyIdRate = roomPlan.get('occupancyIdRate')
                perExtraPerson = roomPlan.get('perExtraPerson')
                extraPerson = roomPlan.get('extraPerson')
                extraPersonRate = roomPlan.get('extraPersonRate')
                extraChildren = roomPlan.get('extraChildren')
                extraChildrenRate = roomPlan.get('extraChildrenRate')
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

                            if availability == '':
                                availability = existing_availability

                            if occupancyId == '' or not isinstance(occupancy, dict):
                                occupancyId = existing_per_occupancy
                            else:
                                for key, value in existing_per_occupancy.items():
                                    if key not in occupancyId or occupancyId[key] == '':
                                        occupancyId[key] = value

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
                                "PerOccupancy": existing_per_occupancy,  
                                "ExtraPerson": existing_extra_person,  
                                "ExtraChildren": existing_extra_children 
                            }

                            if occupancyId:
                                room_rate["PerOccupancy"][occupancyId] = rate

                            if extraPersonId:
                                room_rate["ExtraPerson"][extraPersonId] = rate

                            if extraChildrenId:
                                room_rate["ExtraChildren"][extraChildrenId] = rate

                rate_push_url = "https://api.platform.maximojo.com/mantrasv5.svc/BulkUpdateRateCalendarTask"
                body = {
                    "hotelId": propertyCode,
                    "bulkRateItems": [
                        {
                            "BulkRates": [
                                {
                                    "RoomTypes": [roomId],
                                    "RatePlans": [roomPlanId],
                                    "Availability": availability,
                                    "RoomRate": room_rate,
                                    "perExtraPerson": perExtraPerson
                                }
                            ],
                            "DateRanges": [
                                {
                                    "Start": f'{startDate}T00:00:00.000Z',
                                    "End": f'{endDate}T00:00:00.000Z'
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