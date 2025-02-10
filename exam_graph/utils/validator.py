import ExamDataSet
import pandas as pd
import traceback

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
    print(f'Validating {df.name} data...', end='\n\n')
    try:
        validators = [
            validate_columns,
            validate_dtypes,
        ]
        for validate in validators:
            validate(df)

    except Exception as e:
        error_message = f'Unable to validate data: {e}'
        stack_trace = traceback.format_exc()  # Capture the full traceback
        print(stack_trace)  # Log the detailed error in the console