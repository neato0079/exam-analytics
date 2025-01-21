import matplotlib.pyplot as plt
import pandas as pd
import base64
import io
import numpy as np

def gen_encoded_graph(axes_data: pd.Series, xlabel: str, ylabel: str, mod:list) -> bytes:
        
        # edit y label for turnaround time
        if ylabel == 'tat':
            ylabel = 'tat (min)'
        
        # format label strings 
        metric = ylabel.capitalize()
        period = xlabel.capitalize()
        lst_strp_table = str.maketrans('','',"[]'")
        mod = str(mod).translate(lst_strp_table)
        title = f'{metric} per {period} for Modalities: {mod}'
        

        ## Generate graph using matplotlib

        # initialize matplot lib fig and ax objects
        fig , ax = plt.subplots()
        fig.set_size_inches(10,6)
        fig.set_facecolor('gainsboro')

        # Generate bar positions and labels
        bar_positions = range(len(axes_data))
        bar_labels = axes_data.index

        # Create bar chart
        ax.bar(bar_positions, axes_data, width=0.5,color='steelblue')
        ax.set_facecolor('gainsboro')

        # Format x-axis
        ax.set_xticks(bar_positions)
        ax.set_xticklabels(bar_labels, rotation=45, ha='right', fontsize=8) 


        # format axes display
        ax.tick_params(axis='x', labelrotation = 45)
        ax.set_title(title)
        ax.set_xlabel(period)
        ax.set_ylabel(metric)

        # Save the graph to an in-memory buffer
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', dpi = 200, bbox_inches='tight')
        buffer.seek(0)
        plt.close()

        # Encode the buffer as base64
        graph_base64 = base64.b64encode(buffer.getvalue()).decode()
        buffer.close()

        return graph_base64

def plot_shift(df, period):

    # use pandas time period aliases for period_selection 
    alias = {
        'hour': 'H',
        'day': 'D',
        'week':'W',
        'month': 'M',
        'year': 'Y'
    }

    # map user's period selection to pandas period alias
    period = period.lower()
    period = alias[period]


    # Plotting
    width = 0.5
    fig, ax = plt.subplots()
    fig.set_size_inches(10,6)
    fig.set_facecolor('gainsboro')
    ax.set_facecolor('gainsboro')
    bottom = np.zeros(len(df))

    # Generate bar positions and labels
    bar_positions = range(len(df))
    bar_labels = df.index.to_period(period)

    # Custom colors for each shift
    colors = ['#2fbfd5', '#2f7dd5', '#552fd5']  # Example colors for AM, PM, NOC
    for i, column in enumerate(df.columns):
        ax.bar(bar_positions, df[column], width, label=column, bottom=bottom, color=colors[i]) # error here
        bottom += df[column]

    # Format x-axis
    ax.set_xticks(bar_positions)
    ax.set_xticklabels(bar_labels, rotation=45, ha='right', fontsize=8) 
    ax.set_title("Number of Radiology Exams")
    ax.legend(loc="upper right", reverse = True)

    # Save the graph to an in-memory buffer
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', dpi = 200, bbox_inches='tight')
    buffer.seek(0)
    plt.close()

    # Encode the buffer as base64
    graph_base64 = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()
    return graph_base64