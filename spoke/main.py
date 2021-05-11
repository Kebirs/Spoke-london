import cloudscraper
import pandas as pd
from lxml import html
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager as CM


homepage = []
about = []
careers = []
faq_home = []
return_policy = []
size_charts = []


class DataWriter(object):
    def __init__(self):
        super(DataWriter, self).__init__()

    @staticmethod
    def main_output():
        # Dataframes init and cleaning
        homepage_df = pd.DataFrame(homepage).apply(lambda x: pd.Series(x.dropna().values))
        about_df = pd.DataFrame(about).apply(lambda x: pd.Series(x.dropna().values))
        careers_df = pd.DataFrame(careers).apply(lambda x: pd.Series(x.dropna().values))
        faq_home_df = pd.DataFrame(faq_home).apply(lambda x: pd.Series(x.dropna().values))
        return_policy_df = pd.DataFrame(return_policy).apply(lambda x: pd.Series(x.dropna().values))
        size_charts_df = pd.DataFrame(size_charts).apply(lambda x: pd.Series(x.dropna().values))

        writer = pd.ExcelWriter('spoke-london.xlsx')

        # Dataframes into xlsx sheets
        about_df.to_excel(writer, sheet_name='About.xlsx', index=False)
        homepage_df.to_excel(writer, sheet_name='Homepage.xlsx', index=False)
        careers_df.to_excel(writer, sheet_name='Careers.xlsx', index=False)
        faq_home_df.to_excel(writer, sheet_name='FAQ.xlsx', index=False)
        return_policy_df.to_excel(writer, sheet_name='Return Policy.xlsx', index=False)
        size_charts_df.to_excel(writer, sheet_name='Size Charts.xlsx', index=False)

        writer.save()

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
        options.add_argument("--headless")
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
