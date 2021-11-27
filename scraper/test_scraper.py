import traceback
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC


def main():
    driver = webdriver.Firefox()
    driver.get('https://localhost/prestashop')


    mail = 'patrykpilipczuk@protonmail.com'
    pwd = 'niezbyttajne'

    add_to_card_some_items(driver)
    register_as_new_user(driver, mail, pwd)
    time.sleep(10)
    order_shipment(driver)
    check_order_status(driver)

def add_to_commission(driver, end):
    products_urls = [i.get_attribute('href') for i in driver.find_elements_by_class_name("product-thumbnail")]
    print("ADKOKOADKODAKO", products_urls)

    for v, i in enumerate(products_urls):
        if v == end:
            break
        driver.get(i)
        click_add_to_commission(driver)

def click_add_to_commission(driver):
    driver.find_element_by_class_name('add-to-cart').click()

def order_shipment(driver):
    driver.get('https://localhost/prestashop/index.php?controller=cart&action=show')
    driver.find_elements_by_class_name('remove-from-cart')[0].click()
    driver.find_elements_by_class_name('checkout')[0].click()

    driver.find_element_by_id('field-address1').send_keys("Nie wiem 7")
    driver.find_element_by_id('field-postcode').send_keys('12-137')
    driver.find_element_by_id('field-city').send_keys('Bytów')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    driver.find_element_by_name('confirm-addresses').click()
    driver.find_element_by_id('delivery_option_6').click()
    driver.find_element_by_id('delivery_message').send_keys('pozdrawiam rodziców')
    driver.find_element_by_name("confirmDeliveryOption").click()
    driver.find_element_by_id('payment-option-2').click()
    driver.find_element_by_id('conditions_to_approve[terms-and-conditions]').click()
    driver.find_element_by_xpath('//button[normalize-space()="Złóż zamówienie"]').click()

def check_order_status(driver):
    time.sleep(10)
    #driver.find_element_by_id('advancedButton').click()
    #driver.find_element_by_id('exceptionDialogButton').click()
    driver.get('https://localhost/prestashop/index.php?controller=my-account')
    driver.find_element_by_id('history-link').click()
    time.sleep(5)
    driver.find_elements_by_xpath('//a[@data-link-action="view-order-details"]')[0].click()

def add_to_card_some_items(driver):
    driver.get('https://localhost/prestashop/index.php?id_category=14&controller=category')
    add_to_commission(driver, 3)

    driver.get('http://localhost/prestashop/index.php?id_category=17&controller=category')
    add_to_commission(driver, 10)


def register_as_new_user(driver, mail, pwd):
    driver.get('https://localhost/prestashop/index.php?controller=authentication&create_account=1')

    driver.find_element_by_id("field-id_gender-1").click()
    driver.find_element_by_id("field-firstname").send_keys('TEST')
    driver.find_element_by_id("field-lastname").send_keys("TEST")

    driver.find_element_by_id("field-email").send_keys(mail)
    driver.find_element_by_id("field-password").send_keys(pwd)

    driver.find_element_by_xpath("//input[@name='customer_privacy']").click()

    driver.find_element_by_xpath("//input[@name='psgdpr']").click()

    driver.find_element_by_id("customer-form").submit()




if __name__ == '__main__':
    main()
