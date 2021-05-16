from lxml import html
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from spoke.main import Settings, DataWriter


class LogInPage(Settings, DataWriter):
    def __init__(self):
        super(LogInPage, self).__init__()
        self.scrape_content()

    def scrape_content(self):
        urls = ['https://gb.spoke-london.com/account/login?flash=registration-completed',
                'https://de.spoke-london.com/account/login?flash=registration-completed']

        [self.log_in_page_body(self.get_response(url)) for url in urls]

    def log_in_page_body(self, url):
        data = {}
        s = self._selenium()
        root = "//form[@id='customer_login']"

        top_flash = "//div[@class='top__flashes']"
        title = f"{root}//h2[@class='form__title']//text()"
        byline = f"{root}//p[@class='form__byline']//text()"
        email_hint = f"{root}//input[@name='customer[email]']/@placeholder"
        password_hint = f"{root}//input[@name='customer[password]']/@placeholder"
        email_error = f"{root}//p[contains(@class, 'form__error')]//text()"
        button = f"{root}//span[@class='button__content']//text()"
        forgotten_pass = f"{root}//p[@class='form__link']//text()"
        register = f"{root}//p[contains(@class, 'form__link--separator')]//text()"

        s.get(url.url)
        top_flash = WebDriverWait(s, 10).until(EC.visibility_of_element_located((By.XPATH, top_flash))).text

        title = html.fromstring(url.text).xpath(title)
        byline = html.fromstring(url.text).xpath(byline)
        email_hint = html.fromstring(url.text).xpath(email_hint)
        password_hint = html.fromstring(url.text).xpath(password_hint)
        email_error = html.fromstring(url.text).xpath(email_error)
        button = html.fromstring(url.text).xpath(button)
        forgotten_pass = html.fromstring(url.text).xpath(forgotten_pass)
        register = html.fromstring(url.text).xpath(register)

        properties = {'Title': title,
                      'Byline': byline,
                      'Email hint': email_hint,
                      'Password hint': password_hint,
                      'Email Error Message': email_error,
                      'Button Text': button,
                      'Forgotten Password Text': forgotten_pass,
                      'Register Text': register}
        data['Top Flash after register'] = top_flash
        for k, v in properties.items():
            data[k] = self.clean_data(v)

        self.log_in_output(data)
