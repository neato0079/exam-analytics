import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, time

# # Data
# data = {
#     'Exam Complete Date': ['2024-07-10T00:00:00.000', '2024-07-14T00:00:00.000', '2024-09-10T00:00:00.000'],
#     'AM': [70, 31, 58],
#     'PM': [82, 37, 66],
#     'NOC': [45,57,21]
# }

# # Convert to DataFrame
# df = pd.DataFrame(data)

# print(df)

# # Plotting
# width = 0.5
# fig, ax = plt.subplots()
# bottom = np.zeros(len(df))

# for column in df.columns[1:]:  # Exclude the 'species' column
#     ax.bar(df['Exam Complete Date'], df[column], width, label=column, bottom=bottom)
#     bottom += df[column]

# ax.set_title("Number of Radiolog Exams")
# ax.legend(loc="upper right")

# plt.show()
mock_json = pd.read_json('./mock_datav2.json')

# print(mock_json.head(4))

# Function to determine the shift
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
            
def df_with_shift(): 

    df = mock_json 
    # Ensure 'Exam Order Date/Time' is a datetime object
    df['Exam Complete Date\\/Tm'] = pd.to_datetime(df['Exam Complete Date\\/Tm'])
    df['Shift'] = df['Exam Complete Date\\/Tm'].apply(get_shift)
    df['User_selected_period']= df['Exam Complete Date\\/Tm'].dt.to_period('M')

    # Group by 'Exam Date' and 'Shift', then count the number of exams for each shift
    df = df.groupby(['User_selected_period', 'Shift']).size().unstack(fill_value=0)
    # df = df.reset_index()
    df.index = df.index.to_timestamp()

    # print(df)
    # Reset index to make 'Exam Date' a column and reformat the output
    print(df.columns)
    # print(df['AM'])
    # print(df.index)

    # Plotting
    width = 0.5
    fig, ax = plt.subplots()
    bottom = np.zeros(len(df))

    # Generate bar positions and labels
    bar_positions = range(len(df))
    bar_labels = df.index
    for column in df.columns:  
        ax.bar(bar_positions, df[column], width, label=column, bottom=bottom) # error here
        bottom += df[column]

    # Format x-axis
    ax.set_xticks(bar_positions)
    ax.set_xticklabels(bar_labels, rotation=45, ha='right', fontsize=8) 
    ax.set_title("Number of Radiolog Exams")
    ax.legend(loc="upper right")

    plt.show()

print(df_with_shift())
