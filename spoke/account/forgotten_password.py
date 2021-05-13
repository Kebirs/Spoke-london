from lxml import html
from spoke.main import Settings, DataWriter


class ForgottenPasswordPage(Settings, DataWriter):
    def __init__(self):
        super(ForgottenPasswordPage, self).__init__()
        self.scrape_content()

    def scrape_content(self):
        urls = ['https://gb.spoke-london.com/pages/forgotten-password',
                'https://de.spoke-london.com/pages/forgotten-password']

        [self.forgotten_password_page_body(self.get_request(url)) for url in urls]

    def forgotten_password_page_body(self, url):
        data = {}


        self.newsletter_output(data)