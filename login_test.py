import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class LoginPageTest(unittest.TestCase):
    def setUp(self):
        # Set up Chrome WebDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.get("http://localhost:5000/login")  # Replace with your actual URL

    def tearDown(self):
        self.driver.quit()

    def test_page_title(self):
        self.assertEqual(self.driver.title, "Login")

    def test_google_login_button(self):
        google_button = self.driver.find_element(By.CLASS_NAME, "gbutton")
        self.assertTrue(google_button.is_displayed())
        self.assertIn("Continue with Google".lower(), google_button.text.lower())

    def test_email_input(self):
        email_input = self.driver.find_element(By.ID, "email")
        self.assertTrue(email_input.is_displayed())
        self.assertEqual(email_input.get_attribute("placeholder"), "Enter a valid email address")

    def test_password_input(self):
        password_input = self.driver.find_element(By.ID, "password")
        self.assertTrue(password_input.is_displayed())
        self.assertEqual(password_input.get_attribute("placeholder"), "Enter password")

    def test_login_button(self):
        login_button = self.driver.find_element(By.ID, "submit")
        self.assertTrue(login_button.is_displayed())
        self.assertEqual(login_button.text.lower(), "login")

    def test_forgot_password_link(self):
        forgot_password_link = self.driver.find_element(By.XPATH, "//a[text()='Forgot password?']")
        self.assertTrue(forgot_password_link.is_displayed())
        self.assertEqual(forgot_password_link.get_attribute("href"), "http://localhost:5000/request-password-reset")

    def test_register_link(self):
        register_link = self.driver.find_element(By.XPATH, "//a[text()='Register']")
        self.assertTrue(register_link.is_displayed())
        self.assertEqual(register_link.get_attribute("href"), "http://localhost:5000/register")

    def test_login_form_submission(self):
        email_input = self.driver.find_element(By.ID, "email")
        password_input = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.ID, "submit")

        email_input.send_keys("chrisdepallan@gmail.com")
        password_input.send_keys("#Chris007")
        login_button.click()

        # Wait for the page to load after submission
        # You may need to adjust this based on your application's behavior
        WebDriverWait(self.driver, 10).until(
            EC.url_changes("http://localhost:5000/login")
        )

        # Add assertions to check if login was successful
        # For example, check if the URL changed to a dashboard page
        self.assertNotEqual(self.driver.current_url, "http://localhost:5000/login")

if __name__ == "__main__":
    unittest.main()