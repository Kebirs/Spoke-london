import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from spoke.main import DataWriter, Settings
from lxml import html


class ReferFriendPage(Settings, DataWriter):
    def __init__(self):
        super(ReferFriendPage, self).__init__()
        self.scrape_content()

    def scrape_content(self):
        urls = ['https://spoke-london.com/gb/pages/refer-a-friend',
                'https://spoke-london.com/de/pages/refer-a-friend']

        [self.refer_friend_page_body(url) for url in urls]

    def refer_friend_page_body(self, url):
        data = {}
        data['Link'] = url

        s = self._selenium()
        s.get(url)
        time.sleep(4)

        iframe = '//iframe[@id="mmContentReferrerStage1"]'
        iframe = WebDriverWait(s, 10).until(EC.visibility_of_element_located((By.XPATH, iframe)))
        s.switch_to.frame(iframe)

        content = '//div[@class="europium-container"]'
        content = s.find_element_by_xpath(content).text.replace('\n', ', ')

        data['REFER A FRIEND Content'] = content

        self.refer_friend_output(data)
