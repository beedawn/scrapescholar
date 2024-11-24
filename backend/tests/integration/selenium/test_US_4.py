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

        username_field = driver.find_element(By.NAME, 'username_input')
        password_field = driver.find_element(By.NAME, 'password_input')
        login_button = driver.find_element(By.NAME, 'login_button')
        time.sleep(1)

        username_field.send_keys(testuser)
        password_field.send_keys(testpass)
        login_button.click()

        initial_page = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='navbar']"))
        )

        assert driver.get_cookie("access_token") is not None
        assert initial_page is not None

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise e

    finally:
        time.sleep(1)
        driver.quit()


def test_logout_us_4_delete_cookie():
    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

        driver.get(f"http://{host_ip}:3000/")
        driver.maximize_window()

        username_field = driver.find_element(By.NAME, 'username_input')
        password_field = driver.find_element(By.NAME, 'password_input')
        login_button = driver.find_element(By.NAME, 'login_button')
        time.sleep(1)

        username_field.send_keys(testuser)
        password_field.send_keys(testpass)
        login_button.click()

        initial_page = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='navbar']"))
        )

        assert driver.get_cookie("access_token") is not None

        assert initial_page is not None

        logout_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='logout-button']"))
        )
        logout_button.click()
        time.sleep(1)
        assert driver.get_cookie("access_token") is None

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise e
    finally:
        time.sleep(1)
        driver.quit()
