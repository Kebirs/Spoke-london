from lxml import html
import json
from bs4 import BeautifulSoup as bs
from spoke.main import Settings, DataWriter


class CareersPage(Settings, DataWriter):
    def __init__(self):
        super(CareersPage, self).__init__()
        self.scrape_content()

    def scrape_content(self):
        # Only one cause there is not a Deutsch version of this page
        url = 'https://apply.workable.com/api/v1/accounts/spoke?full=true'
        resp = self.get_response(url)

        self.careers_page_body(resp)

    def careers_page_body(self, url):
        self.company_desc(url)

    def company_desc(self, url):
        data = url.json()
        desc = data['details']['overview']['description']
        clean_desc = bs(desc, 'lxml').text

        data = {'Company Description': clean_desc}

        self.careers_output(data)

    @staticmethod
    def rest_of_content():
        """
        For the rest of content I need to use selenium
        Maybe later if needs
        """
        pass
