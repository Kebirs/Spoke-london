from spoke.main import DataWriter, Settings
from lxml import html


class NewsletterPage(Settings, DataWriter):
    def __init__(self):
        super(NewsletterPage, self).__init__()
        self.scrape_content()

    def scrape_content(self):
        urls = ['https://spoke-london.com/gb/pages/newsletter-confirmation-page',
                'https://spoke-london.com/de/pages/newsletter-confirmation-page']

        [self.newsletter_page_body(self.get_response(url)) for url in urls]

    def newsletter_page_body(self, url):
        data = {}
        data['Link'] = url.url

        title = "//div[contains(@class, 'landing__content')]/h1/text()"
        notes = "//div[contains(@class, 'landing__content')]/h1/../p/text()"
        button = "//a[contains(@data-analytics-props, 'Newsletter Signup Confirmation')]/text()"

        title = html.fromstring(url.text).xpath(title)
        notes = html.fromstring(url.text).xpath(notes)
        button = html.fromstring(url.text).xpath(button)

        title = self.clean_data(title)
        notes = self.clean_data(notes)
        button = self.clean_data(button)

        data['Newsletter Title'] = title
        data['Newsletter Notes'] = notes
        data['Newsletter Button'] = button

        self.newsletter_output(data)