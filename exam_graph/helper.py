import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('./mock_exam_data.csv')

def try_learn(): 

    # Display the first few rows of the DataFrame to check the data
    print(df.head())

    # Example: Filter data for a specific month
    july_data = df[df['Exam Complete Date/Tm'].str.contains('07/2024')]

    # Example: Group by Exam Order Name and count occurrences
    exam_counts = df['Exam Order Name'].value_counts()

    # Example: Plot the number of each type of exam
    exam_counts.plot(kind='bar', figsize=(10, 6))

    # Add titles and labels
    plt.title('Exams From July to September')
    plt.xlabel('Exams')
    plt.ylabel('Count')

    # Show the plot
    plt.show()


def count_by_modality():
    modalities = {
        'XR': 0,
        'CT': 0,
        'MR': 0,
        'US': 0,
        'NM': 0,
    }

    for exam_name in df['Exam Order Name'].str.strip():
        modality = exam_name[1:3]
        print(modality)
        if modality in modalities:
            modalities[modality] += 1

    print(modalities)

count_by_modality()