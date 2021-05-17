from spoke.main import DataWriter, Settings
from lxml import html


class CookiePolicyPage(Settings, DataWriter):
    def __init__(self):
        super(CookiePolicyPage, self).__init__()
        self.scrape_content()

    def scrape_content(self):
        cdn_id = self.get_cdn_id('https://spoke-london.com/de/pages/cookies')

        banners_urls = [
            f'https://cdn.contentful.com/spaces/amhdwl2zsv5z/environments/master/entries?sys.id={cdn_id}&locale=en-GB&include=6',
            f'https://cdn.contentful.com/spaces/amhdwl2zsv5z/environments/master/entries?sys.id={cdn_id}&locale=de-DE&include=6']

        [self.cookie_policy_page_body(url) for url in banners_urls]

    def cookie_policy_page_body(self, url):
        content = self.get_banners(url)
        data = {}
        data['Link'] = 'https://spoke-london.com/pages/cookies'

        page_content_list = content['includes']['Entry'][0]['fields']['content']['content']
        page_content_title = content['includes']['Entry'][1]['fields']['title']
        page_content_cookie_table = content['includes']['Entry'][2]['fields']['table']['table']

        data['Link direct'] = url
        data['COOKIE POLICY Title'] = page_content_title

        self.scrape_text_from_json(page_content_list, data, 'COOKIE POLICY Text')
        self.scrape_table_from_json(page_content_cookie_table, data, 'COOKIE POLICY TABLE Text ROW')

        self.cookie_policy_output(data)

    def scrape_text_from_json(self, target_list, data, column_name):
        counter = 1
        for i in target_list:
            for j in i['content']:

                try:
                    value = j['value']
                    self.find_value(value, counter, data, column_name)
                    counter+=1
                except KeyError:
                    pass

                try:
                    value = j['content'][0]['content'][0]['value']
                    self.find_value(value, counter, data, column_name)
                    counter+=1
                except KeyError:
                    pass

    @staticmethod
    def scrape_table_from_json(target_list, data, column_name):
        for index, i in enumerate(target_list):
            f_1 = i['FIELD1']
            f_2 = i['FIELD2']
            f_3 = i['FIELD3']
            row = f'{f_1}, {f_2}, {f_3}'
            data[f'{column_name} {index+1}'] = row

    @staticmethod
    def find_value(value, counter, data, column_name):
        value = value.replace('\r', '').replace('.', '').replace(')', '').replace('(', '').replace('\n', ',')
        if value != ' ' and value != '':
            data[f'{column_name} {counter}'] = value

