from lxml import html
from spoke.main import Settings, DataWriter


class LogInPage(Settings, DataWriter):
    def __init__(self):
        super(LogInPage, self).__init__()
        self.scrape_content()

    def scrape_content(self):
        urls = ['https://gb.spoke-london.com/account/login',
                'https://de.spoke-london.com/account/login']

        [self.log_in_page_body(self.get_request(url)) for url in urls]

    def log_in_page_body(self, url):
        data = {}


        self.newsletter_output(data)