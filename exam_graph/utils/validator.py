import ExamDataSet
import pandas as pd

def validate_columns(df:pd.DataFrame) -> None:
    defaults = ExamDataSet.HL7Fields().get_columns()
    columns = list(df.columns)
    missing = []
    for col in defaults:
        if col not in columns:
            missing.append(col)
    if len(missing) > 0:
        print(f'Missing columns:{missing}',end='\n\n')
        print(defaults)
        print(list(df.columns),end='\n\n')
    else:
        print('Columns validated!',end='\n\n')

def validate_dtypes(df:pd.DataFrame) -> None:
    print('Inspect data types...',end='\n\n')
    print(df.dtypes,end='\n\n')

def validate_df(df:pd.DataFrame) -> None:
    validate_columns(df)
    validate_dtypes(df)