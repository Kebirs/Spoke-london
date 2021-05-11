import time

from lxml import html
import json
from bs4 import BeautifulSoup as bs
from spoke.main import Settings, DataWriter


class FAQPageStatic(Settings, DataWriter):
    def __init__(self):
        super(FAQPageStatic, self).__init__()
        self.origin_url = 'https://spokelondon.zendesk.com'
        self.faq_home_links = []
        self.scrape_home_content()

    def scrape_home_content(self):
        urls = ['https://spokelondon.zendesk.com/hc/en-us',
                'https://spokelondon.zendesk.com/hc/de']

        [self.faq_home_body(self.get_request(url)) for url in urls]

    def faq_home_body(self, url):
        self.sign_in(url)
        self.search(url)
        self.blocks_item_cat(url)

    def sign_in(self, url):
        soup = bs(url.text, 'lxml')
        login = soup.find('a', {'class': 'login'}).text
        data = {'Login Button': login}

        self.faq_home_output(data)

    def search(self, url):
        search = html.fromstring(url.text).xpath('//input[@type="search"]/@placeholder')
        data = {'Search': search}

        self.faq_home_output(data)

    def blocks_item_cat(self, url):
        blocks = html.fromstring(url.text).xpath('//section[@class="categories blocks"]//text()')
        blocks = self.clean_data(blocks)

        data = {'Categories Blocks': blocks}
        self.faq_home_output(data)


class FAQPageLinks(FAQPageStatic):
    def __init__(self):
        super(FAQPageLinks, self).__init__()
        self.faq_parent_links = []
        self.faq_first_child_links = []
        self.faq_second_child_links = []
        self.links_scrape()

    def links_scrape(self):
        urls = ['https://spokelondon.zendesk.com/hc/en-us',
                'https://spokelondon.zendesk.com/hc/de']

        # [self.faq_parent_links_scrape(self.get_request(url)) for url in urls]

        # alll = self.faq_parent_links
        # for i in alll[0]:
        #     for k in i:
        #         self.faq_parent_links_static_page_scrape(self.get_request(k))
        #
        #         self.faq_parent_links_static_page_scrape(self.get_request(k))
        self.faq_parent_links_scrape()
        [self.faq_parent_links_static_page_scrape(self.get_request(x)) for x in self.faq_parent_links]

        self.faq_first_child_links_scrape()

    def faq_parent_links_scrape(self):
        urls = ['https://spokelondon.zendesk.com/hc/en-us',
                'https://spokelondon.zendesk.com/hc/de']

        # blocks_links = html.fromstring(url.text).xpath('//section[@class="categories blocks"]//a/@href')
        for url in urls[0]:
            resp = self.get_request(url)
            blocks_links = html.fromstring(resp.text).xpath('//section[@class="categories blocks"]//a/@href')
            for i in range(len(blocks_links)):
                for url_lang in urls:
                    resp = self.get_request(url_lang)
                    time.sleep(0.2)
                    link_path = html.fromstring(resp.text).xpath(f'//section[@class="categories blocks"]/ul/li[{i+1}]/a/@href')
                    block_link = self.origin_url + link_path[0]

                    self.faq_parent_links.append(block_link)

    def faq_first_child_links_scrape(self):
        for link in self.faq_parent_links:
            resp = self.get_request(link)
            first_child_links = html.fromstring(resp.text).xpath('//section/h3/a/@href')
            first_child_links = [self.origin_url + link for link in first_child_links]

            # Add links to first child links
            self.faq_first_child_links.append(first_child_links)

    def faq_parent_links_static_page_scrape(self, url):
        soup = bs(url.text, 'lxml')

        data = {'Link': url.url}
        sub_data = []

        navigation = html.fromstring(url.text).xpath('//ol[@class="breadcrumbs"]//text()')
        navigation = self.clean_data(navigation)
        sub_data.append(navigation)

        login = soup.find('a', {'class': 'login'}).text
        sub_data.append(login)

        search = html.fromstring(url.text).xpath('//input[@type="search"]/@placeholder')
        sub_data.append(search)

        data['Navigation text'] = sub_data

        body = html.fromstring(url.text).xpath('//div[@class="container"]//text()')
        body = self.clean_data(body)
        data['Page body (links, titles)'] = body

        self.faq_category_output(data)


    def faq_second_child_links_scrape(self):
        pass


class FAQPage(FAQPageLinks):
    def __init__(self):
        super(FAQPage, self).__init__()
