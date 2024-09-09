import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# Function to load and clean data
def load_data(file_path):
    # Read CSV file
    df = pd.read_csv(file_path)
    
    # Ensure that 'Exam Complete Date/Tm' is in datetime format
    df['Exam Complete Date/Tm'] = pd.to_datetime(df['Exam Complete Date/Tm'], format='%m/%d/%Y')
    
    # Extract modality from 'Order Procedure Accession' (e.g., 'XR' from '24-XR-12345')
    df['Modality'] = df['Order Procedure Accession'].apply(lambda x: x.split('-')[1])
    
    return df

# Function to filter by modality and plot
def plot_exams_by_modality(df, modality):
    # Filter data based on the modality
    filtered_df = df[df['Modality'] == modality]
    
    # Group by 'Exam Complete Date/Tm' and count the number of exams
    exam_counts = filtered_df.groupby('Exam Complete Date/Tm').size()
    print(exam_counts)

    # Extract the month and year from the 'Exam Complete Date/Tm' column
    # filtered_df['Month'] = filtered_df['Exam Complete Date/Tm'].dt.to_period('M')

    # Group by the 'Month' and count the number of exams
    # exam_counts = filtered_df.groupby('Month').size()
    
    # Plot the data
    plt.figure(figsize=(10, 6))
    ax = exam_counts.plot(kind='bar', color='skyblue')
    plt.title(f'Number of {modality} Exams by Date')
    plt.xlabel('Date')
    plt.ylabel('Number of Exams')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Format x-axis to show date without time
    ax.set_xticklabels(exam_counts.index.strftime('%Y-%m-%d'), rotation=90)

    # Ensure y-axis displays integers
    plt.gca().yaxis.set_major_locator(mtick.MaxNLocator(integer=True))

    # Show the plot
    plt.show()

if __name__ == "__main__":
    # Ensure the user provides the modality as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python my_project.py <Modality>")
        sys.exit(1)
    
    modality = sys.argv[1]  # Get the modality from the command line
    file_path = './mock_exam_data.csv'  # Path to your CSV file
    
    # Load the data
    df = load_data(file_path)
    
    # Plot the data for the specified modality
    plot_exams_by_modality(df, modality)
