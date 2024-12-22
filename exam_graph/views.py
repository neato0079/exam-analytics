# aka API handler i guess??
# the urls.py from this same directory "handles" the client's url requests by calling functions from this file

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from my_project import test_serve_browser
import pandas as pd
import pprint
import json
from . import helper
from . import filters
from pathlib import Path
from django.core.files.uploadedfile import InMemoryUploadedFile
import json


################
#  DEBUG MODE  #
debug_mode = False
################

# Create your views here.
def home(request):
    return render(request, 'index.html')
    # return HttpResponse('<h1>asdfasdfasdfasdf</h1>')

def help(request):
    return HttpResponse('<h1>TODO: Add helpful tips for user!</h1>')

# Testing for use with postman
# usecase: again from postman 
# ingest json (in prod we will just json_read the csv stored on disk), done
# parse user's form request, 
# apply filters, 
# plot graph, 
# save graph image, 
# render in html 
def test_api(request):
    filters_post_requirement = {
        'modality': None,
        'shift': None,
        'x-axis':{
            'date':{
            'year': None,
            'month': None,
            'day': None,
            'weekend': None,
            },
        },
        'y-axis':{
            'n exams': 0,
            'exam completion delta': 0,
            'exam finalize delta': 0,
            'ORU:ORM': 1
        }
    }


    filters_post_requirementv2 = {
        'dataframe': 'test json',
        'date range': '',
        'xfilt': {
            'period': '',
            'modalities': []
        },
        'User_selected_metric': '',

    }

    if request.method == 'POST':
        try:
            # Decode and parse the JSON body
            # "<class 'django.core.handlers.wsgi.WSGIRequest'>"
            # the file uploaded by postman is a django.core.files.uploadedfile object
            # we need to convert this object to bytes before we can json read it
            in_memory_file:InMemoryUploadedFile = request.FILES['test_file']
            in_memory_file.seek(0)
            file_bytes = in_memory_file.read()
            test_json = json.loads(file_bytes)

            client_form = request.POST
            # json_data = json.dumps(client_form)


            # This is where the filters will come in
            return JsonResponse({
                'uploaded file type': str(type(test_json)), # this should just be a session key or something in prod
                'json type': 'JSON is <class "dict"> so we are good',
                'uploaded file': str(in_memory_file),
                'User_selected_metric': str(client_form['User_selected_metric']),
                'User_selected_modality': str(client_form['User_selected_modality'])

                                 })
            # return JsonResponse({'success': 'no logic worked'})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON body"}, status=400)

    else:
        return JsonResponse({"Your GET": request.method})

# This is just used to test the graph generation
def result_graph(request):
    graph = test_serve_browser() # this is a pd series

    # convert series to df
    df = graph.to_frame()

    # convert df to html
    html_table = df.to_html()
    print(request)
    return render(request, 'results.html', {'graph': html_table})

def upload_csv(request, modality):
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
        # request.session['csv_data'] = df
        request.session['csv_data'] = df.to_json(date_format='iso')  # Convert to JSON to store in the session. idk why i needed this conversion. i know why now. you cant store a df in a session. you can store a json. so convert to json to store it


        # return redirect('test')  # Redirect to the filter/graph generation page

        if debug_mode:

            # make sure the helper functions are returning what then need to
            df_csv = helper.read_csv_from_session(request.session['csv_data']) # csv in df form
            filtered_df = helper.apply_filt(df_csv, modality)
            print('This is the filtered df returned as a series:')
            print(filtered_df)

            # html_graph = helper.plot_graph(filtered_df) # html friendly graph

            # save graph as png
            graph_file_name = helper.plot_graph(filtered_df)
            print(graph_file_name)
            graph_file_path = 'http://localhost:8000/static/graphs/' + str(graph_file_name)

            return JsonResponse(
                {
                    'message': 'File processed and stored successfully',
                    'original_request': prettify_request(request),
                    'files': f'{request.FILES}',
                    'session': f'{request.session.keys()}', # output: session	"dict_keys(['csv_data'])"
                    'session_key': f'{request.session["csv_data"]}', # this gives us the exam data from the csv yay. also remember we tojson'd this shit
                    'debug_data': f'{prettify_request(request)}',
                    'session_guts': f'{request.session}',
                    'reading from session to df': f'{df_csv}',
                    'filtered df to series': f'{filtered_df}',
                    'graph_path': f'{graph_file_path}'
                    }
                )
        else:
            
            
            df_csv = helper.read_csv_from_session(request.session['csv_data'])
            filtered_df = helper.apply_filt(df_csv, modality)
            graph_file_name = helper.plot_graph(filtered_df, 'Time', '# of exams', 'Cool Graph Title')
            graph_file_path = 'http://localhost:8000/static/graphs/' + str(graph_file_name)
            return render(request, 'results.html', {'graph_path': graph_file_path})
    else:

        return JsonResponse({'error': 'Invalid request gunga bunga'}, status=400)



# Debugging functions:
def debug_request(request):
    request_data = dir(request)  # Lists all attributes and methods of the request object
    return pprint.pformat(request_data, indent=2)


def prettify_request(request):
    return {
        "method": request.method,
        "headers": dict(request.headers),
        "GET_params": dict(request.GET) if request.GET else None,
        "POST_params": dict(request.POST),
        "FILES": {k: str(v) for k, v in request.FILES.items()},
        "path": request.path,
        "content_type": request.content_type,
        "session_keys": list(request.session.keys()),
    }