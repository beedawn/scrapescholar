from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By




try:
    # Initialize the WebDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
 
    # Navigate to the login page
    driver.get("http://0.0.0.0:3000/")
    driver.maximize_window()
 
    # Locate and interact with the login elements
    username_field = driver.find_element(By.XPATH, "//input[1]")
    password_field = driver.find_element(By.XPATH, "//input[2]")
    login_button = driver.find_element(By.XPATH, "//button[1]")
 
    # Enter login credentials and submit the form
    username_field.send_keys("")
    password_field.send_keys("")
    login_button.click()
 
    # Handle post-login tasks if necessary
 
except Exception as e:
    print(f"An error occurred: {str(e)}")
 
finally:
    # Close the WebDriver
     
    time.sleep(20)
    print(driver.title)
    print(driver.current_url)   
    driver.quit()