import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, time, timedelta
from decouple import config, Config
from pathlib import Path
import json
from random import random, randrange, choices
import csv
# # Data
# data = {
#     'Exam Complete Date': ['2024-07-10T00:00:00.000', '2024-07-14T00:00:00.000', '2024-09-10T00:00:00.000'],
#     'AM': [70, 31, 58],
#     'PM': [82, 37, 66],
#     'NOC': [45,57,21]
# }

# # Convert to DataFrame
# df = pd.DataFrame(data)

# print(df)

# # Plotting
# width = 0.5
# fig, ax = plt.subplots()
# bottom = np.zeros(len(df))

# for column in df.columns[1:]:  # Exclude the 'species' column
#     ax.bar(df['Exam Complete Date'], df[column], width, label=column, bottom=bottom)
#     bottom += df[column]

# ax.set_title("Number of Radiolog Exams")
# ax.legend(loc="upper right")

# plt.show()
mock_json = pd.read_json('./mock_datav2.json')

# print(mock_json.head(4))

# Function to determine the shift
def get_shift(exam_time:datetime):

    shifts = {
    'AM': [time(7, 0), time(15, 0)],
    'PM': [time(15, 0), time(23, 0)],
    'NOC': [time(23, 0), time(7, 0)]
}
    exam_time_only = exam_time.time()
    for shift, (start, end) in shifts.items():
        if start <= end:  # AM and PM shifts
            if start <= exam_time_only < end:
                return shift
        else:  # NOC shift (overnight)
            if exam_time_only >= start or exam_time_only < end:
                return shift
            
def df_with_shift(): 

    df = mock_json 
    # Ensure 'Exam Order Date/Time' is a datetime object
    df['Exam Complete Date\\/Tm'] = pd.to_datetime(df['Exam Complete Date\\/Tm'])
    df['Shift'] = df['Exam Complete Date\\/Tm'].apply(get_shift)
    df['User_selected_period']= df['Exam Complete Date\\/Tm'].dt.to_period('M')

    # Group by 'Exam Date' and 'Shift', then count the number of exams for each shift
    df = df.groupby(['User_selected_period', 'Shift']).size().unstack(fill_value=0)
    # Reordering columns
    df = df[['AM', 'PM', 'NOC']]
    # df = df.reset_index()
    df.index = df.index.to_timestamp()

    # print(df)
    # Reset index to make 'Exam Date' a column and reformat the output
    return df
    # print(df['AM'])
    # print(df.index)

def plot_shift(df):
    # Plotting
    width = 0.5
    fig, ax = plt.subplots()
    bottom = np.zeros(len(df))

    # Generate bar positions and labels
    bar_positions = range(len(df))
    bar_labels = df.index
    for column in df.columns:  
        ax.bar(bar_positions, df[column], width, label=column, bottom=bottom) # error here
        bottom += df[column]

    # Format x-axis
    ax.set_xticks(bar_positions)
    ax.set_xticklabels(bar_labels, rotation=45, ha='right', fontsize=8) 
    ax.set_title("Number of Radiolog Exams")
    ax.legend(loc="upper right")

    plt.show()

def make_sr():

    data = [
        ('2024-07', 'AM', 14),
        ('2024-07', 'NOC', 8),
        ('2024-07', 'PM', 3),
        ('2024-08', 'AM', 15),
        ('2024-08', 'NOC', 5),
        ('2024-09', 'AM', 12),
        ('2024-09', 'NOC', 6),
        ('2024-09', 'PM', 4),
    ]

    index = pd.MultiIndex.from_tuples([(period, shift) for period, shift, _ in data], names=["User_selected_period", "Shift"])
    values = [count for _, _, count in data]

    my_ser = pd.Series(values, index=index)

    return my_ser

def plot_sr(df):
    # Plotting
    width = 0.5
    fig, ax = plt.subplots()
    bottom = np.zeros(len(df))

    # Generate bar positions and labels
    bar_positions = range(len(df))
    bar_labels = df.index
    ax.bar(bar_positions, df, width=0.5,color='steelblue')

    # Format x-axis
    ax.set_xticks(bar_positions)
    ax.set_xticklabels(bar_labels, rotation=45, ha='right', fontsize=8) 
    ax.set_title("Number of Radiolog Exams")
    ax.legend(loc="upper right")

    plt.show()

# plot_sr(make_sr())

def selected_df(usr_config_fp:Path):
    with usr_config_fp.open('r') as file:
        data = json.load(file)
        return data
    #     pickle_fn = Path(data['selected_data'] + '.pickle')
    # usr_datasets_dir = Path(config('CONFIG_ROOT') + config('USER_PROP') + config('DATASETS'))
    # pickle_fp = usr_datasets_dir / pickle_fn
    # return pickle_fp

def set_selected_df(file_stem):
    usr_prop_dir = Path(config('CONFIG_ROOT') + config('USER_PROP'))
    usr_config_fp = usr_prop_dir / 'user_config.json'
    with usr_config_fp.open('r') as file:
        data = json.load(file)
    data['selected_dataset'] = file_stem + '.pickle'

    # encode the updated data back to the JSON file
    with usr_config_fp.open('w') as file:
        json.dump(data, file, indent=4)

    print(f'Set dataset to {file_stem}')



def rand_delay():
    # Initialize mock data
    df = pd.read_csv('/Users/mattbot/dev/exam-analytics/mock_exam_data_v3.csv')

    # Convert to datetime
    comp_time = pd.to_datetime(df['Exam Order Date/Time'])

    # Add delay in minutes from 15-45 min
    df['Exam Complete Date/Tm'] = comp_time + pd.to_timedelta(pd.Series(choices(range(15, 46), k=len(df))), unit='m')

    # Save DataFrame to CSV
    df.to_csv('/Users/mattbot/dev/exam-analytics/mock_exam_data_v3.csv', index=False)


    print("CSV file saved successfully.")

# print(Path(config('DATASETS'))) # /user_uploads
# print(Path(str(Config('DATASETS')))) # <decouple.Config object at 0x105523880>
# CONFIG_ROOT = Path(config('CONFIG_ROOT'))
# USER_PROP = Path(config('USER_PROP'))
# DATASETS = Path(config('DATASETS'))

# big_directory = Path(CONFIG_ROOT / USER_PROP / DATASETS)
# print(f"CONFIG_ROOT: {CONFIG_ROOT}")
# print(f"USER_PROP: {USER_PROP}")
# print(f"DATASETS: {DATASETS}")
# print(f"big_directory: {big_directory}")

# The config object is an instance of AutoConfig that instantiates a Config with the proper Repository on the first time it is used.

def gen_rand_dt(daterange:list[str]):

    if len(daterange) != 2:
        raise ValueError("daterange must be a list with exactly two elements: [start, end].")
    

    start, end = [daterange[0], daterange[1]]
    start_dt, end_dt = [datetime.strptime(start, '%m/%d/%Y'), datetime.strptime(end, '%m/%d/%Y')]


    # set date diff range in min
    delta =  end_dt - start_dt
    min_delta = delta.days * 24 * 60
    # print((min_delta))

    # grab a random n min form that range
    rand_min = timedelta(minutes=randrange(min_delta))

    # add min to start date
    rand_date = start_dt + rand_min
    
    # return dt_obj
    return rand_date


start = '07/28/2024'

end = '08/28/2024'

import random
from datetime import datetime

def gen_mod():
    modality = ['CT', 'MR', 'XR', 'US', 'NM']
    weights = [7, 3, 10, 3, 1] 
    cc = random.choices(modality, weights=weights, k=1)[0]
    return cc


def generate_identifier(date_obj: datetime) -> str:
    # set modalities and their freq
    modality = ['CT', 'MR', 'XR', 'US', 'NM']
    weights = [7, 3, 10, 3, 1] 

    # Extract the last two digits of the year
    year = date_obj.strftime('%y')
    
    # Select a random two-character string from the modality list
    cc = random.choices(modality, weights=weights, k=1)[0]
    
    # Generate a random seven-digit number
    nnnnnnn = f"{random.randint(0, 9999999):07d}"
    
    # Combine the parts into the desired format
    identifier = f"{year}-{cc}-{nnnnnnn}"
    
    return identifier

# # Example usage:
# date_obj = datetime.now()
# modality = ['CT', 'MR', 'XR', 'US', 'NM']
# for i in range(30):
#     print(generate_identifier(date_obj))

def mk_df(len, date):
    data = []
    for i in range(30):
        data.append(generate_identifier(date))
    df = pd.DataFrame(data, columns=['acc'])
    return df


# def init_df(len, date_rn):
#     data = []
#     for i in range(len):
#         dates=[]
#         dates.append(gen_rand_dt(date_rn))
#         dates.append('')
#         data.append(dates)

#     print((data))
#     df = pd.DataFrame(data, columns=['ORC.15','empoty'])
#     return df

def gen_start_times(len, date_rn):
    data = []
    for i in range(len):
        data.append(gen_rand_dt(date_rn))
    df = pd.Series(data)
    return df

def mkdf():
    columns = [
        'Exam Complete Date/Tm', # this is our ORM.ORC.5 (order status is complete)
        'Order Procedure Accession', # ORM.ORC.2
        'Exam Order Date/Time', # ex:'2024-07-10T01:15:00'; this is our HL7:ORM.ORC.15 (NW order time)
        'Final Date/Tm', # this is our ORM.OBR.22.1 (time of report)
        'Exam Order Name' # ORM.OBR.4
    ]
    df = pd.DataFrame(columns=columns)
    return df

# df = mkdf()
# dates= gen_start_times(3, [start, end])
# df['Exam Order Date/Time'] = dates
# plot_shift((df))
# print(df)

def create_price_tbl(base_price:int) -> pd.DataFrame:
    c = ['Headshot', 'Bust', 'Half Figure', 'Full Figure']
    r = ['Sketch', 'Lineart', 'B&W Flat','B&W Two-Tone', 'Flat Color', 'Two-Tone Color']
    df = pd.DataFrame(index=r, columns=c)
    df.loc['Sketch', 'Headshot'] = base_price
    # df.reset_index(names='Render')
    return df

def inc_drw_size(df:pd.DataFrame, incr_perc):
    inc_i = 0   
    prev = df.iat[0,0]
    for col in df.columns:
        prev = round(prev * incr_perc[inc_i])
        df.loc['Sketch', col] = int(prev)
        inc_i += 1

    return df

def inc_detail(df:pd.DataFrame, col, incr):

    inc_i = 0
    
    prev = df.loc[df.index[0], col]
    for i in df.index:
        prev += incr[inc_i]
        df.loc[i, col] = int(prev)
        inc_i += 1

    return df


    
incr_perc = [1, 1.33,1.25,1.5]
incr = [0,30,15,10,15,35]

# initalize price sheet with base price
df = create_price_tbl(30)
print(df)

# percentage increase prices by draw size
inc_drw_size(df, incr_perc)
print(df)

# flat increase prices by detail
for col in df.columns:
    inc_detail(df, col, incr)
print(df)