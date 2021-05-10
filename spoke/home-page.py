import time
import cloudscraper
import re
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager as CM
from selenium.webdriver.support import expected_conditions as EC
from spoke.main import SpokeScraperCore


class Settings(object):
    def __init__(self):
        super(Settings, self).__init__()
        self.ENG = 'ENG '
        self.DE = 'DE '
        self.languages_list = [self.ENG, self.DE]

    @staticmethod
    def get_request(url):
        s = cloudscraper.create_scraper()

        r = s.get(url)
        r.encoding = 'UTF-8'
        return r

    def json_script_data(self, url):
        """
        Evaluate data into json format
        :param url:
        :return data formatted into json:
        """
        resp = self.get_request(url)
        script_data = html.fromstring(resp.text).xpath('//script[@id="__NEXT_DATA__"]/text()')
        true = 'true'
        false = 'false'
        null = 'null'
        script_data_json = eval(script_data[0])
        return script_data_json

    @staticmethod
    def _selenium():
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        browser = webdriver.Chrome(executable_path=CM().install(), options=options)
        return browser

    @staticmethod
    def _selenium_lang(lang):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument(f'--lang={lang}')
        browser = webdriver.Chrome(executable_path=CM().install(), options=options)
        return browser


class Menu(Settings):
    def __init__(self):
        super(Menu, self).__init__()

    def over_navbar_info(self, url, lang):
        data = {}
        script_data = self.json_script_data(url)
        over_navbar_text = script_data['props']['initialState']['header']['menu']['items'][0]['flashBanner']['flashBannerItems']['items'][0]['bannerName']
        data[lang + ' Brand Homepage - Over Navbar Info'] = over_navbar_text
        return data

    def menu_content(self, eng_url, de_url):
        """
        Scrape whole data related to MENU content; dropdown menu after hover included
        :param eng_url:
        :param de_url:
        """
        eng_script_data = self.json_script_data(eng_url)
        de_script_data = self.json_script_data(de_url)

        # Target text related to menu
        eng_header_text = eng_script_data['props']['initialState']['header']['menu']['items'][0]['desktop']['primaryNavigation']['items']
        de_header_text = de_script_data['props']['initialState']['header']['menu']['items'][0]['desktop']['primaryNavigation']['items']

        data = {}

        self._menu_titles(data, self.ENG, eng_header_text)
        self._menu_titles(data, self.DE, de_header_text)

        self._menu_titles_dropdown(data, self.ENG, eng_header_text)
        self._menu_titles_dropdown(data, self.DE, de_header_text)

        self._menu_titles_dropdown_additional(data, self.ENG, eng_header_text)
        self._menu_titles_dropdown_additional(data, self.DE, de_header_text)

        self._menu_new_in_card_submenu(data, self.ENG, eng_header_text)
        self._menu_new_in_card_submenu(data, self.DE, de_header_text)

        self._menu_right_side_text(data, self.ENG, eng_script_data)
        self._menu_right_side_text(data, self.DE, de_script_data)

        self._menu_right_side_shop_button_text(data, eng_url, self.ENG)
        self._menu_right_side_shop_button_text(data, de_url, self.DE)

        return data

    @staticmethod
    def _menu_titles(data, lang, target_text):
        data[lang + 'Main menu titles'] = [(i['title']) for i in target_text]

    @staticmethod
    def _menu_titles_dropdown(data, lang, target_text):
        data[lang + 'Main menu titles dropdown'] = [(j['title'])
                                                        for i in target_text
                                                        for j in i['secondaryNavigation']['items']]

    @staticmethod
    def _menu_titles_dropdown_additional(data, lang, target_text):
        data[lang + 'Main menu titles dropdown additional'] = [(k['title'], k['card']['description'],
                                                                k['card']['byline'],
                                                                k['card']['badge']['title'] if k['card']['badge'] != 'null' else None,
                                                                k['card']['button']['text'])
                                                                   for i in target_text
                                                                   for j in i['secondaryNavigation']['items']
                                                                   for k in j['tertiaryNavigation']['items']]

    @staticmethod
    def _menu_new_in_card_submenu(data, lang, target_text):
        data[lang + 'Main menu NEW IN submenu'] = [
            (j['title'], j['byline'], j['description'], j['badge']['title'] if j['badge'] != 'null' else None) for i in
            target_text if i['title'] == 'New In' or i['title'] == 'NEU' for j in
            i['submenuLayout']['grid']['items']]

    @staticmethod
    def _menu_right_side_text(data, lang, target_text):
        data[lang + 'Right menu visible text'] = (target_text['props']['initialState']['header']['menu']['items'][0]['desktop']['secondaryNavigation']['items'][0]['title'])

    def _menu_right_side_shop_button_text(self, data, url, lang):
        s = self._selenium()
        s.get(url)

        # Shopping button
        button_path = '//span[@class="styles_menuCart__26WiL"]'

        # Required window size to scrape desktop content
        s.set_window_size(1100, 818)

        button = WebDriverWait(s, 10).until(EC.visibility_of_element_located((By.XPATH, button_path)))
        button.click()

        # Shopping content
        content_path = '//div[@class="styles_cart__3oMRE styles_enterDone__2KGSy"]'
        content = WebDriverWait(s, 10).until(EC.visibility_of_element_located((By.XPATH, content_path)))
        content = content.text.strip()
        content = content.replace('\n', ', ')

        data[lang + 'Right menu interactive shopping button'] = content


class Banners(Settings):
    def __init__(self):
        super(Banners, self).__init__()

    def banners_content(self, eng_url, de_url):
        # Authorization required for get request
        auth = {
            'Authorization': 'Bearer 56If-j-ANNWSZ9Zk_8lp9EChokF6LNtKJDHC8eHMfSs',
            'If-None-Match': 'W/"16729328500904452549"'
        }

        s = cloudscraper.create_scraper()

        # English response
        eng_r = s.get(eng_url, headers=auth)
        eng_r.encoding = 'UTF-8'
        eng_content = eng_r.json()

        # Deutsch response
        de_r = s.get(de_url, headers=auth)
        de_r.encoding = 'UTF-8'
        de_content = de_r.json()

        data = {}

        # Lists od data; both for eng and de content
        eng_first_banner, de_first_banner = [], []
        eng_benefits, de_benefits = [], []
        eng_mobile, de_mobile = [], []
        eng_clothes, de_clothes = [], []
        eng_additional, de_additional = [], []
        eng_comments, de_comments = [], []

        # Main data root
        eng_all_contents = eng_content['includes']['Entry']
        de_all_contents = de_content['includes']['Entry']

        for eng_content, de_content in zip(eng_all_contents, de_all_contents):
            try:
                try:
                    # Content names as name of banner field
                    content_name = eng_content['fields']['contentName']
                except KeyError:
                    content_name = None

                # ENGLISH
                self.first_banner(eng_content, eng_first_banner)
                self.banner_benefits(eng_content, content_name, eng_benefits)
                self.banner_mobile(eng_content, content_name, eng_mobile)
                self.banner_clothes(eng_content, content_name, eng_clothes)
                self.over_brands_text(eng_content, eng_additional)
                self.comments_content(eng_content, content_name, eng_comments)

                # DEUTSCH
                self.first_banner(de_content, de_first_banner)
                self.banner_benefits(de_content, content_name, de_benefits)
                self.banner_mobile(de_content, content_name, de_mobile)
                self.banner_clothes(de_content, content_name, de_clothes)
                self.over_brands_text(de_content, de_additional)
                self.comments_content(de_content, content_name, de_comments)

                # Banner with animate mobile phone button's
                # if re.compile('.*FineTuneFit.*').match(str(content_button)):
                #     text = content['fields']['text']
                #     mobile.append(text)

            except KeyError:
                continue

        data[self.ENG + ' Home Banner Content'] = eng_first_banner
        data[self.DE + ' Home Banner Content'] = de_first_banner

        data[self.ENG + ' Banner Benefits Content'] = eng_benefits
        data[self.DE + ' Banner Benefits Content'] = de_benefits

        data[self.ENG + ' Banner Mobile Animation Content'] = eng_mobile
        data[self.DE + ' Banner Mobile Animation Content'] = de_mobile

        data[self.ENG + ' Banner Clothes Content'] = eng_clothes
        data[self.DE + ' Banner Clothes Content'] = de_clothes

        data[self.ENG + ' Additional Content'] = eng_additional
        data[self.DE + ' Additional Content'] = de_additional

        data[self.ENG + ' Comments Content'] = eng_comments
        data[self.DE + ' Comments Content'] = de_comments

        return data

    @staticmethod
    def first_banner(content, first_banner):
        try:
            typ = content['sys']['contentType']['sys']['id']
        except KeyError:
            typ = None
        try:
            badge = content['fields']['badgeType']
        except KeyError:
            badge = None
        if typ:
            if typ == 'carouselImage':
                title = content['fields']['title']
                subtitle = content['fields']['subtitle']
                first_banner.append(title)
                first_banner.append(subtitle)
        if badge:
            badge = content['fields']['title']
            first_banner.append(badge)

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
        path = content['fields']
        try:
            text = path['typeAlign']
        except KeyError:
            text = None
        if text:
            if text == 'icons-only':
                text = path['title']
                additional.append(text)

    @staticmethod
    def comments_content(content, content_name, comments):
        # Banner with comments
        if re.compile(r'(Testimonial|Testimonials) Homepage (First|second|Third|Fourth) (item|Item|Item )').match(str(content_name)):
            title = content['fields']['title']
            name = content['fields']['underTitle']
            comments.append(title)
            comments.append(name)


class Footer(Settings):
    def __init__(self):
        super(Footer, self).__init__()

    def footer_content(self, url, lang):
        s = self._selenium()
        s.get(url)
        time.sleep(3)
        data = {}

        sub_data = []
        sub_data.append(s.find_element_by_xpath('/html/body/div[1]/main/div/div[3]/footer/div[1]/div/div/div[1]/div/div/div').text.strip().replace('\n',', '))
        sub_data.append(s.find_element_by_xpath('//input[@id="email"]').get_attribute('placeholder'))
        sub_data.append(s.find_element_by_xpath('//div[@class="styles_footerBaseContent__15eHp"]').text.strip().replace('\n',', '))
        sub_data.append(s.find_element_by_xpath("//div[contains(@class, 'styles_footerWrap__26rQ6')]").text.strip().replace('\n', ', '))

        # Actions required to be able to scrape error info after not passing email AT ALL
        email = s.find_element_by_xpath('//input[@id="email"]')
        email.send_keys(Keys.END)
        email.click()
        country_switcher = '/html/body/div[1]/main/div/div[3]/div/div/div/p/span'
        country_switcher = s.find_element_by_xpath(country_switcher)

        # Double click xd
        for i in range(2):
            country_switcher.click()

        sub_data.append(s.find_element_by_xpath('//p[@class="form__error"]').text)

        email.click()
        email.send_keys('invalid_email')
        s.find_element_by_xpath('//button[@role="submit"]').click()
        sub_data.append(s.find_element_by_xpath('//p[@class="form__error"]').text)

        data[lang + 'FOOTER'] = sub_data
        return data


class BrandHomePage(SpokeScraperCore, Menu, Banners, Footer):

    def __init__(self):
        super(BrandHomePage, self).__init__()
        self.scrape_content()

    def scrape_content(self):
        """
        Scrape whole content related to HomePage
        """
        # For both lang; eng and de side by side in columns
        eng_url = 'https://spoke-london.com/gb'
        de_url = 'https://spoke-london.com/de/'
        banners_url_eng = 'https://cdn.contentful.com/spaces/amhdwl2zsv5z/environments/master/entries?sys.id=2HcDAp7cZd3Vpq5hEK4bMS&locale=en-GB&include=6'
        banners_url_de = 'https://cdn.contentful.com/spaces/amhdwl2zsv5z/environments/master/entries?sys.id=2HcDAp7cZd3Vpq5hEK4bMS&locale=de-DE&include=6'

        # Over navbar
        self.main_output_data(self.over_navbar_info(eng_url, self.ENG))
        self.main_output_data(self.over_navbar_info(de_url, self.DE))

        # Menu
        self.main_output_data(self.menu_content(eng_url, de_url))

        # Banners
        self.main_output_data(self.banners_content(banners_url_eng, banners_url_de))

        # Footer
        self.main_output_data(self.footer_content(eng_url, self.ENG))
        self.main_output_data(self.footer_content(de_url, self.DE))

        # Help button
        self.main_output_data(self.help_button_content(eng_url, self.ENG, 'en'))
        self.main_output_data(self.help_button_content(de_url, self.DE, 'de'))

        # Newsletter Popup
        eng_example_url = 'https://spoke-london.com/gb/pages/about'
        de_example_url = 'https://spoke-london.com/de/pages/about'
        self.main_output_data(self.newsletter_popup(eng_example_url, de_example_url))

    def help_button_content(self, url, lang, selenium_lang):
        # Get url by selenium also based on locale language
        s = self._selenium_lang(selenium_lang)
        s.get(url)
        time.sleep(3)
        data = {}
        sub_data = []

        # Find email and go to the bottom of page
        email = s.find_element_by_xpath('//input[@id="email"]')
        email.send_keys(Keys.END)

        # Switch to iframe which contains help_button
        iframe = WebDriverWait(s, 10).until(EC.visibility_of_element_located((By.XPATH, '//iframe[@id="launcher"]')))
        s.switch_to.frame(iframe)

        # Find help button and click
        help_button = s.find_element_by_xpath('//button[@aria-haspopup="true"]')
        sub_data.append(help_button.text)
        help_button.click()
        time.sleep(2)

        # Back from first iframe to default content
        s.switch_to.default_content()

        # Switch to iframe which contains help_button content after click
        iframe2 = WebDriverWait(s, 10).until(EC.visibility_of_element_located((By.XPATH, '//iframe[@id="webWidget"]')))
        s.switch_to.frame(iframe2)

        # Find help_button text after click
        help_button_text = s.find_element_by_xpath('//div[@data-embed="helpCenterForm"]').text.strip().replace('\n', ', ')
        help_placeholder = s.find_element_by_xpath('//input[@type="search"]').get_attribute('placeholder')

        sub_data.append(help_button_text)
        sub_data.append(help_placeholder)

        data[lang + 'HELP BUTTON'] = sub_data
        return data

    def newsletter_popup(self, *args):
        responses = []
        data = {}

        # TODO chuj sprawdz
        for lang in args:
            responses.append(self.get_request(lang))

        for lang, resp in zip(self.languages_list, responses):
            # Newsletter popup text
            newsletter_tree = html.fromstring(resp.text).xpath('//div[@data-lightbox="newsletter"]//text()')
            newsletter_data = [x.strip() for x in newsletter_tree if x]
            newsletter_data = list(filter(None, newsletter_data))

            data[lang + 'Newsletter POPUP'] = newsletter_data

        for lang, resp in zip(self.languages_list, responses):
            # Klarna popup text
            klarna_tree = html.fromstring(resp.text).xpath('//div[@data-lightbox="klarna"]//text()')
            klarna_data = [x.strip() for x in klarna_tree if x]
            klarna_data = list(filter(None, klarna_data))

            data[lang + 'Klarna POPUP'] = klarna_data

        return data


if __name__ == '__main__':
    BrandHomePage()
