from time import time
from spoke.about import AboutPage
from spoke.home import BrandHomePage
from spoke.careers import CareersPage
from spoke.faq import FAQPage
from spoke.return_policy import ReturnPolicyPage
from spoke.size_charts import SizeChartsPage
from spoke.contact_us import ContactUsPage
from spoke.notfound404 import NotFoundPage
from spoke.submit_request import SubmitRequestPage
from spoke.privacy import PrivacyPolicyPage
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
        # BrandHomePage(), print('BrandHomePage done')
        # AboutPage(), print('AboutPage done')
        # CareersPage(), print('CareersPage done')
        # FAQPage(), print('FAQPage done')
        # ReturnPolicyPage(), print('ReturnPolicyPage done')
        # SizeChartsPage(), print('SizeChartsPage done')
        # ContactUsPage(), print('ContactUsPage done')
        # NotFoundPage(), print('NotFoundPage done')
        # SubmitRequestPage(), print('SubmitRequestPage done')
        PrivacyPolicyPage(), print('PrivacyPolicyPage done')


if __name__ == '__main__':
    SpokeScraperCore()
