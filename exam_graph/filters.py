import pandas as pd
from datetime import datetime
from . import helper

filters = {
    'date_range': {
        'start': '2024-01-01',
        'end': '2024-12-31'
    },
    
    'x_axis': { # Time filters
        'period': 'month',  # Options: 'day', 'month', 'year', 'modalities'
        'shift_filter': ['AM', 'PM', 'NOC'],  # List of shifts to include
        'week_view': None,  # Options: 'weekends', 'weekdays', None
        'modalities': ['XR', 'CT', 'MR', 'US', 'NM'],  # List of selected modalities
        'exam_name': 'Head CT'  # Specific exam name
    },

    'y_axis': { # Metrics
        'metric': 'number_of_exams',  # Options: 'number_of_exams', 'exam_start_to_finish_time', etc.
    },

    'shift_color_indicators': False,
}


##### VALID OPTIONS FOR FILTERS #####

metric_options = [
    'totals',
    'mean',
    'exam_start_to_finish_time',
    'ratio_of_completed_exams_to_ordered_exams'
]

period_options = [
    'hour',
    'day',
    'week',
    'month',
    'year',
    'modalities'
]

modalities = [
    'XR',
    'CT',
    'MR',
    'US',
    'NM'
    ]

week_view_options = [
    'weekends',
    'weekdays',
    None
]

# cut df down to a date range
def dt_range(df: pd.DataFrame, start:datetime, end:datetime) -> pd.DataFrame:
    
    # Ensure 'Exam Order Date/Time' is a datetime object
    df['Exam Order Date/Time'] = pd.to_datetime(df['Exam Order Date/Time'])

    
    # Filter rows where 'Exam Order Date/Time' is between start and end
    filtered_df = df[(df['Exam Order Date/Time'] >= start) & (df['Exam Order Date/Time'] <= end)]
    
    return filtered_df


def get_shifts(df):

    # set shift definitions
    shifts = {
        'AM': ['0700', '1500'],
        'PM': ['1500', '2300'],
        'NOC': ['2300', '0700']
    }
    
    # Convert shift time strings to time objects using list and dict comprehension 
    shifts = {shift: [datetime.strptime(time, '%H%M').time() for time in times] for shift, times in shifts.items()}

    # is this more readable though or am i just a noob. maybe two for loops would be better like this
    # for shift in shifts:
    #     time_range = shifts[shift]
    #     for i, time in enumerate(time_range):
    #         time_range[i] = datetime.strptime(time, '%H%M').time()
    

    # convert to dt
    comp_time = pd.to_datetime(df['Exam Order Date/Time'])

    # check to see if shifts are formatted right

    return shifts

##### X AXIS FILTERS #####

# creates a new column for 'User_selected_period'


def period(df:pd.DataFrame, period_selection:str) -> pd.DataFrame:

    # If the user wants to only see modality metrics, we already have a modality column in our df so nothing needs to be done
    if period_selection == 'modalities':
        return df
    
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

    # set time stamps to datetime object
    df['Exam Complete Date/Tm'] = pd.to_datetime(df['Exam Complete Date/Tm'])

    # create new column to we can group by the user's selected period
    df['User_selected_period'] = df['Exam Complete Date/Tm'].dt.to_period(period_selection)

    return df


# filter df to only the selected modalities
def mod_filt(df:pd.DataFrame, selected_modalities:list) -> pd.DataFrame:
    return df[df['Modality'].isin(selected_modalities)]



##### METRIC FILTERS #####

# gets the exam turnaround time
def tat(df:pd.DataFrame) -> pd.Series:

    # convert date strings to dt objects
    order_time = pd.to_datetime(df['Exam Order Date/Time'])
    final_time = pd.to_datetime(df['Final Date/Tm'])

    # get the dt difference and set a new df column to hold these values
    df['tat'] = final_time - order_time

    # convert timedelta to total minutes
    df['tat'] = df['tat'].dt.total_seconds() / 60  

    # create small df of just the relevat data for plotting tat
    tat_df = df[['tat', 'User_selected_period']]

    # create a series by getting the mean values per period
    tat_series = tat_df.groupby('User_selected_period')['tat'].mean()

    # Look up this warning: 
    # SettingWithCopyWarning: 
    # A value is trying to be set on a copy of a slice from a DataFrame.
    # Try using .loc[row_indexer,col_indexer] = value instead
    return tat_series


def tat_shift_view(df:pd.DataFrame) -> pd.DataFrame:

    # convert date strings to dt objects
    order_time = pd.to_datetime(df['Exam Order Date/Time'])
    final_time = pd.to_datetime(df['Final Date/Tm'])

    df['Shift'] = df['Exam Complete Date/Tm'].apply(helper.get_shift)


    # get the dt difference and set a new df column to hold these values
    df['tat'] = final_time - order_time

    # convert timedelta to total minutes
    df['tat'] = df['tat'].dt.total_seconds() / 60  

    # create small df of just the relevat data for plotting tat
    tat_df = df[['tat', 'User_selected_period','Shift']]

    # get the mean of tat
    tat_series = tat_df.groupby(['User_selected_period', 'Shift'])['tat'].mean()

    # set series to df for stacked bar chart
    tat_shift = tat_series.unstack(fill_value=0)

    # Reordering columns if all three shifts are present
    try:
        df = df[['AM', 'PM', 'NOC']]
    except:
        pass
    
    tat_shift.index = tat_shift.index.to_timestamp()
    # print(tat_shift)

    return tat_shift


def totals(df:pd.DataFrame) -> pd.Series:
    exams_by_period = df.groupby('User_selected_period').size().rename('Totals')
    return exams_by_period

def mean(df:pd.DataFrame) -> pd.Series:
    
    # Convert the date column to datetime
    df['Exam Complete Date/Tm'] = pd.to_datetime(df['Exam Complete Date/Tm'])

    # Group by modality and date to count daily exams
    daily_counts = df.groupby(["Modality", df["Exam Complete Date/Tm"].dt.date]).size()
    # print(daily_counts)

    # Reset the index to make the series easier to process
    daily_counts = daily_counts.reset_index(name="Daily Exam Count")

    # Calculate the average number of daily exams per modality
    average_daily_counts = daily_counts.groupby("Modality")["Daily Exam Count"].mean()

    # print(average_daily_counts)


def shift_view(df:pd.DataFrame) -> pd.DataFrame:
 
    # Ensure 'Exam Order Date/Time' is a datetime object
    df['Exam Complete Date/Tm'] = pd.to_datetime(df['Exam Complete Date/Tm'])
    df['Shift'] = df['Exam Complete Date/Tm'].apply(helper.get_shift) # removed later
    df['Shift Ordered'] = df['Exam Order Date/Time'].apply(helper.get_shift)
    df['Shift Completed'] = df['Exam Complete Date/Tm'].apply(helper.get_shift)
    # print(df)

    # Group by 'Exam Date' and 'Shift', then count the number of exams for each shift
    df = df.groupby(['User_selected_period', 'Shift']).size().unstack(fill_value=0)

    # Reordering columns if all three shifts are present
    try:
        df = df[['AM', 'PM', 'NOC']]
    except:
        pass

    df.index = df.index.to_timestamp()

    return df


def mean_by_modality(df:pd.DataFrame) -> pd.Series:
    
    # Group by modality and date to count daily exams
    daily_counts = df.groupby(['Modality','User_selected_period']).size()
    # return daily_counts

    # Reset the index so that "modality" is a column not an index and so that we can perform a groupby again because reset_index returns a series to a dataframe
    daily_counts = daily_counts.reset_index(name="Exam Count")

    # Calculate the average number of daily exams per modality
    average_daily_counts = daily_counts.groupby("Modality")["Exam Count"].mean()
    # print(average_daily_counts)

    return average_daily_counts

    print(average_daily_counts)


def metric_filt(x_filtered_df:pd.DataFrame, metric:str) -> pd.Series:

    # Metric function dictionary
    metric_dict = {
        'totals': totals,
        'mean': mean,
        'tat': tat,
        'shift': shift_view,
        'tat_shift': tat_shift_view,
        'shift_ratios':shift_ratios,
    }
    
    # Apply relevant metric function to df
    xy_filtered_df = metric_dict[metric](x_filtered_df)

    return xy_filtered_df
   


def master_filter(df:pd.DataFrame, xfilt:dict, metric:str, daterange:list[datetime], filters:dict) -> pd.Series:

    # get date range
    start = daterange[0]
    end = daterange[1]

    df = dt_range(df,start,end)

    # apply x axis value (time constraints)
    df = period(df, xfilt['period'])

    # apply modality filters if needed
    if len(xfilt['modalities']) > 0:
        df = mod_filt(df, xfilt['modalities'])

    # handle shift view on tat
    if filters['shift_view'] and filters['User_selected_metric'] == 'tat':
        return metric_filt(df, 'tat_shift') # returns a df not series

    # handle shift view on totals
    if filters['shift_view']:
        return metric_filt(df, 'shift_ratios') # returns a df not series

    # if metric == 'shift view'
    
    df_axes = metric_filt(df, metric)
    return df_axes


    # apply y axis value (metric)
    series_axes = metric_filt(df, metric)

    return series_axes

def shift_ratios(df:pd.DataFrame) -> pd.DataFrame:
    # get number of completes for PM
    # get number of orders for PM
    # ratio = complete:orders
    # if ratio > 1 then PM shift might need more staffing 
    df['Shift Ordered'] = df['Exam Order Date/Time'].apply(helper.get_shift)
    df['Shift Completed'] = df['Exam Complete Date/Tm'].apply(helper.get_shift)
    # cut df to relevant data
    shift_data = df[['User_selected_period','Shift Ordered','Shift Completed']]

    # create 2 separate dfs grouping by ordered and completed shifts
    ordered = shift_data.groupby(['User_selected_period', 'Shift Ordered']).size().reset_index(name="ordered_count")
    completed = shift_data.groupby(['User_selected_period', 'Shift Completed']).size().reset_index(name="complete_count")

    # merge them and get the ratios for each shift
    merged = pd.merge(ordered, completed,
                  left_on=["User_selected_period", "Shift Ordered"],
                  right_on=["User_selected_period", "Shift Completed"],
                  how="outer").fillna(0)
    merged = merged.rename(columns={"Shift Ordered": "Shift"})
    merged = merged.drop(columns=["Shift Completed"])  # No longer needed
    pivot_df = merged.pivot(index="User_selected_period", columns="Shift", values=["ordered_count", "complete_count"]).fillna(0)
    for shift in ["AM", "PM", "NOC"]:
        pivot_df[("completion_ratio", shift)] = pivot_df[("complete_count", shift)] / pivot_df[("ordered_count", shift)]

    # cut down df again
    new_df=pivot_df['completion_ratio'] 
    return new_df
"""
NOTES

Period aliases for pandas:https://pandas.pydata.org/docs/user_guide/timeseries.html#timeseries-period-aliases

fitler flow

date range gets set first. set this to a default range for mangable data sets (maybe just the past 3 months)

x axis filters get set first. This tells us what portion of the data we want to analyize
with this filter we essentially get rid of only rows from our dataset. all columns remain as the columns will be used later to determine what metrics  will be used
any x axis filter can be combined (ie period=month, shift_filter=['AM'] + weekview=None). or rather, they are all mandatory. wouldnt make sense to not apply one of them?

secondary x filters
these will get set after as they only server to provide a more granular look at our og x filters but they cant be combined? untrue. make these the same as the x fitlers i guess

y filters
this tells us how we want to analyze our data. do we want to see turnaround times? total exam volume? average exam volume? ect The analyses are make on "grouped" data so these filters must be applied to already filtered data. hence we do this after the x filters

pretty filters
this just lets us make a stacked bar graph where different color show work shifts. figure this out later

"""