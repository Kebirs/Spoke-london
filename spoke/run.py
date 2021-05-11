from time import time
from spoke.about import AboutPage
from spoke.home import BrandHomePage
from spoke.careers import CareersPage
from spoke.faq import FAQPage
from spoke.return_policy import ReturnPolicyPage
from spoke.size_charts import SizeChartsPage
from spoke.main import DataWriter


class SpokeScraperCore(DataWriter):
    def __init__(self):
        super(SpokeScraperCore, self).__init__()
        self.scraper_run()
        self.main_output()

    @staticmethod
    def scraper_run():
        """
        Run all sub_classes
        """
        BrandHomePage(), print('BrandHomePage done')
        AboutPage(), print('AboutPage done')
        CareersPage(), print('CareersPage done')
        FAQPage(), print('FAQPage done')
        ReturnPolicyPage(), print('ReturnPolicyPage done')
        SizeChartsPage(), print('SizeChartsPage done')


if __name__ == '__main__':
    SpokeScraperCore()
