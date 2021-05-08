import pandas as pd


class SpokeScraperCore(object):
    def __init__(self):
        super(SpokeScraperCore, self).__init__()
        self.homepage_data = []

    def main_output_data(self, data):
        self.homepage_data.append(data)

        homepage_df = pd.DataFrame(self.homepage_data).apply(lambda x: pd.Series(x.dropna().values))

        writer = pd.ExcelWriter('spoke-london-test.xlsx')

        homepage_df.to_excel(writer, sheet_name='Homepage.xlsx', index=False)

        writer.save()

