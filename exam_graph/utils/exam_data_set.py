from dotenv import load_dotenv
load_dotenv()

import pandas as pd
from exam_graph import helper
from pathlib import Path
from datetime import datetime, date, time
from .formatter import *
from .validator import *




class ExamDataFrame:
    """Contains a provided pd.DataFrame and custom methods to validate and format the data.
    
    On initialization, if nothing is passed, an empty DataFrame is created at self.df with the provided columns from the hl7_fields arg. 

    If a file is passed with arg 'file=', the file is read and then set to the self.df attribute

    If a data frame is passed with 'df=', the self.df attribute is simply set to the provided data frame
    """

    def __init__(self, df:pd.DataFrame=None, hl7_fields=HL7Fields(), file=None, shifts=Shifts().dict(), upload_req=None):
        self.upload_req=upload_req
        self.file = file
        self.hl7_fields = hl7_fields
        self.df = df
        self.shifts = shifts
        self.initialize_df()


    def initialize_df(self):
        if self.upload_req:
            self.read_upload()
        
        if self.df is None and self.file == None:
            "init empty df"
            columns = self.hl7_fields.get_columns()
            self.df = pd.DataFrame(columns=columns)
            return
        
        if self.file and self.df is None:
            self.read_file(self.file)
            return
        

    def read_upload(self):
        """
        Takes a Django HttpRequest.FILES and attempts to read it into a pd.DataFrame

        The resulting dataframe is set to self.df
        """
        # get user uploaded file form http request
        files = self.upload_req.keys()
        file = next(iter(files))
        print(file)
        self.file_str = str(self.upload_req[file]).split('.')[0]
        self.pickle_fn = self.file_str + ".pickle"
        
        csv_file = self.upload_req[file]
        self.df = pd.read_csv(csv_file)
        print(self.df.head())


    def read_file(self, fp:Path | bytes | str):
        """
        Reads a file path to a pd.Dataframe
        """
        file_type = fp.suffix
        f_type_pd_convert_map = {
        '.csv': pd.read_csv,
        '.pickle': pd.read_pickle
        }

        try:
            self.fp = fp

        
            # read into pd.Dataframe with appropriate pd conversion method
            self.df:pd.DataFrame = f_type_pd_convert_map[file_type](self.fp)

            self.df.name = fp.stem

            print(f'Successfully read {self.df.name} to df',end='\n\n')

        except:
            print('Cannot read file {fp}',end='\n\n')
            print(traceback.format_exc())

    def validate_self(self):
        validate_df(self.df)

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




if __name__ == '__main__':
    main()

