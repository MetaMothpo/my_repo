import csv
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import time
# Configure the WebDriver
firefox_options = Options()
firefox_options.headless = True
driver = webdriver.Firefox(options=firefox_options)
driver.maximize_window()
driver.get(url='https://demowebshop.tricentis.com/login')

# Function to log results
def log_result(test_case, status, details):
    with open('test_results.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([test_case, status, details, datetime.datetime.now()])

class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def login(self, email, password):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'Email'))
        )
        self.driver.find_element(By.ID, 'Email').send_keys(email)
        self.driver.find_element(By.ID, 'Password').send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, 'input.login-button').click()

class HomePage:
    def __init__(self, driver):
        self.driver = driver

    def navigate_to_desktops(self):
        self.driver.find_element(By.LINK_TEXT, 'Computers').click()
        self.driver.find_element(By.LINK_TEXT, 'Desktops').click()

    def select_build_your_own_computer(self):
        self.driver.find_element(By.LINK_TEXT, 'Build your own cheap computer').click()

class ProductPage:
    def __init__(self, driver):
        self.driver = driver

    def add_to_cart(self):
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.ID, 'add-to-cart-button-72'))
        )
        self.driver.find_element(By.ID, 'add-to-cart-button-72').click()

class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver

    def go_to_cart(self):
        cart_link = self.driver.find_element(By.CSS_SELECTOR, 'a[href="/cart"]')
        cart_link.click()

    def accept_terms_and_checkout(self):
        time.sleep(3)
        self.driver.find_element(By.ID, 'termsofservice').click()
        self.driver.find_element(By.ID, 'checkout').click()

    def continue_to_next_step(self):
        self.driver.find_element(By.CSS_SELECTOR, 'input.button-1.new-address-next-step-button').click()

    def complete_billing_and_shipping(self):
        self.continue_to_next_step()

    def complete_shipping_method(self):
        time.sleep(5)
        self.driver.find_element(By.ID, 'PickUpInStore').click()
        time.sleep(5)
        self.driver.find_element(By.CSS_SELECTOR, 'input.new-address-next-step-button:nth-child(2)').click()

    def complete_payment_method(self):
        # self.continue_to_next_step()
        time.sleep(5)

        self.driver.find_element(By.CSS_SELECTOR, 'input.button-1.payment-method-next-step-button').click()
        time.sleep(5)

        self.driver.find_element(By.CSS_SELECTOR, 'input.button-1.payment-info-next-step-button').click()

        # self.driver.find_element(By.CSS_SELECTOR, 'input.new-address-next-step-button:nth-child(2)').click()


    def confirm_order(self):
        time.sleep(5)

        self.driver.find_element(By.CSS_SELECTOR, 'input.button-1.confirm-order-next-step-button').click()

        # self.continue_to_next_step()

    def capture_order_number(self):
        # return self.driver.find_element(By.CSS_SELECTOR, 'div.order-number').text
        return self.driver.find_element(By.CSS_SELECTOR, 'ul.details').text
    def wait_for_loading(self):
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located((By.ID, 'shipping-please-wait'))
        )

# Test the script
try:
    login_page = LoginPage(driver)
    login_page.login("johannesmphaka12121994@gmail.com", "Mafonko1994@")
    log_result("Login Test", "Pass", "Login successful")
except Exception as e:
    log_result("Login Test", "Fail", str(e))

try:
    home_page = HomePage(driver)
    home_page.navigate_to_desktops()
    home_page.select_build_your_own_computer()
    log_result("Navigation Test", "Pass", "Navigated to desktops and selected product")
except Exception as e:
    log_result("Navigation Test", "Fail", str(e))

try:
    product_page = ProductPage(driver)
    product_page.add_to_cart()
    log_result("Add to Cart Test", "Pass", "Product added to cart")
except Exception as e:
    log_result("Add to Cart Test", "Fail", str(e))

try:
    checkout_page = CheckoutPage(driver)
    checkout_page.go_to_cart()
    checkout_page.accept_terms_and_checkout()
    checkout_page.complete_billing_and_shipping()
    checkout_page.wait_for_loading()
    checkout_page.complete_shipping_method()
    checkout_page.wait_for_loading()
    checkout_page.complete_payment_method()
    checkout_page.wait_for_loading()
    checkout_page.confirm_order()
    order_number = checkout_page.capture_order_number()
    log_result("Checkout Test", "Pass", f"Order placed successfully. Order Number: {order_number}")
except Exception as e:
    log_result("Checkout Test", "Fail", str(e))

# Close the driver
driver.quit()
