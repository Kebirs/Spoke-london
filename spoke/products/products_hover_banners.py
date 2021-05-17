import cloudscraper
from lxml import html
import json
from bs4 import BeautifulSoup as bs
from spoke.main import Settings, DataWriter


class ProductsBanners(Settings, DataWriter):
    def __init__(self):
        super(ProductsBanners, self).__init__()
        self.scrape_content()

    def scrape_content(self):
        # cdn_id = self.get_cdn_id('https://spoke-london.com/products/smoked-navy-heroes')

        banners_urls = [
            f'https://cdn.contentful.com/spaces/amhdwl2zsv5z/environments/master/entries?sys.id=3Y2dy1zyiarkO6N2jADqra&locale=en-GB&include=10',
            f'https://cdn.contentful.com/spaces/amhdwl2zsv5z/environments/master/entries?sys.id=3Y2dy1zyiarkO6N2jADqra&locale=de-DE&include=10']

        [self.banners_content(url) for url in banners_urls]

    def banners_content(self, url):
        content = self.get_banners(url)
        data = {}
        data['Hover images with pop up (shorts, tops, trousers) Here direct urls'] = url

        all_contents = content['includes']['Entry']

        main_title = content['items'][0]['fields']['title']
        data['Banners main title'] = main_title

        for idx, i in enumerate(all_contents):
            try:
                sub_data = []
                title = i['fields']['title']
                desc = i['fields']['description']
                sub_data.append(title)
                sub_data.append(desc)
                sub_data = self.clean_data(sub_data)

                data[f'Banner {idx+1}'] = sub_data
            except KeyError:
                byline = i['fields']['byline']
                data[f'Banner byline {idx+1}'] = byline

        self.products_hover_banners_output(data)
