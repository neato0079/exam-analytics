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


def mock_df_gen(orm_date_rng:list[str], df_len:int) -> pd.DataFrame:

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


def df_to_mock_csv(df: pd.DataFrame, fn:str):
    fn = fn + '.csv'
    fp = Path('/Users/mattbot/dev/') / fn
    df.to_csv(fp, index=False) 


start = '01/01/2024'

end = '01/21/2025'
time_rng = [start, end]
new_df = mock_df_gen(time_rng, 3000)

df_to_mock_csv(new_df,'big_mock')