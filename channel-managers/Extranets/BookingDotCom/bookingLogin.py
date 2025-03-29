import time
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def bookingLogin(username, password):
    driver = webdriver.Chrome()
    login_url = 'https://admin.booking.com/'
    driver.get(login_url)

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="loginname"]')))
    driver.find_element(By.CSS_SELECTOR, 'input[name="loginname"]').send_keys(username)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-dv-event-id="1"]')))
    driver.find_element(By.CSS_SELECTOR, 'button[data-dv-event-id="1"]').click()

    password_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
    
    driver.execute_script("arguments[0].scrollIntoView();", password_field)

    password_field.click()
    
    password_field.send_keys(password)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-dv-event-id="10"]')))
    driver.find_element(By.CSS_SELECTOR, 'button[data-dv-event-id="10"]').click()

    time.sleep(5)  
    if "Invalid username or password" in driver.page_source:
        print("Login Unsuccessful")
    else:
        print("Login Successful")

    driver.quit()

bookingLogin('Retvensnew', 'October@2024')