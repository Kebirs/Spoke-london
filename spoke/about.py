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
        sec_menu = [x.strip() for x in sec_menu if x]
        sec_menu = list(filter(None, sec_menu))
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

    def first_banner(self, url):
        data = {}
        text = html.fromstring(url.text).xpath('//h1[@class="banner__title"]//text()')
        text = [x.strip() for x in text if x]
        text = list(filter(None, text))
        data['First banner'] = text

        self.about_output(data)

    def under_first_banner_text(self, url):
        data = {}

        title = html.fromstring(url.text).xpath('//h2[@class="blueprint__title"]/text()')
        title = [x.strip().replace('\n', '').replace('  ', '') for x in title]
        data['Under first banner blueprint title'] = title

        lines = html.fromstring(url.text).xpath('//p[@class="blueprint__line"]/text()')
        lines = [x.strip().replace('\n', '').replace('  ', '') for x in lines]

        data['Under first banner blueprint description'] = lines

        self.about_output(data)

    def benefits_banners(self, url):
        pass

    def support_divs(self, url):
        pass

    def social_media_title(self, url):
        pass


if __name__ == '__main__':
    AboutPage()
