import pandas as pd
import json
import re

# Read Excel file
excel_file = "D:\\Downloads\\New OTAs Details For Existing Properties.xlsx"  
df = pd.read_excel(excel_file,'Updated')
# print(df)

# Convert DataFrame to JSON
json_file = "output.json"  
df.to_json(json_file, orient="records")

print("Conversion complete. JSON file saved as:", json_file)

# Open the JSON file
with open('output.json', 'r') as json_file:
    # Load JSON data into a Python data structure
    data = json.load(json_file)
    
def extractHotelId_easymytrip(data):
    if data is None or data == "NA":
        return
    d = data.upper()
    # print(d)
    if 'HTTPS://' in d:
        data = d[d.find("EMT"):].split('&')[0]
        if '-' in data:
            return data.split("-")[1]
        else:
            return data.split("=")[1][3:]
    else:
        return None
    
def extractHotelId_cleartrip(data):
    if data is None or data == "NA":
        return
    d = data.upper()
    # print(d)
    if 'HTTPS://' in d:
        return d.split('/')[5].split('?')[0].split('-')[-1]
    else:
        return None
    

def extractHotelId_tripdotcom(data):
    if data is None or data == "NA":
        return None
    d = data.upper()
    if 'HTTPS://' in d:
        parts = d.split('/')
        if len(parts) > 4:
            d = d[d.find("HOTELID"):].split('=')[1]
            return d.split('&')[0]
    return None



def extractHotelId_expedia(data):
    if data is None or data == "NA":
        return None
    d = data.upper()
    if 'HTTPS://' in d:
        parts = d.split('/')
        # print(parts)
        if len(parts) > 3:
            return parts[3].split('-')[-1]
    return None


def extractHotelId_happyeasygo(data):
    if data is None or data == "NA":
        return None
    d = data.upper()
    if 'HTTPS://' in d:
        return d.split('_')[1].split('/')[0]
    return None


def extractHotelId_hotelsdotcom(data):
    if data is None or data == "NA":
        return None
    d = data.upper()
    if 'HTTPS://' in d:
        parts = d.split('/')
        # print(parts)
        if len(parts) > 3:
            return parts[3].split('HO')[1]
    return None

def extractHotelId_hrs(data):
    if data is None or data == "NA":
        return None
    d = data.upper()
    if 'HTTPS://' in d:
        d = d.split('/')
        if len(d) > 3:
            query_params = d[3].split('?')[1]
            for param in query_params.split('&'):
                key, value = param.split('=')
                if key == 'HN':
                    return value
    return None




lst = []
for item in data:

    if item['HotelId'] is not None:
        extracted_data = {'hId': int(item['HotelId']), 'activeOta': []}
        

    # Extract ClearTrip ID
    cleartrip_id = extractHotelId_cleartrip(item['Cleartrip'])
    if cleartrip_id:
        extracted_data['activeOta'].append({"otaId": 5, "otaPId": cleartrip_id})
    
    # Extract EasyMyTrip ID
    easymytrip_id = extractHotelId_easymytrip(item['EaseMyTrip'])
    if easymytrip_id:
        extracted_data['activeOta'].append({"otaId": 6, "otaPId": easymytrip_id})
    
    
    # Extract HappyEasyGo ID
    happyeasygo_id = extractHotelId_happyeasygo(item['Happy Easy Go'])
    if happyeasygo_id:
        extracted_data['activeOta'].append({"otaId": 7, "otaPId": happyeasygo_id})
    
    # Extract HRS ID
    hrs_id = extractHotelId_hrs(item['HRS'])
    if hrs_id:
        extracted_data['activeOta'].append({"otaId": 8, "otaPId": hrs_id})
    
    # Extract Trip.com ID
    tripdotcom_id = extractHotelId_tripdotcom(item['Trip.com'])
    if tripdotcom_id:
        extracted_data['activeOta'].append({"otaId": 9, "otaPId": tripdotcom_id})
    
    
    if any(value is not None for value in extracted_data.values()):
        # Remove None values from extracted_data dictionary
        extracted_data = {key: value for key, value in extracted_data.items() if value is not None}
        lst.append(extracted_data)

with open("mydata.json", "w") as final:
    json.dump(lst, final)



