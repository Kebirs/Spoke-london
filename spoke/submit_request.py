import re

from spoke.main import DataWriter, Settings
from lxml import html


class SubmitRequestPage(Settings, DataWriter):
    def __init__(self):
        super(SubmitRequestPage, self).__init__()
        self.scrape_content()

    def scrape_content(self):
        urls = ['https://spokelondon.zendesk.com/hc/en-us/requests/new',
                'https://spokelondon.zendesk.com/hc/de/requests/new']

        [self.submit_request_page_body(self.get_request(url)) for url in urls]

    def submit_request_page_body(self, url):
        data = {}
        content = '//main//text()'
        content = html.fromstring(url.text).xpath(content)

        # Slice cause of messy data (html tags)
        content = content[:45]
        content = self.clean_data(content)

        data['Link'] = url.url
        data['SUBMIT REQUEST Content'] = content

        self.submit_request_output(data)
