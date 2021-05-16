import os

import cloudscraper
import pandas as pd
import time
from functools import wraps
from lxml import html
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager as CM
from requests.exceptions import RequestException
from socket import timeout


class ListsInit(object):
    def __init__(self):
        super(ListsInit, self).__init__()

    # STATIC
    @staticmethod
    def home_output(data):
        homepage.append(data)

    @staticmethod
    def about_output(data):
        about.append(data)

    @staticmethod
    def careers_output(data):
        careers.append(data)

    @staticmethod
    def faq_home_output(data):
        faq_home.append(data)

    @staticmethod
    def return_policy_output(data):
        return_policy.append(data)

    @staticmethod
    def size_charts_output(data):
        size_charts.append(data)

    @staticmethod
    def contact_us_output(data):
        contact_us.append(data)

    @staticmethod
    def not_found_output(data):
        not_found.append(data)

    @staticmethod
    def submit_request_output(data):
        submit_request.append(data)

    @staticmethod
    def privacy_output(data):
        privacy.append(data)

    @staticmethod
    def refer_friend_output(data):
        refer_friend.append(data)

    @staticmethod
    def newsletter_output(data):
        newsletter.append(data)

    @staticmethod
    def impressum_output(data):
        impressum.append(data)

    @staticmethod
    def terms_conditions_output(data):
        terms_conditions.append(data)

    @staticmethod
    def cookie_policy_output(data):
        cookie_policy.append(data)

    @staticmethod
    def fit_finder_output(data):
        fit_finder.append(data)

    @staticmethod
    def nps_feedback_output(data):
        nps_feedback.append(data)

    @staticmethod
    def checkout_output(data):
        checkout.append(data)

    @staticmethod
    def arrange_return_output(data):
        arrange_return.append(data)

    # ACCOUNT
    @staticmethod
    def log_in_output(data):
        log_in.append(data)

    @staticmethod
    def register_output(data):
        register.append(data)

    @staticmethod
    def forgotten_password_output(data):
        forgotten_password.append(data)

    @staticmethod
    def account_output(data):
        account.append(data)

    # PRODUCTS
    @staticmethod
    def collections_output(data):
        collections_pages.append(data)

    @staticmethod
    def products_details_output(data):
        products_details.append(data)

    @staticmethod
    def products_benefits_output(data):
        products_benefits.append(data)

    @staticmethod
    def filter_my_size_output(data):
        filter_my_size.append(data)

    @staticmethod
    def products_hover_banners_output(data):
        products_hover_banners.append(data)

# STATIC
homepage = []
about = []
careers = []
faq_home = []
return_policy = []
size_charts = []
contact_us = []
not_found = []
submit_request = []
privacy = []
refer_friend = []
newsletter = []
impressum = []
terms_conditions = []
cookie_policy = []
fit_finder = []
nps_feedback = []
checkout = []
arrange_return = []

# ACCOUNT
log_in = []
register = []
forgotten_password = []
account = []

# PRODUCTS
collections_pages = []
products_details = []
products_benefits = []
products_hover_banners = []
filter_my_size = []


class DataWriter(ListsInit):
    def __init__(self):
        super(DataWriter, self).__init__()

    def main_output(self):

        dfs = {'Homepage': self.clean_df(homepage),
               'About': self.clean_df(about),
               'Careers': self.clean_df(careers),
               'FAQ': self.clean_df(faq_home),
               'Return Policy': self.clean_df(return_policy),
               'Size Charts': self.clean_df(size_charts),
               'Contact Us': self.clean_df(contact_us),
               'Page Not Found (404)': self.clean_df(not_found),
               'Submit Request': self.clean_df(submit_request),
               'Privacy Policy': self.clean_df(privacy),
               'Refer A Friend': self.clean_df(refer_friend),
               'Newsletter': self.clean_df(newsletter),
               'Impressum': self.clean_df(impressum),
               'Terms & Conditions': self.clean_df(terms_conditions),
               'Cookie Policy': self.clean_df(cookie_policy),
               'Fit Finder': self.clean_df(fit_finder),
               'NPS Feedback Form': self.clean_df(nps_feedback),
               'Checkout': self.clean_df(checkout),
               'Arrange A Return': self.clean_df(arrange_return),
               'LOG IN': self.clean_df(log_in),
               'REGISTER': self.clean_df(register),
               'FORGOTTEN PASSWORD': self.clean_df(forgotten_password),
               'ACCOUNT CONTENT': self.clean_df(account),
               'Collections Pages': self.clean_df(collections_pages),
               'Products Details': self.clean_df(products_details),
               'Products Benefits': self.clean_df(products_benefits),
               'Products Hover Banners': self.clean_df(products_hover_banners),
               'Filter My Size': self.clean_df(filter_my_size)}

        file_path = r"\Desktop\spoke-london-output-done.xlsx"
        app_dir = os.path.join(os.path.expanduser("~"))
        writer = pd.ExcelWriter(app_dir + file_path, engine='xlsxwriter')

        # Auto adjust column width, text wrap
        for sheet_name, df in dfs.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            wb = writer.book
            worksheet = writer.sheets[sheet_name]
            text_format = wb.add_format({'text_wrap': True, 'valign': 'top'})

            for idx, col in enumerate(df):
                series = df[col]
                max_len = max((series.astype(str).map(len).max(),
                               len(str(series.name)))) + 1
                if max_len > 100:
                    worksheet.set_column(idx, idx, max_len / 3, text_format)
                else:
                    worksheet.set_column(idx, idx, max_len, text_format)

        writer.save()

    @staticmethod
    def clean_df(list_of_dicts):
        df = pd.DataFrame(list_of_dicts).apply(lambda x: pd.Series(x.dropna().values))
        return df


class Retry(object):
    def __init__(self, times, exceptions, pause=1, retreat=1,
                 max_pause=None, cleanup=None):
        self.times = times
        self.exceptions = exceptions
        self.pause = pause
        self.retreat = retreat
        self.max_pause = max_pause or (pause * retreat ** times)
        self.cleanup = cleanup

    def __call__(self, func):

        @wraps(func)
        def wrapped_func(*args):
            for i in range(self.times):
                pause = min(self.pause * self.retreat ** i, self.max_pause)
                try:
                    return func(*args)
                except self.exceptions:
                    if self.pause is not None:
                        time.sleep(pause)

                    else:
                        pass
            if self.cleanup is not None:
                return self.cleanup(*args)

        return wrapped_func


class Settings(object):
    def __init__(self):
        super(Settings, self).__init__()
        self.ENG = 'ENG '
        self.DE = 'DE '
        self.languages_list = [self.ENG, self.DE]

    def failed_call(*args):
        print(f"Failed call link {args[1]}")

    retry = Retry(times=3, pause=1, retreat=2, cleanup=failed_call,
                  exceptions=(RequestException, timeout))

    def json_script_data(self, url):
        """
        Evaluate data into json format
        :param url:
        :return data formatted into json:
        """
        resp = self.get_response(url)
        script_data = html.fromstring(resp.text).xpath('//script[@id="__NEXT_DATA__"]/text()')
        true = 'true'
        false = 'false'
        null = 'null'
        script_data_json = eval(script_data[0])
        return script_data_json

    @staticmethod
    def clean_data(data):
        clean = [x.strip().replace('\n', '').replace('  ', '') for x in data]
        clean = list(filter(None, clean))
        clean = ', '.join(clean)
        return clean

    @retry
    def get_response(self, url):
        s = cloudscraper.create_scraper()
        r = s.get(url)
        r.encoding = 'UTF-8'

        if r.status_code != 200:
            print(f'{r.status_code} |{url}')
            r.raise_for_status()

        return r

    @staticmethod
    def _selenium():
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("window-size=1400,1000")
        browser = webdriver.Chrome(executable_path=CM().install(), options=options)
        return browser

    @staticmethod
    def _selenium_lang(lang):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument(f'--lang={lang}')
        browser = webdriver.Chrome(executable_path=CM().install(), options=options)
        return browser

    def get_cdn_id(self, url):
        script_data_json = self.json_script_data(url)
        cdn = script_data_json['query']['contentfulId']
        return str(cdn)

    @staticmethod
    def get_banners(url):
        # Authorization required for get request
        auth = {
            'Authorization': 'Bearer 56If-j-ANNWSZ9Zk_8lp9EChokF6LNtKJDHC8eHMfSs',
            # 'If-None-Match': 'W/"16729328500904452549"'
            'If-None-Match': 'W/"14186816362649224049"'
        }

        s = cloudscraper.create_scraper()

        r = s.get(url, headers=auth)
        r.encoding = 'UTF-8'
        content = r.json()
        return content
