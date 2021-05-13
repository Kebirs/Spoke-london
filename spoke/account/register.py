from lxml import html
from spoke.main import Settings, DataWriter


class RegisterPage(Settings, DataWriter):
    def __init__(self):
        super(RegisterPage, self).__init__()
        self.scrape_content()

    def scrape_content(self):
        urls = ['https://gb.spoke-london.com/account/register',
                'https://de.spoke-london.com/account/register']

        [self.register_page_body(self.get_request(url)) for url in urls]

    def register_page_body(self, url):
        data = {}


        self.newsletter_output(data)