import time
import cloudscraper
from bs4 import BeautifulSoup as bs
from lxml import html
from spoke.main import Settings, DataWriter


class ProductsDetails(Settings, DataWriter):
    def __init__(self):
        super(ProductsDetails, self).__init__()
        self.scrape_content()

    def scrape_content(self):

        urls = ['https://spoke-london.com/gb/products/stone-summerweights-2',
                'https://spoke-london.com/de/products/stone-summerweights-2']

        delivery_links = [
            'https://cdn.contentful.com/spaces/amhdwl2zsv5z/environments/master/entries?sys.id=1EGp9l4cH1DPBtAjMJlWBG&locale=en-GB',
            'https://cdn.contentful.com/spaces/amhdwl2zsv5z/environments/master/entries?sys.id=1EGp9l4cH1DPBtAjMJlWBG&locale=de-DE']

        # [self.free_delivery_info(url) for url in delivery_links]
        # [self.products_details_page_body(self.get_request(url)) for url in urls]

        # links1 = ['https://spoke-london.com/gb/products/stone-summerweights-2',
        #           'https://spoke-london.com/gb/products/charcoal',
        #           'https://spoke-london.com/gb/products/khaki-sharps',
        #           'https://spoke-london.com/gb/products/navy-stripe-tolo',
        #           'https://spoke-london.com/gb/products/charcoal-house-trouser',
        #           'https://spoke-london.com/gb/products/navy-stripe-tolo',
        #           'https://spoke-london.com/gb/products/broken-in',
        #           'https://spoke-london.com/gb/products/army-friday-shorts']
        #
        # links2 = ['https://spoke-london.com/de/products/stone-summerweights-2',
        #           'https://spoke-london.com/de/products/charcoal',
        #           'https://spoke-london.com/de/products/khaki-sharps',
        #           'https://spoke-london.com/de/products/navy-stripe-tolo',
        #           'https://spoke-london.com/de/products/charcoal-house-trouser',
        #           'https://spoke-london.com/de/products/navy-stripe-tolo',
        #           'https://spoke-london.com/de/products/broken-in',
        #           'https://spoke-london.com/de/products/army-friday-shorts']

        s = cloudscraper.create_scraper()
        r = s.get('https://spoke-london.com/eu/sitemap_products_1.xml')
        soup = bs(r.text, 'lxml')

        links_eu = [i.text for i in soup.find_all('loc')]

        links_us = [i.replace('eu', 'us') for i in links_eu]
        links_de = [i.replace('eu', 'de') for i in links_eu]

        links = [i for j in zip(links_us, links_de) for i in j]

        [self.free_delivery_info(url) for url in delivery_links]

        for url in links:
            resp = self.get_response(url)
            if resp:
                self.products_details_page_body(resp)

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

        properties = [title, byline, types, color, title_above_sizes_1, build, build_desc,
                      title_above_sizes_2, title_under_sizes_2, size_helper, leg_types, quick_links_text,
                      basket_button_text, button_labels]

        # [(self.clean_data(x)) for x in properties]
        for idx, x in enumerate(properties):
            data[f'Text {idx}'] = self.clean_data(x)
            if x is size_helper:
                data['Size Helper'] = self.clean_data(x)
            elif x is button_labels:
                data['Button labels'] = self.clean_data(x)

        for idx, x in enumerate(button_divs):
            text = x.xpath('string()')
            data[f'PRODUCT DESC {idx}'] = text

        self.products_details_output(data)


    def free_delivery_info(self, url):
        content = self.get_banners(url)

        info = content['items'][0]['fields']['genericText']

        data = {'DELIVERY NOTE': info}
        self.products_details_output(data)
