import pandas as pd
from datetime import datetime, time
import traceback


class HL7Fields:

    def __init__(self):
        self.order_complete_dt = 'Exam Complete Date/Tm' # this is our ORM.ORC.5 (order status is complete)
        self.acc = 'Order Procedure Accession' # ORM.ORC.2
        self.order_dt = 'Exam Order Date/Time' # ex:'2024-07-10T01:15:00'; this is our HL7:ORM.ORC.15 (NW order time)
        self.final_dt = 'Final Date/Tm' # this is our ORM.OBR.22.1 (time of report)
        self.order_name = 'Exam Order Name' # ORM.OBR.4
        self.modality = 'Modality'
        
    def get_fields(self) -> dict:
        return {
            'ORC5': self.order_complete_dt,
            'ORC2': self.acc,
            'ORC15': self.order_dt,
            'OBR22_1': self.final_dt,
            'OBR4': self.order_name,
            'OBR24': self.modality
        }
    
    def get_columns(self) -> list:
        return  list(self.get_fields().values())
    
    # returns a df with attributes as columns and no data
    def make_df(self) -> pd.DataFrame:
        fields = self.get_columns(self)
        df = pd.DataFrame(columns=fields)
        return df
    
    @classmethod
    def show_default_fields(cls) -> list:
        return  list(cls().get_fields().values())
    

class Shifts:
    def __init__(self):
        self.AM = [time(7, 0), time(15, 0)]
        self.PM = [time(15, 0), time(23, 0)]
        self.NOC = [time(23, 0), time(7, 0)]

    def dict(self):
        return self.__dict__


# change to object to allow for changing of column names and shift times
class Formatter:

    def __init__(self, df:pd.DataFrame=None, shifts:dict=Shifts().dict(), hl7=HL7Fields()):
        self.shifts = shifts
        self.hl7 = hl7
        self.df = df

    def __str__(self):
        return 'Pass a new shift object to change the defualt shift times. Example:\n\n {default_shifts}'

    def strip_ws(self) -> pd.DataFrame:
        print("Stripping white spaces ...", end='\n\n')
        self.df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)
        return self.df
    
    def set_dt_columns(self) -> None:
        converted = []
        for column in self.df.columns:
            try:
                self.df[column] = pd.to_datetime(self.df[column])
                converted.append(column)
            except ValueError:
                print(f"Column {column} could not be converted to datetime.",end='\n\n')
        print(f'{len(converted)} columns successfully converted to datetime:',end='\n\n')
        print(converted,end='\n\n')
    
    def determine_shift(self, exam_time:datetime) -> str:

        # ignore date
        exam_time_only = exam_time.time()

        for shift, (start, end) in self.shifts.items():
            if start <= end:  # AM and PM shifts
                if start <= exam_time_only < end:
                    return shift
            else:  # NOC shift (overnight)
                if exam_time_only >= start or exam_time_only < end:
                    return shift
    
    def set_shift(self) -> pd.DataFrame:
        self.df['Shift'] = self.df[self.hl7.order_complete_dt].apply(determine_shift)
        return self.df
    
    def set_modality_col(self) -> None:
        if self.hl7.modality not in self.df.columns or self.df[self.hl7.modality].empty:
            # extract modality alias from order name
            self.df[self.hl7.modality] = self.df[self.hl7.order_name].apply(lambda x: x[1:3])
            print("Setting Modalities...",end='\n\n')
            print(self.df[self.hl7.modality].head(),end='\n\n')

    def format_df(self, df:pd.DataFrame=None) -> pd.DataFrame:
        if df == None:
            df = self.df 
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
