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
df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

date_range = {
    # make this ISO
    'start': '00:00:0000',
    'end': '00:00:0000'
}

modalities = {
    'XR': 0,
    'CT': 0,
    'MR': 0,
    'US': 0,
    'NM': 0,
}

x_plot_filters = {
    'day': False,
    'month': False,
    'year': False,
    'shift' : False,
    'modalities': [],
    'tat': False,
    'weekends only': False,
    'weekdays only': False,
}

def try_learn(): 

    # Display the first few rows of the DataFrame to check the data
    # print(df.head())

    # Example: Filter data for a specific month
    date_filt =df['Exam Complete Date/Tm'].str.contains('07')
    modal_filt = df['Exam Order Name'].str.contains('XR')
    filt_big = date_filt & modal_filt
    
    july_xr_data = df[filt_big]
    # print(july_xr_data)
    print(df.describe())
    # Example: Group by Exam Order Name and count occurrences
    # exam_counts = df.loc['Exam Order Name', july_data]
    # print(exam_counts)
    # Example: Plot the number of each type of exam
    # july_data.plot(kind='bar', figsize=(10, 6))

    # Add titles and labels
    # plt.title('Exams From July to September')
    # plt.xlabel('Exams')
    # plt.ylabel('Count')

    # Show the plot
    # plt.show()


def count_by_modality():

    for exam_name in df['Exam Order Name'].str.strip():
        modality = exam_name[1:3]
        if modality in modalities:
            modalities[modality] += 1

    print(modalities)


def one_modality():
    filt = df['Exam Order Name'].str.contains('XR')
    count = df[df['Exam Order Name'].str.contains('XR')].value_counts()
    count.plot(kind='bar', figsize=(10, 6))
    plt.title('Exams From July to September')
    plt.xlabel('Exams')
    plt.ylabel('Count') 
    # Show the plot
    plt.show()
  

# pull csv from session
def read_csv_from_session(file): 
    df = pd.read_json(file)
    
    return df

# set default filters
def apply_filt(df, modality):
    # Filter data based on the modality
    filtered_df = df[df['Modality'] == modality]
    
    # # Group by 'Exam Complete Date/Tm' and count the number of exams
    exam_counts = filtered_df.groupby('Exam Complete Date/Tm').size().rename("# of exams")
    # i think groupby turns the df into a series?

    # SOMETHING IS FUCKED UP WITH THE TIME FORMAT. COME BACK TO THIS LATER
    # Extract the month and year from the 'Exam Complete Date/Tm' column
    # filtered_df['Month'] = filtered_df['Exam Complete Date/Tm'].dt.to_period('M')


    # Group by the 'Month' and count the number of exams
    if x_plot_filters['month']:
        exam_counts = filtered_df.groupby('Month').size().rename("# of exams")
    # NOTE: df.series.rename() keeps it a series where df.series.reset_index() turns it into a df
    
    # print(exam_counts)
    return exam_counts # returns a panda series. NOT a df

def get_next_graph_filename():
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
     

# generate graph
def plot_graph(pd_series):

    # create the matplotlib figure/axes explicitly for better readability. By default Matplotlib uses a stateful interface for these objects

    fig , ax = plt.subplots()

    # Pass the axes object created above to plot data to our graph (fig)
    cool_graph = pd_series.plot(kind='bar', color='skyblue', ax=ax)

    # Set the title and axis labels using the `Axes` object
    ax.set_title('Exams over some time')
    ax.set_xlabel('Time')
    ax.set_ylabel('# of exams')
    print(f'Type of "cool_graph": {type(cool_graph)}') # Matplt Axes object
    file_name = get_next_graph_filename()
    file_path = settings.STATICFILES_DIRS[0] / 'graphs'/ file_name
    fig.savefig(fname = file_path, format='png')
    plt.close(fig)
    return file_name