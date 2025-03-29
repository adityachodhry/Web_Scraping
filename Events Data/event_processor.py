import json
from Academic_World_Search.Events import academic_world_events
from Conference_Alerts.Events import CA_Events
from Insider.Events import insider_events
from International_Conference_Alerts.Events import International_Events
from National_Conferences.Events import national_events
from Town_Script.Final_Code import get_townscript_events
from concurrent.futures import ThreadPoolExecutor

def process_events(data):
    city = data.get('city')
    country = data.get('country')
    city_code = data.get('city_code')

    # Create a thread pool executor
    with ThreadPoolExecutor(max_workers=6) as executor:
        # Submit each event extraction function to the executor
        future_academic = executor.submit(academic_world_events, city, country)
        future_alerts = executor.submit(CA_Events, city, city_code)
        future_insider = executor.submit(insider_events, city.lower(), 'physical', city_code)
        future_international = executor.submit(International_Events, 1, 'null', 'null', 'null', 'India')
        future_national = executor.submit(national_events, city, city_code)
        future_town_script = executor.submit(get_townscript_events, city, city_code, 10, 100, 0)

        # Wait for all tasks to complete
        academic = future_academic.result()
        alerts = future_alerts.result()
        insider = future_insider.result()
        International = future_international.result()
        National = future_national.result()
        Town_Script = future_town_script.result()

    # Save results to JSON files
    if academic:
        with open('Academic_World_Search_Event_Data.json', 'w', encoding='utf-8') as file:
            json.dump(academic, file, ensure_ascii=False, indent=4)
        print("Academic World Search events extracted!")
    else:
        print("No Academic World Search events found.")
    
    with open('Conference_Alerts_Event_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(alerts, json_file, indent=2)
    print("Conference Alerts Data!")

    with open('Insider_Event_Data.json', 'w') as json_file:
        json.dump(insider, json_file, indent=2)
    print("Insider Event Data!")

    with open('International_Conference_Alerts_Event_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(International, json_file, indent=2)
    print("International Conference Data!")

    with open('National_Conferences_Event_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(National, json_file, ensure_ascii=False, indent=2)
    print("National Conferences Data!")

    if Town_Script:
        with open('Town_Script_Event_Data.json', 'w') as json_file:
            json.dump(Town_Script, json_file, indent=2)
        print("Town Script Data!")
    else:
        print('No Town Script events found.')
