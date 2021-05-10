import time
import cloudscraper
import re
from lxml import html

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support import expected_conditions as EC
from spoke.main import DataWriter, Settings


class Menu(Settings, DataWriter):
    def __init__(self):
        super(Menu, self).__init__()

    def over_navbar_info(self, url):
        data = {}

        script_data = self.json_script_data(url)
        over_navbar_text = script_data['props']['initialState']['header']['menu']['items'][0]['flashBanner']['flashBannerItems']['items'][0]['bannerName']
        data['Brand Homepage - Over Navbar Info'] = over_navbar_text

        self.home_output(data)

    def menu_content(self, url):
        """
        Scrape whole data related to MENU content; dropdown menu after hover included
        :param url:
        """
        script_data = self.json_script_data(url)

        # Target text related to menu
        header_text = script_data['props']['initialState']['header']['menu']['items'][0]['desktop']['primaryNavigation']['items']

        data = {}

        self._menu_titles(data, header_text)
        self._menu_titles_dropdown(data, header_text)
        self._menu_titles_dropdown_additional(data, header_text)
        self._menu_new_in_card_submenu(data, header_text)
        self._menu_right_side_text(data, script_data)
        self._menu_right_side_shop_button_text(data, url)

        self.home_output(data)

    @staticmethod
    def _menu_titles(data, target_text):
        data['Main menu titles'] = [(i['title']) for i in target_text]

    @staticmethod
    def _menu_titles_dropdown(data, target_text):
        data['Main menu titles dropdown'] = [(j['title'])
                                                        for i in target_text
                                                        for j in i['secondaryNavigation']['items']]

    @staticmethod
    def _menu_titles_dropdown_additional(data, target_text):
        data['Main menu titles dropdown additional'] = [(k['title'], k['card']['description'],
                                                                k['card']['byline'],
                                                                k['card']['badge']['title'] if k['card']['badge'] != 'null' else None,
                                                                k['card']['button']['text'])
                                                                   for i in target_text
                                                                   for j in i['secondaryNavigation']['items']
                                                                   for k in j['tertiaryNavigation']['items']]

    @staticmethod
    def _menu_new_in_card_submenu(data, target_text):
        data['Main menu NEW IN submenu'] = [
            (j['title'], j['byline'], j['description'], j['badge']['title'] if j['badge'] != 'null' else None) for i in
            target_text if i['title'] == 'New In' or i['title'] == 'NEU' for j in
            i['submenuLayout']['grid']['items']]

    @staticmethod
    def _menu_right_side_text(data, target_text):
        data['Right menu visible text'] = (target_text['props']['initialState']['header']['menu']['items'][0]['desktop']['secondaryNavigation']['items'][0]['title'])

    def _menu_right_side_shop_button_text(self, data, url):
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

        data['Right menu interactive shopping button'] = content


class Banners(Settings, DataWriter):
    def __init__(self):
        super(Banners, self).__init__()

    def banners_content(self, url):
        # Authorization required for get request
        auth = {
            'Authorization': 'Bearer 56If-j-ANNWSZ9Zk_8lp9EChokF6LNtKJDHC8eHMfSs',
            # 'If-None-Match': 'W/"16729328500904452549"'
            'If-None-Match': 'W/"14186816362649224049"'
        }

        s = cloudscraper.create_scraper()

        r = s.get(url, headers=auth)
        r.encoding = 'UTF-8'
        content = r.json()

        data = {}

        # Lists od data; both for eng and de content
        first_banner = []
        benefits = []
        mobile = []
        clothes = []
        additional = []
        comments = []

        # Main data root
        all_contents = content['includes']['Entry']

        for content in all_contents:
            try:
                try:
                    # Content names as name of banner field
                    content_name = content['fields']['contentName']
                except KeyError:
                    content_name = None

                # ENGLISH
                self.first_banner(content, first_banner)
                self.banner_benefits(content, content_name, benefits)
                self.banner_mobile(content, content_name, mobile)
                self.banner_clothes(content, content_name, clothes)
                self.over_brands_text(content, additional)
                self.comments_content(content, content_name, comments)

                # Banner with animate mobile phone button's
                # if re.compile('.*FineTuneFit.*').match(str(content_button)):
                #     text = content['fields']['text']
                #     mobile.append(text)

            except KeyError:
                continue

        data['Home Banner Content'] = first_banner
        data['Banner Benefits Content'] = benefits
        data['Banner Mobile Animation Content'] = mobile
        data['Banner Clothes Content'] = clothes
        data['Additional Content'] = additional
        data['Comments Content'] = comments

        self.home_output(data)

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


class Footer(Settings, DataWriter):
    def __init__(self):
        super(Footer, self).__init__()

    def footer_content(self, url):
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

        data['FOOTER'] = sub_data

        self.home_output(data)


class BrandHomePage(Menu, Banners, Footer):
    def __init__(self):
        super(BrandHomePage, self).__init__()
        self.scrape_homepage_content()

    def scrape_homepage_content(self):
        """
        Scrape whole content related to HomePage
        """
        # For both lang; eng and de side by side in columns
        urls = ['https://spoke-london.com/gb',
                'https://spoke-london.com/de/']

        cdn_id = self.get_cdn_id('https://spoke-london.com')

        banners_urls = [f'https://cdn.contentful.com/spaces/amhdwl2zsv5z/environments/master/entries?sys.id={cdn_id}&locale=en-GB&include=6',
                        f'https://cdn.contentful.com/spaces/amhdwl2zsv5z/environments/master/entries?sys.id={cdn_id}&locale=de-DE&include=6']

        example_urls = ['https://spoke-london.com/gb/pages/about',
                        'https://spoke-london.com/de/pages/about']

        # Over navbar
        [self.over_navbar_info(url) for url in urls]
        # # Menu
        # [self.menu_content(url) for url in urls]
        # Banners
        # [self.banners_content(url) for url in banners_urls]
        # # Footer
        # [self.footer_content(url) for url in urls]
        # Help button
        # self.help_button_content(urls[0], 'en')  # ENGLISH url
        # self.help_button_content(urls[1], 'de')  # DEUTSCH url
        # # Newsletter Popup
        # [self.newsletter_popup(url) for url in example_urls]

    def help_button_content(self, url, selenium_lang):
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

        data['HELP BUTTON'] = sub_data

        self.home_output(data)

    def newsletter_popup(self, url):

        data = {}

        resp = self.get_request(url)

        # Newsletter popup text
        newsletter_tree = html.fromstring(resp.text).xpath('//div[@data-lightbox="newsletter"]//text()')
        newsletter_data = [x.strip() for x in newsletter_tree if x]
        newsletter_data = list(filter(None, newsletter_data))

        data['Newsletter POPUP'] = newsletter_data

        # Klarna popup text
        klarna_tree = html.fromstring(resp.text).xpath('//div[@data-lightbox="klarna"]//text()')
        klarna_data = [x.strip() for x in klarna_tree if x]
        klarna_data = list(filter(None, klarna_data))

        data['Klarna POPUP'] = klarna_data

        self.home_output(data)
