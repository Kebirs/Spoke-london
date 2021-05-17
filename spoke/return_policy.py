import cloudscraper
from lxml import html
import json
from bs4 import BeautifulSoup as bs
from spoke.main import Settings, DataWriter


class ReturnPolicyPage(Settings, DataWriter):
    def __init__(self):
        super(ReturnPolicyPage, self).__init__()
        self.scrape_content()

    def scrape_content(self):
        cdn_id = self.get_cdn_id('https://spoke-london.com/pages/return-policy')

        banners_urls = [
            f'https://cdn.contentful.com/spaces/amhdwl2zsv5z/environments/master/entries?sys.id={cdn_id}&locale=en-GB&include=6',
            f'https://cdn.contentful.com/spaces/amhdwl2zsv5z/environments/master/entries?sys.id={cdn_id}&locale=de-DE&include=6']

        [self.banners_content(url) for url in banners_urls]

    def banners_content(self, url):
        content = self.get_banners(url)
        data = {}

        data['Link'] = 'https://spoke-london.com/pages/return-policy'
        data['Link direct'] = url

        try:
            banner_title = content['includes']['Entry'][0]['fields']['title']
        except Exception:
            banner_title = ''

        data['Banner Title'] = banner_title

        page_content_list = content['includes']['Entry'][1]['fields']['content']
        counter = 1
        for desc in page_content_list['content']:
            try:
                path = desc['content']
            except KeyError:
                path = None

            if path:
                for value in path:
                    try:
                        value = value['value']
                        if value != '.':
                            if value != '':
                                counter += 1
                                data[f'Return Policy Text {counter}'] = value
                    except KeyError:
                        pass

        self.return_policy_output(data)
