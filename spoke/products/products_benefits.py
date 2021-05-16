import time
import cloudscraper
from bs4 import BeautifulSoup as bs
from lxml import html
from spoke.main import Settings, DataWriter


class ProductsBenefits(Settings, DataWriter):
    def __init__(self):
        super(ProductsBenefits, self).__init__()
        self.scrape_content()

    def scrape_content(self):
        # Only those types have benefit banners, could improve to all types and than return
        # blank columns if there's no content at all. It can be useful if there will be added
        # new benefits for certain product type
        prod_types = ['heroes', 'fives', 'sharps', 'swims', '12oz-original', '10oz-travel',
                      '14oz-japanese']

        root_url = "https://cdn.contentful.com/spaces/amhdwl2zsv5z/environments/master/" \
                   "entries?content_type=storytelling&fields.productType={}&include=6"

        urls = [root_url.format(x) for x in prod_types]

        [self.products_benefits_body(url) for url in urls]

    def products_benefits_body(self, url):
        content = self.get_banners(url)
        data = {}

        all_contents = content['includes']['Entry']

        for i in all_contents:
            try:
                key = i['fields']['contentName']
                try:
                    sub_data = []
                    value1 = i['fields']['title']
                    value2 = i['fields']['description']
                    sub_data.append(value1)
                    sub_data.append(value2)
                    sub_data = self.clean_data(sub_data)
                    data[key] = sub_data
                except KeyError:
                    value = i['fields']['copy']
                    data[key] = value

            except KeyError:
                key = i['fields']['title']
                value = i['fields']['text']
                data[key] = value

        self.products_benefits_output(data)
