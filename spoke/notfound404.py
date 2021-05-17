import cloudscraper

from spoke.main import DataWriter, Settings
from lxml import html


class NotFoundPage(Settings, DataWriter):
    def __init__(self):
        super(NotFoundPage, self).__init__()
        self.scrape_content()

    def scrape_content(self):
        # Actually not working page
        url = 'https://spoke-london.com/obviously_invalid_page'

        # Also this link not working
        # https://spoke-london.com/de/pages/edit-preorder

        s = cloudscraper.create_scraper()
        r = s.get(url)

        self.not_found_page_body(r)

    def not_found_page_body(self, url):
        content = '//div[@class="wrapper__content"]//text()'
        content = html.fromstring(url.text).xpath(content)
        content = self.clean_data(content)

        data = {'PAGE NOT FOUND Content': content}

        self.not_found_output(data)
