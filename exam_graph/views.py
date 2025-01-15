# aka API handler i guess??
# the urls.py from this same directory "handles" the client's url requests by calling functions from this file

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpRequest
import pandas as pd
import pprint
from . import helper
from . import filters
from django.core.files.uploadedfile import InMemoryUploadedFile
import matplotlib.pyplot as plt
import traceback
from . import myplot
from pathlib import Path
import pickle
from django.contrib import messages
from decouple import config

################
#  DEBUG MODE  #
debug_mode = False
################

# Create your views here.
def home(request:HttpRequest):

    upload_dir = Path(config('CONFIG_ROOT') + config('USER_PROP') + config('DATASETS'))

    if upload_dir.exists():
        files = [f.stem for f in upload_dir.iterdir() if f.is_file()]  # List only files without suffix

    else:
        files = ['no datasets uploaded']
    return render(request, 'index.html', {'files': files})
    # return HttpResponse('<h1>asdfasdfasdfasdf</h1>')

def form_page(request):
    return render(request, 'form.html', {'graph': 'graph_file_path'})

def help(request):
    return HttpResponse('<h1>TODO: Add helpful tips for user!</h1>')

def display_mock_csv(request):
    df = helper.build_test_master_json_df()
    graph = df.to_html()
    return render(request, 'test_template.html', {'graph': graph})

def test(request):
    file_name = request.GET['file'] + '.pickle'
    return JsonResponse({'Your Selection': f"File: {file_name}"}, status=200)


def upload_csv(request):

    try:

        files = request.FILES.keys()
        file = next(iter(files))

        # check if its a cvs file
        file_prefx = str(request.FILES[file]).split('.')[1]
        print(f'requested file upload type: .{file_prefx}')
        if file_prefx != 'csv':
            print('not a csv')
            messages.error(request, 'Upload ".csv" files only please! I am still just a baby app!')

            return redirect('/exam_graph')

        file_str = str(request.FILES[file]).split('.')[0]
        pickle_name = file_str + ".pickle"
        csv_file = request.FILES[file]

        # Read CSV into a DataFrame
        df = pd.read_csv(csv_file)

        # Format data for filters
        df = helper.format_df(df)


        if debug_mode:

            return JsonResponse(
                {
                    'message': 'File processed and stored successfully',
                    'original_request': prettify_request(request),
                    'files': f'{request.FILES}',
                    'session': f'{request.session.keys()}', # output: session	"dict_keys(['csv_data'])"
                    'session_key': f'{request.session["csv_data"]}', # this gives us the exam data from the csv yay. also remember we tojson'd this shit
                    'debug_data': f'{prettify_request(request)}',
                    'session_guts': f'{request.session}',
                    }
                )
            
        # non debug mode
        else:
            
            # set config paths
            usr_datasets_dir = Path(config('CONFIG_ROOT') + config('USER_PROP') + config('DATASETS'))
            usr_prop_dir = Path(config('CONFIG_ROOT') + config('USER_PROP'))
            pickle_fp = usr_datasets_dir / pickle_name
            usr_config_fp = usr_prop_dir / 'user_config.json'

            # check to see if user_config.json exists
            if usr_config_fp.exists():
                # update user_config.json with name of newly uploaded dataset
                print('user_config.json exists yaya')
            else:
                if not usr_prop_dir.exists():
                    # create neccessary dir
                    usr_prop_dir.mkdir(parents=True, exist_ok=True)

                # create user_config.json and add pickel
                helper.build_usr_config(pickle_name, usr_prop_dir)

            # check if dataset dir exists for pickle write
            if not usr_datasets_dir.exists():
                usr_datasets_dir.mkdir(parents=True, exist_ok=True)

            # Store df on disk
            helper.store_df_as_pickle(pickle_fp, df)
            messages.info(request, f'{file_str} uploaded!')
            return redirect('/exam_graph')
        
    except Exception as e:
        error_message = f"An error occurred: {e}"
        stack_trace = traceback.format_exc()  # Capture the full traceback
        print(stack_trace)  # Log the detailed error in the console
        return HttpResponse(f"{error_message}<br><pre>{stack_trace}</pre>", content_type="text/html")


def filter_submission_handler(request):

    parsed_mocked_data = helper.build_test_master_json_df()
    

    try:

        # parse filter request
        filter_params: dict = helper.parse_filter_request(request) # returns a dictionary containing the necessary arguments for master_filter()

        # df = filter_params['source_dataframe']
        period = filter_params['xfilt']['period']
        modality_lst = filter_params['xfilt']['modalities']
        metric = filter_params['User_selected_metric']
        daterange = filter_params['date_range']
        datestr = filter_params['date_str']
        shift_view = filter_params['shift_view']

        # TESTING SHIFT PLOT. TOTALS ONLY

        axes_data = filters.master_filter(parsed_mocked_data, filter_params['xfilt'], metric ,daterange, filter_params)
        
        if shift_view:
            graph_base64 = myplot.plot_shift(axes_data, period)
            axes_data = axes_data.to_html()

        else:
            # graph without shift view
            graph_base64 = myplot.gen_encoded_graph(axes_data, period, metric, modality_lst)
            axes_data = axes_data.to_frame().to_html()# convert to df for html view

        stuff_for_html_render = {
            'graph': graph_base64,
            'selected_period': period,
            'selected_modality': modality_lst,
            'selected_metric': metric,
            'start_date': datestr[0],
            'end_date': datestr[1],
            'shift_view': shift_view,
            'summary': axes_data
        }
  
        return render(request, 'form.html', stuff_for_html_render)


    except Exception as e:
            error_message = f"An error occurred: {e}"
            stack_trace = traceback.format_exc()  # Capture the full traceback
            print(stack_trace)  # Log the detailed error in the console
            return HttpResponse(f"{error_message}<br><pre>{stack_trace}</pre>", content_type="text/html")



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