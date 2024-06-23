from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
import csv
import datetime

# Set up headless Firefox browser
firefox_options = Options()
firefox_options.headless = True
driver = webdriver.Firefox(options=firefox_options)
driver.maximize_window()
driver.get(url='http://www.saucedemo.com/')

def log_result(test_case, status, details):
    with open('My_Test_Results.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([test_case, status, details, datetime.datetime.now()])

# Define LoginPage class
class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def login(self, username, password):
        self.driver.find_element(By.ID, 'user-name').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.ID, 'login-button').click()

# Define AddToCart class
class AddToCart:
    def __init__(self, driver):
        self.driver = driver

    def addItemToCart(self):
        # Get item name from product page
        item_name_in_product_page = self.driver.find_element(By.XPATH, '//*[@id="item_4_title_link"]/div').text
        print(f'Item name description on product page: {item_name_in_product_page}')

        # Add item to the cart
        self.driver.find_element(By.ID, 'add-to-cart-sauce-labs-backpack').click()
        self.driver.find_element(By.XPATH, '//*[@id="shopping_cart_container"]/a').click()

        # Get item description from the cart page
        item_name_in_cart = self.driver.find_element(By.XPATH, '//*[@id="item_4_title_link"]/div').text
        print(f'Item name description in cart: {item_name_in_cart}')

        if item_name_in_product_page == item_name_in_cart:
            print('Correct item is added to the cart')
        else:
            print('Wrong item is added to the cart')

# Define CheckOut class
class CheckOut:
    def __init__(self, driver):
        self.driver = driver

    def checkoutProcess(self, first_name, last_name, postal_code):
        time.sleep(5)
        self.driver.find_element(By.ID, 'checkout').click()

        self.driver.find_element(By.ID, 'first-name').send_keys(first_name)
        self.driver.find_element(By.ID, 'last-name').send_keys(last_name)
        self.driver.find_element(By.ID, 'postal-code').send_keys(postal_code)
        self.driver.find_element(By.ID, 'continue').click()

# Define checkOutOverview class
class checkOutOverview:
    def __init__(self, driver):
        self.driver = driver
    
    def payment(self):
        self.driver.find_element(By.ID, 'finish').click()

# Test the script
try:
    # Perform login
    log_in = LoginPage(driver)
    log_in.login('standard_user', 'secret_sauce')
    log_result('Login Test', 'Passed', 'Login successful')
except Exception as e:
    log_result('Login Test', 'Failed', str(e))

try:
    # Add product to cart
    addProductInCart = AddToCart(driver)
    addProductInCart.addItemToCart()
    log_result('Add Item to Cart Test', 'Passed', 'Item added successfully to the cart')
except Exception as e:
    log_result('Add Item to Cart Test', 'Failed', str(e))

try:
    # Perform checkout process
    checkOutPage = CheckOut(driver)
    checkOutPage.checkoutProcess('Meta', 'Mothapo', '8080')
    log_result('Checkout Test', 'Passed', 'Checkout successful')
except Exception as e:
    log_result('Checkout Test', 'Failed', str(e))

try:
    # Finish the process
    FinishPage = checkOutOverview(driver)
    FinishPage.payment()
    log_result('Payment Test', 'Passed', 'Payment done successfully')
except Exception as e:
    log_result('Payment Test', 'Failed', str(e))

# Close the browser
time.sleep(3)
driver.quit()
