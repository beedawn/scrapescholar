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
        username_field.send_keys(professor_user)
        password_field.send_keys(professor_pass)
        login_button.click()

        # Wait for navbar to populate after login
        navbar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='navbar']"))
        )

        # Navigate to the user management section
        settings_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='user_settings']"))
        )
        settings_element.click()

        user_management_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='settings_user_management']"))
        )
        user_management_element.click()

        # Check if the roles and permissions of each user are displayed
        roles_displayed = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-testid='user_role_text']"))
        )
        permissions_displayed = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-testid='user_permissions_text']"))
        )


        # Verify that roles and permissions are displayed correctly
        assert roles_displayed is not None
        assert permissions_displayed is not None

        # Additional checks to verify specific roles and permissions can be added here
        for role in roles_displayed:
            assert role.text in ["Professor", "GradStudent", "Student"]

        for permission in permissions_displayed:
            assert "Permission" in permission.text  # Example check for permissions content

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise e
    finally:
        # Close the WebDriver
        time.sleep(1)
        driver.quit()