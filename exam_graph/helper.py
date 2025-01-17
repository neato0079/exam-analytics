import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend for server use
import re
import json
from django.http import JsonResponse, HttpRequest
from datetime import datetime, time
from pathlib import Path
import os
import re
import pickle

# used for testing filters
def build_test_master_json_df() -> pd.DataFrame:

    mock_json = pd.read_json('./mock_datav2.json')

    return mock_json


filters = {
    'date_range': {
        # make this ISO. edit later. sample data set is small enough for this not to matter yet
        'start': '00:00:0000',
        'end': '00:00:0000'
    },
    'modalities': {
        'XR': 0,
        'CT': 0,
        'MR': 0,
        'US': 0,
        'NM': 0,
    },
    'x_plot_filters': {
        'day': False,
        'month': True,
        'year': False,
        'shift' : False,
        'modalities': [],
        'tat': False,
        'weekends only': False,
        'weekdays only': False,
    },
    'y_plot_filters': {
        'number of exams': True,
        'exam start to finish time': '00:00',
        'ratio of completed exams to ordered exams': {
            'completed': 0,
            'ordered':0
        }
    }

}


# take user's filter request and convert it into a dictionary compliant with our graphing function
def parse_filter_request(request:HttpRequest) -> dict: 

    if request.method == 'POST':

        try:
            # parse form request
            client_form: dict = request.POST
            start_str = client_form.get('start_date')
            end_str = client_form.get('end_date')
            start_date = datetime.strptime(start_str, '%Y-%m-%d') if start_str else None
            end_date = datetime.strptime(end_str, '%Y-%m-%d') if end_str else None
            metric = client_form['User_selected_metric']
            modality = client_form.getlist('User_selected_modality')
            period = client_form['period']
            shift_view = None

            if 'shift_view' in client_form:
                
                shift_view = client_form['shift_view']


            post_req = {
                'date_range': [start_date, end_date], 
                'date_str': [start_str, end_str],
                'xfilt': {
                    'period': period,
                    'modalities': modality
                },
                'User_selected_metric': metric,
                'shift_view': shift_view
            }

            print(f'Parsed filter form request{client_form}')

            return post_req
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON body"}, status=400)

    else:
        return JsonResponse({"Your GET": request.method})
    

# returns shift str for a given dt
def get_shift(exam_time:datetime) -> str:
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

# set any date strings to a dt object  
def set_dt_columns(df:pd.DataFrame) -> None:
    for column in df.columns:
        try:
            df[column] = pd.to_datetime(df[column])
        except ValueError:
            print(f"Column {column} could not be converted to datetime.")


def build_usr_config(pickle_fn: str, config_fp:Path):

    # create parent dir if not present already
    user_conf_dir = config_fp.parent
    if not user_conf_dir.exists():
        create_directory(user_conf_dir)

    # check if config file already exists and update if so
    if config_fp.exists():
        update_user_config(pickle_fn,config_fp)

    # create user_config.json contents and fn
    data = {}
    data['user datasets'] = [pickle_fn]
    print(type(config_fp)) #<class 'pathlib.PosixPath'>
    print(config_fp)
    with config_fp.open("w") as f:
        json.dump(data, f, indent=4)
    
    print(f'Created "user_config.json" in "{dir}" successfully!')


def save_pickle(df:pd.DataFrame, pickle_fp:Path):

    #check if parent directory exists
    dataset_dir = pickle_fp.parent
    if not dataset_dir.exists(): # can probably just put this conditional in create_directory at this point. write tests first
        create_directory(dataset_dir)

    # Store df on disk
    with pickle_fp.open('wb') as fp:
        pickle.dump(df, fp)
    print(f'File uploaded: "{pickle_fp}')


def format_df(df:pd.DataFrame) -> pd.DataFrame:

    # for any column with strings, strip white spaces
    df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

    # Ensure that 'Exam Complete Date/Tm' is in datetime format
    df['Exam Complete Date/Tm'] = pd.to_datetime(df['Exam Complete Date/Tm'], format='ISO8601')

    # Extract modality from 'Order Procedure Accession' (e.g., 'XR' from '24-XR-12345')
    df['Modality'] = df['Exam Order Name'].apply(lambda x: x[1:3])

    return df


def update_verion_fn(s: str) -> str:
    # Regular expression to match a suffix in the format "(n)" at the end of the string
    pattern = r"\((\d+)\)$"
    match = re.search(pattern, s)
    
    if match:
        # If a match is found, increment the number
        current_number = int(match.group(1))
        new_number = current_number + 1
        # Replace the old number with the new incremented number
        new_string = re.sub(pattern, f"({new_number})", s)
    else:
        # If no match is found, add "(1)" to the string
        new_string = f"{s}(1)"
    
    return new_string

def pickle_copy(pickle_fp:Path) -> Path: 
    pickle_name = str(pickle_fp.stem)
    new_pickle_name = update_verion_fn(pickle_name)
    pickle_fp = pickle_fp.with_stem(new_pickle_name)
    return pickle_fp


def update_user_config(pickle_str:str, config_path:Path):
    config_file = Path(config_path)

    # decode to json
    with config_file.open('r') as file:
        data = json.load(file)

    # Add the new pickle file name
    data["user datasets"].append(pickle_str)

    # encode the updated data back to the JSON file
    with config_file.open('w') as file:
        json.dump(data, file, indent=4)


def create_directory(path:Path):
    # Create the directory
    path.mkdir(parents=True, exist_ok=True)
    
    # Remove .DS_Store if it exists
    ds_store = path / ".DS_Store"
    if ds_store.exists():
        os.remove(ds_store)


def update_server_on_usr_upload():
    # TODO combine the above functions maybe
    return 0

def pickle_to_df(pickle_fp:Path) -> pd.DataFrame:
    return pd.read_pickle(pickle_fp)

# update user_config.json with newly selected dataset
def set_selected_dataset(pickle_fn, usr_config_fp:Path):

    # decode config file and update it
    with usr_config_fp.open('r') as file:
        data = json.load(file)
    data['selected_dataset'] = pickle_fn

    # encode the updated data back to the JSON file
    with usr_config_fp.open('w') as file:
        json.dump(data, file, indent=4)

    print(f'Set dataset to {pickle_fn}')


# read selected dataset from config the returns the dataset fp
def selected_pickle_fp(usr_config_fp:Path, dataset_dir:Path) -> Path:
    with usr_config_fp.open('r') as file:
        data = json.load(file)
        
    pickle_fn = Path(data['selected_dataset'])
    pickle_fp = dataset_dir / pickle_fn
    return pickle_fp


# Get earliest and latest dates from a given dt column in a df
def check_date_range(df: pd.DataFrame, date_column:str = 'Exam Complete Date/Tm') -> tuple:

    earliest_date = df[date_column].min().strftime("%Y-%m-%d")
    latest_date = df[date_column].max().strftime("%Y-%m-%d")
    
    return earliest_date, latest_date