import matplotlib.pyplot as plt
import pandas as pd
import base64
import io

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