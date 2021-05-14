import cloudscraper
import pandas as pd
from lxml import html
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager as CM


class ListsInit(object):
    def __init__(self):
        super(ListsInit, self).__init__()

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
    def log_in_output(data):
        log_in.append(data)

    @staticmethod
    def register_output(data):
        register.append(data)

    @staticmethod
    def forgotten_password_output(data):
        forgotten_password.append(data)


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
log_in = []
register = []
forgotten_password = []


class DataWriter(ListsInit):
    def __init__(self):
        super(DataWriter, self).__init__()

    def main_output(self):
        # Dataframes init and cleaning
        homepage_df = self.clean_df(homepage)
        about_df = self.clean_df(about)
        careers_df = self.clean_df(careers)
        faq_home_df = self.clean_df(faq_home)
        return_policy_df = self.clean_df(return_policy)
        size_charts_df = self.clean_df(size_charts)
        contact_us_df = self.clean_df(contact_us)
        not_found_df = self.clean_df(not_found)
        submit_request_df = self.clean_df(submit_request)
        privacy_df = self.clean_df(privacy)
        refer_friend_df = self.clean_df(refer_friend)
        newsletter_df = self.clean_df(newsletter)
        impressum_df = self.clean_df(impressum)
        terms_conditions_df = self.clean_df(terms_conditions)
        cookie_policy_df = self.clean_df(cookie_policy)
        fit_finder_df = self.clean_df(fit_finder)

        log_in_df = self.clean_df(log_in)
        register_df = self.clean_df(register)
        forgotten_password_df = self.clean_df(forgotten_password)

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
               'LOG IN': self.clean_df(log_in),
               'REGISTER': self.clean_df(register),
               'FORGOTTEN PASSWORD': self.clean_df(forgotten_password),}

        writer = pd.ExcelWriter('spoke-london.xlsx',  engine='xlsxwriter')

        # Auto adjust column width
        for sheetname, df in dfs.items():  # loop through `dict` of dataframes
            df.to_excel(writer, sheet_name=sheetname, index=False)  # send df to writer
            worksheet = writer.sheets[sheetname]
            # pull worksheet object
            for idx, col in enumerate(df):  # loop through all columns
                series = df[col]
                max_len = max((
                    series.astype(str).map(len).max(),  # len of largest item
                    len(str(series.name))  # len of column name/header
                )) + 1  # adding a little extra space
                worksheet.set_column(idx, idx, max_len)  # set column width
        writer.save()

        # # Dataframes into xlsx sheets
        # about_df.to_excel(writer, sheet_name='About.xlsx', index=False)
        # homepage_df.to_excel(writer, sheet_name='Homepage.xlsx', index=False)
        # careers_df.to_excel(writer, sheet_name='Careers.xlsx', index=False)
        # faq_home_df.to_excel(writer, sheet_name='FAQ.xlsx', index=False)
        # return_policy_df.to_excel(writer, sheet_name='Return Policy.xlsx', index=False)
        # size_charts_df.to_excel(writer, sheet_name='Size Charts.xlsx', index=False)
        # contact_us_df.to_excel(writer, sheet_name='Contact Us.xlsx', index=False)
        # not_found_df.to_excel(writer, sheet_name='Page Not Found (404).xlsx', index=False)
        # submit_request_df.to_excel(writer, sheet_name='Submit Request.xlsx', index=False)
        # privacy_df.to_excel(writer, sheet_name='Privacy Policy.xlsx', index=False)
        # refer_friend_df.to_excel(writer, sheet_name='Refer A Friend.xlsx', index=False)
        # newsletter_df.to_excel(writer, sheet_name='Newsletter.xlsx', index=False)
        # impressum_df.to_excel(writer, sheet_name='Impressum.xlsx', index=False)
        # terms_conditions_df.to_excel(writer, sheet_name='Terms & Conditions.xlsx', index=False)
        # cookie_policy_df.to_excel(writer, sheet_name='Cookie Policy.xlsx', index=False)
        # fit_finder_df.to_excel(writer, sheet_name='Fit Finder.xlsx', index=False)
        #
        # log_in_df.to_excel(writer, sheet_name='LOG IN.xlsx', index=False)
        # register_df.to_excel(writer, sheet_name='REGISTER.xlsx', index=False)
        # forgotten_password_df.to_excel(writer, sheet_name='FORGOTTEN PASSWORD.xlsx', index=False)
        #
        # writer.save()

    @staticmethod
    def clean_df(list_of_dicts):
        df = pd.DataFrame(list_of_dicts).apply(lambda x: pd.Series(x.dropna().values))
        return df


class Settings(object):
    def __init__(self):
        super(Settings, self).__init__()
        self.ENG = 'ENG '
        self.DE = 'DE '
        self.languages_list = [self.ENG, self.DE]

    @staticmethod
    def get_request(url):
        s = cloudscraper.create_scraper()

        r = s.get(url)
        r.encoding = 'UTF-8'
        return r

    def json_script_data(self, url):
        """
        Evaluate data into json format
        :param url:
        :return data formatted into json:
        """
        resp = self.get_request(url)
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

    @staticmethod
    def _selenium():
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
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
