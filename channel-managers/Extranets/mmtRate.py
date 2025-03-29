import time
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def mmtCurrentRate():
    # Initialize the WebDriver
    driver = webdriver.Chrome()
    mmtUrl = 'https://www.makemytrip.com/hotels/'
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

mmtCurrentRate()
