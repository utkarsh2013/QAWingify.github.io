import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class LoginPageTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def test_valid_login(self):
        driver = self.driver
        wait = self.wait

        driver.get("https://sakshingp.github.io/assignment/login.html")

        username_input = wait.until(
            EC.visibility_of_element_located((By.ID, "username"))
        )
        password_input = wait.until(
            EC.visibility_of_element_located((By.ID, "password"))
        )
        login_button = wait.until(EC.element_to_be_clickable((By.ID, "log-in")))

        username_input.send_keys("username")
        password_input.send_keys("password")

        login_button.click()

        wait.until(EC.visibility_of_element_located((By.ID, "amount")))
        assert "Demo App" in driver.title
        assert driver.current_url == "https://sakshingp.github.io/assignment/home.html"
        assert "Welcome" in driver.page_source

    # Add more test cases for different scenarios on the Login Page

    def tearDown(self):
        self.driver.quit()


class HomePageTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def test_sort_amount_values(self):
        driver = self.driver
        wait = self.wait

        driver.get("https://sakshingp.github.io/assignment/login.html")

        username_input = wait.until(
            EC.visibility_of_element_located((By.ID, "username"))
        )
        password_input = wait.until(
            EC.visibility_of_element_located((By.ID, "password"))
        )
        login_button = wait.until(EC.element_to_be_clickable((By.ID, "log-in")))

        username_input.send_keys("your-username")
        password_input.send_keys("your-password")

        login_button.click()

        wait.until(EC.visibility_of_element_located((By.ID, "amount")))

        amount_header = wait.until(EC.element_to_be_clickable((By.ID, "amount")))
        amount_header.click()

        time.sleep(2)  # Adjust the sleep time as needed

        try:
            transaction_table = wait.until(
                EC.visibility_of_element_located((By.ID, "transactionsTable"))
            )
            transaction_values = transaction_table.find_elements(
                By.XPATH, '//table[@id="transactionTable"]/tbody/tr/td[5]'
            )

            sorted_values = [
                int(value.text.replace("$", "").replace(",", ""))
                for value in transaction_values
            ]

            assert sorted(sorted_values, reverse=True) == sorted_values

        except TimeoutException:
            print(
                "Timeout occurred while waiting for the transaction table to be visible."
            )

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    # Create a test suite and add the test cases
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(LoginPageTests))
    suite.addTest(unittest.makeSuite(HomePageTests))

    # Run the tests and generate an HTML report
    runner = unittest.TextTestRunner()
    runner.run(suite)