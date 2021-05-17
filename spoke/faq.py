import time

from lxml import html
import json
from bs4 import BeautifulSoup as bs
from spoke.main import Settings, DataWriter


class FAQPage(Settings, DataWriter):
    def __init__(self):
        super(FAQPage, self).__init__()
        self.origin_url = 'https://spokelondon.zendesk.com'
        self.faq_home_links = []
        self.scrape_home_content()

    def scrape_home_content(self):
        """
        Sign in interactive popup not included cause
        it comes from zendesk.com
        """
        urls = ['https://spokelondon.zendesk.com/hc/en-us',
                'https://spokelondon.zendesk.com/hc/de']

        [self.faq_home_body(self.get_response(url)) for url in urls]

    def faq_home_body(self, url):
        self.sign_in(url)
        self.search(url)
        self.blocks_item_cat(url)

    def sign_in(self, url):
        data = {}
        data['Link'] = url.url
        soup = bs(url.text, 'lxml')
        login = soup.find('a', {'class': 'login'}).text

        data['Login Button'] = login

        self.faq_home_output(data)

    def search(self, url):
        search = html.fromstring(url.text).xpath('//input[@type="search"]/@placeholder')
        data = {'Search': search}

        self.faq_home_output(data)

    def blocks_item_cat(self, url):
        blocks = html.fromstring(url.text).xpath('//section[@class="categories blocks"]//text()')
        blocks = self.clean_data(blocks)

        data = {'Categories Blocks': blocks}
        self.faq_home_output(data)
