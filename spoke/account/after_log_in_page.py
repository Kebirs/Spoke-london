import time
import cloudscraper
from lxml import html
import asyncio
import requests
from spoke.main import Settings, DataWriter


class AfterLogInPage(Settings, DataWriter):
    def __init__(self):
        super(AfterLogInPage, self).__init__()
        self.scrape_content()

    def scrape_content(self):
        urls = ['https://gb.spoke-london.com/account/login',
                'https://de.spoke-london.com/account/login']

        [self.after_log_in_page(self.get_request(url)) for url in urls]

    def after_log_in_page(self, url):
        data = {}
        s = self._selenium()
        s.get(url.url)

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
                    print('Retrying ...')
                    time.sleep(3)
                else:
                    requ = res.json()['request']
                    js = f'document.getElementById("g-recaptcha-response").innerHTML="{requ}";'
                    s.execute_script(js)
                    print("Done ...")
                    s.find_element_by_xpath(submit_button).submit()
                    status = 1
        except Exception:
            pass
        # nav = s.find_element_by_xpath("//nav[@class='nav__container']")
        # nav = nav.text
        print(1)
