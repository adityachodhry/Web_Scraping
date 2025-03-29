import json
from Academic_World_Search.Events import academic_world_events
from AIC.Events import AIC_Events
from All_Conference_Alert.Events import ACA 
from Conference_Alerts.Events import CA_Events
from Insider.Events import insider_events
from International_Conference_Alerts.Events import International_Events
from National_Conferences.Events import national_events
from Town_Script.Final_Code import get_townscript_events
from World_Conference.events import World_Conference

def main():

    # Academic World Search
    city = 'Delhi'
    city_code = 'CTXMS'

    academic = academic_world_events(city, city_code)

    if academic:

        with open('Mussoorie_Academic_World_Search_Event_Data.json', 'w', encoding='utf-8') as file:
            json.dump(academic, file, ensure_ascii=False, indent=4)
        print("Academic World Search events extracted and saved!")
    else:
        print("No Academic World Search events found.")

    # ACA 
    events_data = ACA()

    # Save the events data to a JSON file
    with open('ACA_Event_Data.json', 'w', encoding='utf-8') as json_file:
        json.dump(events_data, json_file, ensure_ascii=False, indent=4)

    print("Data Extracted!")

    # AIC
    AIC_Events()

    # Conference_Alerts
    city = 'Delhi'
    city_code = 'CTXMS'
    alerts = CA_Events(city, city_code)

    # print(f"Page {page_no} data extracted!")

    with open('Mussoorie_Conference_Alerts_Event_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(alerts, json_file, indent=2)

    print("Data extraction complete and saved to Mussoorie_Conference_Alerts_Event_data.json!")

    # Insider
    city = 'delhi'
    event_type = 'physical'
    city_code = 'CTXMS'

    insider = insider_events(city, event_type, city_code)

    with open('Mussoorie_Insider_Event_Data.json', 'w') as json_file:
        json.dump(insider, json_file, indent=2)

    # International_Conference
    page_no = 1
    month = 'null'
    topic = 'null'
    subtopic = 'null'
    country = 'India'

    International = International_Events(page_no, month, topic, subtopic, country)

    # Save the extracted data to a JSON file
    with open('Mussoorie_International_Conference_Alerts_Event_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(International, json_file, indent=2)


    # National_Conferences
    place = 'Delhi'
    city_code = 'CTXMS'

    National = national_events(place, city_code)

    # Save data to JSON file
    with open('Mussoorie_National_Conferences_Event_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(National, json_file, ensure_ascii=False, indent=2)

    # Town Script
    city_name = 'delhi'
    city_code = 'CTXMS'
    size = 10
    distance = 100
    page_no = 0

    Town_Script = get_townscript_events(city_name, city_code, size, distance, page_no)

    if Town_Script:
        with open('Mussoorie_Town_Script_Event_Data.json', 'w') as json_file:
            json.dump(Town_Script, json_file, indent=2)
        print('Town Script events extracted and saved!')
    else:
        print('No Town Script events found.')


    # World_Conference
    page_no = 2
    World = World_Conference(page_no)

    with open('Mussoorie_World_Conference_Event_Data.json', 'w', encoding='utf-8') as file:
        json.dump(World, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
