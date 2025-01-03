import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend for server use
import matplotlib.pyplot as plt
import re
from pathlib import Path

from django.conf import settings

df = pd.read_csv('./mock_exam_data.csv')


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
     

# generate graph and save as png
def plot_graph(pd_series: pd.Series, xlabel:str, ylabel:str, title:str):

    # create the matplotlib figure/axes explicitly for better readability. By default Matplotlib uses a stateful interface for these objects

    fig , ax = plt.subplots()

    # Pass the axes object created above to plot data to our graph (fig)
    cool_graph = pd_series.plot(kind='bar', color='skyblue', ax=ax)

    # Set the title and axis labels using the `Axes` object
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    print(f'Type of "cool_graph": {type(cool_graph)}') # Matplt Axes object
    file_name = get_next_graph_filename()
    file_path = settings.STATICFILES_DIRS[0] / 'graphs'/ file_name
    fig.savefig(fname = file_path, format='png')
    plt.close(fig)
    return file_name