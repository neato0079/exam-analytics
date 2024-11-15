# aka API handler i guess

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from my_project import test_serve_browser
import pandas as pd


# Create your views here.
def home(request):
    return render(request, 'index.html')
    # return HttpResponse('<h1>asdfasdfasdfasdf</h1>')

def help(request):
    return HttpResponse('<h1>TODO: Add helpful tips for user!</h1>')

# This is just used to test the graph generation
def result_graph(request):
    graph = test_serve_browser() # this is a pd series

    # convert series to df
    df = graph.to_frame()

    # convert df to html
    html_table = df.to_html()
    print(request)
    return render(request, 'results.html', {'graph': html_table})

def upload_csv(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']

        # Read CSV into a DataFrame
        df = pd.read_csv(csv_file)

        # for any column with strings, strip white spaces
        df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

        # Ensure that 'Exam Complete Date/Tm' is in datetime format
        df['Exam Complete Date/Tm'] = pd.to_datetime(df['Exam Complete Date/Tm'], format='%m/%d/%Y')

        # Extract modality from 'Order Procedure Accession' (e.g., 'XR' from '24-XR-12345')
        df['Modality'] = df['Exam Order Name'].apply(lambda x: x[1:3])

        # Store the DataFrame in the session (serialize as needed)
        request.session['csv_data'] = df.to_json()  # Convert to JSON to store in the session
        # return redirect('results')  # Redirect to the filter/graph generation page
        return JsonResponse({'message': 'File processed and stored successfully'})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)