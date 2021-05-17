import time
import cloudscraper
import selenium.common.exceptions
from bs4 import BeautifulSoup as bs
from lxml import html
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from spoke.main import Settings, DataWriter


class ProductsDetails(Settings, DataWriter):
    def __init__(self):
        super(ProductsDetails, self).__init__()
        self.scrape_content()

    def scrape_content(self):
        delivery_links = [
            'https://cdn.contentful.com/spaces/amhdwl2zsv5z/environments/master/entries?sys.id=1EGp9l4cH1DPBtAjMJlWBG&locale=en-GB',
            'https://cdn.contentful.com/spaces/amhdwl2zsv5z/environments/master/entries?sys.id=1EGp9l4cH1DPBtAjMJlWBG&locale=de-DE'
        ]

        s = cloudscraper.create_scraper()
        r = s.get('https://spoke-london.com/eu/sitemap_products_1.xml')
        soup = bs(r.text, 'lxml')

        links_eu = [i.text for i in soup.find_all('loc')]
        links_us = [i.replace('eu', 'us') for i in links_eu]
        links_de = [i.replace('eu', 'de') for i in links_eu]
        links = [i for j in zip(links_eu, links_de) for i in j]

        for url in links:
            resp = self.get_response(url)
            if resp:
                self.products_details_page_body(resp)

        below_prod_urls = ['https://spoke-london.com/gb/products/olive-flex',
                           'https://spoke-london.com/de/products/olive-flex']
        [self.below_product_content(url) for url in below_prod_urls]

        [self.free_delivery_info(url) for url in delivery_links]

    def products_details_page_body(self, url):
        data = {}
        data['Link'] = url.url
        print(url.url)

        section_titles = "(//h2[@class='styles_productForm__subtitle__vIIdt'])[{}]/span/text()"

        title = "//h1//text()"
        byline = "//h3[contains(@class, 'productForm__byline')]/text()"
        types = "//div[@class='grid__container']/a[contains(@class, 'fabricTab')]/../a/text()"
        color = "//h2[contains(@class, 'productForm__color')]/text()"
        title_above_sizes_1 = section_titles.format(1)
        build = section_titles.format(2)
        build_desc = "//li[contains(@class, 'build')]/p[contains(@class, 'productForm__buildDescription')]/text()"
        desc_of_3_blocks_additional = ""
        title_above_sizes_2 = section_titles.format(3)
        title_under_sizes_2 = section_titles.format(4)
        size_helper = "//div[contains(@class, 'sizeHelper__description')]//text()"
        leg_desc_helper = ""
        leg_types = "//ul[contains(@class, 'productForm__options')]/li[contains(@class, 'options')]//text()"
        quick_links_text = "//div[contains(@class, 'productForm__quickLinks')]//text()"
        basket_button_text = "//button[contains(@class, 'add-to-cart')]/span/text()"
        button_labels = "//div[@class='styles_accordion__section__3yPCM']//button/@label"
        button_divs_text = "//div[@class='styles_accordion__section__3yPCM']/div"

        main_title1_below_product = "//p[contains(@class, 'productPageYmal__title')]/text()"


        title = html.fromstring(url.text).xpath(title)
        byline = html.fromstring(url.text).xpath(byline)
        types = html.fromstring(url.text).xpath(types)
        color = html.fromstring(url.text).xpath(color)
        title_above_sizes_1 = html.fromstring(url.text).xpath(title_above_sizes_1)
        build = html.fromstring(url.text).xpath(build)
        build_desc = html.fromstring(url.text).xpath(build_desc)
        title_above_sizes_2 = html.fromstring(url.text).xpath(title_above_sizes_2)
        title_under_sizes_2 = html.fromstring(url.text).xpath(title_under_sizes_2)
        size_helper = html.fromstring(url.text).xpath(size_helper)
        leg_types = html.fromstring(url.text).xpath(leg_types)
        quick_links_text = html.fromstring(url.text).xpath(quick_links_text)
        basket_button_text = html.fromstring(url.text).xpath(basket_button_text)
        button_labels = html.fromstring(url.text).xpath(button_labels)
        button_divs = html.fromstring(url.text).xpath(button_divs_text)
        main_title1_below_product = html.fromstring(url.text).xpath(main_title1_below_product)

        properties = {
            'Title': title,
            'Byline': byline,
            'Types': types,
            'Color': color,
            'Title above sizes_1': title_above_sizes_1,
            'Build': build,
            'Build desc': build_desc,
            'Title above sizes 2': title_above_sizes_2,
            'Title under sizes 2': title_under_sizes_2,
            'Size helper': size_helper,
            'Leg types': leg_types,
            'Quick links text': quick_links_text,
            'Basket button text': basket_button_text,
            'Button labels': button_labels,
            'Main title1 below product': main_title1_below_product
        }

        # [(self.clean_data(x)) for x in properties]
        # for idx, x in enumerate(properties):
        #     data[f'Text {idx}'] = self.clean_data(x)
        #     if x is size_helper:
        #         data['Size Helper'] = self.clean_data(x)
        #     elif x is button_labels:
        #         data['Button labels'] = self.clean_data(x)

        for k, v in properties.items():
            data[k] = self.clean_data(v)

        if len(button_divs) == 0:
            button_divs = 'x'

        for idx, x in enumerate(button_divs):
            try:
                text = x.xpath('string()')
            except Exception:
                text = ''

            data[f'PRODUCT DESC {idx + 1}'] = text

        self.products_details_output(data)

    def free_delivery_info(self, url):
        content = self.get_banners(url)

        info = content['items'][0]['fields']['genericText']

        data = {'DELIVERY NOTE': info}
        self.products_details_output(data)

    def below_product_content(self, url):
        data = {}
        s = self._selenium()
        data['Link'] = url
        s.get(url)

        ex_content_load = "//h1[contains(@class, 'productForm__title')]"
        WebDriverWait(s, 10).until(EC.presence_of_element_located((By.XPATH, ex_content_load)))

        y = 1000
        for timer in range(0, 8):
            s.execute_script("window.scrollTo(0, " + str(y) + ")")
            y += 1000
            time.sleep(0.1)

        time.sleep(1)

        main_title2_below_product = "(//div[contains(@class, 'sectionHeader__byline')]//p[contains(@class, 'byline--secondary')])[2]/text()"
        subtitle_title2_below_product = "(//h2[contains(@class, 'title--secondary')])[2]/text()"
        main_title3_below_product_main = "(//div[contains(@class, 'sectionHeader__byline')]//p[contains(@class, 'byline--secondary')])[3]/text()"
        subtitle_title3_below_product_main = "(//h2[contains(@class, 'title--secondary')])[3]/text()"

        main_title2_below_product = html.fromstring(s.page_source).xpath(main_title2_below_product)
        subtitle_title2_below_product = html.fromstring(s.page_source).xpath(subtitle_title2_below_product)
        main_title3_below_product_main = html.fromstring(s.page_source).xpath(main_title3_below_product_main)
        subtitle_title3_below_product_main = html.fromstring(s.page_source).xpath(subtitle_title3_below_product_main)

        properties = {
            'Main Title 2': main_title2_below_product,
            'Subtitle of Title 2': subtitle_title2_below_product,
            'Main Title 3': main_title3_below_product_main,
            'Subtitle of Title 3': subtitle_title3_below_product_main
        }

        for k, v in properties.items():
            data[f'BELOW PRODUCT {k}'] = self.clean_data(v)

        self.products_details_output(data)




