import json
from pymongo import MongoClient
import time
from datetime import datetime, timedelta
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def mmtRate(hId):
    client = MongoClient("mongodb+srv://Retvens:JMdZt2hEPsqHuVQl@r-rate-shopper-cluster.nlstcxk.mongodb.net/")
    db = client['ratex']
    collection = db['verifiedproperties']
    properties = collection.find({'hId': hId})

    # Get current date
    current_date = datetime.now().strftime("%m%d%Y")
    check_out_date = (datetime.now() + timedelta(days=1)).strftime("%m%d%Y")

    for property in properties:
        activeOtas = property.get('activeOta')
        for ota in activeOtas:
            otaPId = ota.get("otaPId")
            otaId = ota.get("otaId")
            if otaId == 1:
                
                driver = webdriver.Chrome()
                link = f"https://www.makemytrip.com/hotels/hotel-details/?hotelId={otaPId}&checkin={current_date}&checkout={check_out_date}&city=CTUDR"
                print(link)
                driver.get(mmtUrl)
                
                # Wait for the page to load
                time.sleep(2)
                
                try:
                    # Wait for the popup to appear and attempt to close it
                    WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, "section[data-cy='CommonModal_2']"))
                    )
                    close_button = driver.find_element(By.CSS_SELECTOR, "span[data-cy='closeModal']")
                    close_button.click()
                    print("Popup closed successfully.")
                except Exception as e:
                    print("Popup not found or already closed.", e)
                
                driver.quit()

            else:
                print("No link generated for this OTA ID.")

mmtRate(259489)