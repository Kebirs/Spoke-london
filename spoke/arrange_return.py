import time
import cloudscraper
from lxml import html
import asyncio
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from spoke.main import Settings, DataWriter


class ArrangeReturn(Settings, DataWriter):
    def __init__(self):
        super(ArrangeReturn, self).__init__()
        self.scrape_content()

    def scrape_content(self):
        urls = ['https://spoke-london.com/gb/pages/returns',
                'https://spoke-london.com/de/pages/returns']

        [self.arrange_return_page_body(url) for url in urls]

    def arrange_return_page_body(self, url):
        data = {}
        data['Link'] = url
        s = self._selenium()
        s.get(url)
        time.sleep(3)

        title = "//h2[contains(@class, 'title--center')]"
        content = "//form[contains(@class, 'form__content')]"

        title = s.find_element_by_xpath(title).text
        content = s.find_element_by_xpath(content).text.replace('\n', ', ')

        data['Title'] = title
        data['Content'] = content
        print(1)
        self.arrange_return_output(data)
