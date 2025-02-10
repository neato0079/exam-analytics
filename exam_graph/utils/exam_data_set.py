from dotenv import load_dotenv
load_dotenv()

import pandas as pd
from exam_graph import helper
from exam_graph import filters
from pathlib import Path
from datetime import datetime, date
from formatter import *
import validator


class HL7Fields:

    def __init__(self):
        self.order_complete_dt = 'Exam Complete Date/Tm' # this is our ORM.ORC.5 (order status is complete)
        self.acc = 'Order Procedure Accession' # ORM.ORC.2
        self.order_dt = 'Exam Order Date/Time' # ex:'2024-07-10T01:15:00'; this is our HL7:ORM.ORC.15 (NW order time)
        self.final_dt = 'Final Date/Tm' # this is our ORM.OBR.22.1 (time of report)
        self.order_name = 'Exam Order Name' # ORM.OBR.4
        self.modality = 'Modality'
        
    def get_fields(self) -> dict:
        return {
            'ORC5': self.order_complete_dt,
            'ORC2': self.acc,
            'ORC15': self.order_dt,
            'OBR22_1': self.final_dt,
            'OBR4': self.order_name,
            'OBR24': self.modality
        }
    
    def get_columns(self) -> list:
        return  list(self.get_fields().values())
    
    # returns a df with attributes as columns and no data
    def make_df(self) -> pd.DataFrame:
        fields = self.get_columns(self)
        df = pd.DataFrame(columns=fields)
        return df
    
    @classmethod
    def show_default_fields(cls) -> list:
        return  list(cls().get_fields().values())
    
# csv gets ingested into this class
# we can do validation here and df conversion
class ExamDataFrame:
    def __init__(self, df:pd.DataFrame=None, hl7_fields=HL7Fields()):
        self.hl7_fields = hl7_fields
        self.df = None

    def read_file(self, fp:Path):
        accepted_file_types = {'.csv': pd.read_csv}
        file_type = fp.suffix
        if file_type in accepted_file_types:
            self.fp = fp
            self.df = accepted_file_types[file_type](self.fp)
            self.df.name = fp.stem
            print(f'Successfully read {self.fp.stem} to df',end='\n\n')
            self.df = Formatter(df=self.df,hl7=self.hl7_fields).format_df()
        else:
            print('Cannot read file',end='\n\n')

    def validate_self(self):
        validator.validate_df(self.df)

    def format_self(self):
        self.df = Formatter.format_df(self.df)

    def df_type(self):
        return type(self.df)


    def get_df(self) -> pd.DataFrame:
        return self.df


# this will contain the selected filters for a given analysis
class UserFilters:

    # Metric function dict
    metric_dict = {
        'totals': filters.totals,
        'mean': filters.mean,
        'tat': filters.tat,
        'shift_view': filters.shift_view,
        'tat_shift': filters.tat_shift_view,
        'shift_ratios': filters.shift_ratios,
    }

    def __init__(self, metric:str, view:str, granular_view:str, date_range:str):
        self.metric = metric
        columns = []
        # each filter can tell us what columns to keep. in other words, what columns are relevant to out neccessary calculations
        # the goal is to cut down as much of data we can so that we are working with a small amount, recuding any excessive overhead. As we read through the filters, toss the needed column names into an array or something

        # first thing to consider is the date range. this is an easy cut because the only data we need for calculations is within that range

        # next we can look at the selected modalities. We can delete any rows that don't match the selected modalities. We can also just delete the modality column if the user wants to view all the modalities. Same for shifts

        # next, we can look at the metric. Right now we only have totals and tat. for totals, row count is enough so no specific column needed there. for tat we need exam compelete time, and exam final time so keep those columns

        # next we can look at the view. This should tell us a lot about what we can cut. default view is just value of the metric(y) over time(x). But if our view is set to Shift ?....


    def averages(self, period):
        # if the user has selected a monthly period, the x axis will represent months in a range. the value of each month for this filter is a weekly avgerage. so july would have a weekly average 

        # maybe make the user choose a specific average. given the user selected period, you can get averages of any time unit smaller than the selected period. so if the user chose a selected priod of "month", the would then be able to look at weekly, daily, and hourly averages per month
        # 
        # Give the user 4 filters with wich to get averages from our large dataset of exams.
        # 1. A date range in which to limit the amount of data we intend to calculate averages on
        # 2. A period that will let us know how to increment our averages
        # 3. A time window that will specify how we are gathering averages.
        # 4. A metric that tells us what we are averaging(ie totals, duration, ect...)
        # So for example, a user selects a date range of 7-01-24 to 7-31-24. Then they give us a period of "week". Then they give us a averge time window of "daily". Then they give us a metric of "totals". Now we will analize the large data set such that we can see the daily averge number of exams per week within our given time range. 
        # 
        # 
        # Questions:
        # What can I name that "time window" so that it is understandable to the user and also readable in the codebase(open to having two different names if that makes things easier)
        #  


        # Concept	               Current Name	  Suggested Name (User-Facing)	Suggested Code Name
        # Date Range	            date range	          "Date Range"	             date_range
        # Period for averaging 
        # (How often we summarize 
        # averages, e.g., per week)	  period	       "Averaging Period"	          avg_period
        # Time window for 
        # aggregation (Granularity 
        # of averages, e.g., daily)	time window	       "Aggregation Window"	          agg_window
        # Metric to be averaged
        # (Total exams, 
        # durations, etc.)	          metric	             "Metric"	                metric
        pass


# validated df goes here and a filter
# this is where we apply all the filters
class FilteredExamData(ExamDataFrame):
    def __init__(self, df:pd.DataFrame, filter:str):
        super().__init__(df)
        self.filter = filter

    

    def child_df_type(self):
        return self.df


def main():
    my_csv = Path('/Users/mattbot/dev/big_mock_july2.csv')
    master_df = ExamDataFrame()
    master_df.read_file(my_csv)
    df = master_df.get_df()
    # df['Modality'] = 1

    # master_df.validate_columns()
    # str_dt = '2024-09-14T14:15:00'
    # a = date.fromisoformat(str_dt)


    # df['Exam Order Date/Time'] = pd.to_datetime(df['Exam Order Date/Time'] )
    master_df.validate_self()
    print(df.head())



if __name__ == '__main__':
    main()

