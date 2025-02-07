import pandas as pd
import pickle
from datetime import datetime , timedelta
from random import random, randrange, choices, randint
from pathlib import Path

# create df of ORC.15
def gen_orc_sr(len:int, date_range:list[str]):
    #
    data = []
    for i in range(len):
        data.append(gen_rand_dt(date_range))
    sr = pd.DataFrame(data,)
    return sr


def gen_mock_df(orm_date_rng:list[str], df_len:int) -> pd.DataFrame:

    # set column names:
    columns = [
        'Exam Complete Date/Tm', # this is our ORM.ORC.5 (order status is complete)
        'Order Procedure Accession', # ORM.ORC.2
        'Exam Order Date/Time', # ex:'2024-07-10T01:15:00'; this is our HL7:ORM.ORC.15 (NW order time)
        'Final Date/Tm', # this is our ORM.OBR.22.1 (time of report)
        'Exam Order Name', # ORM.OBR.4
        'Modality'
    ]
    # create empty df
    df = pd.DataFrame(columns=columns)
    # print(df)

    # set order times
    df['Exam Order Date/Time'] = gen_start_times(df_len, orm_date_rng)

    # gen acc nums off of the dates
    df['Order Procedure Accession'] = df['Exam Order Date/Time'].apply(generate_acc_num)

    # Add delay to ORC.5 in minutes from 15-45 min
    df['Exam Complete Date/Tm'] = df['Exam Order Date/Time'] + pd.to_timedelta(pd.Series(choices(range(15, 46), k=len(df))), unit='m')

    # Add delay to OBR.22 in minutes from 15-60 min
    df['Final Date/Tm'] = df['Exam Complete Date/Tm'] + pd.to_timedelta(pd.Series(choices(range(15, 46), k=len(df))), unit='m')

    # Populate modality col
    df['Modality'] = df['Modality'].apply(lambda x: gen_mod())
    # print(df['Modality'])

    return df

def gen_rand_dt(daterange:list[str]):

    if len(daterange) != 2:
        raise ValueError("daterange must be a list with exactly two elements: [start, end].")
    
    start, end = [daterange[0], daterange[1]]
    start_dt, end_dt = [datetime.strptime(start, '%m/%d/%Y'), datetime.strptime(end, '%m/%d/%Y')]

    # set date diff range in min
    delta =  end_dt - start_dt
    min_delta = delta.days * 24 * 60

    # grab a random n min form that range
    rand_min = timedelta(minutes=randrange(min_delta))

    # add min to start date
    rand_date = start_dt + rand_min
    
    # return dt_obj
    return rand_date


def generate_acc_num(date_obj: datetime) -> str:
    # set modalities and their freq
    modality = ['CT', 'MR', 'XR', 'US', 'NM']
    weights = [7, 3, 10, 3, 1] 

    # Extract the last two digits of the year
    year = date_obj.strftime('%y')
    
    # Select a random two-character string from the modality list
    modality = choices(modality, weights=weights, k=1)[0]
    
    # Generate a random seven-digit number
    rand_num = f"{randint(0, 9999999):07d}"
    
    # Combine the parts into the desired format
    acc_num = f"{year}-{modality}-{rand_num}"
    
    return acc_num


def gen_start_times(len:int, date_range:list[str]):
    data = []
    for i in range(len):
        data.append(gen_rand_dt(date_range))
    df = pd.Series(data)
    return df

def gen_mod():
    modality = ['CT', 'MR', 'XR', 'US', 'NM']
    weights = [7, 3, 10, 3, 1] 
    cc = choices(modality, weights=weights, k=1)[0]
    return cc


def save_df_as_mock_csv(df: pd.DataFrame, fn:str):
    fn = fn + '.csv'
    fp = Path('/Users/mattbot/dev/') / fn
    df.to_csv(fp, index=False) 


start = '08/01/2024'

end = '08/03/2024'
time_rng = [start, end]
new_df = gen_mock_df(time_rng, 10000)

class MockedHL7Fields:

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
        return  self.get_fields().values()
    
    def rename_ORC5(self, name):
        self.ORC5 = name
    
    # returns a df with attributes as columns and no data
    def make_df(self) -> pd.DataFrame:
        fields = self.get_columns()
        df = pd.DataFrame(columns=fields)
        return df
    

# behavior?
class MockedData:
    def __init__(self, mock_hl7=None):
        self.mock_HL7 = MockedHL7Fields().get_fields()

    def gen_mod(self):

        # set modalities and their freq
        modality = ['CT', 'MR', 'XR', 'US', 'NM']
        weights = [7, 3, 10, 3, 1] 

        # select a random two-character string from the modality list
        cc = choices(modality, weights=weights, k=1)[0]
        return cc
    
    def generate_acc_num(self, date_obj: datetime, modality:str) -> str:

        # Extract the last two digits of the year
        year = date_obj.strftime('%y')

        # Generate a random seven-digit number
        rand_num = f"{randint(0, 9999999):07d}"

        # Combine the parts into the desired format
        acc_num = f"{year}-{modality}-{rand_num}"

        return acc_num 
    







class ExamsDataFrame:
    def __init__(self, hl7_fields:dict=MockedHL7Fields().get_fields()):
        # set column names:
        self.columns = hl7_fields.values()
        self.hl7_map = hl7_fields
        
    # create empty df
    def make_df(self) -> pd.DataFrame:
        return  pd.DataFrame(columns=self.columns)
    def get_hl7_map(self):
        return self.hl7_map 

            
# data
class BuildData:

    def __init__(self, df:object=ExamsDataFrame().make_df(), datast_len:int=300, dt_rng_start:str='07/01/2024', dt_rng_end:str='07/31/2024', mock_hl7=ExamsDataFrame().get_hl7_map()):
        self.df = df
        self.datast_len = datast_len
        self.dt_rng_start = dt_rng_start
        self.dt_rng_end = dt_rng_end
        self.dt_rng = [self.dt_rng_start, self.dt_rng_end]
        self.mock_HL7 = mock_hl7
        self.go_go_gadget_build()

    # returns a random date/time within a given dt range    
    def rand_dt(self) -> datetime:

        if len(self.dt_rng) != 2:
            raise ValueError("dt_rng must be a list with exactly two elements: [start, end].")
        
        start, end = [self.dt_rng[0], self.dt_rng[1]]
        start_dt, end_dt = [datetime.strptime(start, '%m/%d/%Y'), datetime.strptime(end, '%m/%d/%Y')]

        # set date diff range in min
        delta =  end_dt - start_dt
        min_delta = delta.days * 24 * 60

        # grab a random n min form that range
        rand_min = timedelta(minutes=randrange(min_delta))

        # add min to start date
        rand_date = start_dt + rand_min
        
        # return dt_obj
        return rand_date
    

    # generate start times for ORC5
    def gen_order_times(self):
        date = self.mock_HL7['ORC15'] 
        data = []
        for i in range(self.datast_len):
            data.append(self.rand_dt())
        times = pd.Series(data)
        self.df[date] = times
    

    def build_modalities(self):
        mod_col = self.mock_HL7['OBR24']

        def mod():
            # set modalities and their freq
            modality = ['CT', 'MR', 'XR', 'US', 'NM']
            weights = [7, 3, 10, 3, 1] 

            # select a random two-character string from the modality list
            return  choices(modality, weights=weights, k=1)[0]

        self.df[mod_col] = self.df[mod_col].apply(lambda x:mod())


    def generate_acc_num(self, date_obj: datetime, modality:str) -> str:

        # Extract the last two digits of the year
        year = date_obj.strftime('%y')

        # Generate a random seven-digit number
        rand_num = f"{randint(0, 9999999):07d}"

        # Combine the parts into the desired format
        acc_num = f"{year}-{modality}-{rand_num}"

        return acc_num 
    
    def build_acc_num(self) -> str:
        mod = self.mock_HL7['OBR24']
        date = self.mock_HL7['ORC15']   
        acc = self.mock_HL7['ORC2']

        self.df[acc] = self.df.apply(lambda col: self.generate_acc_num(col[date], col[mod]), axis=1)

    # Add delay to exam complete in minutes from 15-45 min
    def build_complete_dt(self):
        order_time = self.mock_HL7['ORC15']
        complete_time = self.mock_HL7['ORC5']
        # Add delay to ORC.5 in minutes from 15-45 min
        self.df[complete_time] = self.df[order_time] + pd.to_timedelta(pd.Series(choices(range(15, 46), k=len(self.df))), unit='m')

    # Add delay to exam Final in minutes from 15-60 min
    def build_final_dt(self):
        complete_time = self.mock_HL7['ORC5']
        final_time = self.mock_HL7['OBR22_1']
        self.df[final_time] = self.df[complete_time] + pd.to_timedelta(pd.Series(choices(range(15, 46), k=len(self.df))), unit='m')

    def go_go_gadget_build(self):
        self.gen_order_times()
        self.build_modalities()
        self.build_acc_num()
        self.build_complete_dt()
        self.build_final_dt()
        return self.df

    def save_df_as_mock_csv(self, fn:str, path:str='/Users/mattbot/dev/'):
        fn = fn + '.csv'
        fp = Path(path) / fn
        if fp.exists():
            print(f'{fp} already exists!!!')
            return
        self.df.to_csv(fp, index=False) 
        print(f'Successfully saved file @ {fp}!!!')

def main():

    df = BuildData(datast_len=100)
    df.save_df_as_mock_csv('OOP_test2')
    
    # df2 = data.go_go_gadget_build(datast_len=3)
    # df=df.go_go_gadget_build()
    # print(df)

if __name__ == "__main__":
    main()