from spoke.main import DataWriter, Settings
from lxml import html


class SecondMenu(Settings, DataWriter):
    def __init__(self):
        super(SecondMenu, self).__init__()

    def menu_content_about(self, url):
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
        self.scrape_about_content()

    def scrape_about_content(self):
        urls = ['https://spoke-london.com/gb/pages/about',
                'https://spoke-london.com/de/pages/about']

        [self.menu_content_about(url) for url in urls]


if __name__ == '__main__':
    AboutPage()
