import pandas as pd

filters = {
    "date_range": {
        "start": "2024-01-01",
        "end": "2024-12-31"
    },
    
    "x_axis": { # Time filters
        "group_by": "month",  # Options: "day", "month", "year"
        "shift_filter": ["AM", "PM", "NOC"],  # List of shifts to include
        "week_view": None  # Options: "weekends", "weekdays", None
    },

    "y_axis": { # Metrics
        "metric": "number_of_exams",  # Options: "number_of_exams", "exam_start_to_finish_time", etc.
    },

    "exam_filters": {
        "modalities": ["CT", "MRI"],  # List of selected modalities
        "exam_name": "Head CT"  # Specific exam name
    },

    "shift_color_indicators": False,
}

# VALID OPTIONS FOR FILTERS:

metric_options = [
    'number_of_exams',
    'exam_start_to_finish_time'
    'ratio_of_completed_exams_to_ordered_exams'
]

groupby_options = [
    'hour'
    'day'
    'month',
    'year'
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
def period(df:pd.DataFrame, period_selection:str) -> pd.Series:

    if period_selection == 'month':
        # set time stamps to datetime object
        df['Exam Complete Date\/Tm'] = pd.to_datetime(df['Exam Complete Date\/Tm'])

        # create new column to we can group by month
        df['Exam Complete Month'] = df['Exam Complete Date\/Tm'].dt.to_period('M')
        exams_by_month = df.groupby('Exam Complete Month').size()

        return exams_by_month   
    
    elif period_selection == 'day':
        # set time stamps to datetime object
        df['Exam Complete Date\/Tm'] = pd.to_datetime(df['Exam Complete Date\/Tm'])

        # we can already group by day off of this column. its time is zeroed so it's effectively a day column
        exams_by_day = df.groupby('Exam Complete Date\/Tm').size()

        return exams_by_day
    
    elif period_selection == 'year':
        # set time stamps to datetime object
        df['Exam Complete Date\/Tm'] = pd.to_datetime(df['Exam Complete Date\/Tm'])

        # create new column to we can group by year
        df['Exam Complete Year'] = df['Exam Complete Date\/Tm'].dt.to_period('Y')
        exams_by_year = df.groupby('Exam Complete Year').size()

        return exams_by_year
    
"""
NOTES

Period aliases for pandas:https://pandas.pydata.org/docs/user_guide/timeseries.html#timeseries-period-aliases
"""