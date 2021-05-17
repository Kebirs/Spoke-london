import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from spoke.main import DataWriter, Settings


class FitFinderSteps(Settings, DataWriter):
    def __init__(self):
        super(FitFinderSteps, self).__init__()
        self.root = "//div[@class='next-enter-done']"
        self.begin_button = "//button[contains(@class, 'styles_button_primary__2bVgk')]"
        self.next_button = f"{self.root}//button[contains(@class, 'styles_button_primary__2bVgk')]"
        self.nav_top = f"{self.root}//div[contains(@class, 'content__navigation')]"
        self.nav_bottom = f"{self.root}//div[contains(@class, 'bottomSliderText')]"
        self.title = f"{self.root}//h3[contains(@class, 'content_title')]"
        self.list_content = f"{self.root}//div[@class='wrapper wrapper--one']"
        self.list_div_button = f"{self.root}//div[@tabindex='0']"
        self.list_button_button = f"{self.root}//button[@tabindex='0']"
        self.note = f"{self.root}//p[contains(@class, 'content_copy')]"

    def step_0(self, s, data, sub_data):
        content = "//div[contains(@class, 'styles_content__main')]"

        content = s.find_element_by_xpath(content).text
        button = s.find_element_by_xpath(self.begin_button)
        button_text = button.text

        sub_data.append(content)
        sub_data.append(button_text)
        sub_data = self.clean_data(sub_data)

        data['Step 0'] = sub_data

        button.click()
        time.sleep(2)

    def step_1(self, s, data, sub_data):
        title = s.find_element_by_xpath(self.title).text
        nav_bottom = s.find_element_by_xpath(self.nav_bottom).text

        button = s.find_element_by_xpath(self.next_button)
        button_text = button.text

        properties = [title, nav_bottom, button_text]
        [sub_data.append(x) for x in properties]

        sub_data = self.clean_data(sub_data)
        data['Step 1'] = sub_data

        button.click()
        time.sleep(2)

    def step_2(self, s, data, sub_data):
        nav_top = s.find_element_by_xpath(self.nav_top).text
        title = s.find_element_by_xpath(self.title).text
        nav_bottom = s.find_element_by_xpath(self.nav_bottom).text
        button_text = s.find_element_by_xpath(self.next_button).text

        properties = [nav_top, title, nav_bottom, button_text]

        [sub_data.append(x) for x in properties]
        sub_data = self.clean_data(sub_data)

        data['Step 2'] = sub_data

        s.find_element_by_xpath(self.next_button).click()
        time.sleep(2)

    def step_3(self, s, data, sub_data):
        nav_top = s.find_element_by_xpath(self.nav_top).text
        title = s.find_element_by_xpath(self.title).text
        note = s.find_element_by_xpath(self.note).text
        list_content = s.find_element_by_xpath(self.list_content).text.replace('\n', ', ')

        properties = [nav_top, title, note, list_content]

        [sub_data.append(x) for x in properties]
        sub_data = self.clean_data(sub_data)

        data['Step 3'] = sub_data

        s.find_element_by_xpath(self.list_div_button).click()
        time.sleep(2)

    def step_4(self, s, data, sub_data):
        nav_top = s.find_element_by_xpath(self.nav_top).text
        title = s.find_element_by_xpath(self.title).text

        properties = [nav_top, title]

        [sub_data.append(x) for x in properties]
        sub_data = self.clean_data(sub_data)

        data['Step 4'] = sub_data

        s.find_element_by_xpath(self.list_button_button).click()
        time.sleep(2)

    def step_5(self, s, data, sub_data):
        nav_top = s.find_element_by_xpath(self.nav_top).text
        title = s.find_element_by_xpath(self.title).text
        list_content = s.find_element_by_xpath(self.list_content).text.replace('\n', ', ')

        properties = [nav_top, title, list_content]
        [sub_data.append(x) for x in properties]
        sub_data = self.clean_data(sub_data)

        data['Step 5'] = sub_data

        s.find_element_by_xpath(self.list_div_button).click()
        time.sleep(2)

    def step_6(self, s, data, sub_data):
        nav_top = s.find_element_by_xpath(self.nav_top).text
        title = s.find_element_by_xpath(self.title).text
        list_content = s.find_element_by_xpath(self.list_content).text

        properties = [nav_top, title, list_content]
        [sub_data.append(x) for x in properties]
        sub_data = self.clean_data(sub_data)

        data['Step 6'] = sub_data

        s.find_element_by_xpath(self.list_div_button).click()
        time.sleep(2)

    def step_7(self, s, data, sub_data):
        gallery_content = f"{self.root}//div[@class='gallery']"

        nav_top = s.find_element_by_xpath(self.nav_top).text
        title = s.find_element_by_xpath(self.title).text
        gallery_content = s.find_element_by_xpath(gallery_content).text.replace('\n', ', ')

        properties = [nav_top, title, gallery_content]
        [sub_data.append(x) for x in properties]
        sub_data = self.clean_data(sub_data)

        data['Step 7'] = sub_data

        s.find_element_by_xpath(self.list_div_button).click()
        time.sleep(2)

    def step_8(self, s, data, sub_data):
        nav_top = s.find_element_by_xpath(self.nav_top).text
        title = s.find_element_by_xpath(self.title).text
        list_content = s.find_element_by_xpath(self.list_content).text

        properties = [nav_top, title, list_content]
        [sub_data.append(x) for x in properties]
        sub_data = self.clean_data(sub_data)

        data['Step 8'] = sub_data

        s.find_element_by_xpath(self.list_div_button).click()
        time.sleep(2)

    def step_9(self, s, data, sub_data):
        nav_top = s.find_element_by_xpath(self.nav_top).text
        title = s.find_element_by_xpath(self.title).text

        properties = [nav_top, title]
        [sub_data.append(x) for x in properties]
        sub_data = self.clean_data(sub_data)

        data['Step 9'] = sub_data

        s.find_element_by_xpath(self.list_button_button).click()
        time.sleep(2)

    def step_10(self, s, data, sub_data):
        no_idea = f"{self.root}//div[contains(@class, 'unknowChoice')]"

        nav_top = s.find_element_by_xpath(self.nav_top).text
        title = s.find_element_by_xpath(self.title).text
        note = s.find_element_by_xpath(self.note).text
        no_idea = s.find_element_by_xpath(no_idea).text

        properties = [nav_top, title, note, no_idea]
        [sub_data.append(x) for x in properties]
        sub_data = self.clean_data(sub_data)

        data['Step 10'] = sub_data

        s.find_element_by_xpath(self.list_button_button).click()
        time.sleep(2)

    def step_11(self, s, data, sub_data):
        title = f"{self.root}//div[contains(@class, 'titleWrapper')]/h2"
        byline = f"{self.root}//p[contains(@class, 'register-copy')]"
        note = f"{self.root}//label[@for='customerMarketingId']"
        email = f"{self.root}//input[@id='email']"
        button = f"{self.root}//button[contains(@class, 'submit')]"
        nav_bottom = self.nav_top

        title = s.find_element_by_xpath(title).text
        byline = s.find_element_by_xpath(byline).text
        note = s.find_element_by_xpath(note).text
        button_text = s.find_element_by_xpath(button).text
        nav_bottom = s.find_element_by_xpath(nav_bottom).text

        email = s.find_element_by_xpath(email)
        email_hint = email.get_attribute('placeholder')

        properties = [title, byline, note, email_hint, button_text, nav_bottom]
        [sub_data.append(x) for x in properties]
        sub_data = self.clean_data(sub_data)

        data['Step 11'] = sub_data

        email.send_keys('valid@email.com')

        s.find_element_by_xpath(button).click()
        time.sleep(2)

    def step_last(self, s, data, sub_data):
        # TODO: loading content scrape if needs

        root = "//div[@class='modal__content']"
        content = f"{root}//div[contains(@class, 'results')]"

        title = f"{root}//h2[contains(@class, 'title')]"
        byline = f"{root}//p[contains(@class, 'byline')]"
        left_button = f"{root}//h2[contains(@class, 'focused')]"
        left_content = content
        right_button = f"{root}//h2[@class='styles_data__header__3Adh5 ']"

        # title = s.find_element_by_xpath(title).text
        title = WebDriverWait(s, 10).until(EC.visibility_of_element_located((By.XPATH, title))).text
        byline = s.find_element_by_xpath(byline).text
        left_button = s.find_element_by_xpath(left_button)
        left_content = s.find_element_by_xpath(left_content).text.replace('\n',', ')
        right_button = s.find_element_by_xpath(right_button)

        left_button_text = left_button.text
        right_button_text = right_button.text

        right_button.click()

        right_content = content
        button_text = f"{root}//button[contains(@class, 'secondary')]"

        right_content = s.find_element_by_xpath(right_content).text.replace('\n',', ')
        button_text = s.find_element_by_xpath(button_text).text

        properties = [title, byline, left_button_text, right_button_text, left_content, right_content, button_text]
        [sub_data.append(x) for x in properties]
        sub_data = self.clean_data(sub_data)

        data['LAST STEP'] = sub_data


class FitFinderPage(FitFinderSteps):
    def __init__(self):
        super(FitFinderPage, self).__init__()
        self.scrape_content()

    def scrape_content(self):
        urls = ['https://spoke-london.com/gb/pages/fit-finder',
                'https://spoke-london.com/de/pages/fit-finder']

        [self.fit_finder_body(url) for url in urls]

    def fit_finder_body(self, url):
        data = {}
        data['Link'] = url
        sub_data = []

        s = self._selenium()
        s.get(url)
        time.sleep(4)

        self.step_0(s, data, sub_data), sub_data.clear()
        self.step_1(s, data, sub_data), sub_data.clear()
        self.step_2(s, data, sub_data), sub_data.clear()
        self.step_3(s, data, sub_data), sub_data.clear()
        self.step_4(s, data, sub_data), sub_data.clear()
        self.step_5(s, data, sub_data), sub_data.clear()
        self.step_6(s, data, sub_data), sub_data.clear()
        self.step_7(s, data, sub_data), sub_data.clear()
        self.step_8(s, data, sub_data), sub_data.clear()
        self.step_9(s, data, sub_data), sub_data.clear()
        self.step_10(s, data, sub_data), sub_data.clear()
        self.step_11(s, data, sub_data), sub_data.clear()
        self.step_last(s, data, sub_data), sub_data.clear()

        self.fit_finder_output(data)






