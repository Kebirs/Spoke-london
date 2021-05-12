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
        data = {}

        sections = "//*[contains(@class, 'styles_contact__section')]"
        title = "//h2[contains(@class, 'contact__title')]/text()"
        title = html.fromstring(url.text).xpath(title)
        title = self.clean_data(title)
        data[f'CONTACT US Title'] = title

        sections = html.fromstring(url.text).xpath(sections)
        for i, section in enumerate(sections):
            text = section.xpath(f"//*[contains(@class, 'styles_contact__section')][{i+1}]//text()")
            text = self.clean_data(text)
            data[f'CONTACT US Section {i+1}'] = text

        self.contact_us_output(data)
