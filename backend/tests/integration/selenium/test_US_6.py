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


# UT-6.1
def test_find_graph():
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

        # await navbar to populate
        initial_page = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='navbar']"))
        )
        search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                           "[data-test-id='search_input']")))

        search_input.send_keys("test")
        search_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                                 "[data-test-id='search_button']")))
        search_button.click()

        bubble_plot = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                        "[data-test-id='bubble_plot']")))


        assert bubble_plot is not None


    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise e
    finally:
        # Close the WebDriver
        time.sleep(1)
        # print(driver.title)
        # print(driver.current_url)
        driver.quit()




# UT-6.2
def test_graph_loads_zero():
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

        # await navbar to populate
        initial_page = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='navbar']"))
        )
        search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                           "[data-test-id='search_input']")))

        search_input.send_keys("test")
        search_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                                 "[data-test-id='search_button']")))
        search_button.click()



        relevancy = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                        "[data-test-id='relevancy-column-default']")))
        relevancy.click()

        relevant_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class, 'bg-green-600') and contains(@class, 'p-2') and text()='Relevant']"))
        )
        relevant_div.click()

        bubble_plot = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@data-test-id='bubble_plot' and .//text()[contains(., 'Relevant 0')]]"))
        )

        assert bubble_plot is not None


    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise e
    finally:
        # Close the WebDriver
        time.sleep(1)
        # print(driver.title)
        # print(driver.current_url)
        driver.quit()


#UT-6.3
def test_graph_accuracy_after_change():
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

        # await navbar to populate
        initial_page = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='navbar']"))
        )
        search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                           "[data-test-id='search_input']")))

        search_input.send_keys("test")
        search_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                                 "[data-test-id='search_button']")))
        search_button.click()



        relevancy = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                        "[data-test-id='relevancy-column-default']")))
        relevancy.click()

        relevant_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class, 'bg-green-600') and contains(@class, 'p-2') and text()='Relevant']"))
        )
        relevant_div.click()

        bubble_plot = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@data-test-id='bubble_plot' and .//text()[contains(., 'Relevant 1')]]"))
        )

        assert bubble_plot is not None


    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise e
    finally:
        # Close the WebDriver
        time.sleep(1)
        # print(driver.title)
        # print(driver.current_url)
        driver.quit()

