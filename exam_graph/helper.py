import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('./mock_exam_data.csv')
modalities = {
    'XR': 0,
    'CT': 0,
    'MR': 0,
    'US': 0,
    'NM': 0,
}

def try_learn(): 

    # Display the first few rows of the DataFrame to check the data
    # print(df.head())

    # Example: Filter data for a specific month
    filt =df['Exam Complete Date/Tm'].str.contains('07')
    filt2 = df['Exam Order Name'].str.contains('XR')
    filt_big = filt & filt2
    
    july_data = df[filt_big]
    print(july_data)
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
  

try_learn()