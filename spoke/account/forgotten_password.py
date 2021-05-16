import time
import cloudscraper
from lxml import html
from spoke.main import Settings, DataWriter


class ForgottenPasswordPage(Settings, DataWriter):
    def __init__(self):
        super(ForgottenPasswordPage, self).__init__()
        self.scrape_content()

    def scrape_content(self):
        urls = ['https://gb.spoke-london.com/pages/forgotten-password',
                'https://de.spoke-london.com/pages/forgotten-password']

        [self.forgotten_password_page_body(self.get_response(url)) for url in urls]

    def forgotten_password_page_body(self, url):
        data = {}
        s = self._selenium()
        s.get(url.url)
        root = "//form[contains(@class, 'forgotten-password')]"

        title = f"{root}//h2[@class='form__title']//text()"
        email = f"{root}//input[@name='email']"
        button = f"{root}//span[@class='button__content']"

        title = html.fromstring(url.text).xpath(title)
        email_hint = html.fromstring(url.text).xpath(email + '/@placeholder')
        button_text = html.fromstring(url.text).xpath(button + '//text()')

        properties = {'Title': title,
                      'Email hint': email_hint,
                      'Button Text': button_text}
        for k, v in properties.items():
            data[k] = self.clean_data(v)

        self.forgotten_password_output(data)
