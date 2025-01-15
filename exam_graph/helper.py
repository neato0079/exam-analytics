import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend for server use
import re
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
import json
from django.http import JsonResponse
from datetime import datetime, time
from pathlib import Path
from decouple import config
import pickle
from django.shortcuts import render, redirect
import os
import re

# df = pd.read_csv('./mock_exam_data.csv')

def build_test_master_json_df() -> pd.DataFrame:

    mock_json = pd.read_json('./mock_datav2.json')

    return mock_json


# for any column with strings, strip white spaces
def df_strip(df: pd.DataFrame) -> pd.DataFrame:
    df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)


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


"""
You declare panda data types with type hints as follows
Also read up on mypy: https://mypy-lang.org/
This allows for datatype testing within functions i think

import pandas as pd

def filter1(df: pd.DataFrame) -> pd.Series: 
    filtered_df = df[df['col1'] == 'value']
    
    return filtered_df
"""
# pull csv from session
def read_csv_from_session(file: str) -> pd.DataFrame: 
    df = pd.read_json(file)
    
    return df

def get_next_graph_filename() -> str:
    # Path to the static/img directory
    img_dir = settings.STATICFILES_DIRS[0] / 'graphs'

    # Ensure the directory exists
    img_dir.mkdir(parents=True, exist_ok=True)

    # Regex pattern to match files like 'test_graphX.png'
    filename_pattern = re.compile(r'^test_graph(\d+)\.png$')

    # List all files in the directory and filter those matching the pattern
    existing_files = [f.name for f in img_dir.iterdir() if filename_pattern.match(f.name)]

    # Extract numbers from matching filenames
    numbers = [
        int(filename_pattern.match(f).group(1))
        for f in existing_files
    ]

    # Find the highest number, default to 0 if no files exist
    next_number = max(numbers, default=0) + 1

    # Construct the next filename
    next_filename = f'test_graph{next_number}.png'
    return next_filename  # Return only file name as a Path object
     


# take user's filter request and convert it into a dictionary compliant with our graphing function
def parse_filter_request(request) -> dict: 

    mock_json = build_test_master_json_df

    if request.method == 'POST':
        try:
            # Decode and parse the JSON body
            # "<class 'django.core.handlers.wsgi.WSGIRequest'>"
            # the file uploaded by postman is a django.core.files.uploadedfile object
            # we need to convert this object to bytes before we can json read it
            if len(request.FILES) > 0:
                # create InMemoryUploadedFile object from our mock_data.json stored in the 'test_file' key of our postman POST request 
                in_memory_file:InMemoryUploadedFile = request.FILES['test_file']

                # stackoverflow says to do this but idk what seek() does
                in_memory_file.seek(0)

                # read our object as bytes
                file_bytes = in_memory_file.read()

                # decode bytes to JSON string
                file_string = file_bytes.decode('utf-8')

                # convert from bytes to JSON file
                file_json = json.loads(file_string)

                # convert from JSON to pandas DataFrame
                mock_json = pd.DataFrame.from_dict(file_json)


            # parse form request

            start_str = request.POST.get('start_date')
            end_str = request.POST.get('end_date')
            start_date = datetime.strptime(start_str, '%Y-%m-%d') if start_str else None
            end_date = datetime.strptime(end_str, '%Y-%m-%d') if end_str else None


            client_form: dict = request.POST

            metric = client_form['User_selected_metric']
            # modality = [mod.strip() for mod in client_form['User_selected_modality'].split(',')] # this is for postman
            modality = client_form.getlist('User_selected_modality')
            period = client_form['period']
            df = mock_json
            shift_view = None

            if 'shift_view' in client_form:
                
                shift_view = client_form['shift_view']


            post_req = {
                'source_dataframe': df,
                'date_range': [start_date, end_date], 
                'date_str': [start_str, end_str],
                'xfilt': {
                    'period': period,
                    'modalities': modality
                },
                'User_selected_metric': metric,
                'shift_view': shift_view

            }

            return post_req
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON body"}, status=400)

    else:
        return JsonResponse({"Your GET": request.method})
    

def get_shift(exam_time:datetime):

    shifts = {
    'AM': [time(7, 0), time(15, 0)],
    'PM': [time(15, 0), time(23, 0)],
    'NOC': [time(23, 0), time(7, 0)]
}
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


def build_usr_config(file_name, config_fp):
    data = {}
    data['user datasets'] = [file_name]
    print(type(config_fp)) #<class 'pathlib.PosixPath'>
    print(config_fp)
    with config_fp.open("w") as f:
        json.dump(data, f, indent=4)
    
    print(f'Created "user_config.json" in "{dir}" successfully!')


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

def set_selected_dataset(file_stem, usr_config_fp:Path):
    with usr_config_fp.open('r') as file:
        data = json.load(file)
    data['selected_dataset'] = file_stem + '.pickle'

    # encode the updated data back to the JSON file
    with usr_config_fp.open('w') as file:
        json.dump(data, file, indent=4)

    print(f'Set dataset to {file_stem}')


def selected_pickle_fp(usr_config_fp:Path, dataset_dir:Path) -> Path:
    with usr_config_fp.open('r') as file:
        data = json.load(file)
        
    pickle_fn = Path(data['selected_dataset'])
    pickle_fp = dataset_dir / pickle_fn
    print('asdfasdfasdfasdfasdfasdfasdfasdfasdf')
    return pickle_fp