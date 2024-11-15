# This file is just for testing functions from the cli rather than the browser
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import base64
from io import BytesIO

plot_filters = {
    'date': False,
    'month': False,
    'shift' : False,
    'modalities': [],
    'tat': False,
    'weekends only': False,
    'weekdays only': False,
}

shift_filters = {
    'am': 700,
    'pm': 1500,
    'noc': 2300
}

# Function to load and clean data
def load_data(file_path):
    # Read CSV file
    df = pd.read_csv(file_path)
    
    # for any column with strings, strip white spaces
    df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

    # Ensure that 'Exam Complete Date/Tm' is in datetime format
    df['Exam Complete Date/Tm'] = pd.to_datetime(df['Exam Complete Date/Tm'], format='%m/%d/%Y')
    
    # Extract modality from 'Order Procedure Accession' (e.g., 'XR' from '24-XR-12345')
    df['Modality'] = df['Exam Order Name'].apply(lambda x: x[1:3])
    print(df['Modality'].head())
    return df

def plot_data(df):

    # Plot the data
    plt.figure(figsize=(10, 6))
    ax = df.plot(kind='bar', color='skyblue')
    plt.title(f'Number of {modality} Exams')
    plt.xlabel('Date')
    plt.ylabel('Number of Exams')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Format x-axis to show date without time
    ax.set_xticklabels(df.index.strftime('%Y-%m-%d'), rotation=90)

    # Ensure y-axis displays integers
    plt.gca().yaxis.set_major_locator(mtick.MaxNLocator(integer=True))

    # Show the plot
    plt.show()


# Function to filter by modality, date, w/e
def apply_filt(df, modality):
    # Filter data based on the modality
    filtered_df = df[df['Modality'] == modality]
    
    # # Group by 'Exam Complete Date/Tm' and count the number of exams
    exam_counts = filtered_df.groupby('Exam Complete Date/Tm').size().rename("# of exams")
    # i think groupby turns the df into a series?

    # Extract the month and year from the 'Exam Complete Date/Tm' column
    filtered_df['Month'] = filtered_df['Exam Complete Date/Tm'].dt.to_period('M')


    # Group by the 'Month' and count the number of exams
    if plot_filters['month']:
        exam_counts = filtered_df.groupby('Month').size().rename("# of exams")
    # NOTE: df.series.rename() keeps it a series where df.series.reset_index() turns it into a df
    
    print(exam_counts)
    return exam_counts

def test_serve_browser():
    # fig = plt.figure()
    # #plot sth

    # tmpfile = BytesIO()
    # fig.savefig(tmpfile, format='png')
    # encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')

    file_path = './mock_exam_data.csv'
    df = load_data(file_path)
    filtered_data = apply_filt(df, "CT")
    print(type(filtered_data))
    df = filtered_data

    
    return df # returns pd series
    # return "hello world"

if __name__ == "__main__":
    # Ensure the user provides the modality as a command-line argument
    if len(sys.argv) < 2:
        print("Usage: python my_project.py <Modality:XR, CT, US, NM, MR> <Month:bool>")
        sys.exit(1)
    
    modality = sys.argv[1]  # Get the modality from the command line

    if len(sys.argv) >= 3 and sys.argv[2] == 'true':
        plot_filters['month'] = True 
        print(len(sys.argv))

    # print(type(plot_filters['month']))

    file_path = './mock_exam_data.csv'  # Path to your CSV file
    # Load the data
    df = load_data(file_path)
    print('doodoo')
    print(type(df))
    
    # Apply filters and plot the data for the specified modality
    filtered_data = apply_filt(df, modality)
    print('too high for this')
    print(type(filtered_data))
    plot_data(filtered_data)

