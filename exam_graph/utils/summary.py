import pandas as pd
import json


class DataSummary:
    def __init__(self, axes_data:pd.Series):
        self.axes_data = axes_data
        self.general_summary:dict = {}
        self.build_summary()

    def build_summary(self):
        # init summary json
        # create analysis series
        # desc = axes_data.describe().astype(int)
        # desc_str = desc.to_json()
        # desc_dict = json.loads(desc_str)
        # summary_json.update(desc_dict)
        agg_sr:pd.Series = self.axes_data.aggregate(['mean', 'max', 'sum']).astype(int)
        agg_sr.rename(index={'mean':'Avg', 'sum': 'Total'}, inplace=True)
        agg_str = agg_sr.to_json()
        agg_dict = json.loads(agg_str)
        # add data to summary_json
        self.general_summary.update(agg_dict)