import time
import cloudscraper
from lxml import html
from spoke.main import Settings, DataWriter


class CollectionsPage(Settings, DataWriter):
    def __init__(self):
        super(CollectionsPage, self).__init__()
        self.links = []
        self.scrape_content()

    def scrape_content(self):
        urls = ['https://spoke-london.com/us/pages/about',
                'https://spoke-london.com/de/pages/about']

        # [self.collections_page_body(self.get_request(url)) for url in urls]
        [self.get_links(self.get_request(url)) for url in urls]

    def get_links(self, url):
        data = {}

        all_links = "//div[@id='Products']//a[contains(@href, 'collections')]/@href"
        all_links = html.fromstring(url.text).xpath(all_links)

        for i, link in enumerate(all_links):

            title = "//h1[contains(@class, 'title')]/text()"
            byline = "//h2[contains(@class, 'byline')]/text()"
            headers_titles = "//div[contains(@class, 'collectionHeader__container')]//text()"

            sub_data = []
            self.links.append(link)

            r = self.get_request(link)
            print(f'|{r.status_code} collection link: {link}')

            title = html.fromstring(r.text).xpath(title)
            byline = html.fromstring(r.text).xpath(byline)
            headers_titles = html.fromstring(r.text).xpath(headers_titles)

            title = self.clean_data(title)
            byline = self.clean_data(byline)
            headers_titles = self.clean_data(headers_titles)

            properties = [title, byline, headers_titles]
            [sub_data.append(x) for x in properties]

            sub_data = self.clean_data(sub_data)

            data[f'Collection {i}'] = sub_data

        self.collections_output(data)

    def collections_page_body(self, url):
        data = {}

        self.collections_output(data)
