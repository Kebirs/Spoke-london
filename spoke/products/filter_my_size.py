import time
import cloudscraper
from lxml import html
import asyncio
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from spoke.main import Settings, DataWriter


class FilterMySize(Settings, DataWriter):
    def __init__(self):
        super(FilterMySize, self).__init__()
        self.scrape_content()

    def scrape_content(self):
        urls = ['https://spoke-london.com/gb/collections/trousers',
                'https://spoke-london.com/de/collections/trousers']
        [self.filter_size_button(url) for url in urls]

    def filter_size_button(self, url):
        data = {}
        s = self._selenium()
        s.get(url)
        time.sleep(2)

        temp_position = "//h2[contains(@class, 'title--center')]"
        temp_position = s.find_element_by_xpath(temp_position)
        s.execute_script("arguments[0].scrollIntoView();", temp_position)
        time.sleep(1)

        filter_button = "//div[@id='filterButton']"
        s.find_element_by_xpath(filter_button).click()
        time.sleep(1)

        subtitles = "//h2[contains(@class, 'productForm__subtitle')]/text()"
        build_types = "//p[contains(@class, 'options__description')]/text()"
        filter_footer = "//div[contains(@class, 'filters__footer')]//text()"

        subtitles = html.fromstring(s.page_source).xpath(subtitles)
        build_types = html.fromstring(s.page_source).xpath(build_types)
        filter_footer = html.fromstring(s.page_source).xpath(filter_footer)

        properties = {
            'FILTER Subtitles': subtitles,
            'FILTER Build Types': build_types,
            'FILTER Footer Content': filter_footer
        }

        for k, v in properties.items():
            data[k] = self.clean_data(v)

        self.filter_my_size_output(data)


