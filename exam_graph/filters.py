import pandas as pd

filters = {
    "date_range": {
        "start": "2024-01-01",
        "end": "2024-12-31"
    },
    
    "x_axis": { # Time filters
        "period": "month",  # Options: "day", "month", "year", "modalities"
        "shift_filter": ["AM", "PM", "NOC"],  # List of shifts to include
        "week_view": None  # Options: "weekends", "weekdays", None
    },

    "exam_filters": {
        "modalities": ["CT", "MRI"],  # List of selected modalities
        "exam_name": "Head CT"  # Specific exam name
    },

    "y_axis": { # Metrics
        "metric": "number_of_exams",  # Options: "number_of_exams", "exam_start_to_finish_time", etc.
    },


    "shift_color_indicators": False,
}

# VALID OPTIONS FOR FILTERS:

metric_options = [
    'number_of_exams',
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

# x axis filters

# creates a new column for 'User_selected_period'
# use pandas time period aliases for period_selection 
def period(df:pd.DataFrame, period_selection:str) -> pd.DataFrame:

    # If the user wants to only see modality metrics, we already have a modality column in our df so nothing needs to be done
    if period_selection == 'modalities':
        return df
    
    # set time stamps to datetime object
    df['Exam Complete Date\/Tm'] = pd.to_datetime(df['Exam Complete Date\/Tm'])

    # create new column to we can group by the user's selected period
    df['User_selected_period'] = df['Exam Complete Date\/Tm'].dt.to_period(period_selection)

    return df


# gets the exam turnaround time
def tat(df:pd.DataFrame) -> pd.DataFrame:
    order_time = pd.to_datetime(df['Exam Order Date\/Time'])
    final_time = pd.to_datetime(df['Final Date\/Tm'])
    df['tat'] = final_time - order_time
    # print(df)
    return df


# final filters

# Metric function dictionary
metrics = {
    'tat': tat,
}

# takes y filter and applies to x axis 
# hardcoding turnaround time as y filter for now
def metric_filt(x_filtered_df:pd.DataFrame, metric:str= 'tat') -> pd.Series:
    mydf = tat(x_filtered_df)
    small_df = mydf[['tat', 'User_selected_period']]
    mean_df = small_df.groupby('User_selected_period').mean()

    # da_end_filt = pd.Series(mean_df['tat'], index= mean_df['User_selected_period'])
    return mean_df


def n_exams_by_period(df:pd.DataFrame) -> pd.Series:
    exams_by_period = df.groupby('User_selected_period').size()
    return exams_by_period


def total_filter(df:pd.DataFrame, date_range:str, xfilt:dict, yfilt:dict, modality:list,) -> pd.Series:

    # get date range
    date_range = []

    # apply x axis value (time constraints)
    df = period(df, xfilt['period'])

    # apply modality filters if needed
    if xfilt['modalities'].len() > 0:
        df = mod_filt(df, xfilt['modalities'])


    # apply y axis value (metric)
    series_axes = metric_filt(df)

    # 
    return series_axes
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