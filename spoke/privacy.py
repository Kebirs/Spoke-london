from spoke.main import DataWriter, Settings
from lxml import html


class PrivacyPolicyPage(Settings, DataWriter):
    def __init__(self):
        super(PrivacyPolicyPage, self).__init__()
        self.scrape_content()

    def scrape_content(self):
        cdn_id = self.get_cdn_id('https://spoke-london.com/de/pages/privacy')

        banners_urls = [
            f'https://cdn.contentful.com/spaces/amhdwl2zsv5z/environments/master/entries?sys.id={cdn_id}&locale=en-GB&include=6',
            f'https://cdn.contentful.com/spaces/amhdwl2zsv5z/environments/master/entries?sys.id={cdn_id}&locale=de-DE&include=6']

        [self.privacy_page_body(url) for url in banners_urls]

    def privacy_page_body(self, url):
        content = self.get_banners(url)
        data = {}
        data['Link'] = 'https://spoke-london.com/pages/privacy'

        data['Link direct'] = url

        page_content_list = content['includes']['Entry'][0]['fields']['content']['content']

        counter = 0
        for i in page_content_list:
            for j in i['content']:
                try:
                    value = j['value']
                    if value != '.':
                        if value != '':
                            counter += 1
                            data[f'PRIVACY POLICY Text {counter}'] = value

                except KeyError:
                    pass

        self.privacy_output(data)
