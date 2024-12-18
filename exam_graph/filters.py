import pandas as pd

filters = {
    "date_range": {
        "start": "2024-01-01",
        "end": "2024-12-31"
    },
    
    "x_axis": { # Time filters
        "period": "month",  # Options: "day", "month", "year"
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

period_options = [
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

# use pandas time period aliases for period_selection 
def period(df:pd.DataFrame, period_selection:str) -> pd.DataFrame:
    # set time stamps to datetime object
    df['Exam Complete Date\/Tm'] = pd.to_datetime(df['Exam Complete Date\/Tm'])

    # create new column to we can group by the user's selected period
    df['User_selected_period'] = df['Exam Complete Date\/Tm'].dt.to_period(period_selection)

    return df


def n_exams_by_period(df:pd.DataFrame) -> pd.Series:
    exams_by_period = df.groupby('User_selected_period').size()
    return exams_by_period

"""
NOTES

Period aliases for pandas:https://pandas.pydata.org/docs/user_guide/timeseries.html#timeseries-period-aliases
"""