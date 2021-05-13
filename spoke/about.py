from spoke.main import DataWriter, Settings
from lxml import html


class SecondMenu(Settings, DataWriter):
    def __init__(self):
        super(SecondMenu, self).__init__()

    def menu_content_about(self, url):
        # TODO: Split it ...
        data = {}
        resp = self.get_request(url)
        sec_menu = html.fromstring(resp.text).xpath('//header//text()')
        sec_menu = self.clean_data(sec_menu)
        data['Second Menu Text'] = sec_menu

        self.about_output(data)


class AboutPage(SecondMenu):
    def __init__(self):
        super(AboutPage, self).__init__()
        self.scrape_content()

    def scrape_content(self):
        urls = ['https://spoke-london.com/gb/pages/about',
                'https://spoke-london.com/de/pages/about']

        [self.menu_content_about(url) for url in urls]
        # [self.first_banner(self.get_request(url)) for url in urls]
        [self.about_page_body(self.get_request(url)) for url in urls]

    def about_page_body(self, url):
        self.first_banner(url)
        self.under_first_banner_text(url)
        self.benefits_banners(url)
        self.support_divs(url)
        self.social_media_title(url)

    def first_banner(self, url):
        data = {}
        text = html.fromstring(url.text).xpath('//h1[@class="banner__title"]//text()')
        text = self.clean_data(text)
        data['First banner'] = text

        self.about_output(data)

    def under_first_banner_text(self, url):
        data = {}

        title = html.fromstring(url.text).xpath('//h2[@class="blueprint__title"]/text()')
        title = self.clean_data(title)
        data['Under first banner blueprint title'] = title

        lines = html.fromstring(url.text).xpath('//p[@class="blueprint__line"]/text()')
        lines = self.clean_data(lines)

        data['Under first banner blueprint description'] = lines

        self.about_output(data)

    def benefits_banners(self, url):
        data = {}

        banner_titles = html.fromstring(url.text).xpath('//div[@class="formula__container grid__container"]//span//text()')
        banner_titles = self.clean_data(banner_titles)
        data['Banners Titles'] = banner_titles

        banner_descriptions = html.fromstring(url.text).xpath('//div[@class="formula__container grid__container"]//li//text()')
        banner_descriptions = self.clean_data(banner_descriptions)
        data['Banners Descriptions'] = banner_descriptions

        button = html.fromstring(url.text).xpath('//a[@data-relative="true"]/span[@class="button__content"]/text()')
        data['Under Banners button'] = button[0].strip()

        self.about_output(data)

    def support_divs(self, url):
        data = {}

        first_box = html.fromstring(url.text).xpath('//div[@class="boxes__box grid__item"][1]//text()')
        second_box = html.fromstring(url.text).xpath('//div[@class="boxes__box grid__item"][2]//text()')

        first_box = self.clean_data(first_box)
        data['First Support Box'] = first_box

        second_box = self.clean_data(second_box)
        data['Second Suppoer Box'] = second_box

        self.about_output(data)

    def social_media_title(self, url):

        title = html.fromstring(url.text).xpath('//section[@class="socialise grid grid--column grid--gutter grid--horizontal-center"]//h3/text()')
        title = self.clean_data(title)

        data = {'Socialise title': title}

        self.about_output(data)




if __name__ == '__main__':
    AboutPage()
