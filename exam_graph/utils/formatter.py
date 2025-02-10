import pandas as pd
from datetime import datetime, time
import traceback

# change to object to allow for changing of column names and shift times
class Formatter:
    
    default_shifts = {
        'AM': [time(7, 0), time(15, 0)],
        'PM': [time(15, 0), time(23, 0)],
        'NOC': [time(23, 0), time(7, 0)]
    }

    def __init__(self, shifts=default_shifts):
        self.shifts = shifts
        

def strip_ws(df:pd.DataFrame) -> pd.DataFrame:
    print("Stripping white spaces ...", end='\n\n')
    df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)
    return df


def set_dt_columns(df:pd.DataFrame) -> None:
    converted = []
    for column in df.columns:
        try:
            df[column] = pd.to_datetime(df[column])
            converted.append(column)
        except ValueError:
            print(f"Column {column} could not be converted to datetime.",end='\n\n')
    print(f'{len(converted)} columns successfully converted to datetime:',end='\n\n')
    print(converted,end='\n\n')

def determine_shift(exam_time:datetime) -> str:
    shifts = {
        'AM': [time(7, 0), time(15, 0)],
        'PM': [time(15, 0), time(23, 0)],
        'NOC': [time(23, 0), time(7, 0)]
    }

    # ignore date
    exam_time_only = exam_time.time()

    for shift, (start, end) in shifts.items():
        if start <= end:  # AM and PM shifts
            if start <= exam_time_only < end:
                return shift
        else:  # NOC shift (overnight)
            if exam_time_only >= start or exam_time_only < end:
                return shift

def set_shift(df:pd.DataFrame) -> pd.DataFrame:
    df['Shift'] = df['Exam Complete Date/Tm'].apply(determine_shift)

    return df

def set_modality_col(df:pd.DataFrame):
    if 'Modality' not in df.columns or df['Modality'].empty:
        df['Modality'] = df['Exam Order Name'].apply(lambda x: x[1:3])
        print("Setting Modalities...",end='\n\n')
        print(df['Modality'].head(),end='\n\n')


def format_df(df:pd.DataFrame):
    # df = df.apply(lambda x: convert_dt(x))
    print(f'Formatting {df.name} ...',end='\n\n')
    try:
        formatters = [
            strip_ws,
            set_dt_columns,
            set_shift,
            set_modality_col,
        ]
        for formatter in formatters:
            formatter(df)

        print(f'{df.name} successfully formatted!', end='\n\n')
    except Exception as e:
        error_message = f'Unable to format data: {e}'
        stack_trace = traceback.format_exc()  # Capture the full traceback
        print(stack_trace)  # Log the detailed error in the console

    return df
