import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# Get user input for username and password
username = input("Enter your username: ")
password = input("Enter your password: ")

# Initialize the WebDriver (Chrome)
driver = webdriver.Chrome()

try:
    url = 'https://apps.djubo.com/sign-in/'

    # Go to the login page
    driver.get(url)

    # Input credentials and submit the form
    driver.find_element(By.NAME, 'email_address').send_keys(username)
    driver.find_element(By.NAME, 'password').send_keys(password)
    driver.find_element(By.CLASS_NAME, 'submitBtn').click()

    # Wait for the login process to complete
    time.sleep(4)

    # Check if the URL changed after login attempt
    if driver.current_url != url:
        print("Login Successful. The Provided Credentials are Correct.")
    else:
        print("Login failed. Please Check Your Username and Password.")

finally:
    # Close the browser in the finally block to ensure it happens even if there's an exception
    if 'driver' in locals():
        driver.quit()
