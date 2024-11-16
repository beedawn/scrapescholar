# backend/tests/integration/selenium/test_ut_18-2.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
from dotenv import load_dotenv
import time
import pytest

# Load environment variables from .env file
load_dotenv()

# Test credentials for Professor/Admin
professor_user = os.getenv('TEST_USER')
professor_pass = os.getenv('TEST_PASSWORD')
host_ip = os.getenv('HOST_IP')

@pytest.mark.integration
def test_view_user_roles_and_permissions():
    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.get(f"http://{host_ip}:3000/")
        driver.maximize_window()


        username_field = driver.find_element(By.NAME, 'username_input')
        password_field = driver.find_element(By.NAME, 'password_input')
        login_button = driver.find_element(By.NAME, 'login_button')
        time.sleep(1)

        username_field.send_keys(professor_user)
        password_field.send_keys(professor_pass)
        login_button.click()


        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='navbar']"))
        )

        settings_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='user_settings']"))
        )
        settings_element.click()

        user_management_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='settings_user_management']"))
        )
        user_management_element.click()

        roles_displayed = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-testid='user_role']"))
        )
        assert roles_displayed is not None
        for role in roles_displayed:
            assert ("Professor" or "Student" or "GradStudent") in role.text
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise e
    finally:
        time.sleep(1)
        driver.quit()