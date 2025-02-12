from dotenv import load_dotenv
load_dotenv()

import pandas as pd
from exam_graph import helper
from pathlib import Path
from datetime import datetime, date, time
from formatter import *
import validator



    
# csv gets ingested into this class
# we can do validation here and df conversion
class ExamDataFrame:
    def __init__(self, df:pd.DataFrame=None, hl7_fields=HL7Fields(), shifts=Shifts().dict()):
        self.hl7_fields = hl7_fields
        self.df = None
        self.shifts = shifts

    def read_file(self, fp:Path):
        accepted_file_types = {'.csv': pd.read_csv}
        file_type = fp.suffix
        if file_type in accepted_file_types:
            self.fp = fp
            self.df = accepted_file_types[file_type](self.fp)
            self.df.name = fp.stem
            print(f'Successfully read {self.fp.stem} to df',end='\n\n')
            self.df = Formatter(df=self.df, shifts=self.shifts, hl7=self.hl7_fields).format_df()
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



class FilteredExamData:
    def __init__(self, exam_data:ExamDataFrame):
        self.exam_data = exam_data
        self.df = pd.DataFrame(self.exam_data.get_df())
        self.hl7_fields = self.exam_data.hl7_fields



    def period(self, period_selection:str) -> pd.DataFrame:
        # if df == None:
        #     df = self.df


        # use pandas time period aliases for period_selection 
        alias = {
            'hour': 'H',
            'day': 'D',
            'week':'W',
            'month': 'M',
            'year': 'Y'
        }

        # map user's period selection to pandas period alias
        period_selection = period_selection.lower()
        period_selection = alias[period_selection]

        # create new column to we can group by the user's selected period
        self.df['User_selected_period'] = self.df[self.hl7_fields.order_complete_dt].dt.to_period(period_selection)

        return self.df    

    

    def child_df_type(self):
        return self.df


def main():
    my_csv = Path('/Users/mattbot/dev/big_mock_july2.csv')
    master_df = ExamDataFrame()
    master_df.read_file(my_csv)
    df = master_df.get_df()

    print(df.head())

    filt = FilteredExamData(master_df)


    period_filtered= filt.period('Week')
    print(period_filtered.head())
    # filt = filt.period('Week').head()
    # print(filt.head())
    # df['Modality'] = 1

    # master_df.validate_columns()
    # str_dt = '2024-09-14T14:15:00'
    # a = date.fromisoformat(str_dt)


    # df['Exam Order Date/Time'] = pd.to_datetime(df['Exam Order Date/Time'] )
    # master_df.validate_self()
    print(df.head())
    # shi = Shifts()
    # print(shi.dict())
    # shi.EX = [time(17, 0), time(1, 0)]
    # print(shi.dict())




if __name__ == '__main__':
    main()

