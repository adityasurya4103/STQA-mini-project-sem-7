from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import mysql.connector
from datetime import datetime

# Database connection
def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",      # XAMPP default host
            user="root",           # Default user is 'root' (lowercase)
            password="",           # Leave empty if you haven't set a password in XAMPP
            database="selenium_tests"  # Replace with your actual database name
        )
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

# Store result in the database
def store_result(test_case_name, result):
    connection = connect_db()
    if connection is None:
        print("Failed to connect to the database. Skipping result storage.")
        return  # Skip storing the result if connection failed

    try:
        cursor = connection.cursor()
        query = "INSERT INTO test_cases (test_case_name, result, execution_time) VALUES (%s, %s, %s)"
        cursor.execute(query, (test_case_name, result, datetime.now()))
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error storing result: {err}")
    finally:
        cursor.close()
        connection.close()

# Test case: Google Search
def test_google_search(driver):
    test_case_name = "Test Google Search"
    result = "Fail"  # Default result

    try:
        driver.get("https://www.google.com")

        # Wait until the search box is visible and interactable
        search_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "q"))
        )
        search_box.click()  # Click to ensure it's focused before typing
        search_box.send_keys("omkar naiknavare ")

        # Wait for the search button to be clickable
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "btnK"))
        )
        search_button.click()

        # Check if the title contains "Selenium"
        if "Selenium" in driver.title:
            result = "Pass"
    except Exception as e:
        print(f"Error during {test_case_name}: {e}")
    finally:
        # Store the result in the database
        store_result(test_case_name, result)

# Test case: Check YouTube
def test_youtube(driver):
    test_case_name = "Test YouTube"
    result = "Fail"  # Default result

    try:
        driver.get("https://www.youtube.com")
        
        # Wait until the search box is visible and interactable
        search_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "search_query"))
        )
        search_box.send_keys("Selenium WebDriver")
        search_box.submit()

        # Check if the title contains "Selenium"
        if "Selenium" in driver.title:
            result = "Pass"
    except Exception as e:
        print(f"Error during {test_case_name}: {e}")
    finally:
        # Store the result in the database
        store_result(test_case_name, result)

# Test case: Check Wikipedia
def test_wikipedia(driver):
    test_case_name = "Test Wikipedia"
    result = "Fail"  # Default result

    try:
        driver.get("https://www.wikipedia.org")
        
        # Wait until the search box is visible and interactable
        search_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "search"))
        )
        search_box.send_keys("Selenium (software)")
        search_box.submit()

        # Check if the title contains "Selenium"
        if "Selenium" in driver.title:
            result = "Pass"
    except Exception as e:
        print(f"Error during {test_case_name}: {e}")
    finally:
        # Store the result in the database
        store_result(test_case_name, result)
        
def test_covid_info(driver):
    test_case_name = "Test COVID-19 Information"
    result = "Fail"  # Default result

    try:
        driver.get("https://www.who.int/emergencies/diseases/novel-coronavirus-2019")

        # Check if the title contains "COVID-19"
        if "COVID-19" in driver.title:
            result = "Pass"
    except Exception as e:
        print(f"Error during {test_case_name}: {e}")
    finally:
        # Store the result in the database
        store_result(test_case_name, result)
def test_instagram_login(driver):
    test_case_name = "Test Instagram Login"
    result = "Fail"  # Default result

    try:
        driver.get("https://www.instagram.com/accounts/login/")

        # Wait for the username field to be visible and fill in the username
        username_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "username"))
        )
        username_input.send_keys("username")  # Replace with your Instagram username

        # Fill in the password
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys("password")  # Replace with your Instagram password

        # Click the login button
        login_button = driver.xpath("//button[@type='submit']")
        login_button.click()

        # Wait for the profile icon to be visible after login (or any other element that indicates successful login)
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//a[@href='/your_username/']"))  # Adjust based on your username
        )

        result = "Pass"
    except Exception as e:
        print(f"Error during {test_case_name}: {e}")
    finally:
        # Store the result in the database
        store_result(test_case_name, result)




def test_registration_login_comment(driver):
    test_case_name = "Test Registration, Login, and Comment"
    result = "Fail"  # Default result

    try:
        # Step 1: Registration
        driver.get("http://localhost/covid19_website/")

        # Wait for the registration form to be visible
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//section[@id='registration']//form"))
        )

        # Fill in the registration form with a delay for realism
        username_input = driver.find_element(By.NAME, "username")
        email_input = driver.find_element(By.NAME, "email")
        password_input = driver.find_element(By.NAME, "password")

        for char in "testuser":
            username_input.send_keys(char)
            time.sleep(0.1)  # Simulating typing delay

        for char in "testuser@example.com":
            email_input.send_keys(char)
            time.sleep(0.1)

        for char in "TestPassword123":
            password_input.send_keys(char)
            time.sleep(0.1)

        # Submit the registration form
        driver.find_element(By.XPATH, "//section[@id='registration']//button").click()

        # Wait for registration success message
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Registration successful')]"))
        )

        # Step 2: Login
        driver.get("http://localhost/covid19_website/")

        # Wait for the login form to be visible
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//section[@id='login']//form"))
        )

        # Fill in the login form with a delay for realism
        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")

        for char in "testuser":
            username_input.send_keys(char)
            time.sleep(0.1)  # Simulating typing delay

        for char in "TestPassword123":
            password_input.send_keys(char)
            time.sleep(0.1)

        # Submit the login form
        driver.find_element(By.XPATH, "//section[@id='login']//button").click()

        # Wait for login success message or redirection
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Login successful')]"))
        )

        # Step 3: Comment Submission
        driver.get("http://localhost/covid19_website/")

        # Wait for the comment form to be visible
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//section[@id='comments']//form"))
        )

        # Fill in the comment form with a delay for realism
        comment_input = driver.find_element(By.NAME, "comment")
        for char in "This is a test comment!":
            comment_input.send_keys(char)
            time.sleep(0.1)  # Simulating typing delay

        # Submit the comment form
        driver.find_element(By.XPATH, "//section[@id='comments']//button").click()

        # Wait for the comment to be displayed
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'This is a test comment!')]"))
        )

        result = "Pass"

    except Exception as e:
        print(f"Error during {test_case_name}: {e}")
    finally:
        # Store the result in the database
        store_result(test_case_name, result)








def main():
    # Update the path to your ChromeDriver
    service = Service("C:/Users/omkar/OneDrive/Desktop/selenium_automation_project/lib/chromedriver-win64/chromedriver.exe")  # Updated path
    driver = webdriver.Chrome(service=service)
    try:
        test_google_search(driver)
        test_youtube(driver)
        test_wikipedia(driver)
        test_covid_info(driver)  # Add the COVID-19 test case
        test_instagram_login(driver)
        test_registration_login_comment(driver)
      
    finally:
        driver.quit()




if __name__ == "__main__":
    main()
