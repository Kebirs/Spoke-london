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
from spoke.refer_a_friend import ReferFriendPage
from spoke.newsletter import NewsletterPage
from spoke.impressum_de import ImpressumPage
from spoke.terms_and_conditions import TermsConditionsPage
from spoke.cookie_policy import CookiePolicyPage
from spoke.fit_finder import FitFinderPage
from spoke.account.log_in import LogInPage
from spoke.account.register import RegisterPage
from spoke.account.forgotten_password import ForgottenPasswordPage
from spoke.account.after_log_in_page import AfterLogInPage
from spoke.products.collections_pages import CollectionsPage
from spoke.products.products_details import ProductsDetails
from spoke.nps_feedback import NPSFeedbackPage
from spoke.checkout import CheckoutPage
from spoke.products.filter_my_size import FilterMySize
from spoke.products.products_hover_banners import ProductsBanners
from spoke.arrange_return import ArrangeReturn
from spoke.products.products_benefits import ProductsBenefits
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
        # # NotFoundPage(), print('NotFoundPage done')
        # SubmitRequestPage(), print('SubmitRequestPage done')
        # PrivacyPolicyPage(), print('PrivacyPolicyPage done')
        # ReferFriendPage(), print('ReferFriendPage done')
        # NewsletterPage(), print('NewsletterPage done')
        # ImpressumPage(), print('ImpressumPage done')
        # TermsConditionsPage(), print('TermsConditionsPage done')
        CookiePolicyPage(), print('CookiePolicyPage done')
        # FitFinderPage(), print('FitFinderPage done')
        # NPSFeedbackPage(), print('NPSFeedbackPage done')
        # CheckoutPage(), print('CheckoutPage done')
        # ArrangeReturn(), print('ArrangeReturn done')

        LogInPage(), print('LogInPage done')
        # RegisterPage(), print('RegisterPage done')
        # ForgottenPasswordPage(), print('ForgottenPasswordPage done')
        # AfterLogInPage(), print('AfterLogInPage done')
        #
        # CollectionsPage(), print('CollectionsPage done')
        # ProductsBenefits(), print('ProductsBenefits done')
        FilterMySize(), print('FilterMySize done')
        # ProductsBanners(), print('ProductsBanners done')
        # ProductsDetails(), print('ProductsDetails done')


if __name__ == '__main__':
    SpokeScraperCore()
