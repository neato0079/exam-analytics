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
    """Contains a provided pd.DataFrame and custom methods to validate and format the data.
    
    On initialization, if nothing is passed, an empty DataFrame is created at self.df with the provided columns from the hl7_fields arg. 

    If a file is passed with arg 'file=', the file is read and then set to the self.df attribute

    If a data frame is passed with 'df=', the self.df attribute is simply set to the provided data frame
    """

    def __init__(self, df:pd.DataFrame=None, hl7_fields=HL7Fields(), file=None, shifts=Shifts().dict()):
        self.file = file
        self.hl7_fields = hl7_fields
        self.df = df
        self.shifts = shifts
        self.initialize_df()


    def initialize_df(self):
        
        if self.df is None and self.file == None:
            "init empty df"
            columns = self.hl7_fields.get_columns()
            self.df = pd.DataFrame(columns=columns)
            return
        
        if self.file and self.df is None:
            self.read_file(self.file)
            return

    
    def read_file(self, fp:Path | bytes | str):
        file_type = fp.suffix
        f_type_pd_convert_map = {
        '.csv': pd.read_csv
        }
        if file_type in f_type_pd_convert_map:
            self.fp = fp

        
            # read into pd.Dataframe with appropriate pd conversion method
            self.df:pd.DataFrame = f_type_pd_convert_map[file_type](self.fp)

            self.df.name = fp.stem

            print(f'Successfully read {self.df.name} to df',end='\n\n')

        else:
            print('Cannot read file',end='\n\n')

    def validate_self(self):
        validator.validate_df(self.df)

    def format_self(self):
        self.df = Formatter(df=self.df).basic_format()




class FilteredExamData:
    def __init__(self, exam_data:ExamDataFrame):
        self.exam_data = exam_data
        self.df = pd.DataFrame(self.exam_data.df)
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
    """is tis a doc"""
    my_csv = Path('/Users/mattbot/dev/big_mock_july2.csv')
    master_df = ExamDataFrame(file=my_csv)
    print(master_df.df.head())
    # master_df.format_self()
    # df = master_df.df

    # df2 = ExamDataFrame(df=df)
    # df2.format_self()
    # print(df)
    # print(df2.df)
    # # print(master_df.file)

    # print(isinstance(df, NoneType))
    # def build_df(df=None):
    #     if df.empty:
    #         # some logic
    #         return
    #     if df == None:
    #         # some logic
    #         return

    # filt = FilteredExamData(master_df)


    # period_filtered= filt.period('Week')


    # test 
    # create custom HL7 and build df with ExamDataFrame to emulate a user uploading a csv with differently formatted column names







if __name__ == '__main__':
    main()

