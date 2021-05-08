import ast
import time

import lxml.html
import pandas as pd
import requests
import json
import cloudscraper
import re
from bs4 import BeautifulSoup as bs
from lxml import html
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager as CM
from spoke.main import SpokeScraperCore

# TODO make it as func to init selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")
browser = webdriver.Chrome(executable_path=CM().install(), options=options)


class BrandPageStatic(SpokeScraperCore):

    def __init__(self):
        super(BrandPageStatic, self).__init__()
        self.scrape_content()

    def scrape_content(self):
        # For both lang; eng and de side by side in columns
        url_eng = 'https://spoke-london.com'
        url_de = 'https://spoke-london.com/de/'

        self.main_output_data(self.over_navbar_info(url_eng, 'ENG', self.eng_encoding))
        self.main_output_data(self.over_navbar_info(url_de, 'DE', self.de_encoding))

        self.menu_content(url_eng, url_de)

        # banners_url_eng = 'https://cdn.contentful.com/spaces/amhdwl2zsv5z/environments/master/entries?sys.id=2HcDAp7cZd3Vpq5hEK4bMS&locale=en-GB&include=6'
        # banners_url_de = 'https://cdn.contentful.com/spaces/amhdwl2zsv5z/environments/master/entries?sys.id=2HcDAp7cZd3Vpq5hEK4bMS&locale=de-DE&include=6'
        # self.main_output_data(self.banners_content(banners_url_eng))
        # self.main_output_data(self.banners_content(banners_url_de))
        #
        # self.main_output_data(self.footer_content(url_eng))
        # self.main_output_data(self.footer_content(url_de))

    @staticmethod
    def get_request(url):
        s = cloudscraper.create_scraper()
        r = s.get(url)
        return r

    def json_script_data(self, url, encoding):
        resp = self.get_request(url)
        resp.encoding = encoding
        script_data = html.fromstring(resp.text).xpath('//script[@id="__NEXT_DATA__"]/text()')
        true = 'true'
        false = 'false'
        null = 'null'
        script_data_json = eval(script_data[0])
        return script_data_json

    def over_navbar_info(self, url, lang, encoding):
        data = {}
        script_data = self.json_script_data(url, encoding)
        over_navbar_text = script_data['props']['initialState']['header']['menu'][
            'items'][0]['flashBanner']['flashBannerItems'][
            'items'][0]['bannerName']
        data[lang + ' Brand Homepage - Over Navbar Info'] = over_navbar_text
        return data

    def menu_content(self, url_eng, url_de):
        script_data_eng = self.json_script_data(url_eng, self.eng_encoding)
        script_data_de = self.json_script_data(url_de, self.de_encoding)
        scripts = [script_data_eng, script_data_de]
        # header_text = script_data_eng['props']['initialState']['header']['menu']['items'][0]['desktop']['primaryNavigation']['items']

        for i, _ in enumerate(scripts):
            header_text = _['props']['initialState']['header']['menu']['items'][0]['desktop']['primaryNavigation']['items']
            data = {}
            data[' Main menu titles'] = [(i['title']) for i in header_text]

            data[' Main menu titles dropdown'] = [(j['title']) for i in header_text
                                                  for j in i['secondaryNavigation']['items']]

            data[' Main menu titles dropdown additional'] = [(k['title'],
                                                              k['card']['description'],
                                                              k['card']['byline'],
                                                              k['card']['badge']['title'] if k['card'][
                                                                                                 'badge'] != 'null' else None,
                                                              k['card']['button']['text'])
                                                             for i in header_text
                                                             for j in i['secondaryNavigation']['items']
                                                             for k in j['tertiaryNavigation']['items']]

            data[' Main menu NEW IN submenu'] = [(j['title'],
                                                  j['byline'],
                                                  j['description'],
                                                  j['badge']['title'] if j['badge'] != 'null' else None)
                                                 for i in header_text if i['title'] == 'New In' or i['title'] == 'NEU'
                                                 for j in i['submenuLayout']['grid']['items']]

            data[' Right menu content'] = (_['props']['initialState'][
                                               'header']['menu']['items'][0]['desktop']['secondaryNavigation'][
                                               'items'][0]['title'], 'Log In')

            self.main_output_data(data)

    def banners_content(self, url):
        auth = {
            'Authorization': 'Bearer 56If-j-ANNWSZ9Zk_8lp9EChokF6LNtKJDHC8eHMfSs',
            'If-None-Match': 'W/"16729328500904452549"'
        }
        s = cloudscraper.create_scraper()
        r = s.get(url, headers=auth)
        content = r.json()

        data = {}
        benefits = []
        mobile = []
        clothes = []
        additional = []
        comments = []

        all_contents = content['includes']['Entry']

        for content in all_contents:
            try:
                try:
                    # Content names as name of banner field
                    content_name = content['fields']['contentName']


                except KeyError:
                    content_name = None

                self.banner_benefits(content, content_name, benefits)
                self.banner_mobile(content, content_name, mobile)
                self.banner_clothes(content, content_name, clothes)
                self.over_brands_text(content,  additional)
                self.comments_content(content, content_name, comments)

                # Banner with animate mobile phone button's
                # if re.compile('.*FineTuneFit.*').match(str(content_button)):
                #     text = content['fields']['text']
                #     mobile.append(text)

            except KeyError:
                continue
        data[self.ENG + ' Banner Benefits Content'] = benefits
        data[self.ENG + ' Banner Mobile Animation Content'] = mobile
        data[self.ENG + ' Banner Clothes Content'] = clothes
        data[self.ENG + ' Additional Content'] = additional
        data[self.ENG + ' Comments Content'] = comments

        # Banners

        return data

    @staticmethod
    def banner_benefits(content, content_name, benefits):
        # Banner with benefits
        if re.compile(r'Home[p|P]age Benefit (First|Second|Third) Item').match(str(content_name)):
            title = content['fields']['title']
            description = content['fields']['description']
            benefits.append(title)
            benefits.append(description)

    @staticmethod
    def banner_mobile(content, content_name, mobile):
        # Banner with animate mobile phone
        if re.compile(r'Fine Tune my Fit Homepage').match(str(content_name)):
            title = content['fields']['title']
            description = content['fields']['description']
            mobile.append(title)
            mobile.append(description)

    @staticmethod
    def banner_clothes(content, content_name, clothes):
        # Banner with clothes; over clothes description
        if re.compile(r'Product BreakDown Homepage').match(str(content_name)):
            title = content['fields']['title']
            byline = content['fields']['byline']
            clothes.append(title)
            clothes.append(byline)

        # Banner with clothes; clothes title and description
        if re.compile(r'.*Product[b|B]reakdown Item.*').match(str(content_name)):
            title = content['fields']['title']
            byline = content['fields']['byline']
            desc = content['fields']['description']
            clothes.append(title)
            clothes.append(byline)
            clothes.append(desc)

    @staticmethod
    def over_brands_text(content, additional):
        text = content['fields']['title']
        if text == 'As seen in':
            additional.append(text)

    @staticmethod
    def comments_content(content, content_name, comments):
        # Banner with comments
        if re.compile(r'(Testimonial|Testimonials) Homepage (First|second|Third|Fourth) (item|Item|Item )').match(str(content_name)):
            print(1)
            title = content['fields']['title']
            name = content['fields']['underTitle']
            comments.append(title)
            comments.append(name)


    def footer_content(self, url):
        browser.get(url)
        time.sleep(3)
        data = {}
        sub_data = []
        sub_data.append(browser.find_element_by_xpath('/html/body/div[1]/main/div/div[3]/footer/div[1]/div/div/div[1]/div/div/div').text.strip().replace('\n', ', '))
        sub_data.append(browser.find_element_by_xpath('//input[@id="email"]').get_attribute('placeholder'))
        sub_data.append('Please enter an email')
        sub_data.append(browser.find_element_by_xpath('//div[@class="styles_footerBaseContent__15eHp"]').text.strip().replace('\n', ', '))
        sub_data.append(browser.find_element_by_xpath("//div[contains(@class, 'styles_footerWrap__26rQ6')]").text.strip().replace('\n', ', '))

        data[self.ENG + ' FOOTER'] = sub_data
        print(data)
        return data

if __name__ == '__main__':
    BrandPageStatic()
