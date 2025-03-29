import time
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Run the script with CLI options')
    parser.add_argument('--username', required=True)
    parser.add_argument('--password', required=True)
    return parser.parse_args()

# Get command-line arguments
args = parse_args()

# List of accounts with Property Code, Username, and Password
accounts = [{'username': args.username, 'password': args.password}]

# Initialize the driver
driver = webdriver.Chrome()

try:
    for account in accounts:
        username = account['username']
        password = account['password']

        url = 'https://www.eglobe-solutions.com/hms/dashboard'

        # Go to the login page
        driver.get(url)
        time.sleep(4)

        # Input credentials and submit the form
        driver.find_element(By.NAME, 'Username').send_keys(username)
        driver.find_element(By.NAME, 'Password').send_keys(password)
    
        # Click on the button (assuming this is what btnER does)
        driver.find_element(By.NAME, 'button').click()

        # Wait for the button click to take effect
        time.sleep(2)

        # Check if login was successful
        if "Invalid username or password" in driver.page_source:
            print("Login Unsuccessful")
        else:
            print("Login Successful")

except Exception as e:
    print("An error occurred:", e)

finally:
    # Close the browser window
    driver.quit()
