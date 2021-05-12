import time

from lxml import html
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from spoke.main import Settings, DataWriter


class SizeChartBanners(Settings, DataWriter):
    def __init__(self):
        super(SizeChartBanners, self).__init__()

    def banners_content(self, url):
        content = self.get_banners(url)
        sub_data = []
        static_data_title = content['items'][0]['fields']['title']
        sub_data.append(static_data_title)

        static_data_desc = content['items'][0]['fields']['description']
        sub_data.append(static_data_desc)

        all_contents = content['includes']['Entry']

        for content in all_contents:
            try:
                title = content['fields']['title']
                desc = content['fields']['description']

                sub_data.append(title)
                sub_data.append(desc)
            except KeyError:
                byline = content['fields']['byline']
                sub_data.append(byline)

        sub_data = self.clean_data(sub_data)

        data = {'Banners Content': sub_data}
        self.size_charts_output(data)


class HowToMeasureDynamic(Settings, DataWriter):
    def __init__(self):
        super(HowToMeasureDynamic, self).__init__()

    def how_to_measure_content(self, url):
        self.how_to_measure_dynamic_banners(url)

    def how_to_measure_dynamic_banners(self, url):
        s = self._selenium()
        s.get(url.url)
        data = {}
        sub_data = []

        time.sleep(5)
        cookies = '//div[@class="styles_gdprContent__QxL-q grid"]//button/span'
        cookies = WebDriverWait(s, 10).until(EC.element_to_be_clickable((By.XPATH, cookies)))
        cookies.click()
        # s.execute_script("arguments[0].click();", cookies)

        time.sleep(2)
        button = '//div[@class="styles_oldFashioned__item__button__1zaHn"]/button'
        button = WebDriverWait(s, 10).until(EC.visibility_of_element_located((By.XPATH, button)))
        # button = s.find_element_by_xpath(button)
        button.click()
        time.sleep(1)

        title = '//div[@class="modal__content"]//h3'
        byline = '//div[@class="modal__content"]//h3/../p'
        nav = '//div[@class="modal__content"]//nav'

        title = s.find_element_by_xpath(title).text
        byline = s.find_element_by_xpath(byline).text
        nav = s.find_element_by_xpath(nav).text.replace('\n', ', ')

        sub_data.append(title)
        sub_data.append(byline)
        sub_data.append(nav)

        sub_data = self.clean_data(sub_data)

        source = html.fromstring(s.page_source)
        section_xpath = '//div[@data-index="{}"]//text()'

        waist = source.xpath(section_xpath.format(0))
        rise = source.xpath(section_xpath.format(1))
        thigh = source.xpath(section_xpath.format(2))
        knee = source.xpath(section_xpath.format(3))
        leg = source.xpath(section_xpath.format(4))

        contents_list = {'waist': waist,
                         'rise': rise,
                         'thigh': thigh,
                         'knee': knee,
                         'leg': leg}

        data['HOW TO MEASURE header text'] = sub_data

        for k, v in contents_list.items():
            data[f'Section {k}'] = self.clean_data(v)

        self.size_charts_output(data)


class SizeChartsPage(SizeChartBanners, HowToMeasureDynamic):
    def __init__(self):
        super(SizeChartsPage, self).__init__()
        self.scrape_banners_content()
        self.scrape_static_content()

    def scrape_banners_content(self):
        cdn_id = '3Y2dy1zyiarkO6N2jADqra'
        banners_urls = [
            f'https://cdn.contentful.com/spaces/amhdwl2zsv5z/environments/master/entries?sys.id={cdn_id}&locale=en-GB&include=10',
            f'https://cdn.contentful.com/spaces/amhdwl2zsv5z/environments/master/entries?sys.id={cdn_id}&locale=de-DE&include=10']

        [self.banners_content(url) for url in banners_urls]

    def scrape_static_content(self):
        urls = ['https://spoke-london.com/pages/tops-size-chart',
                'https://spoke-london.com/de/pages/tops-size-chart']

        [self.size_charts_body(self.get_request(url)) for url in urls]

    def size_charts_body(self, url):
        self.all_possible_table_col_names(url)
        self.charts_header(url)
        self.table_buttons_text(url)
        self.under_table_note(url)
        self.measure_diy_title(url)
        self.measure_diy_boxes(url)
        self.how_to_measure_content(url)

    def charts_header(self, url):
        data = {}

        path = '//div[@class="styles_sizeChart__wrapper__3KjAo"]/header//text()'
        header_tree = html.fromstring(url.text).xpath(path)
        header_tree = self.clean_data(header_tree)

        data['Over Table Content'] = header_tree

        line_text = bs(url.text, 'lxml').find('div',
                                              {'class': 'styles_sizeChart__titleContainer__2sZ4T'}).h3.text.strip()

        data['Over Table Content Additional'] = line_text

        self.size_charts_output(data)

    def table_buttons_text(self, url):
        buttons = html.fromstring(url.text).xpath('//div[@class="styles_sizeChart__tabs__-eNj5  "]//text()')
        buttons = self.clean_data(buttons)

        data = {'Table Buttons': buttons}

        self.size_charts_output(data)

    def all_possible_table_col_names(self, url):
        s = self._selenium()
        s.get(url.url)
        time.sleep(5)

        cols_path = '//th[@scope="col"]'
        primary_button = '//header[@class="styles_sizeChart__header__hqJBG"]//button'
        navs = '//nav/a'

        primary_button = s.find_element_by_xpath(primary_button)
        navs = s.find_elements_by_xpath(navs)

        sub_data = []
        for nav in navs:
            primary_button.click()
            nav.click()
            cols = s.find_elements_by_xpath(cols_path)
            for col in cols:
                sub_data.append(col.text)

        sub_data = self.clean_data(sub_data)

        data = {'Table column names': sub_data}

        self.size_charts_output(data)

    def under_table_note(self, url):
        note = bs(url.text, 'lxml').find('p', {'class': 'styles_sizeChart__note__3QY6s'}).text.strip()
        data = {'Under Table Note': note}
        self.size_charts_output(data)

    def measure_diy_title(self, url):
        sub_data = []

        title = html.fromstring(url.text).xpath('//h2[@class="styles_oldFashioned__title__sBVGp"]/text()')
        byline = html.fromstring(url.text).xpath('//p[@class="styles_oldFashioned__byline__2VZyD"]/text()')

        sub_data.append(title[0])
        sub_data.append(byline[0])

        sub_data = self.clean_data(sub_data)

        data = {'Measure DIY title': sub_data}
        self.size_charts_output(data)

    def measure_diy_boxes(self, url):
        boxes = html.fromstring(url.text).xpath('//li[@class="styles_oldFashioned__item__2270W grid__item"]//text()')
        boxes = self.clean_data(boxes)

        data = {'Measure DIY boxes content': boxes}
        self.size_charts_output(data)
