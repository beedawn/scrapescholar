from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import os
from dotenv import load_dotenv

load_dotenv()
testuser = os.getenv('TEST_USER')
testpass = os.getenv('TEST_PASSWORD')
host_ip = os.getenv('HOST_IP')


#UT-4.5
def test_login_us_4():
    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.get(f"http://{host_ip}:3000/")
        driver.maximize_window()
        azure_button = driver.find_element(By.NAME, 'azure_button')
        azure_button.click()
        time.sleep(5)

        first_input = driver.find_element("css selector", "input")
        first_input.send_keys(f"{testuser}@{testuser}.com")

        submit_button = driver.find_element("id", "idSIButton9")
        submit_button.click()
        time.sleep(5)


        password_input = driver.find_element("id", "i0118")
        password_input.send_keys(testpass)

        password_button =driver.find_element("id","idSIButton9")
        password_button.click()
        time.sleep(5)

        assert driver.get_cookie("access_token") is None
        driver.back()
        assert driver.get_cookie("access_token") is None
        driver.back()
        assert driver.get_cookie("access_token") is None
        driver.back()
        assert driver.get_cookie("access_token") is None

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise e

    finally:
        time.sleep(1)
        driver.quit()

