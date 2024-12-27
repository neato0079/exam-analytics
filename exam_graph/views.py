# aka API handler i guess??
# the urls.py from this same directory "handles" the client's url requests by calling functions from this file

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
# from my_project import test_serve_browser
import pandas as pd
import pprint
import json
from . import helper
from . import filters
from pathlib import Path
from django.core.files.uploadedfile import InMemoryUploadedFile
import json
import io
import matplotlib.pyplot as plt

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

def build_test_master_json_df() -> pd.DataFrame:

    mock_json = pd.read_json('./mock_data.json')

    # # Read JSON into a DataFrame
    # df = pd.read_csv(mock_json)

    # # for any column with strings, strip white spaces
    # df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

    # # Ensure that 'Exam Complete Date/Tm' is in datetime format
    # df['Exam Complete Date/Tm'] = pd.to_datetime(df['Exam Complete Date/Tm'], format='%m/%d/%Y')

    # # Extract modality from 'Order Procedure Accession' (e.g., 'XR' from '24-XR-12345')
    # df['Modality'] = df['Exam Order Name'].apply(lambda x: x[1:3])

    return mock_json

def parse_filter_request(request) -> dict: 

    mock_json = build_test_master_json_df

    if request.method == 'POST':
        try:
            # Decode and parse the JSON body
            # "<class 'django.core.handlers.wsgi.WSGIRequest'>"
            # the file uploaded by postman is a django.core.files.uploadedfile object
            # we need to convert this object to bytes before we can json read it
            if len(request.FILES) > 0:
                # create InMemoryUploadedFile object from our mock_data.json stored in the 'test_file' key of our postman POST request 
                in_memory_file:InMemoryUploadedFile = request.FILES['test_file']

                # stackoverflow says to do this but idk what seek() does
                in_memory_file.seek(0)

                # read our object as bytes
                file_bytes = in_memory_file.read()

                # decode bytes to JSON string
                file_string = file_bytes.decode('utf-8')

                # convert from bytes to JSON file
                file_json = json.loads(file_string)

                # convert from JSON to pandas DataFrame
                mock_json = pd.DataFrame.from_dict(file_json)


            # parse form request

            client_form = request.POST

            metric = client_form['User_selected_metric']
            # modality = [mod.strip() for mod in client_form['User_selected_modality'].split(',')] # this is for postman
            modality = client_form.getlist('User_selected_modality')
            period = client_form['period']
            df = mock_json


            post_req = {
                'source dataframe': df,
                'date range': '',
                'xfilt': {
                    'period': period,
                    'modalities': modality
                },
                'User_selected_metric': metric,

            }

            return post_req
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON body"}, status=400)

    else:
        return JsonResponse({"Your GET": request.method})
    

# Testing for use with postman
# usecase: again from postman 
# ingest json (in prod we will just json_read the csv stored on disk), done
# parse user's form request, done
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



    if request.method == 'POST':
        try:
            # Decode and parse the JSON body
            # "<class 'django.core.handlers.wsgi.WSGIRequest'>"
            # the file uploaded by postman is a django.core.files.uploadedfile object
            # we need to convert this object to bytes before we can json read it

            # create InMemoryUploadedFile object from our mock_data.json stored in the 'test_file' key of our postman POST request 
            in_memory_file:InMemoryUploadedFile = request.FILES['test_file']

            # stackoverflow says to do this but idk what seek() does
            in_memory_file.seek(0)

            # read our object as bytes
            file_bytes = in_memory_file.read()

            # decode bytes to JSON string
            file_string = file_bytes.decode('utf-8')

            # convert from bytes to JSON file
            file_json = json.loads(file_string)

            # convert from JSON to pandas DataFrame
            mock_json = pd.DataFrame.from_dict(file_json)


            # parse form request

            client_form = request.POST

            metric = client_form['User_selected_metric']
            modality = [mod.strip() for mod in client_form['User_selected_modality'].split(',')]
            period = client_form['period']
            filename = str(in_memory_file)


            post_req = {
                'dataframe name': filename,
                'date range': '',
                'xfilt': {
                    'period': period,
                    'modalities': modality
                },
                'User_selected_metric': metric,

            }

            # Use user shit to plot data
            plot_data = filters.master_filter(mock_json, post_req['date range'], post_req['xfilt'], post_req['User_selected_metric'])

            # Save file to see if it works
            helper.plot_graph(plot_data,'first', 'test', 'title')

            # This is where the filters will come in
            return JsonResponse({
                'uploaded file type': str(mock_json), # this should just be a session key or something in prod
                'json type': 'JSON is <class "dict"> so we are good',
                'uploaded file': str(in_memory_file),
                'User_selected_metric': str(client_form['User_selected_metric']),
                'User_selected_modality': modality,
                'period': str(client_form['period']),
                'plot data as a pd series': str(type(plot_data))
                                 })
        
            # return JsonResponse({'success': 'no logic worked'})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON body"}, status=400)

    else:
        return JsonResponse({"Your GET": request.method})

# This is just used to test the graph generation
# def result_graph(request):
#     graph = test_serve_browser() # this is a pd series

#     # convert series to df
#     df = graph.to_frame()

#     # convert df to html
#     html_table = df.to_html()
#     print(request)
#     return render(request, 'results.html', {'graph': html_table})

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


def filter_submission_handler(request):

    parsed_mocked_data = build_test_master_json_df()

    try:

        # parse filter request
        filter_params = parse_filter_request(request) # returns a dictionary containing the necessary arguments for master_filter()

        # apply filters
        axes_data = filters.master_filter(parsed_mocked_data,filter_params['date range'], filter_params['xfilt'], filter_params['User_selected_metric']) # returns a panda Series appropriate for graph generation

        # Generate graph using matplotlib
        plt.figure(figsize=(10, 6))
        axes_data.plot(kind='bar')  # Adjust based on your axes_data
        plt.title('Filtered Exam Data')
        plt.xlabel('X-Axis Label')
        plt.ylabel('Y-Axis Label')

        # # Save the graph to an in-memory buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()

        # Serve the image as an HTTP response
        # return HttpResponse('<h1>AGRAPCH!</h1>')
        return HttpResponse(buffer, content_type='image/png')
    
    except Exception as e:
        print(f"An error occurred: {e}") 
        # return e
        return HttpResponse(f"An error occurred: {e}")


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