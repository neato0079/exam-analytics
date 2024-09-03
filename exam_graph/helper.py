import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv('./mock_exam_data.csv')

# Display the first few rows of the DataFrame to check the data
print(df.head())

# Example: Filter data for a specific month
july_data = df[df['Exam Complete Date/Tm'].str.contains('07/2024')]

# Example: Group by Exam Order Name and count occurrences
exam_counts = df['Exam Order Name'].value_counts()

print(exam_counts)
