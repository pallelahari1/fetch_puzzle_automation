from unittest import TestCase
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class FakeGoldBar(TestCase):
    # Automatically download and use the latest ChromeDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    def verify_page_loaded(self):
        # Navigate to the website
        self.driver.get("http://sdetchallenge.fetch.com/")

        # Get the title of the page
        title = self.driver.title
        # Verify the title
        expected_title = "React App"
        # Verify if the title of page is as expected
        self.assertEqual(title, expected_title)

        # Verify that page is loaded
        # Element definition
        react_page = self.driver.find_element(By.XPATH, '//div[@class="game"]')
        if react_page.is_displayed():
            print("Page is successfully loaded")
        else:
            print("Page is not loaded")
            exit(1)

    def get_fake_bar(self):

        # Element definition
        bars_buttons = self.driver.find_elements(By.XPATH, '//div[@class="coins"]//button')
        weigh_button = self.driver.find_element(By.XPATH, '//button[@id="weigh"]')
        reset_button = self.driver.find_element(By.XPATH, '//button[text()="Reset"]')
        result_field = self.driver.find_element(By.XPATH, '//div[@class="result"]//button[@id="reset"]')

        # list of gold bar numbers displayed
        gold_bar_numbers = []
        for numbers in bars_buttons:
            gold_bar_numbers.append(numbers.text)

        # Splitting the list if gold bar numbers into 3 sets [0,1,2], [3,4,5], [6,7,8]

        # Entering the first set of values in left row
        self.driver.find_element(By.XPATH, '//div[@class="board-row"]//input[@id="left_0"]').send_keys(
            gold_bar_numbers[0])
        self.driver.find_element(By.XPATH, '//div[@class="board-row"]//input[@id="left_1"]').send_keys(
            gold_bar_numbers[1])
        self.driver.find_element(By.XPATH, '//div[@class="board-row"]//input[@id="left_2"]').send_keys(
            gold_bar_numbers[2])

        # Entering the second set of values in right row
        self.driver.find_element(By.XPATH, '//div[@class="board-row"]//input[@id="right_0"]').send_keys(
            gold_bar_numbers[3])
        self.driver.find_element(By.XPATH, '//div[@class="board-row"]//input[@id="right_1"]').send_keys(
            gold_bar_numbers[4])
        self.driver.find_element(By.XPATH, '//div[@class="board-row"]//input[@id="right_2"]').send_keys(
            gold_bar_numbers[5])

        # click on weigh button
        weigh_button.click()

        # Wait until the weighing list is displayed
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="game-info"]//li')))

        # If left bowl is greater than right bowl - then it means  numbers in right bowl bars has fake bar
        if result_field.text == '>':
            # Numbers entered in right row has fake bar
            gold_bar_numbers = gold_bar_numbers[slice(3, 6)]
            print("One of the following gold bars is a fake one:")
            print(gold_bar_numbers, sep=", ")

        # If left bowl is less than right bowl - then it means left bowl bars has fake bar
        if result_field.text == '<':
            # Numbers entered in left row has fake bar
            gold_bar_numbers = gold_bar_numbers[slice(0, 3)]
            print("One of the following gold bars is a  fake one:")
            print(gold_bar_numbers, sep=", ")

        # If left bowl is equal right bowl one - then it means third set has fake bar
        if result_field.text == '=':
            gold_bar_numbers = gold_bar_numbers[slice(6, 9)]
            print("One of the following gold bars is a fake one:")
            print(* gold_bar_numbers, sep=", ")

        # click on reset button
        reset_button.click()

        # From the above list - Enter first number on left bowl
        self.driver.find_element(By.XPATH, '//div[@class="board-row"]//input[@id="left_0"]').send_keys(
            gold_bar_numbers[0])

        # From the above list - Enter second number on right bowl
        self.driver.find_element(By.XPATH, '//div[@class="board-row"]//input[@id="right_0"]').send_keys(
            gold_bar_numbers[1])

        # click on weigh button
        weigh_button.click()

        # Wait until the weighing list is displayed
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="game-info"]//li[2]')))

        # If left bowl is greater than right bowl - then it means number in right bowl is fake bar
        if result_field.text == '>':
            gold_bar_numbers = gold_bar_numbers[1]
            print("Expected Fake bar number is:" + gold_bar_numbers)

        # If left bowl is less than right bowl - then it means number in left bowl is fake bar
        if result_field.text == '<':
            gold_bar_numbers = gold_bar_numbers[0]
            print("Expected Fake bar number is:" + gold_bar_numbers)

        # If left bowl is equal right bowl - then it means number in third number in the list is fake bar
        if result_field.text == '=':
            gold_bar_numbers = gold_bar_numbers[2]
            print("Expected Fake bar number is:" + gold_bar_numbers)

        # Get the list of Weighings
        weighing_list = self.driver.find_elements(By.XPATH, '//div[@class="game-info"]//li')
        print("The list of weighings are:")
        for weights in weighing_list:
            print(weights.text)

        # Click on the fake bar number
        self.driver.find_element(By.XPATH, f'//div[@class="coins"]//button[text()="' + gold_bar_numbers + '"]').click()

        # create alert object
        alert = Alert(self.driver)
        # Validate if fake gold bar was found
        if alert.text == "Yay! You find it!":
            print(alert.text)
            print("Successfully Found the fake gold bar! " + gold_bar_numbers)
        elif alert.text == 'Oops! Try Again!':
            print(alert.text)
            print("Failed to find the fake gold bar!")

    def close(self):
        # Close the browser
        self.driver.quit()


if __name__ == "__main__":
    FakeGoldBar().verify_page_loaded()
    FakeGoldBar().get_fake_bar()
    FakeGoldBar().close()

