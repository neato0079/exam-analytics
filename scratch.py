from datetime import datetime, time
from dateutil import tz
import matplotlib.pyplot as plt
import pandas as pd
import random

# # unix timestamp is in milliseconds
# unix_sec = 1720569600000 / 1000



# dt = datetime.datetime.fromtimestamp(unix_sec)

# test_plot = plt
# test_plot.plot([1, 2, 3, 4])
# test_plot.ylabel('some numbers')
# print(type(test_plot))
# # test_plot.savefig(fname = 'test_graph1.png', format='png')

# import secrets
# print(secrets.token_urlsafe(50))  # This will print a secure random string

def build_test_master_json_df():

    mock_json = pd.read_json('./mock_data.json')

    return mock_json


# cut df down to a date range
def dt_range(df):
    
    # Ensure 'Exam Order Date/Time' is a datetime object
    df['Exam Order Date\/Time'] = pd.to_datetime(df['Exam Order Date\/Time'])

    
    # Define the start and end date range
    start = datetime.datetime(2024, 7, 11)
    end = datetime.datetime(2024, 7, 13)
    
    # Filter rows where 'Exam Order Date/Time' is between start and end
    filtered_df = df[(df['Exam Order Date\/Time'] >= start) & (df['Exam Order Date\/Time'] <= end)]
    
    return filtered_df



# def rand_delay():
#     df = build_test_master_json_df()
#     print(df)
#     comp_time = pd.to_datetime(df['Exam Order Date\/Time'])
#     start = '2024-07-10T01:15:00'
#     startdt = datetime.fromisoformat(start)

#     random_int = random.randint(15, 45)

#     # random time in minutes from 10-45 min
#     min = timedelta(minutes=random_int)
#     df['Exam Complete Date\\/Tm'] = comp_time + min
#     return df

# add variable times to order date. right now theyre all at 0000 HHMM so looking at totals via shifts only gives totals for noc
def rand_delay():

    # initialize mock data
    df = build_test_master_json_df()

    # convert to dt
    comp_time = pd.to_datetime(df['Exam Order Date\/Time'])

    # add delay in minutes from 10-45 min
    df['Exam Complete Date\\/Tm'] = comp_time + pd.to_timedelta(pd.Series(random.choices(range(15, 46), k=len(df))), unit='m')

    # Convert to JSON
    json_result = df.to_json(orient='columns', date_format='iso')

    # Save JSON to disk
    with open('mock_datav2.json', 'w') as json_file:
        json_file.write(json_result)

    print("JSON file saved successfully.")

def get_shifts():

    # set shift definitions
    shifts = {
        'AM': ['0700', '1500'],
        'PM': ['1500', '2300'],
        'NOC': ['2300', '0700']
    }
    
    # convert to date time objects
    for shift in shifts:
        time_range = shifts[shift]
        for i, time in enumerate(time_range):
            time_range[i] = datetime.strptime(time, '%H%M').time()

    df = build_test_master_json_df()

    # Ensure 'Exam Order Date/Time' is a datetime object
    df['Exam Order Date\/Time'] = pd.to_datetime(df['Exam Order Date\/Time'])


    if df['Exam Order Date\/Time'].loc in shift[shift]:
        df['Shift'] = shift

    return shifts



def test():
    var = {
        'AM': 'value1',
        'PM': 'value2',
        'NOC': 'value3'
    }
    
    print(var)
    print(var.items())

timeso = ['2300', '0700']
a = list(map(lambda hour: datetime.strptime(hour, '%H%M').time(), timeso))
# print(a[0])
# print(datetime.strptime('2300', '%H%M').time())


def set_shifts():
    # shift_bins = [
    #     time(0, 0),   # Start of the day
    #     time(7, 0),   # End of NOC shift
    #     time(15, 0),  # End of AM shift
    #     time(23, 0),  # End of PM shift
    #     time(23, 59, 59)  # End of the day
    # ]
    # shift_labels = ['NOC', 'AM', 'PM']

    # # Example DataFrame
    # # df = build_test_master_json_df()
    # # # print(df['Exam Complete Date\\/Tm'])

    # # # convert to dt
    # # df = pd.to_datetime(df['Exam Complete Date\\/Tm'])

    # # # Convert 'Exam Order Date/Time' to just the time part
    # # df['Exam Time'] = df['Exam Complete Date\\/Tm'].dt.time

    # # Example DataFrame
    # df = pd.DataFrame({
    #     'Exam Order Date/Time': [
    #         datetime(2024, 7, 11, 8, 0),   # AM
    #         datetime(2024, 7, 11, 16, 0),  # PM
    #         datetime(2024, 7, 11, 23, 30), # NOC
    #         datetime(2024, 7, 12, 6, 0)    # NOC
    #     ]
    # })
    # df['Exam Time'] = df['Exam Order Date/Time'].dt.time
    # # Assign shifts using cut
    # df['Shift'] = pd.cut(
    #     [time.hour * 60 + time.minute for time in df['Exam Time']],
    #     bins=[0, 7*60, 15*60, 23*60, 24*60],  # Convert hours to total minutes for binning
    #     labels=shift_labels,
    #     right=False
    # )

    # return df

    # Example of the DataFrame with datetime values
    data = {
        'Exam Order Date/Time': [
            '2024-07-11 02:15:00',
            '2024-07-11 08:30:00',
            '2024-07-11 16:45:00',
            '2024-07-11 23:15:00'
        ]
    }

    df = pd.DataFrame(data)

    # Convert 'Exam Order Date/Time' column to datetime
    df['Exam Order Date/Time'] = pd.to_datetime(df['Exam Order Date/Time'])

    # Define custom bins for the shifts
    # Using 'pd.to_datetime' to convert times to proper datetime objects for comparison
    shift_bins = [
        pd.to_datetime('1900-01-01 23:00:00'),  # 11:00 PM (start of NOC)
        pd.to_datetime('1900-01-02 07:00:00'),  # 7:00 AM (end of NOC, start of AM)
        pd.to_datetime('1900-01-02 15:00:00'),  # 3:00 PM (end of AM, start of PM)
        pd.to_datetime('1900-01-02 23:00:00'),  # 11:00 PM (end of PM, back to NOC)
    ]

    # Define the corresponding shift labels
    shift_labels = ['NOC', 'AM', 'PM']

    # Use pd.cut() to categorize the times into shifts based on the datetime values
    df['Shift'] = pd.cut(df['Exam Order Date/Time'], bins=shift_bins, labels=shift_labels, right=False)

    # Display the DataFrame
    return df

print(set_shifts())