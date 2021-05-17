from lxml import html
from spoke.main import Settings, DataWriter


class RegisterPage(Settings, DataWriter):
    def __init__(self):
        super(RegisterPage, self).__init__()
        self.scrape_content()

    def scrape_content(self):
        urls = ['https://gb.spoke-london.com/account/register',
                'https://de.spoke-london.com/account/register']

        [self.register_page_body(self.get_response(url)) for url in urls]

    def register_page_body(self, url):
        data = {}
        data['Link'] = url.url

        root = "//form[@id='create_customer']"

        title = f"{root}//h2[@class='form__title']//text()"
        byline = f"{root}//p[@class='form__byline']//text()"

        first_name_hint = f"{root}//input[@name='customer[first_name]']/@placeholder"
        last_name_hint = f"{root}//input[@name='customer[last_name]']/@placeholder"
        email_hint = f"{root}//input[@name='customer[email]']/@placeholder"
        password_hint = f"{root}//input[@name='customer[password]']/@placeholder"

        required_fields = f"{root}//div[@class='grid'][1]//text()"
        over_button_notes = f"{root}//div[contains(@class, 'gdpr-fields')]//text()"
        button = f"{root}//span[@class='button__content']//text()"

        title = html.fromstring(url.text).xpath(title)
        byline = html.fromstring(url.text).xpath(byline)
        first_name_hint = html.fromstring(url.text).xpath(first_name_hint)
        last_name_hint = html.fromstring(url.text).xpath(last_name_hint)
        email_hint = html.fromstring(url.text).xpath(email_hint)
        password_hint = html.fromstring(url.text).xpath(password_hint)
        required_fields = html.fromstring(url.text).xpath(required_fields)
        over_button_notes = html.fromstring(url.text).xpath(over_button_notes)
        button = html.fromstring(url.text).xpath(button)

        properties = {'Title': title,
                      'Byline': byline,
                      'First name hint': first_name_hint,
                      'Last name hint': last_name_hint,
                      'Email hint': email_hint,
                      'Password hint': password_hint,
                      'Required fields': required_fields,
                      'Over button notes': over_button_notes,
                      'Button Text': button}

        for k, v in properties.items():
            data[k] = self.clean_data(v)

        self.register_output(data)