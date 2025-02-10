import pandas as pd
import sys
# for line in sys.path:
#      print(line)

# print(dir(sys))
# print(sys.modules)
# print(globals())
import os
# os.environ['PYTHONPATH'] = '/Users/mattbot/dev/exam-analytics'
# try:
#     user_paths = os.environ['PYTHONPATH'].split(os.pathsep)
# except KeyError:
#     user_paths = []
# print(os.environ)
# print(user_paths)
from exam_graph import helper
from exam_graph import filters
from pathlib import Path

# csv gets ingested into this class
# we can do validation here and df conversion
class ExamDataFrame:
    def __init__(self, df:pd.DataFrame):
        self.df=df
        self.fields = HL7Fields()
        pass

    def validate_columns(self):
        columns = HL7Fields().get_columns()
        return columns
    
    def df_type(self):
        return type(self.df)
    
    def get_df(self):
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


class HL7Fields:

    def __init__(self):
        self.ORC5 = 'Exam Complete Date/Tm' # this is our ORM.ORC.5 (order status is complete)
        self.ORC2 = 'Order Procedure Accession' # ORM.ORC.2
        self.ORC15 = 'Exam Order Date/Time' # ex:'2024-07-10T01:15:00'; this is our HL7:ORM.ORC.15 (NW order time)
        self.OBR22_1 = 'Final Date/Tm' # this is our ORM.OBR.22.1 (time of report)
        self.OBR4 = 'Exam Order Name' # ORM.OBR.4
        self.OBR24 = 'Modality'
        
    def get_fields(self) -> dict:
        return {
            'ORC5': self.ORC5 ,
            'ORC2': self.ORC2,
            'ORC15': self.ORC15,
            'OBR22_1': self.OBR22_1,
            'OBR4': self.OBR4,
            'OBR24': self.OBR24
        }
    
    def get_columns(self) -> list:
        return  list(self.get_fields().values())
    
    def rename_ORC5(self, name):
        self.ORC5 = name
    
    # returns a df with attributes as columns and no data
    def make_df(self) -> pd.DataFrame:
        fields = self.get_columns(self)
        df = pd.DataFrame(columns=fields)
        return df
    
    @classmethod
    def show_default_fields(cls) -> list:
        return  cls().get_fields().values()

class Person:
    def __init__(self, name):
        self.name = name

class Employee(Person):  # Employee inherits from Person
    def __init__(self, name, salary):
        super().__init__(name)
        self.salary = salary
def main():
    # df = helper.pickle_to_df('/Users/mattbot/dev/exam_analytics_properties/user_uploads/big_mock_july.pickle')
    # print(df.head())
    # empty_df = HL7Fields()
    # my_df = ExamDataFrame(df)
    # filt = FilteredExamData(my_df)
    # print(my_df.df_type()) #<class 'pandas.core.frame.DataFrame'>
    # print(filt.child_df_type()) # <class '__main__.ExamDataFrame'>
    me = Employee('Me', )

# main()


if __name__ == '__main__':
    main()

