# backend/tests/integration/selenium/test_ut_18-3.py
import os
import pytest
from sqlalchemy.orm import Session
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
from app.db.session import SessionLocal
from app.schemas.user import UserCreate
from app.crud.user import create_user, delete_user, get_user_by_username

# Load environment variables from .env file
load_dotenv()

professor_user = os.getenv('TEST_USER')
professor_pass = os.getenv('TEST_PASSWORD')
grad_student_user = "t2_student"
grad_student_cred = "gradstudent3489"
grad_student_email = "t2_student@example.com"
host_ip = os.getenv('HOST_IP')

# Start a new database session
db = SessionLocal()

@pytest.fixture(scope="function")
def setup_grad_student():
    """Fixture to create a graduate student user before the test and delete after."""
    try:
        # Create a new Graduate Student user
        new_user = UserCreate(
            username=grad_student_user,
            password=grad_student_cred,
            email=grad_student_email,
            role_id=2  # Assuming role_id 2 is for GradStudent
        )
        created_user = create_user(db, new_user)
        yield created_user  # Run the test with created_user available

    finally:
        # Clean up: Delete the Graduate Student user after the test
        user = get_user_by_username(db, grad_student_user)
        if user:
            delete_user(db, user.user_id)

@pytest.mark.integration
def test_role_based_access_control(setup_grad_student):
    try:
        # Initialize the WebDriver
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.get(f"http://{host_ip}:3000/")
        driver.maximize_window()

        # Helper function to login
        def login(username, password):
            username_field = driver.find_element(By.NAME, 'username_input')
            password_field = driver.find_element(By.NAME, 'password_input')
            login_button = driver.find_element(By.NAME, 'login_button')
            username_field.send_keys(username)
            password_field.send_keys(password)
            login_button.click()
            # Wait for navbar to confirm login
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='navbar']"))
            )

        # Helper function to search for a keyword
        def search_keyword(keyword):
            search_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='search_input']"))
            )
            search_input.clear()
            search_input.send_keys(keyword)
            search_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='search_button']"))
            )
            search_button.click()
            # Wait for search results to appear
            WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-testid^='evaluation-dropdown']"))
            )

        # Step 1: Graduate Student login, search for "cyber", and check for disabled dropdown
        login(grad_student_user, grad_student_cred)
        search_keyword("cyber")

        # Check if the evaluation dropdown is disabled for Graduate Student
        dropdown = driver.find_element(By.CSS_SELECTOR, "[data-testid^='evaluation-dropdown']")
        assert "opacity-50" in dropdown.get_attribute("class")

        # Log out Graduate Student
        logout_button = driver.find_element(By.CSS_SELECTOR, "[data-testid='logout-button']")
        logout_button.click()

        # Step 2: Professor login, search for "cyber", and check for enabled dropdown
        login(professor_user, professor_pass)
        search_keyword("cyber")

        # Check if the evaluation dropdown is enabled for Professor
        dropdown = driver.find_element(By.CSS_SELECTOR, "[data-testid^='evaluation-dropdown']")
        assert "opacity-50" not in dropdown.get_attribute("class")

        # Optional: Interact with dropdown if needed
        dropdown.click()
        option_accept = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'bg-green-600') and text()='Accept']"))
        )
        option_accept.click()

        # Verify that selection was successful (check for visual state or database change if available)
        assert dropdown.text == "Accept"

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise e

    finally:
        # Close the WebDriver
        driver.quit()