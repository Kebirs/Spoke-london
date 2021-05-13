from spoke.main import DataWriter, Settings
from lxml import html


class TermsConditionsPage(Settings, DataWriter):
    def __init__(self):
        super(TermsConditionsPage, self).__init__()
        self.scrape_content()

    def scrape_content(self):
        cdn_id = self.get_cdn_id('https://spoke-london.com/de/pages/terms')

        banners_urls = [
            f'https://cdn.contentful.com/spaces/amhdwl2zsv5z/environments/master/entries?sys.id={cdn_id}&locale=en-GB&include=6',
            f'https://cdn.contentful.com/spaces/amhdwl2zsv5z/environments/master/entries?sys.id={cdn_id}&locale=de-DE&include=6']

        [self.terms_conditions_page_body(url) for url in banners_urls]

    def terms_conditions_page_body(self, url):
        content = self.get_banners(url)
        data = {}

        page_content_list = content['includes']['Entry'][0]['fields']['content']['content']
        data['Link'] = url

        counter = 0
        for i in page_content_list:
            for j in i['content']:
                try:
                    value = j['value']
                    value = value.replace('\r','').replace('.','').replace(')','').replace('(','').replace('\n',',')
                    if value != ' ' and value != '':
                        counter += 1
                        data[f'TERMS & CONDITIONS Text {counter}'] = value

                except KeyError:
                    pass

        self.terms_conditions_request_output(data)
