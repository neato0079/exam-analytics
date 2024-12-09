import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('./mock_exam_data.csv')

# for any column with strings, strip white spaces
df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

modalities = {
    'XR': 0,
    'CT': 0,
    'MR': 0,
    'US': 0,
    'NM': 0,
}

plot_filters = {
    'date': False,
    'month': False,
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
    if plot_filters['month']:
        exam_counts = filtered_df.groupby('Month').size().rename("# of exams")
    # NOTE: df.series.rename() keeps it a series where df.series.reset_index() turns it into a df
    
    print(exam_counts)
    return exam_counts

# generate graph
def plot_graph():
    # convert graph to something html can display
    return 'graph'