from typing import List

import pandas as pd


class SpokeScraperCore(object):
    def __init__(self):
        super(SpokeScraperCore, self).__init__()
        self.de_encoding = 'UTF-8'
        self.eng_encoding = 'UTF-8'
        self.main_data = []

    def main_output_data(self, data):
        self.main_data.append(data)
        df = pd.DataFrame(self.main_data)
        df.to_csv('spoke-london1.csv')
        df.to_excel('spoke-london1.xlsx', index=False)

