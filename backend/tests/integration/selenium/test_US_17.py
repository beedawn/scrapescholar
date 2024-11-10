from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pytest
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()            

testuser = os.getenv('TEST_USER')
testpass = os.getenv('TEST_PASSWORD')
host_ip = os.getenv('HOST_IP')


#UT-17.1
def test_find_usermanagement_link_us_17():
    try:
        # Initialize the WebDriver
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    
        # Navigate to the login page
        driver.get(f"http://{host_ip}:3000/")
        driver.maximize_window()
    
        # Locate and interact with the login elements
        username_field = driver.find_element(By.NAME, 'username_input')
        password_field = driver.find_element(By.NAME, 'password_input')
        login_button = driver.find_element(By.NAME, 'login_button')
        time.sleep(1)

        # Enter login credentials and submit the form
        username_field.send_keys(testuser)
        password_field.send_keys(testpass)
        login_button.click()

        #await navbar to populate
        initial_page = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='navbar']"))
        )
        settings_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                           "[data-testid='user_settings']")))
        settings_element.click()
        usermanagement_element= WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                                "[data-testid='settings_user_management']")))
        assert driver.get_cookie("access_token") is not None

        assert initial_page is not None
        assert usermanagement_element is not None

    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise e    
    finally:
        # Close the WebDriver
        time.sleep(1)
        # print(driver.title)
        # print(driver.current_url)   
        driver.quit()



        