import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, time
from decouple import config
from pathlib import Path
import json
import random
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
    df['Exam Complete Date/Tm'] = comp_time + pd.to_timedelta(pd.Series(random.choices(range(15, 46), k=len(df))), unit='m')

    # Save DataFrame to CSV
    df.to_csv('/Users/mattbot/dev/exam-analytics/mock_exam_data_v3.csv', index=False)


    print("CSV file saved successfully.")

rand_delay()