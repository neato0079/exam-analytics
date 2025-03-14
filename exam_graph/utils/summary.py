import pandas as pd
import json
from json2html import *
from typing import TypeAlias


class DataSummary:
    def __init__(self, axes_data:pd.Series | pd.DataFrame):
        self.axes_data = axes_data
        self.general_summary:dict | pd.DataFrame = 'Need to build logic for this . . . '
        self.data_summary_type = type(axes_data)

    def build_summary_data(self) -> dict | pd.DataFrame:

        # our methods of building summary data is contingent on what type of data we are passed. same thing for building a table
        if isinstance(self.axes_data, pd.Series):
            agg_sr:pd.Series = self.axes_data.aggregate(['mean', 'max', 'sum']).astype(int)
            agg_sr.rename(index={'mean':'Avg', 'sum': 'Total'}, inplace=True)
            agg_str = agg_sr.to_json()
            agg_dict = json.loads(agg_str)
            # add data to summary_json
            return agg_dict

        if isinstance(self.axes_data, pd.DataFrame):
            # compile summary data
            agg_df:pd.DataFrame = self.axes_data.aggregate(['mean', 'max', 'sum']).astype(int)           
            agg_df.columns.name = ''
            agg_df.rename(index={'mean':'Avg', 'sum': 'Total'}, inplace=True)
            return agg_df

    HtmlTable: TypeAlias = str
    def build_table(self) -> HtmlTable:
        if isinstance(self.axes_data, pd.Series):
            return json2html.convert(json = self.build_summary_data())
        if isinstance(self.axes_data, pd.DataFrame):
            return  self.build_summary_data().to_html()