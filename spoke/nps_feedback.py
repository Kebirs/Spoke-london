import time
import cloudscraper
from lxml import html
from spoke.main import Settings, DataWriter


class NPSFeedbackPage(Settings, DataWriter):
    def __init__(self):
        super(NPSFeedbackPage, self).__init__()
        self.scrape_content()

    def scrape_content(self):
        urls = ['https://spoke-london.com/gb/pages/spoke-feedback',
                'https://spoke-london.com/de/pages/spoke-feedback']

        [self.nps_page_body(self.get_response(url)) for url in urls]

    def nps_page_body(self, url):
        data = {}

        banner_content = "//div[contains(@class, 'formHeader__6-JBs')]//text()"
        questions = "//p[contains(@class, 'styles_form__label')]/text()"
        answers = "//div[@id='how_did_you_hear_about_us']//span/text()"
        rate_details = "//div[@class='styles_form__details__22K58']//text()"
        email_hint = "//input[@id='email']/@placeholder"

        banner_content = html.fromstring(url.text).xpath(banner_content)
        banner_content = self.clean_data(banner_content)
        data['BANNER CONTENT'] = banner_content

        email_hint = html.fromstring(url.text).xpath(email_hint)
        email_hint = self.clean_data(email_hint)
        data['EMAIL HINT'] = email_hint

        questions = html.fromstring(url.text).xpath(questions)
        for idx, question in enumerate(questions):
            data[f'QUESTION {idx+1}'] = question

        answers = html.fromstring(url.text).xpath(answers)
        # How did you head about us answers
        for idx, answer in enumerate(answers):
            data[f'ANSWER {idx+1}'] = answer

        rate_details = html.fromstring(url.text).xpath(rate_details)
        rate_details = list(dict.fromkeys(rate_details))
        rate_details = self.clean_data(rate_details)
        data['RATE DETAILS'] = rate_details

        self.nps_feedback_output(data)
