import time
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def exelyReservation(username, password):

    driver = webdriver.Chrome()
    login_url = 'https://secure.exely.com/secure/Enter.aspx'
    driver.get(login_url)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="username"]')))
    driver.find_element(By.CSS_SELECTOR, 'input[name="username"]').send_keys(username)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
    driver.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys(password)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn.btn-md.btn-primary')))
    driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-md.btn-primary').click()

    time.sleep(5)  
    if "Invalid username or password" in driver.page_source:
        print("Login Unsuccessful")
        driver.quit()
        return
    else:
        print("Login Successful")

    driver.quit()

exelyReservation('TL-503098-REV', 'NEST@786*1263')
