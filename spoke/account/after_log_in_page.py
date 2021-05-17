import time
import cloudscraper
from lxml import html
import asyncio
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from spoke.main import Settings, DataWriter


class AfterLogInPage(Settings, DataWriter):
    def __init__(self):
        super(AfterLogInPage, self).__init__()
        self.scrape_content()

    def scrape_content(self):
        urls = ['https://gb.spoke-london.com/account/login',
                'https://de.spoke-london.com/account/login']

        [self.after_log_in_page(self.get_response(url)) for url in urls]

    def after_log_in_page(self, url):
        s = self._selenium()

        self.log_in(s, url)
        self.your_fit(s)
        self.order_history(s)
        self.my_pre_orders(s)
        self.addresses(s)
        self.referrals(s)
        self.settings(s)

    def log_in(self, s, url):
        data = {}
        s.get(url.url)

        data['Link'] = url.url

        root = "//form[@id='customer_login']"

        login = f"{root}//input[@name='customer[email]']"
        password = f"{root}//input[@name='customer[password]']"
        button = f"{root}//span[@class='button__content']"

        s.find_element_by_xpath(login).send_keys('kebirdso@gmail.com')
        s.find_element_by_xpath(password).send_keys('allotedsine123')
        s.find_element_by_xpath(button).click()
        time.sleep(5)

        pageurl = 'https://gb.spoke-london.com/challenge'
        site_key = "6LeoeSkTAAAAAA9rkZs5oS82l69OEYjKRZAiKdaF"
        api_key = "17154ef34d5923c9682e41eb2a5196e9"
        form = {"method": "userrecaptcha",
                "googlekey": site_key,
                "key": api_key,
                "pageurl": pageurl,
                "json": 1}
        response = requests.post('http://2captcha.com/in.php', data=form)
        request_id = response.json()['request']
        url = f"http://2captcha.com/res.php?key={api_key}&action=get&id={request_id}&json=1"
        submit_button = "//input[@type='submit']"

        status = 0
        try:
            s.find_element_by_xpath(submit_button)
            while not status:
                res = requests.get(url)
                if res.json()['status'] == 0:
                    print('Captcha solving in progress ...')
                    time.sleep(3)
                else:
                    requ = res.json()['request']
                    js = f'document.getElementById("g-recaptcha-response").innerHTML="{requ}";'
                    s.execute_script(js)
                    print("Captcha solved. Logging in.")
                    s.find_element_by_xpath(submit_button).submit()
                    status = 1
        except Exception:
            pass
        self.account_output(data)

    def your_fit(self, s):
        time.sleep(3)
        data = {}

        nav = "//nav[@class='nav__container']//text()"
        col_1_title_text = "//header/p[@class='grid__item']/text()"
        col_1_text = "//div[@class='card-fit__item__summary']//text()"
        my_fit_footer_button = "//a[contains(@data-analytics-props, 'Complete Fit Finder')]//text()"
        recommended_products_section = "//header[contains(@class, 'header-stock')]/p/..//text()"

        nav = html.fromstring(s.page_source).xpath(nav)
        col_1_title_text = html.fromstring(s.page_source).xpath(col_1_title_text)
        col_1_text = html.fromstring(s.page_source).xpath(col_1_text)
        col_1_text = list(dict.fromkeys(col_1_text))
        my_fit_footer_button = html.fromstring(s.page_source).xpath(my_fit_footer_button)
        recommended_products_section = html.fromstring(s.page_source).xpath(recommended_products_section)

        properties = {
            'Navigation': nav,
            'Card item title': col_1_title_text,
            'Card item text': col_1_text,
            'Fit Finder button': my_fit_footer_button,
            'Under Fit Finder button section content': recommended_products_section
        }

        for k, v in properties.items():
            data[k] = self.clean_data(v)

        self.account_output(data)

    def order_history(self, s):
        time.sleep(1)
        data = {}
        button = "//a[contains(@data-analytics-props, 'Order History')]"
        s.find_element_by_xpath(button).click()
        time.sleep(2)
        content = "//section[contains(@class, 'grid--column')]"
        content = s.find_element_by_xpath(content).text
        data['ORDER HISTORY Content'] = content

        self.account_output(data)

    def my_pre_orders(self, s):
        time.sleep(2)
        data = {}

        button = "//a[contains(@href, 'pre-orders')]"
        s.find_element_by_xpath(button).click()
        time.sleep(2)

        title = "//h2[@class='preorders__title']"
        title = s.find_element_by_xpath(title).text
        data['PRE ORDERS Title'] = title

        iframe = "//iframe[@class='purple-dot-frame']"
        iframe = WebDriverWait(s, 10).until(EC.visibility_of_element_located((By.XPATH, iframe)))
        s.switch_to.frame(iframe)
        time.sleep(1)

        pre_order_content = "//div[contains(@class, 'pre-order-status')]"
        pre_order_content = s.find_element_by_xpath(pre_order_content).text.replace('\n', ', ')
        data['PRE ORDERS Content'] = pre_order_content

        s.switch_to_default_content()

        self.account_output(data)

    def addresses(self, s):
        time.sleep(2)
        data = {}

        button = "//a[contains(@data-analytics-props, 'Addresses')]"
        s.find_element_by_xpath(button).click()
        time.sleep(2)

        content = "//section[contains(@class, 'grid--gutter')]"
        content = s.find_element_by_xpath(content).text
        data['ADDRESSES Content'] = content

        self.account_output(data)

    def referrals(self, s):
        data = {}

        button = "//a[contains(@data-analytics-props, 'Referrals')]"
        s.find_element_by_xpath(button).click()
        time.sleep(2)

        title = "//h2[@class='referrals__title']"
        notes = "//div[contains(@class, 'referrals__content')]/p/text()"

        notes = html.fromstring(s.page_source).xpath(notes)
        notes = [x.strip().replace('\n', '').replace('  ', '') for x in notes]

        title = s.find_element_by_xpath(title).text

        data['REFERRALS Title'] = title

        for idx, note in enumerate(notes):
            data[f'REFERRALS Note {idx+1}'] = note

        self.account_output(data)

    def settings(self, s):
        data = {}

        button = "//a[contains(@href, 'settings')]"
        s.find_element_by_xpath(button).click()
        time.sleep(2)

        boxes = "//div[contains(@class, 'card--address')]"
        boxes = html.fromstring(s.page_source).xpath(boxes)

        for idx, x in enumerate(boxes):
            text = x.xpath('string()')
            data[f'SETTINGS BOX {idx+1}'] = text.strip().replace('\n', ' ').replace('  ', '')

        self.account_output(data)



