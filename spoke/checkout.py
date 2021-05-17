import time
import cloudscraper
import re

from lxml import html

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from spoke.main import DataWriter, Settings


class CheckoutPage(Settings, DataWriter):
    def __init__(self):
        super(CheckoutPage, self).__init__()
        self.scrape_content()

    def scrape_content(self):
        urls = ['https://spoke-london.com/eu/products/rinse-wash-travel-denim',
                'https://spoke-london.com/de/products/rinse-wash-travel-denim']

        [self.checkout_page_body(url) for url in urls]

    def checkout_page_body(self, url):
        data = {}
        data['Link'] = url
        s = self._selenium()
        s.get(url)
        # time.sleep(5)

        click_1 = "(//button[contains(@class, 'options__item')])[1]"
        click_2 = "(//li[contains(@class, 'active')])[1]"
        click_3 = "(//button[contains(@class, 'options__item')])[12]"

        WebDriverWait(s, 10).until(EC.visibility_of_element_located((By.XPATH, click_1))).click()
        WebDriverWait(s, 10).until(EC.visibility_of_element_located((By.XPATH, click_2))).click()

        temp_position = "(//h2[@class='styles_productForm__subtitle__vIIdt'])[2]"
        temp_position = s.find_element_by_xpath(temp_position)
        time.sleep(1)

        s.execute_script("arguments[0].scrollIntoView();", temp_position)

        WebDriverWait(s, 10).until(EC.visibility_of_element_located((By.XPATH, click_3))).click()
        time.sleep(1)


        # Find product, add to basket, go to checkout, scrape content
        add_to_basket_button = "//button[contains(@class, 'add-to-cart')]"
        add_to_basket_button = WebDriverWait(s, 10).until(EC.visibility_of_element_located((By.XPATH, add_to_basket_button)))

        add_to_basket_button.click()
        time.sleep(1)

        note1 = "//p[contains(@class, 'cart__delivery')]"
        note2 = "//p[contains(@class, 'cart__guarantee')]"
        close_button = "//button[contains(@class, 'cart__keepShopping')]"

        note1 = s.find_element_by_xpath(note1).text
        note2 = s.find_element_by_xpath(note2).text
        close_button = s.find_element_by_xpath(close_button).text

        checkout_button = "//a[contains(@class, 'cart__button')]"
        checkout_button = WebDriverWait(s, 10).until(EC.visibility_of_element_located((By.XPATH, checkout_button)))

        checkout_button_text = checkout_button.text

        time.sleep(2)
        checkout_button.click()
        time.sleep(2)

        # Left content
        title_left = "//h3[contains(@class, 'title--left')]"
        header = "//div[contains(@class, 'basket__headers')]"
        remove = "//a[contains(@class, 'link--block link--light-grey link--small')]"
        add_gift = "(//button[contains(@class, 'button_giftMessage')])[1]"
        referred_friend = "//a[@class='styles_link__2gw0X link link--block']"
        total = "//h5[contains(@class, 'basket__total')]"
        delivery = "//div[contains(@class, 'basket__delivery')]"

        # Right content
        title_right = "//h4[contains(@class, 'basketAddon__title')]"
        add_button = "(//div[@class='grid grid--column grid__item styles_basketAddon__i8fCr']//button/span)[1]"

        title_left = s.find_element_by_xpath(title_left).text
        header = s.find_element_by_xpath(header).text.replace('\n', ', ')
        remove = s.find_element_by_xpath(remove).text
        add_gift = s.find_element_by_xpath(add_gift).text
        referred_friend = s.find_element_by_xpath(referred_friend).text
        total = s.find_element_by_xpath(total).text
        delivery = s.find_element_by_xpath(delivery).text

        title_right = s.find_element_by_xpath(title_right).text
        add_button = s.find_element_by_xpath(add_button).text

        properties = {
            'Free Delivery Note': note1,
            'Return Guarantee Note': note2,
            'Close Button text': close_button,
            'Checkout button text': checkout_button_text,
            'LEFT Title': title_left,
            'HEADER Text': header,
            'Remove button text': remove,
            'Add to gift text': add_gift,
            'Referred a friend link text': referred_friend,
            'TOTAL': total,
            'DELIVERY': delivery,
            'RIGHT Title': title_right,
            'ADD Button': add_button
        }

        data['Link'] = url

        for k, v in properties.items():
            data[k] = v

        self.checkout_output(data)


















