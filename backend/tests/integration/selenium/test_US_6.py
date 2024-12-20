from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os
from dotenv import load_dotenv
from tests.integration.tools.get_cookie import get_cookie
from app.crud.search import get_search_by_title, delete_search
from app.crud.user_data import delete_user_data_by_article
from app.crud.article import get_article_by_search_id, delete_article
from app.db.session import SessionLocal

load_dotenv()

testuser = os.getenv('TEST_USER')
testpass = os.getenv('TEST_PASSWORD')
host_ip = os.getenv('HOST_IP')

session = get_cookie()
db = SessionLocal()

# UT-6.1
def test_find_graph():
    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.get(f"http://{host_ip}:3000/")
        driver.maximize_window()

        username_field = driver.find_element(By.NAME, 'username_input')
        password_field = driver.find_element(By.NAME, 'password_input')
        login_button = driver.find_element(By.NAME, 'login_button')
        time.sleep(5)

        username_field.send_keys(testuser)
        password_field.send_keys(testpass)
        login_button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='navbar']"))
        )
        search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                       "[data-testid='search_input']")))

        search_input.send_keys("test")
        search_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                        "[data-testid='search_button']")))
        search_button.click()
        time.sleep(20)
        bubble_plot = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "bubbleplot")))

        assert bubble_plot is not None
        search_title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                       "[data-testid='search-title-span']")))
        clean_up(search_title)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise e
    finally:
        time.sleep(1)
        driver.quit()


# UT-6.2
def test_graph_loads_zero():
    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.get(f"http://{host_ip}:3000/")
        driver.maximize_window()

        username_field = driver.find_element(By.NAME, 'username_input')
        password_field = driver.find_element(By.NAME, 'password_input')
        login_button = driver.find_element(By.NAME, 'login_button')
        time.sleep(20)

        username_field.send_keys(testuser)
        password_field.send_keys(testpass)
        login_button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='navbar']"))
        )
        search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                       "[data-testid='search_input']")))

        search_input.send_keys("test")
        search_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                        "[data-testid='search_button']")))
        search_button.click()
        time.sleep(20)
        bubble_plot = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@data-testid='bubble_plot' and .//text()[contains(., 'Relevant 0')]]"))
        )

        assert bubble_plot is not None
        search_title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                       "[data-testid='search-title-span']")))
        clean_up(search_title)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise e
    finally:
        time.sleep(1)
        driver.quit()


#UT-6.3
def test_graph_accuracy_after_change():
    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.get(f"http://{host_ip}:3000/")
        driver.maximize_window()

        username_field = driver.find_element(By.NAME, 'username_input')
        password_field = driver.find_element(By.NAME, 'password_input')
        login_button = driver.find_element(By.NAME, 'login_button')

        username_field.send_keys(testuser)
        password_field.send_keys(testpass)
        login_button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='navbar']"))
        )
        search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                       "[data-testid='search_input']")))

        search_input.send_keys("test")
        search_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                        "[data-testid='search_button']")))
        search_button.click()

        time.sleep(20)
        relevancy = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                    "[data-testid='relevancy-column-default']")))
        relevancy.click()

        relevant_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class, 'bg-green-600') and contains(@class, 'p-2') and text()='Relevant']"))
        )
        relevant_div.click()

        bubble_plot = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@data-testid='bubble_plot' and .//text()[contains(., 'Relevant 1')]]"))
        )

        assert bubble_plot is not None
        search_title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                       "[data-testid='search-title-span']")))

        clean_up(search_title)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise e
    finally:
        time.sleep(1)
        driver.quit()


def clean_up(search_title):
    found_search = get_search_by_title(db, search_title.text)
    articles = get_article_by_search_id(db, found_search.search_id)
    for article in articles:
        delete_user_data_by_article(db, article.article_id)
        delete_article(db, article.article_id)
    delete_search(db, found_search.search_id)
