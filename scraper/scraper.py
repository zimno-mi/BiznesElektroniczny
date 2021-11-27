import csv
import traceback

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

def get_page_categories(driver):
    category_banner = driver.find_element_by_id("responsive")
    categories_buttons = category_banner.find_elements_by_tag_name("a")
    # First three elements are redundant, so we skip it in ugly way
    filtered_categories = categories_buttons[3:]
    urls = [i.get_attribute('href') for i in filtered_categories]
    return urls

def get_all_product_pages(driver):
    try:
        paginator = driver.find_element_by_class_name("pagination-container")
        pages = paginator.find_elements_by_tag_name("a")
        urls = [i.get_attribute('href') for i in pages]
        return urls
    except Exception as ex:
        return [driver.current_url]

def retrieve_products_from_page(product_page):
    products = product_page.find_elements_by_class_name("linkItem")
    urls = [i.get_attribute('href') for i in products]
    return urls

def parse_product_details_from_page(driver):
    try:
        details = driver.find_element_by_class_name("basic-table")
        elements = details.find_elements_by_tag_name("tr")
        values = {}
        characteristic_values = {}
        for i in elements:
            col, value = map(lambda x: x.text,
                             i.find_elements_by_tag_name('td'))
            characteristic_values[col] = value

        image_tags = driver.find_elements_by_class_name("mfp-gallery")
        image_urls = [i.get_attribute('href') for i in image_tags]

        values['characteristics'] = '|'.join([f"{i}:{j}"
                                              for i, j in characteristic_values.items()])

        values['image_urls'] = image_urls

        values['price'] = driver.find_element_by_class_name('product-price').\
                            find_element_by_tag_name('span').text

        values['name'] = driver.find_element_by_class_name('title').find_element_by_tag_name('h2').text.replace('=','-')

        values['category'] = driver.find_element_by_id('breadcrumbs').find_elements_by_tag_name('li')[1].find_element_by_tag_name('a').text

        values['description'] = [i.text for i in driver.find_element_by_class_name("tab-content").find_elements_by_tag_name('p')]

        return values
    except Exception as ex:
        print("Parsing err", ex)
        return

def save_products_details_in_csv(writer, products):
    try:
        odkurzacz = [
            products['name'],
            '|'.join(products['image_urls']),
            products['price'],
            ''.join(products['description']),
            products['category'],
            products['characteristics'],
        ]
        writer.writerow(odkurzacz)
    except Exception as ex:
        print("Saving to csv", ex)

def get_popup_with_promotion_exit_button(driver):
    return WebDriverWait(driver, 1000000).\
            until(EC.element_to_be_clickable((By.ID, "js-exit-popup-close")))

def close_popup_with_promotion(popup_button):
    popup_button.click()

def run_scraping_items(driver):
    csv_file = open('scrap_result.csv', 'w')
    writer = csv.writer(csv_file, delimiter=';')
    for i in get_page_categories(driver):
        print("Category page:", i)
        driver.get(i)
        try:
            for table_page in get_all_product_pages(driver):
                    driver.get(table_page)
                    print("Table page:", table_page)
                    retrieved_products = retrieve_products_from_page(driver)
                    for i in retrieved_products:
                            driver.get(i)
                            parsed_products = parse_product_details_from_page(driver)
                            save_products_details_in_csv(writer, parsed_products)
        except NoSuchElementException as ex:
            print("Could not find element: ", str(ex))

if __name__ == '__main__':
    try:
        driver = webdriver.Firefox()
        driver.get("https://www.pp-design.pl")
        run_scraping_items(driver)
    except Exception as ex:
        print(ex)
        traceback.print_exc()
    finally:
        driver.quit()

