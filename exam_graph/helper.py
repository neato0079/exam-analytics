import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend for server use
import re
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
import json
from django.http import JsonResponse
from datetime import datetime


df = pd.read_csv('./mock_exam_data.csv')

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


            client_form = request.POST

            metric = client_form['User_selected_metric']
            # modality = [mod.strip() for mod in client_form['User_selected_modality'].split(',')] # this is for postman
            modality = client_form.getlist('User_selected_modality')
            period = client_form['period']
            df = mock_json


            post_req = {
                'source_dataframe': df,
                'date_range': [start_date, end_date], 
                'date_str': [start_str, end_str],
                'xfilt': {
                    'period': period,
                    'modalities': modality
                },
                'User_selected_metric': metric,

            }

            return post_req
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON body"}, status=400)

    else:
        return JsonResponse({"Your GET": request.method})