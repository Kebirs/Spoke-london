from spoke.main import DataWriter, Settings
from lxml import html


class ContactUsPage(Settings, DataWriter):
    def __init__(self):
        super(ContactUsPage, self).__init__()
        self.scrape_content()

    def scrape_content(self):
        urls = ['https://spoke-london.com/gb/pages/contact-us',
                'https://spoke-london.com/de/pages/contact-us']

        [self.contact_us_page_body(self.get_request(url)) for url in urls]

    def contact_us_page_body(self, url):
        pass
