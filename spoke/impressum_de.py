from spoke.main import DataWriter, Settings
from lxml import html


class ImpressumPage(Settings, DataWriter):
    def __init__(self):
        super(ImpressumPage, self).__init__()
        self.scrape_content()

    def scrape_content(self):
        cdn_id = self.get_cdn_id('https://spoke-london.com/de/pages/impressum')

        banners_urls = [
            f'https://cdn.contentful.com/spaces/amhdwl2zsv5z/environments/master/entries?sys.id={cdn_id}&locale=en-GB&include=6',
            f'https://cdn.contentful.com/spaces/amhdwl2zsv5z/environments/master/entries?sys.id={cdn_id}&locale=de-DE&include=6']

        [self.impressum_page_body(url) for url in banners_urls]

    def impressum_page_body(self, url):
        content = self.get_banners(url)
        data = {}

        page_content_list = content['includes']['Entry'][1]['fields']['content']['content']
        data['Link'] = url

        counter = 0
        for i in page_content_list:
            for j in i['content']:
                try:
                    value = j['value']
                    if value != '.' and value != ' ' and value != '':
                        counter += 1
                        data[f'IMPRESSUM Text {counter}'] = value

                except KeyError:
                    pass

        self.impressum_request_output(data)
